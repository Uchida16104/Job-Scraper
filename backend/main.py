from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re
from urllib.parse import urlparse
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
def safe_text(el):
    try:
        return el.get_text(" ", strip=True)
    except:
        return ""
def generic_extract(soup, base_url):
    text = soup.get_text("\n", strip=True)
    company = ""
    title = ""
    location = ""
    emp_type = ""
    salary = ""
    link = base_url
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    company_candidates = soup.select("meta[name=og:site_name], meta[property='og:site_name']")
    if company_candidates:
        company = company_candidates[0].get("content","").strip()
    if not company:
        comps = soup.select("[class*=company],[id*=company],[class*=employer]")
        for c in comps:
            v = safe_text(c)
            if v:
                company = v
                break
    locs = re.search(r'(勤務地[:：]?\s*[^\n,，]+)', text)
    if locs:
        location = locs.group(1).split("：")[-1].strip()
    types = re.search(r'(正社員|契約社員|嘱託社員|パート|アルバイト|派遣|業務委託)', text)
    if types:
        emp_type = types.group(1)
    sal = re.search(r'([0-9,\.]+\s*(?:万円|万|円|円以上|万円以上|時給))', text)
    if sal:
        salary = sal.group(1)
    anchors = soup.find_all("a", href=True)
    for a in anchors:
        if a.get_text(strip=True):
            link = a.get("href")
            break
    return {"会社名": company or "不明", "職種": title or "不明", "勤務地": location or "不明", "雇用形態": emp_type or "不明", "給与": salary or "不明", "求人URL": link or base_url}
def parse_atgp(soup, url):
    rows = []
    items = soup.select("div.searchResultList, li, article, div.jobCard, div.card")
    if not items:
        items = soup.select("article, li, div")
    for it in items:
        title_el = it.select_one("a, h2, h3, .title, .jobTitle")
        company_el = it.select_one(".company, .jobCompany, .companyName")
        loc_el = it.select_one(".location, .jobLocation, .prefecture")
        salary_el = it.select_one(".salary, .pay, .jobSalary")
        emp_el = it.select_one(".employmentType, .jobType, .type")
        link = ""
        if title_el and title_el.name == "a":
            link = title_el.get("href")
        if title_el and not link:
            a = it.select_one("a")
            if a:
                link = a.get("href")
        title = safe_text(title_el) or safe_text(it.select_one("a")) or ""
        company = safe_text(company_el) or ""
        location = safe_text(loc_el) or ""
        salary = safe_text(salary_el) or ""
        emp = safe_text(emp_el) or ""
        if not title and not company:
            continue
        rows.append({"会社名": company or "不明", "職種": title or "不明", "勤務地": location or "不明", "雇用形態": emp or "不明", "給与": salary or "不明", "求人URL": link or url})
    if not rows:
        rows.append(generic_extract(soup, url))
    return rows
def parse_mlg(soup, url):
    return parse_atgp(soup, url)
def parse_litalico(soup, url):
    return parse_atgp(soup, url)
def parse_doda(soup, url):
    return parse_atgp(soup, url)
def parse_indeed(soup, url):
    rows = []
    cards = soup.select("div.jobsearch-SerpJobCard, .job_seen_beacon, .jobCard")
    for c in cards:
        title = safe_text(c.select_one("h2, .jobTitle, a"))
        company = safe_text(c.select_one(".company, .companyName"))
        location = safe_text(c.select_one(".location, .companyLocation"))
        salary = safe_text(c.select_one(".salary, .salaryText"))
        link = ""
        a = c.select_one("a")
        if a and a.get("href"):
            link = a.get("href")
            if link.startswith("/"):
                parsed = urlparse(url)
                link = f"{parsed.scheme}://{parsed.netloc}{link}"
        rows.append({"会社名": company or "不明", "職種": title or "不明", "勤務地": location or "不明", "雇用形態": "不明", "給与": salary or "不明", "求人URL": link or url})
    if not rows:
        rows.append(generic_extract(soup, url))
    return rows
