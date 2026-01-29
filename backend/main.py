import os
import re
import json
import base64
import tempfile
from datetime import datetime
from urllib.parse import urlparse, urljoin
from io import BytesIO
import traceback

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
CORS(app)

SUPPORTED_DOMAINS = [
    'atgp.jp',
    'minor-league.jp',
    'snabi.jp',
    'doda.jp',
    'indeed.com',
    'mynavi.jp',
    'rikunabi.com'
]

def is_supported_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    for supported in SUPPORTED_DOMAINS:
        if supported in domain:
            return True
    return False

def fetch_page_content(url, timeout=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        raise Exception(f"ページの取得に失敗しました: {str(e)}")

def extract_text_safe(element):
    if element is None:
        return ""
    text = element.get_text(separator=" ", strip=True)
    return text if text else ""

def parse_salary_to_monthly_low(salary_text):
    if not salary_text or str(salary_text).strip() == "":
        return 0
    
    text = str(salary_text).replace(',', '').replace('¥', '').replace('￥', '').strip()
    text = text.replace('〜', '~').replace('～', '~').replace('－', '-')
    
    is_month = bool(re.search(r'月給|月収|月額', text))
    is_year = bool(re.search(r'年収|年俸', text))
    is_hour = bool(re.search(r'時給', text))
    
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    if not match:
        return 0
    
    try:
        num = float(match.group(1))
    except:
        return 0
    
    if '万' in text:
        base = int(num * 10000)
    elif '円' in text or re.search(r'\d{4,}', text):
        base = int(num)
    else:
        base = int(num)
    
    if is_hour:
        monthly = int(base * 160)
    elif is_year:
        monthly = int(base // 12)
    elif is_month:
        monthly = int(base)
    else:
        if base >= 1000000:
            monthly = int(base // 12)
        else:
            monthly = int(base)
    
    return max(0, int(monthly))

def extract_job_items_generic(soup, url):
    items = []
    
    selectors = [
        'article',
        'div.search_result_item',
        'div.job-card',
        'div.jobCard',
        'li.job',
        'div.cassetteRecruit',
        'section.item',
        'div.resultItem',
        'div.c-job_card'
    ]
    
    elements = []
    for selector in selectors:
        found = soup.select(selector)
        if found and len(found) > 0:
            elements = found
            break
    
    if not elements:
        elements = soup.find_all(['article', 'div'], limit=200)
    
    for element in elements:
        text_content = extract_text_safe(element)
        
        if len(text_content) < 30:
            continue
        
        company_name = "不明"
        company_selectors = [
            '.p-search_result_item__company',
            '.c-job_card__company',
            '.company',
            '.company-name',
            '.companyName',
            '.cassetteRecruit__name',
            '[class*="company"]',
            '[class*="Company"]'
        ]
        for sel in company_selectors:
            comp_elem = element.select_one(sel)
            if comp_elem:
                name = extract_text_safe(comp_elem)
                if name:
                    company_name = name
                    break
        
        if company_name == "不明":
            match = re.search(r'([^\n]{1,60}(?:株式会社|有限会社|合同会社|一般社団法人|公益財団法人)[^\n]*)', text_content)
            if match:
                company_name = match.group(1).strip()
            else:
                lines = [ln.strip() for ln in text_content.splitlines() if ln.strip()]
                if lines:
                    company_name = lines[0][:60]
        
        job_title = ""
        job_url = ""
        link = element.find('a')
        if link:
            job_title = extract_text_safe(link).splitlines()[0] if link.get_text() else ""
            href = link.get('href', '')
            if href:
                job_url = urljoin(url, href)
        
        if not job_title:
            title_selectors = ['.job-title', '.title', 'h2', 'h3', '.jobTitle', '[class*="title"]']
            for sel in title_selectors:
                title_elem = element.select_one(sel)
                if title_elem:
                    job_title = extract_text_safe(title_elem).splitlines()[0]
                    if job_title:
                        break
        
        location = "不明"
        loc_match = re.search(r'勤務地[:：]?\s*([^\n,，]+)', text_content)
        if loc_match:
            location = loc_match.group(1).strip().split()[0]
        else:
            pref_match = re.search(r'(東京都|神奈川県|埼玉県|千葉県|大阪府|愛知県|北海道|福岡県|京都府|静岡県|茨城県|栃木県|群馬県|山梨県|長野県|新潟県|富山県|石川県|福井県|岐阜県|三重県|滋賀県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県|青森県|岩手県|宮城県|秋田県|山形県|福島県)[^ \n,，]*', text_content)
            if pref_match:
                location = pref_match.group(0)
        
        employment_type = "不明"
        for emp_type in ["正社員", "契約社員", "嘱託社員", "パート", "アルバイト", "派遣", "業務委託", "紹介予定派遣"]:
            if emp_type in text_content:
                employment_type = emp_type
                break
        
        salary = "不明"
        sal_match = re.search(r'(年収|給与|月給|時給|年俸)[^ \n，]*[:：]?\s*([^\n]+)', text_content)
        if sal_match:
            salary = sal_match.group(0).strip()
        else:
            sal_match2 = re.search(r'(\d[\d,\.]*\s*(?:万円|万|円|万円以上|円以上|万〜))', text_content)
            if sal_match2:
                salary = sal_match2.group(0).strip()
            else:
                sal_match3 = re.search(r'([0-9]+(?:\.[0-9]+)?\s*(?:万|円))', text_content)
                if sal_match3:
                    salary = sal_match3.group(0).strip()
        
        monthly_low = parse_salary_to_monthly_low(salary)
        
        item = {
            "会社名": company_name,
            "職種": job_title,
            "勤務地": location,
            "雇用形態": employment_type,
            "給与": salary,
            "求人URL": job_url,
            "月給換算(下限)": monthly_low
        }
        
        items.append(item)
    
    return items

def create_dataframe(records):
    if not records:
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    
    if "求人URL" in df.columns and "職種" in df.columns:
        df = df.drop_duplicates(subset=["求人URL", "職種"])
    else:
        df = df.drop_duplicates()
    
    if "月給換算(下限)" not in df.columns:
        df["月給換算(下限)"] = df["給与"].apply(parse_salary_to_monthly_low)
    
    return df

def generate_files(df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_buffer.seek(0)
    csv_base64 = base64.b64encode(csv_buffer.getvalue()).decode('utf-8')
    csv_data_url = f"data:text/csv;charset=utf-8;base64,{csv_base64}"
    
    xlsx_buffer = BytesIO()
    try:
        df_sorted = df.sort_values("月給換算(下限)", ascending=False)
        df_sorted.to_excel(xlsx_buffer, index=False, engine='openpyxl')
    except:
        df.to_excel(xlsx_buffer, index=False, engine='openpyxl')
    xlsx_buffer.seek(0)
    xlsx_base64 = base64.b64encode(xlsx_buffer.getvalue()).decode('utf-8')
    xlsx_data_url = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{xlsx_base64}"
    
    return csv_data_url, xlsx_data_url

def generate_statistics(df):
    stats = {
        "total_records": len(df)
    }
    
    if "月給換算(下限)" in df.columns and len(df) > 0:
        monthly_positive = df[df["月給換算(下限)"] > 0]["月給換算(下限)"]
        if not monthly_positive.empty:
            stats["average_salary"] = int(monthly_positive.mean())
            stats["max_salary"] = int(df["月給換算(下限)"].max())
        else:
            stats["average_salary"] = None
            stats["max_salary"] = None
    
    if "勤務地" in df.columns:
        location_counts = df["勤務地"].value_counts().head(5)
        stats["top_locations"] = [
            {"location": loc, "count": int(count)} 
            for loc, count in location_counts.items()
        ]
    
    if "雇用形態" in df.columns:
        employment_counts = df["雇用形態"].value_counts()
        stats["employment_types"] = {
            emp_type: int(count) 
            for emp_type, count in employment_counts.items()
        }
    
    return stats

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({"error": "URLが指定されていません"}), 400
        
        url = data['url']
        max_items = data.get('max_items', 100)
        
        if not is_supported_domain(url):
            return jsonify({"error": "サポートされていないドメインです"}), 400
        
        html_content = fetch_page_content(url)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        records = extract_job_items_generic(soup, url)
        
        if max_items and len(records) > max_items:
            records = records[:max_items]
        
        if not records:
            return jsonify({"error": "求人情報が見つかりませんでした"}), 404
        
        df = create_dataframe(records)
        
        if df.empty:
            return jsonify({"error": "有効なデータが抽出できませんでした"}), 404
        
        csv_url, xlsx_url = generate_files(df)
        
        stats = generate_statistics(df)
        
        response_data = {
            "csv_url": csv_url,
            "xlsx_url": xlsx_url,
            **stats
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error: {error_trace}")
        return jsonify({"error": f"処理中にエラーが発生しました: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "Job Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/scrape": "POST - スクレイピング実行",
            "/health": "GET - ヘルスチェック"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
