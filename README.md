# 求人サイトスクレイピング統合システム / Job Site Scraping Integration System

## 概要 / Overview

複数の求人サイト（atgp、LITALICO仕事ナビ、マイナビ系）から求人情報を自動収集し、CSV形式で出力するフルスタックアプリケーションです。

A full-stack application that automatically collects job listings from multiple job sites (atgp, LITALICO, Mynavi series) and exports them in CSV format.

## 技術スタック / Technology Stack

### フロントエンド / Frontend
- **Next.js** (latest)
- **React** (latest)
- **TypeScript** (latest)
- **Tailwind CSS** (latest)
- **HTMX** (latest)
- **Alpine.js** (latest)
- **Vercel** (ホスティング / Hosting)

### バックエンド / Backend
- **Python** (latest)
- **FastAPI** (0.115.0)
- **C#** (.NET 8.0)
- **PostgreSQL** (latest)
- **Docker**
- **Render** (ホスティング / Hosting)

## 主な機能 / Key Features

1. **マルチサイトスクレイピング / Multi-site Scraping**
   - atgp
   - LITALICO仕事ナビ
   - マイナビ系求人サイト

2. **データ処理 / Data Processing**
   - Webスクレイピング
   - データ分析・正規化
   - CSV出力

3. **履歴管理 / History Management**
   - スクレイピング履歴の保存
   - フィルタリング機能
   - CSVダウンロード

4. **自動化 / Automation**
   - Cronジョブによる定期実行
   - 古いファイルの自動削除

5. **認証システム / Authentication**
   - ユーザー別履歴管理
   - JWT認証

## ディレクトリ構成 / Directory Structure

```
job-scraper-system/
├── frontend/                 # Next.js フロントエンド
│   ├── src/
│   │   ├── app/             # ページとレイアウト
│   │   ├── components/      # Reactコンポーネント
│   │   └── lib/             # ユーティリティ
│   └── package.json
│
└── backend/                  # Python + C# バックエンド
    ├── python/              # FastAPI アプリケーション
    │   ├── routes/          # APIルート
    │   ├── services/        # ビジネスロジック
    │   ├── scheduler/       # Cronジョブ
    │   └── utils/           # ユーティリティ
    └── csharp/              # C# スクレイパー
        ├── Scrapers/        # サイト別スクレイパー
        ├── Services/        # サービス層
        └── Models/          # データモデル
```

## 取得データ項目 / Data Fields

各求人から以下の情報を取得します：

The following information is collected from each job listing:

1. **求人数 / Job Count**
2. **会社名 / Company Name**
3. **業種 / Industry Type**
4. **職種 / Job Type**
5. **雇用形態 / Employment Type**
6. **勤務時間 / Work Hours**
7. **仕事内容 / Job Description**
8. **給与 / Salary**
9. **会社所在地 / Company Location**
10. **勤務地 / Work Location**
11. **福利厚生 / Benefits**
12. **休日・休暇 / Holidays**
13. **対象となる方 / Requirements**
14. **求人URL / Job URL**

## セットアップ / Setup

### 必要な環境 / Prerequisites

- Node.js (latest)
- Python (latest)
- .NET SDK (latest)
- PostgreSQL (latest)
- Docker (オプション / Optional)

### ローカル開発環境 / Local Development

#### 1. リポジトリのクローン / Clone Repository

```bash
git clone <repository-url>
cd job-scraper-system
```

#### 2. フロントエンドのセットアップ / Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
```

`.env.local`を編集：
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

```bash
npm run dev
```

フロントエンドは http://localhost:3000 で起動します

#### 3. バックエンドのセットアップ / Backend Setup

##### データベース / Database

```bash
createdb jobscraper
```

##### 環境変数 / Environment Variables

```bash
cd backend
cp .env.example .env
```

`.env`を編集：
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/jobscraper
SECRET_KEY=your-secret-key-here
CSHARP_SCRAPER_PATH=/app/csharp/JobScraperCore
```

##### C#スクレイパーのビルド / Build C# Scraper

```bash
cd csharp
dotnet restore
dotnet build
dotnet publish -c Release -o ../python/csharp
```

##### Pythonの起動 / Start Python

```bash
cd ../python
pip install -r ../requirements.txt
uvicorn app:app --reload
```

