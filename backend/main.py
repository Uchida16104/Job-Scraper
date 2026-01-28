#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import time
import logging
import re
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException, WebDriverException, NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdriver-manager helps auto-download chromedriver
from webdriver_manager.chrome import ChromeDriverManager

LOG = logging.getLogger("scraper")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def build_driver(headless=False, timeout=30):
    """Chrome webdriver を組み立てて返す。headless を指定可。"""
    chrome_options = Options()
    # GUIで実行したい場合は headless=False にする(デフォルト)。自動実行サーバでは True。
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    # ログを抑える
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Optional: ユーザーデータを分けたい場合は user-data-dir を指定
    # chrome_options.add_argument("--user-data-dir=/tmp/selenium-profile")

    # Service を作り webdriver 起動(webdriver-manager が driver をインストール)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(timeout)
    driver.implicitly_wait(1)  # 補助的な短い暗黙等待ち
    return driver


def robust_find_text(item):
    """要素のテキストを安全に取得"""
    try:
        txt = item.text
        return txt.strip() if txt else ""
    except Exception:
        return ""


def parse_salary_to_monthly_low(s):
    """
    給与文字列 s を解析して「月給換算(下限)」を整数(円)として返す。
    解析ロジック(優先順位):
    - 月給表記(月給, 月収) → 下限をそのまま
    - 年収(年俸) → 下限を12で割る
    - 時給 → 月換算は「時給 * 月間労働時間(デフォルト160h)」
    - 万円 / 万 / 円 の扱い、範囲は "-" または "〜" を解析して下限を使用
    - 値が取れない場合は 0 を返す
    """
    if not s or str(s).strip() == "":
        return 0
    text = str(s).replace(',', '').replace('¥', '').replace('￥', '').strip()
    # normalize fullwidth digits etc
    text = text.replace('〜', '~').replace('〜', '~').replace('−', '-')
    # common keywords
    is_month = bool(re.search(r'月給|月収|月額', text))
    is_year = bool(re.search(r'年収|年俸', text))
    is_hour = bool(re.search(r'時給', text))
    # find numbers with optional 万 or 円
    # capture ranges like "25万〜35万" or "300,000 - 400,000円"
    # first try patterns with 万
    def extract_first_number(txt):
        # find first numeric group (including decimals)
        m = re.search(r'(\d+(?:\.\d+)?)', txt)
        if not m:
            return None
        try:
            return float(m.group(1))
        except:
            return None

    # handle ranges: take the first number in the string
    num = extract_first_number(text)
    if num is None:
        return 0

    # detect '万' near that number
    # find position of number and see suffix characters
    # simpler: if '万' appears anywhere before a currency or near number, scale accordingly
    if '万' in text:
        # when user writes "25万" -> 25 * 10000 (could be monthly or yearly)
        base = int(num * 10000)
    elif '円' in text or re.search(r'\d{4,}', text):
        # plain yen number
        base = int(num)
    else:
        # fallback: treat as plain yen
        base = int(num)

    # now convert depending on type
    if is_hour:
        # assume 160h/month
        monthly = int(base * 160)
    elif is_year:
        # if number looks like annual (e.g., 400万円 or 4,800,000)
        # if value seems small and had '万' already converted, assume it's annual
        # convert annual to monthly
        monthly = int(base // 12)
    elif is_month:
        monthly = int(base)
    else:
        # ambiguous: heuristic
        # if base >= 1_000_000 -> probably annual
        if base >= 1_000_000:
            monthly = int(base // 12)
        else:
            # treat as monthly or hourly? assume monthly if '万' used; else monthly
            monthly = int(base)
    # ensure non-negative
    return max(0, int(monthly))


def extract_fields_from_item(item):
    """1件の求人要素から情報抽出を試みる。戻り: dict"""
    text = robust_find_text(item)
    # company: 複数の候補セレクタで試す
    company = "不明"
    for sel in [
        ".p-search_result_item__company", ".c-job_card__company",
        ".company", ".company-name", ".job-company", ".job-card-company"
    ]:
        try:
            el = item.find_element(By.CSS_SELECTOR, sel)
            name = el.text.strip()
            if name:
                company = name
                break
        except Exception:
            continue
    # fallback: try to find lines that look like company (heuristic: 行に「株式会社」など)
    if company == "不明":
        m = re.search(r'([^\n]{1,60}株式会社[^\n]*)', text)
        if m:
            company = m.group(1).strip()
        else:
            # take first non-empty line
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            if lines:
                company = lines[0][:60]

    # title and url: find first anchor inside item
    job_title = ""
    job_url = ""
    try:
        a = item.find_element(By.TAG_NAME, "a")
        job_title = a.text.strip().splitlines()[0] if a.text else ""
        job_url = a.get_attribute("href") or ""
    except Exception:
        # fallback: find any heading-like or .title
        try:
            el = item.find_element(By.CSS_SELECTOR, ".job-title, .title, h2, h3")
            job_title = el.text.strip().splitlines()[0]
        except Exception:
            job_title = ""
    # location: look for "勤務地" or patterns like "東京都○○市"
    location = "不明"
    lm = re.search(r'勤務地[::]?\s*([^\n,，]+)', text)
    if lm:
        location = lm.group(1).strip().split()[0]
    else:
        # try common prefectures/cities
        pref_match = re.search(r'(東京都|神奈川県|埼玉県|千葉県|大阪府|愛知県|北海道|福岡県|京都府|静岡県)[^ \n,，]*', text)
        if pref_match:
            location = pref_match.group(0)

    # employment type
    emp_type = "不明"
    for et in ["正社員", "契約社員", "嘱託社員", "パート", "アルバイト", "派遣", "業務委託"]:
        if et in text:
            emp_type = et
            break

    # salary: try to find lines containing 給与/年収/月給/時給
    salary = "不明"
    sal_m = re.search(r'(年収|給与|月給|時給|年俸)[^ \n，]*[::]?\s*([^\n]+)', text)
    if sal_m:
        # take the remainder of the line after the keyword
        salary = sal_m.group(0).strip()
    else:
        # fallback: find numbers and yen units nearby
        m2 = re.search(r'(\d[\d,\.]*\s*(?:万円|万|円|万円以上|円以上|万〜))', text)
        if m2:
            salary = m2.group(0).strip()
        else:
            # last resort: any '万' or '円' occurrence
            m3 = re.search(r'([0-9]+(?:\.[0-9]+)?\s*(?:万|円))', text)
            if m3:
                salary = m3.group(0).strip()

    monthly_low = parse_salary_to_monthly_low(salary)

    return {
        "会社名": company,
        "職種": job_title,
        "勤務地": location,
        "雇用形態": emp_type,
        "給与": salary,
        "求人URL": job_url,
        "月給換算(下限)": monthly_low,
        "raw_text": text
    }


def find_items_on_page(driver, timeout=10):
    """ページ上の求人要素群を探す(複数のXPath/CSSを順に試す)。"""
    # candidate xpaths/selectors (拡張可能)
    candidates = [
        "//article",
        "//section[contains(@class,'item')]",
        "//div[contains(@class,'search_result_item')]",
        "//div[contains(@class,'job-card')]",
        "//ul[contains(@class,'search_results')]//li",
        "//div[contains(@class,'resultList')]//div[contains(@class,'job')]",
    ]
    for xp in candidates:
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xp))
            )
            items = driver.find_elements(By.XPATH, xp)
            if items and len(items) > 0:
                LOG.info("Found %d items by XPath: %s", len(items), xp)
                return items
        except TimeoutException:
            continue
        except Exception as e:
            LOG.debug("find attempt error for %s: %s", xp, e)
            continue
    # 最後の手段: 全てのarticleやdivを返す(空配列を返すより安全)
    try:
        items = driver.find_elements(By.XPATH, "//article | //div")
        LOG.info("Fallback: found %d article/div elements", len(items))
        return items
    except Exception:
        return []