def parse_mynavi(soup, url):
    return parse_atgp(soup, url)
def parse_rikunabi(soup, url):
    return parse_atgp(soup, url)
PARSERS = {
    "atgp.jp": parse_atgp,
    "mlg.kaien-lab.com": parse_mlg,
    "litalico": parse_litalico,
    "doda.jp": parse_doda,
    "indeed": parse_indeed,
    "mynavi": parse_mynavi,
    "rikunabi": parse_rikunabi
}
def fetch_html(url, timeout=15):
    headers = {"User-Agent":"Mozilla/5.0 (compatible; JobScraper/1.0; +https://example.com)","Accept-Language":"ja-JP,ja;q=0.9"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text
def domain_of(url):
    try:
        p = urlparse(url)
        host = p.netloc.lower()
        return host
    except:
        return ""
def run_parse_for_url(url):
    try:
        text = fetch_html(url)
    except Exception:
        return [generic_extract(BeautifulSoup("", "lxml"), url)]
    soup = BeautifulSoup(text, "lxml")
    host = domain_of(url)
    for key, fn in PARSERS.items():
        if key in host:
            try:
                return fn(soup, url)
            except:
                return [generic_extract(soup, url)]
    return [generic_extract(soup, url)]
def normalize_records(recs):
    df = pd.DataFrame(recs)
    if "求人URL" in df.columns:
        df = df.drop_duplicates(subset=["求人URL", "職種"])
    df["月給換算(下限)"] = df.get("給与", "").apply(lambda s: parse_salary_to_monthly_low(s))
    return df
def parse_salary_to_monthly_low(s):
    try:
        if not s:
            return 0
        text = str(s).replace(",", "").replace("¥","").replace("￥","").strip()
        text = text.replace("〜","~").replace("－","-")
        is_month = bool(re.search(r'月給|月収|月額', text))
        is_year = bool(re.search(r'年収|年俸', text))
        is_hour = bool(re.search(r'時給', text))
        m = re.search(r'(\d+(?:\.\d+)?)', text)
        if not m:
            return 0
        num = float(m.group(1))
        if "万" in text:
            base = int(num * 10000)
        elif "円" in text or re.search(r'\d{4,}', text):
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
    except:
        return 0
@app.post("/api/scrape")
async def scrape(request: Request):
    form = await request.form()
    urls_text = form.get("urls") or ""
    site_hint = (form.get("site") or "").strip().lower()
    urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
    if not urls:
        return JSONResponse({"error":"no urls provided"}, status_code=400)
    all_rows = []
    for u in urls:
        if not urlparse(u).scheme:
            u = "https://" + u
        rows = run_parse_for_url(u)
        all_rows.extend(rows)
    df = normalize_records(all_rows)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = f"job_scraper_{timestamp}"
    csv_path = os.path.join(DOWNLOAD_DIR, base_name + ".csv")
    xlsx_path = os.path.join(DOWNLOAD_DIR, base_name + ".xlsx")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    host = request.headers.get("host") or ""
    scheme = "https" if request.url.scheme == "https" else request.url.scheme
    download_base = f"{scheme}://{host}/downloads"
    result = {"csv": f"{download_base}/{base_name}.csv", "xlsx": f"{download_base}/{base_name}.xlsx", "count": len(df)}
    html = "<div class='p-4 bg-white rounded shadow'><p class='font-medium'>完了</p><p>件数: " + str(len(df)) + "</p><ul class='mt-2'>"
    html += f"<li><a class='text-blue-600' href='{result['csv']}'>CSV をダウンロード</a></li>"
    html += f"<li><a class='text-blue-600' href='{result['xlsx']}'>XLSX をダウンロード</a></li>"
    html += "</ul></div>"
    return HTMLResponse(content=html)
app.mount("/downloads", StaticFiles(directory=DOWNLOAD_DIR), name="downloads")
@app.get("/")
def root():
    return {"status":"ok"}

