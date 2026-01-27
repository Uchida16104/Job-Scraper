# デプロイマニュアル（初心者向け） / Deployment Manual (For Beginners)

このガイドでは、求人スクレイピングシステムをVercel（フロントエンド）とRender（バックエンド）にデプロイする手順を詳しく説明します。

This guide provides detailed instructions for deploying the Job Scraping System to Vercel (frontend) and Render (backend).

---

## 事前準備 / Prerequisites

### 1. アカウント作成 / Account Creation

以下のサービスでアカウントを作成してください：

Create accounts on the following services:

- **GitHub**: https://github.com
- **Vercel**: https://vercel.com
- **Render**: https://render.com

### 2. GitHubリポジトリ作成 / Create GitHub Repository

1. GitHubにログイン
2. "New repository" をクリック
3. リポジトリ名を入力（例：job-scraper-system）
4. "Create repository" をクリック

### 3. コードをGitHubにプッシュ / Push Code to GitHub

```bash
cd job-scraper-system
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/job-scraper-system.git
git push -u origin main
```

---

## パート1: Renderへのバックエンドデプロイ / Part 1: Backend Deployment to Render

### ステップ1: PostgreSQLデータベースの作成 / Step 1: Create PostgreSQL Database

#### 1-1. Renderダッシュボードにアクセス

https://dashboard.render.com にアクセスしてログイン

#### 1-2. データベース作成

1. 画面右上の **"New +"** ボタンをクリック
2. **"PostgreSQL"** を選択

#### 1-3. データベース設定

| 項目 / Field | 値 / Value |
|-------------|-----------|
| Name | job-scraper-db |
| Database | jobscraper |
| User | postgres (自動生成 / Auto-generated) |
| Region | Oregon (US West) |
| PostgreSQL Version | 15 (最新 / Latest) |
| Datadog API Key | 空欄 / Leave empty |
| Plan | Starter ($7/month) |

#### 1-4. 作成

**"Create Database"** ボタンをクリック

#### 1-5. 接続情報の保存

データベースが作成されたら、以下の情報をメモ帳にコピーして保存してください：

- **Internal Database URL**: `postgresql://postgres:...@...`
- **External Database URL**: `postgresql://postgres:...@...`

バックエンドのデプロイで **Internal Database URL** を使用します。

---

### ステップ2: Web Serviceの作成 / Step 2: Create Web Service

#### 2-1. Web Service作成開始

1. Renderダッシュボードに戻る
2. **"New +"** → **"Web Service"** を選択

#### 2-2. リポジトリ接続

1. **"Connect a repository"** セクションで、GitHubアカウントを接続
2. 作成したリポジトリ（job-scraper-system）を選択
3. **"Connect"** をクリック

#### 2-3. サービス設定

| 項目 / Field | 値 / Value |
|-------------|-----------|
| Name | job-scraper-backend |
| Region | Oregon (US West) |
| Branch | main |
| Root Directory | `backend` |
| Runtime | Docker |
| Plan | Starter ($7/month) |

#### 2-4. 環境変数の設定

**"Advanced"** セクションを展開し、以下の環境変数を追加：

| Key | Value | 説明 / Description |
|-----|-------|-------------------|
| DATABASE_URL | [ステップ1-5でコピーしたInternal Database URL] | データベース接続URL |
| SECRET_KEY | [ランダムな64文字の文字列] | JWT認証用シークレット |
| CSHARP_SCRAPER_PATH | /app/csharp/JobScraperCore | C#スクレイパーのパス |
| PYTHONUNBUFFERED | 1 | Pythonログ出力設定 |

**SECRET_KEYの生成方法:**

以下のコマンドを実行してランダムな文字列を生成：

```bash
openssl rand -hex 32
```

または、オンラインツールを使用：
https://www.random.org/strings/

#### 2-5. ヘルスチェック設定

**"Health Check Path"** に `/health` と入力