def process_url(driver, url, max_items_per_page=100):
    """1 URL を開いて求人要素を抽出して dict の list を返す。"""
    LOG.info("Opening %s", url)
    try:
        driver.get(url)
    except Exception as e:
        LOG.warning("ページ取得で例外: %s", e)
        # retry with a short sleep
        time.sleep(2)
        try:
            driver.get(url)
        except Exception as e2:
            LOG.error("Retry失敗: %s", e2)
            return []

    # ページが動的に読み込む可能性があるのでスクロールして読み込ませる
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
    except Exception:
        pass

    items = find_items_on_page(driver, timeout=8)
    results = []
    for i, item in enumerate(items):
        if i >= max_items_per_page:
            break
        try:
            # filter tiny divs
            txt = robust_find_text(item)
            if not txt or len(txt) < 20:
                continue
            rec = extract_fields_from_item(item)
            # optionally filter only URLs if user requested that specifically
            results.append(rec)
        except Exception as e:
            LOG.debug("アイテム解析エラー: %s", e)
            continue
    LOG.info("Extracted %d raw records from %s", len(results), url)
    return results


def normalize_and_save(all_records, output_dir=None, base_name_prefix="data"):
    """pandas DataFrame にして重複排除・数値化してCSV/Excel保存。返り値: dataframe"""
    if not all_records:
        LOG.warning("保存するレコードがありません。")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)
    # Dedup: same URL + title
    if "求人URL" in df.columns:
        df = df.drop_duplicates(subset=["求人URL", "職種"])
    else:
        df = df.drop_duplicates()

    # ensure 月給換算 column exists (already created in extraction)
    if "月給換算(下限)" not in df.columns:
        df["月給換算(下限)"] = df["給与"].apply(parse_salary_to_monthly_low)

    # 出力先ファイル名タイムスタンプ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_profile = os.path.expanduser("~")
    out_dir = output_dir if output_dir else user_profile
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, f"{base_name_prefix}_{timestamp}.csv")
    xlsx_path = os.path.join(out_dir, f"{base_name_prefix}_{timestamp}.xlsx")

    # CSV は Excel で開けるようにBOM付きutf-8で出す
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    # Excel:openpyxl backend
    try:
        df.sort_values("月給換算(下限)", ascending=False).to_excel(xlsx_path, index=False)
    except Exception:
        # fallback: no sorting if column missing
        df.to_excel(xlsx_path, index=False)

    LOG.info("Saved CSV: %s", csv_path)
    LOG.info("Saved XLSX: %s", xlsx_path)
    return df, csv_path, xlsx_path


