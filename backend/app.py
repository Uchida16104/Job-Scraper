# backend/app.py
import os
import shutil
import tempfile
import glob
import subprocess
import time
from flask import Flask, request, send_file, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/run": {
        "origins": "https://job-scraper-indol-nine.vercel.app",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 最大実行時間（秒）
SCRAPE_TIMEOUT = int(os.environ.get("SCRAPE_TIMEOUT", "240"))

# main.py が backend フォルダにある前提
MAIN_SCRIPT_NAME = "main.py"

@app.route("/")
def index():
    return "Job Scraper Backend (Flask). Use POST /run with form field 'link'."

@app.route("/run", methods=["POST"])
def run_scrape():
    link = request.form.get("link") or request.json and request.json.get("link")
    if not link:
        return "Error: missing 'link' field", 400

    # 一時ディレクトリを作成して、そこで main.py を実行（ファイルの衝突を避ける）
    workdir = tempfile.mkdtemp(prefix="job-scraper-")
    try:
        # copy main.py into workdir
        src_main = os.path.join(os.path.dirname(__file__), MAIN_SCRIPT_NAME)
        if not os.path.exists(src_main):
            return "Error: main.py not found on server.", 500
        shutil.copy(src_main, workdir)

        # 実行
        cmd = ["python", MAIN_SCRIPT_NAME, link]
        start = time.time()
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=SCRAPE_TIMEOUT)
        elapsed = time.time() - start

        stdout = proc.stdout or ""
        stderr = proc.stderr or ""

        # find CSV/XLSX files created in workdir
        csv_files = glob.glob(os.path.join(workdir, "*.csv"))
        xlsx_files = glob.glob(os.path.join(workdir, "*.xlsx"))

        files = csv_files + xlsx_files

        if proc.returncode != 0:
            # 実行エラー: stderr を返す（初心者向けにわかりやすく）
            body = f"""
            <div class="p-4 bg-red-100 rounded">
              <h2 class="font-semibold">実行中にエラーが発生しました</h2>
              <pre style="white-space:pre-wrap;max-height:300px;overflow:auto">{stderr}</pre>
              <p>stdout:</p>
              <pre style="white-space:pre-wrap;max-height:200px;overflow:auto">{stdout}</pre>
              <p>注: Render の環境では Chrome/Chromedriver が無いと Selenium が失敗する場合があります。README を参照して下さい。</p>
            </div>
            """
            return render_template_string(body), 500

        if not files:
            body = f"""
            <div class="p-4 bg-yellow-100 rounded">
              <h2 class="font-semibold">ファイルが生成されませんでした</h2>
              <p>stdout:</p>
              <pre style="white-space:pre-wrap;max-height:200px;overflow:auto">{stdout}</pre>
              <p>stderr:</p>
              <pre style="white-space:pre-wrap;max-height:200px;overflow:auto">{stderr}</pre>
            </div>
            """
            return render_template_string(body), 200

        # 成功: ダウンロード用リンク一覧を返す
        links_html = "<div class='space-y-2'>"
        for p in files:
            fname = os.path.basename(p)
            links_html += f"<div><a class='text-blue-600' href='/download/{os.path.basename(workdir)}/{fname}' target='_blank' rel='noopener'>{fname}</a></div>"
        links_html += "</div>"

        # 付加情報（実行ログ）を表示
        body = f"""
        <div class="p-4 bg-green-50 rounded">
          <h2 class="font-semibold">完了 — {len(files)} 件のファイルを生成しました（実行時間: {elapsed:.1f}s）</h2>
          {links_html}
          <details class="mt-4 p-2 border rounded"><summary>ログ（stdout / stderr）</summary>
            <pre style="white-space:pre-wrap;max-height:240px;overflow:auto">{stdout}\n\n{stderr}</pre>
          </details>
        </div>
        """
        return render_template_string(body), 200

    except subprocess.TimeoutExpired:
        return render_template_string("<div class='p-4 bg-red-100 rounded'>処理がタイムアウトしました（%d秒）</div>" % SCRAPE_TIMEOUT), 500
    finally:
        # NOTE: workdir のファイルをそのまま参照可能にするため、download では workdir を参照する。
        # 一時ディレクトリは削除しない（短時間でのダウンロードのため）か、別の仕組みで削除するようREADMEで説明
        pass

@app.route("/download/<workdir_name>/<filename>")
def download_file(workdir_name, filename):
    # セキュリティ対策：workdir_name は prefix をチェック
    base_tmp = "/tmp"
    # the tmp dirs we create start with "job-scraper-"
    expected_prefix = "job-scraper-"
    if not workdir_name.startswith(expected_prefix):
        return "Invalid request.", 400

    path = os.path.join(tempfile.gettempdir(), workdir_name, filename)
    if not os.path.exists(path):
        return "File not found.", 404
    return send_file(path, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)