#### 2-6. デプロイ開始

**"Create Web Service"** ボタンをクリック

#### 2-7. デプロイ完了を確認

デプロイには5-10分かかります。ログを確認して、以下のメッセージが表示されれば成功です：

```
==> Your service is live 🎉
```

#### 2-8. バックエンドURLの保存

デプロイ完了後、画面上部に表示されるURLをコピーして保存してください：

例: `https://job-scraper-backend.onrender.com`

このURLは次のVercelデプロイで使用します。

---

## パート2: Vercelへのフロントエンドデプロイ / Part 2: Frontend Deployment to Vercel

### ステップ3: Vercelプロジェクトの作成 / Step 3: Create Vercel Project

#### 3-1. Vercelダッシュボードにアクセス

https://vercel.com/dashboard にアクセスしてログイン

#### 3-2. 新規プロジェクト作成

1. **"Add New..."** → **"Project"** をクリック
2. **"Import Git Repository"** セクションで、GitHubアカウントを接続
3. job-scraper-systemリポジトリの **"Import"** をクリック

#### 3-3. プロジェクト設定

| 項目 / Field | 値 / Value |
|-------------|-----------|
| Framework Preset | Next.js |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `.next` |
| Install Command | `npm install` |

**"Root Directory"の設定:**
- **"Edit"** ボタンをクリック
- `frontend` と入力
- **"Continue"** をクリック

#### 3-4. 環境変数の設定

**"Environment Variables"** セクションで以下を追加：

| Name | Value |
|------|-------|
| NEXT_PUBLIC_API_URL | [ステップ2-8でコピーしたバックエンドURL] |

例: `https://job-scraper-backend.onrender.com`

#### 3-5. デプロイ開始

**"Deploy"** ボタンをクリック

#### 3-6. デプロイ完了を確認

デプロイには3-5分かかります。完了すると、以下のような成功画面が表示されます：

```
🎉 Congratulations!
Your project is live
```

#### 3-7. フロントエンドURLの確認

画面に表示されるURLをクリックして、アプリケーションにアクセス：

例: `https://job-scraper-system.vercel.app`

---

## パート3: 動作確認 / Part 3: Testing

### ステップ4: アプリケーションのテスト / Step 4: Test Application

#### 4-1. ヘルスチェック

ブラウザで以下のURLにアクセス：

```
https://job-scraper-backend.onrender.com/health
```

以下のレスポンスが表示されればOK：

```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### 4-2. フロントエンドアクセス

Vercelから提供されたURLにアクセス：

```
https://job-scraper-system.vercel.app
```

トップページが表示されることを確認。

#### 4-3. スクレイピングテスト

1. トップページの入力欄に求人サイトのURLを入力
2. **"スクレイピング開始"** ボタンをクリック
3. 結果が表示されることを確認
4. **"CSVダウンロード"** ボタンが表示されることを確認

#### 4-4. 履歴ページのテスト

1. ナビゲーションバーの **"履歴"** をクリック
2. スクレイピング履歴が表示されることを確認
3. **"ダウンロード"** ボタンをクリックしてCSVがダウンロードできることを確認

---

## トラブルシューティング / Troubleshooting

### 問題1: バックエンドのビルドが失敗する

**症状:** Renderのログに "Build failed" と表示される

**解決方法:**

1. Dockerfileが正しい位置にあるか確認
   - パス: `backend/Dockerfile`

2. requirements.txtが正しい位置にあるか確認
   - パス: `backend/requirements.txt`

3. Root Directoryが `backend` に設定されているか確認

### 問題2: データベース接続エラー

**症状:** `/health` にアクセスすると "Database connection failed" と表示される

**解決方法:**

1. DATABASE_URL環境変数が正しく設定されているか確認
   - Renderダッシュボード → Web Service → Environment
   - Internal Database URLを使用しているか確認

2. PostgreSQLデータベースが起動しているか確認
   - Renderダッシュボード → PostgreSQL → Status が "Available" になっているか

### 問題3: フロントエンドからバックエンドにアクセスできない

**症状:** スクレイピングボタンをクリックしても "Failed to fetch" エラーが表示される

**解決方法:**

1. NEXT_PUBLIC_API_URL環境変数が正しく設定されているか確認
   - Vercelダッシュボード → Settings → Environment Variables
   - バックエンドのURLが正しいか確認（https:// を含む）

2. バックエンドが正常に動作しているか確認
   - `https://your-backend.onrender.com/health` にアクセス