バックエンドは http://localhost:8000 で起動します

### Dockerを使用した起動 / Using Docker

```bash
cd backend
docker-compose up --build
```

## デプロイマニュアル / Deployment Manual

### Vercel (フロントエンド / Frontend)

#### 1. Vercelアカウントにログイン / Login to Vercel

https://vercel.com にアクセスしてログイン

#### 2. 新規プロジェクト作成 / Create New Project

- "Add New Project" をクリック
- GitHubリポジトリを接続

#### 3. プロジェクト設定 / Project Settings

**Framework Preset:** Next.js

**Root Directory:** `frontend`

**Build Command:** `npm run build`

**Output Directory:** `.next`

**Install Command:** `npm install`

#### 4. 環境変数設定 / Environment Variables

Settings → Environment Variables で以下を追加：

| Key | Value |
|-----|-------|
| NEXT_PUBLIC_API_URL | https://your-backend.onrender.com |

#### 5. デプロイ / Deploy

"Deploy" ボタンをクリック

### Render (バックエンド / Backend)

#### 1. Renderアカウントにログイン / Login to Render

https://render.com にアクセスしてログイン

#### 2. PostgreSQLデータベース作成 / Create PostgreSQL Database

- "New +" → "PostgreSQL" を選択
- **Name:** job-scraper-db
- **Database:** jobscraper
- **Plan:** Starter ($7/month)
- **Region:** Oregon (US West)

データベース作成後、Internal Database URLをコピー

#### 3. Web Service作成 / Create Web Service

- "New +" → "Web Service" を選択
- GitHubリポジトリを接続

#### 4. サービス設定 / Service Settings

**Name:** job-scraper-backend

**Region:** Oregon (US West)

**Root Directory:** `backend`

**Runtime:** Docker

**Plan:** Starter ($7/month)

**Dockerfile Path:** `./Dockerfile`

#### 5. 環境変数設定 / Environment Variables

| Key | Value |
|-----|-------|
| DATABASE_URL | [PostgreSQLのInternal Database URL] |
| SECRET_KEY | [ランダムな文字列を生成] |
| CSHARP_SCRAPER_PATH | /app/csharp/JobScraperCore |
| PYTHONUNBUFFERED | 1 |

#### 6. ヘルスチェック設定 / Health Check

**Health Check Path:** `/health`

#### 7. デプロイ / Deploy

"Create Web Service" ボタンをクリック

#### 8. バックエンドURLの確認 / Get Backend URL

デプロイ完了後、表示されるURLをコピーして、Vercelの環境変数`NEXT_PUBLIC_API_URL`に設定

## 使用方法 / Usage

### 1. 求人検索 / Job Search

1. トップページにアクセス
2. 求人サイトの検索結果URLを入力
3. "スクレイピング開始" ボタンをクリック
4. 結果がテーブル形式で表示される
5. CSVダウンロードリンクが生成される

### 2. 履歴確認 / View History

1. ナビゲーションバーの "履歴" をクリック
2. フィルターを適用（任意）
3. 過去のスクレイピング結果を確認
4. CSVをダウンロード

## API エンドポイント / API Endpoints

### スクレイピング / Scraping

```
POST /api/scrape
Content-Type: application/json

{
  "url": "https://www.atgp.jp/..."
}
```

### 履歴取得 / Get History

```
GET /api/history?site=atgp&start_date=2024-01-01&end_date=2024-12-31
```

### CSVダウンロード / Download CSV

```
GET /api/download/{history_id}
```

### ヘルスチェック / Health Check

```
GET /health
```

## トラブルシューティング / Troubleshooting

### スクレイピングが失敗する / Scraping Fails

- URLが正しいか確認
- 対応サイトかどうか確認
- サイトの構造が変更されていないか確認

### データベース接続エラー / Database Connection Error

- DATABASE_URL環境変数を確認
- PostgreSQLが起動しているか確認
- ファイアウォール設定を確認

### C#スクレイパーが見つからない / C# Scraper Not Found

- CSHARP_SCRAPER_PATH環境変数を確認
- C#プロジェクトがビルドされているか確認
- .NET Runtimeがインストールされているか確認

## ライセンス / License

MIT License

## サポート / Support

問題が発生した場合は、GitHubのIssuesに報告してください。

For issues, please report on GitHub Issues.
