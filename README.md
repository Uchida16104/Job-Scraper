# Job Scraper — フロント（Vercel） + バック（Render）サンプル

## 概要
このリポジトリは、ユーザ提供の `main.py`（求人サイトをスクレイピングして csv / xlsx を出力するスクリプト）をバックエンドで呼び出し、フロントエンド（Next.js）から URL を入力して実行・結果の CSV/XLSX をダウンロードできる仕組みのサンプルです。

**重要な前提**:
- `main.py` は Selenium / Chrome を使う想定です。Render の標準 non-Docker 環境では Chrome がないため、**そのままデプロイしても Selenium エラーが発生する可能性が高い**です。
- 本リポジトリでは以下 2 つの方法を案内します（推奨は A）:
  - A（推奨）: Render にデプロイ → `BROWSERLESS_URL` を設定して Browserless（外部ヘッドレス）を利用する。→ 安定稼働。
  - B（代替）: Docker を使って Chrome を含むコンテナを作る → 最も安定するが Docker 使用。

## 使い方（ローカルで試す）
1. `backend` に `main.py`（あなたの元ファイル）を置く
2. `cd backend`
3. `python -m venv venv && source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python app.py`（起動後 `http://localhost:8000`）
6. `frontend` を別ターミナルで `npm install` → `npm run dev`、ブラウザで Next のフォームから URL を送る

## デプロイ（概要）
### Vercel（フロント）
- Root Directory: `frontend`
- Install Command: `npm ci` または `npm install`
- Build Command: `npm run build`
- Output Directory: `.next`
- Environment Variables:
  - `NEXT_PUBLIC_BACKEND_URL` = `https://<your-render-backend-url>`（Render 側公開 URL）

### Render（バック）
- Service: Web Service (Python)
- Region: 任意（例: `oregon` / `iad` / `tokyo`）
- Root Directory: `backend`
- Build Command:
  ```
  pip install -r requirements.txt
  ```
- Start Command:
  ```
  gunicorn app:app -b 0.0.0.0:$PORT --workers=1
  ```
- Environment Variables:
  - `SCRAPE_TIMEOUT` (任意, default 240)
  - **もし Browserless を使う場合**: `BROWSERLESS_URL` を設定（必須）
    - 例: `wss://chrome.browserless.io?token=XXXXX`

## 注意点（初心者向け）
- **必ず** `main.py` がどのように webdriver を作成しているか（ローカル Chrome を期待しているか／remote webdriver を受け入れるか）を確認してください。Render でそのまま動かない場合は README_BACKEND.md にある「remote webdriver 実装の1行追加」を加えると安定します。
- 一時ファイルは backend 側で一時保存しています。運用時は古い一時ファイルを削除する cron 的処理を入れてください。
- 連続実行・大量アクセスは対象サイトの利用規約や robots.txt に注意してください。