def print_report(df):
    """コンソール集計レポート出力"""
    print("\n" + "=" * 40)
    print("       求人厳密分析レポート")
    print("=" * 40)
    n = len(df)
    print(f"■ 有効データ数: {n} 件")
    if "月給換算(下限)" in df.columns and n > 0:
        monthly_positive = df[df["月給換算(下限)"] > 0]["月給換算(下限)"]
        if not monthly_positive.empty:
            print(f"■ 平均月給(下限): {int(monthly_positive.mean()):,d} 円")
            print(f"■ 最高月給(下限): {int(df['月給換算(下限)'].max()):,d} 円")
        else:
            print("■ 月給データが存在しません。")
    else:
        print("■ 月給換算カラムが存在しません。")

    if "勤務地" in df.columns:
        print("\n■ 勤務地分布 (Top 10):")
        print(df["勤務地"].value_counts().head(10).to_string())

    if "雇用形態" in df.columns:
        print("\n■ 雇用形態内訳:")
        print(df["雇用形態"].value_counts().to_string())

    print("\n")


def load_urls_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    return lines


def main():
    parser = argparse.ArgumentParser(description="/求人ページ汎用スクレイパー (Selenium)")
    parser.add_argument("urls", nargs="*", help="解析したいURL(複数可)")
    parser.add_argument("--input-file", "-i", help="URLが列挙されたテキストファイル(改行区切り)")
    parser.add_argument("--headless", action="store_true", help="ヘッドレスで実行する(ブラウザ非表示)")
    parser.add_argument("--output-dir", "-o", help="出力ディレクトリ(省略時はホームディレクトリ)")
    parser.add_argument("--max-items", type=int, default=200, help="ページあたり最大解析アイテム数(デフォルト200)")
    args = parser.parse_args()

    url_list = list(args.urls)
    if args.input_file:
        url_list += load_urls_from_file(args.input_file)

    if not url_list:
        print("解析するURLが指定されていません。コマンドライン引数か --input-file でURLを与えてください。")
        sys.exit(1)

    LOG.info("解析対象URL数: %d", len(url_list))
    driver = None
    try:
        driver = build_driver(headless=args.headless, timeout=30)
    except WebDriverException as e:
        LOG.error("WebDriver の起動に失敗しました: %s", e)
        sys.exit(1)

    all_records = []
    try:
        for url in url_list:
            # sanity: require at least a scheme
            if not urlparse(url).scheme:
                url = "https://" + url
            records = process_url(driver, url, max_items_per_page=args.max_items)
            # optionally filter to the domain if the user only wants the urls:
            #records = [r for r in records if it in (r.get("求人URL") or "")]
            all_records.extend(records)
            # short delay between pages
            time.sleep(0.6)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    df, csv_path, xlsx_path = normalize_and_save(all_records, output_dir=args.output_dir)
    print_report(df if not df.empty else pd.DataFrame())
    LOG.info("完了。出力: %s, %s", csv_path if 'csv_path' in locals() else "-", xlsx_path if 'xlsx_path' in locals() else "-")


if __name__ == "__main__":
    main()
