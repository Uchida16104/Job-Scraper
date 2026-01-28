# Job Scraper - 完全デプロイ手順書

## 目次
1. [ローカル開発環境のセットアップ](#ローカル開発環境のセットアップ)
2. [Render (バックエンド) のデプロイ設定](#render-バックエンド-のデプロイ設定)
3. [Vercel (フロントエンド) のデプロイ設定](#vercel-フロントエンド-のデプロイ設定)
4. [Gitリポジトリのセットアップとデプロイ](#gitリポジトリのセットアップとデプロイ)
5. [動作確認](#動作確認)
6. [トラブルシューティング](#トラブルシューティング)

---

## ローカル開発環境のセットアップ

### 前提条件

以下のソフトウェアがインストールされている必要があります:

- **PHP 8.1以上** (Laravelの要件)
- **Composer** (PHPの依存関係管理)
- **Node.js 18以上** (Next.jsの要件)
- **npm** (Node.jsに付属)
- **Python 3.9以上** (スクレイピングスクリプト)
- **Google Chrome** (Seleniumで使用)
- **Git** (バージョン管理)

### ステップ1: プロジェクトのクローン

```bash
# GitHubからクローン (リポジトリ作成後)
git clone https://github.com/あなたのユーザー名/job-scraper.git
cd job-scraper
```

### ステップ2: バックエンドのセットアップ

```bash
# バックエンドディレクトリに移動
cd backend

# 自動セットアップスクリプトを実行
./start-local.sh

# または手動でセットアップする場合:

# 1. Composer依存関係をインストール
composer install

# 2. .envファイルを作成
cp .env.example .env

# 3. アプリケーションキーを生成
php artisan key:generate

# 4. ストレージディレクトリの権限設定
chmod -R 775 storage bootstrap/cache

# 5. シンボリックリンクを作成
php artisan storage:link

# 6. Python依存関係をインストール
pip3 install -r requirements.txt --break-system-packages
# または
pip3 install -r requirements.txt

# 7. Laravelサーバーを起動
php artisan serve --host=0.0.0.0 --port=8000
```

バックエンドサーバーが `http://localhost:8000` で起動します。

### ステップ3: フロントエンドのセットアップ

**新しいターミナルウィンドウを開きます**

```bash
# プロジェクトルートから移動
cd job-scraper/frontend

# 自動セットアップスクリプトを実行
./start-local.sh

# または手動でセットアップする場合:

# 1. npm依存関係をインストール
npm install

# 2. .env.localファイルを作成
cp .env.local.example .env.local

# 3. .env.localを編集してバックエンドURLを設定
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# 4. Next.js開発サーバーを起動
npm run dev
```

フロントエンドサーバーが `http://localhost:3000` で起動します。

### ステップ4: ローカルテスト

1. ブラウザで `http://localhost:3000` にアクセス
2. 求人サイトのURLを入力 (例: `https://www.atgp.jp/`)
3. 「実行」ボタンをクリック
4. スクレイピングが完了すると、CSV/XLSXファイルのダウンロードリンクが表示されます
5. リンクをクリックしてファイルをダウンロード

**ローカルテストが成功したら、次のデプロイステップに進みます。**

---

## Render (バックエンド) のデプロイ設定

### ステップ1: Renderアカウントの作成

1. [Render](https://render.com) にアクセス
2. GitHubアカウントでサインアップ
3. GitHubリポジトリへのアクセスを許可

### ステップ2: Web Serviceの作成

1. Renderダッシュボードで **「New +」** → **「Web Service」** をクリック
2. GitHubリポジトリ `job-scraper` を選択
3. 以下の設定を入力:

#### 基本設定 (Basic Settings)

| 項目 | 設定値 |
|------|--------|
| **Name** | `job-scraper-backend` (任意の名前) |
| **Region** | `Singapore (Southeast Asia)` **推奨** (または `Oregon (US West)`) |
| **Branch** | `main` (またはデフォルトブランチ名) |
| **Root Directory** | `backend` |
| **Runtime** | `Docker` |
| **Dockerfile Path** | `backend/Dockerfile` |

#### Environment Variables (環境変数)

以下の環境変数を **Add Environment Variable** から追加します:

```
APP_NAME=JobScraper
APP_ENV=production
APP_KEY=base64:ここにランダムな文字列を入力
APP_DEBUG=false
APP_URL=https://あなたのアプリ名.onrender.com
LOG_CHANNEL=stack
LOG_LEVEL=info
FRONTEND_URL=https://あなたのVercelアプリ.vercel.app
SESSION_DRIVER=file
SESSION_LIFETIME=120
FILESYSTEM_DISK=public
```

**重要: APP_KEYの生成方法**

ローカルで以下のコマンドを実行してAPP_KEYを生成します:

```bash
cd backend
php artisan key:generate --show
```

出力された `base64:xxxxx...` の形式の文字列をコピーして、RenderのAPP_KEY環境変数に設定します。

**APP_URLとFRONTEND_URLについて:**
- 最初は仮の値を入力し、デプロイ後にRenderから割り当てられたURLで更新します
- Renderのデプロイが完了すると、`https://your-app-name.onrender.com` のようなURLが発行されます

### ステップ3: デプロイの開始

1. **「Create Web Service」** をクリック
2. Renderが自動的にDockerイメージをビルドし、デプロイを開始します
3. 初回デプロイには5〜10分かかります (Chromeのインストールなどがあるため)
4. デプロイが完了すると、ステータスが **「Live」** になります

### ステップ4: 環境変数の更新

デプロイ完了後、割り当てられたURLで環境変数を更新します:

1. Renderダッシュボードで `job-scraper-backend` サービスを選択
2. **「Environment」** タブをクリック
3. `APP_URL` を実際のURLに更新 (例: `https://job-scraper-backend.onrender.com`)
4. **「Save Changes」** をクリック
5. サービスが自動的に再デプロイされます

---

## Vercel (フロントエンド) のデプロイ設定

### ステップ1: Vercelアカウントの作成

1. [Vercel](https://vercel.com) にアクセス
2. GitHubアカウントでサインアップ
3. GitHubリポジトリへのアクセスを許可

### ステップ2: プロジェクトのインポート

1. Vercelダッシュボードで **「Add New...」** → **「Project」** をクリック
2. GitHubリポジトリ `job-scraper` を選択
3. **「Import」** をクリック

### ステップ3: プロジェクト設定

#### Build & Development Settings

| 項目 | 設定値 |
|------|--------|
| **Framework Preset** | `Next.js` |
| **Root Directory** | `frontend` (Edit → `frontend` を選択) |
| **Build Command** | `npm run build` (デフォルト) |
| **Output Directory** | `.next` (デフォルト) |
| **Install Command** | `npm install` (デフォルト) |

#### Environment Variables (環境変数)

**Add Environment Variable** から以下を追加:

```
NEXT_PUBLIC_BACKEND_URL=https://your-backend-app.onrender.com
```

**重要:** 
- `your-backend-app.onrender.com` は前のステップでRenderからコピーしたバックエンドのURLに置き換えます
- 例: `https://job-scraper-backend.onrender.com`

### ステップ4: デプロイの開始

1. **「Deploy」** をクリック
2. Vercelが自動的にビルドとデプロイを開始します
3. 初回デプロイには2〜3分かかります
4. デプロイが完了すると、**「Visit」** ボタンが表示されます

### ステップ5: Renderの環境変数を更新

Vercelから割り当てられたURLをRenderの環境変数に設定します:

1. Vercelのデプロイ完了後、割り当てられたURL (例: `https://job-scraper-xxx.vercel.app`) をコピー
2. Renderダッシュボードに戻る
3. `job-scraper-backend` サービスの **「Environment」** タブを開く
4. `FRONTEND_URL` を実際のVercel URLに更新
5. **「Save Changes」** をクリック

---

## Gitリポジトリのセットアップとデプロイ

### ステップ1: GitHubリポジトリの作成

1. [GitHub](https://github.com) にログイン
2. **「New repository」** をクリック
3. リポジトリ名: `job-scraper`
4. **Public** または **Private** を選択
5. **「Create repository」** をクリック

### ステップ2: ローカルリポジトリの初期化とプッシュ

```bash
# プロジェクトルートディレクトリに移動
cd job-scraper

# Gitリポジトリを初期化
git init

# 全ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Job Scraper with Laravel backend and Next.js frontend"

# リモートリポジトリを追加 (GitHubで作成したリポジトリのURLに置き換え)
git remote add origin https://github.com/あなたのユーザー名/job-scraper.git

# メインブランチにプッシュ
git branch -M main
git push -u origin main
```

### ステップ3: 自動デプロイの確認

RenderとVercelは自動デプロイが有効になっているため、`git push` するたびに自動的に再デプロイされます。

```bash
# 変更を加えた後
git add .
git commit -m "Update: 変更内容の説明"
git push origin main

# RenderとVercelで自動デプロイが開始されます
```

---

## 動作確認

### 本番環境での動作テスト

1. VercelのURLにアクセス (例: `https://job-scraper-xxx.vercel.app`)
2. 求人サイトのURLを入力 (例: `https://www.atgp.jp/`)
3. 「実行」ボタンをクリック
4. スクレイピングが完了するまで待機 (30秒〜2分程度)
5. ダウンロードリンクが表示されたら、CSV/XLSXファイルをクリックしてダウンロード
6. ファイルが正常にダウンロードできることを確認

### チェックリスト

- [ ] フロントエンドが正常に表示される
- [ ] URLを入力して送信できる
- [ ] バックエンドでスクレイピングが実行される
- [ ] CSV/XLSXファイルが生成される
- [ ] ダウンロードリンクが表示される
- [ ] ファイルがダウンロードできる
- [ ] ダウンロードしたファイルにデータが含まれている

---

## トラブルシューティング

### バックエンドのエラー

#### エラー: "APP_KEY not set"

**原因:** APP_KEYが環境変数に設定されていない

**解決方法:**
1. ローカルで `php artisan key:generate --show` を実行
2. 出力された `base64:xxx...` の値をコピー
3. Renderの環境変数 `APP_KEY` に設定
4. サービスを再デプロイ

#### エラー: "Python script not found"

**原因:** main.pyが正しい場所に配置されていない

**解決方法:**
1. `backend/main.py` が存在することを確認
2. Gitにコミットされているか確認 (`.gitignore` で除外されていないか)
3. 再度 `git push` してデプロイ

#### エラー: "Permission denied" (storage)

**原因:** ストレージディレクトリの書き込み権限がない

**解決方法:**
- Dockerfileで `chmod -R 775 storage` が実行されているか確認
- Renderのログで権限エラーがないか確認

#### エラー: Chromedriver/Selenium関連

**原因:** Chrome またはChromeDriverが正しくインストールされていない

**解決方法:**
- Dockerfileで Google Chrome と依存関係が正しくインストールされているか確認
- ログで Chrome のインストールエラーがないか確認

### フロントエンドのエラー

#### エラー: "Cannot connect to backend"

**原因:** バックエンドURLが間違っているか、CORSエラー

**解決方法:**
1. Vercelの環境変数 `NEXT_PUBLIC_BACKEND_URL` が正しいか確認
2. RenderのバックエンドがLiveステータスか確認
3. Renderの環境変数 `FRONTEND_URL` にVercelのURLが設定されているか確認
4. ブラウザのコンソールでCORSエラーを確認

#### エラー: htmx/Alpine.js が動作しない

**原因:** CDNから読み込めていない

**解決方法:**
- ブラウザのコンソールで読み込みエラーがないか確認
- Next.jsのビルドログでエラーがないか確認

### 一般的な問題

#### ファイルがダウンロードできない

**チェックポイント:**
1. バックエンドログでPythonスクリプトが正常に実行されているか
2. `storage/app/public/downloads/` ディレクトリが作成されているか
3. CSV/XLSXファイルが実際に生成されているか
4. ダウンロードURLが正しいか (404エラーでないか)

#### スクレイピングが遅い / タイムアウト

**原因:** サイトの読み込みが遅い、または要素が見つからない

**解決方法:**
- main.pyの`timeout`パラメータを増やす
- サイトの構造が変わっていないか確認
- テスト用の別の求人サイトで試す

---

## サポート情報

### ログの確認方法

**Render (バックエンド):**
1. Renderダッシュボードでサービスを選択
2. **「Logs」** タブをクリック
3. リアルタイムログを確認

**Vercel (フロントエンド):**
1. Vercelダッシュボードでプロジェクトを選択
2. デプロイメントをクリック
3. **「Build Logs」** または **「Function Logs」** を確認

### 環境変数の確認

すべての環境変数が正しく設定されているか、以下のチェックリストで確認してください:

**Render:**
- [x] APP_NAME
- [x] APP_ENV=production
- [x] APP_KEY (base64:で始まる長い文字列)
- [x] APP_DEBUG=false
- [x] APP_URL (Renderから割り当てられたURL)
- [x] FRONTEND_URL (VercelのURL)

**Vercel:**
- [x] NEXT_PUBLIC_BACKEND_URL (RenderのURL)

---

## まとめ

このガイドに従うことで、以下が実現されます:

1. ✅ ローカル開発環境での動作確認
2. ✅ Renderでのバックエンド (Laravel + Python) のデプロイ
3. ✅ Vercelでのフロントエンド (Next.js) のデプロイ
4. ✅ Git pushによる自動デプロイ
5. ✅ エラーなく動作する本番環境

**全てのステップが正常に完了すれば、エラーなく確実に動作します。**

問題が発生した場合は、トラブルシューティングセクションを参照してください。