3. CORS設定を確認
   - バックエンドのログでCORSエラーが出ていないか確認

### 問題4: C#スクレイパーが動作しない

**症状:** スクレイピング時に "C# scraper not found" エラーが表示される

**解決方法:**

1. CSHARP_SCRAPER_PATH環境変数を確認
   - 値: `/app/csharp/JobScraperCore`

2. Dockerfileでのビルド設定を確認
   - C#プロジェクトが正しくビルドされているか

3. .NET Runtimeがインストールされているか確認
   - Dockerfileを確認

### 問題5: CSVダウンロードが404エラー

**症状:** CSVダウンロードボタンをクリックすると404エラーが表示される

**解決方法:**

1. OUTPUT_DIR環境変数を確認（設定していない場合はデフォルト値が使用される）

2. /app/data/output ディレクトリが作成されているか確認

3. ファイル書き込み権限があるか確認

---

## 環境変数一覧 / Environment Variables Reference

### Render (Backend)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | postgresql://postgres:...@... | PostgreSQL接続URL |
| SECRET_KEY | Yes | abc123...xyz789 | JWT認証用シークレット（64文字推奨） |
| CSHARP_SCRAPER_PATH | Yes | /app/csharp/JobScraperCore | C#スクレイパーの実行パス |
| PYTHONUNBUFFERED | Yes | 1 | Pythonログのバッファリング無効化 |

### Vercel (Frontend)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | Yes | https://job-scraper-backend.onrender.com | バックエンドAPIのURL |

---

## デプロイ後の設定 / Post-Deployment Configuration

### カスタムドメインの設定（オプション）

#### Vercel

1. Vercelダッシュボード → Settings → Domains
2. カスタムドメインを入力
3. DNSレコードを設定

#### Render

1. Renderダッシュボード → Settings → Custom Domain
2. カスタムドメインを入力
3. DNSレコードを設定

### 自動デプロイの設定

#### GitHub連携の確認

- Vercel: 自動的にGitHubと連携され、mainブランチへのpushで自動デプロイ
- Render: 自動的にGitHubと連携され、mainブランチへのpushで自動デプロイ

---

## サポート / Support

質問や問題がある場合：

1. GitHubのIssuesに報告
2. Renderのサポートチャットを利用
3. Vercelのサポートチャットを利用

---

## 費用 / Pricing

### 月額費用概算

- **Render PostgreSQL Starter**: $7/月
- **Render Web Service Starter**: $7/月
- **Vercel Hobby Plan**: 無料

**合計**: 約$14/月（フロントエンドは無料）

### 無料枠の活用

- Vercelは無料プランで十分な機能を提供
- Renderは初回$5クレジットが付与される場合あり

---

## まとめ / Summary

このマニュアルに従うことで、以下が完了します：

This manual completes the following:

1. ✅ PostgreSQLデータベースの作成
2. ✅ RenderへのDockerバックエンドのデプロイ
3. ✅ VercelへのNext.jsフロントエンドのデプロイ
4. ✅ 環境変数の正しい設定
5. ✅ 動作確認とテスト

デプロイが完了したら、アプリケーションは24時間365日稼働し、世界中からアクセス可能になります！

🎉 おめでとうございます！デプロイ完了です！ / Congratulations! Deployment Complete! 🎉
