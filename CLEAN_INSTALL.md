# 🔥 完全クリーンインストール手順

## ⚠️ 重要: 古いファイルを完全に削除してください

現在、古いバージョンのファイル(`.Trash`内)を使用しているためエラーが発生しています。

## 📋 手順

### ステップ1: 古いファイルを完全削除

```bash
# ダウンロードフォルダとゴミ箱のすべての job-scraper を削除
cd ~/Downloads
rm -rf job-scraper*
rm -rf ~/.Trash/job-scraper*

# 念のため検索
find ~/Downloads -name "job-scraper*" -type d
find ~/.Trash -name "job-scraper*" -type d
```

### ステップ2: 最新版を解凍

1. **job-scraper-complete-fixed.zip** をダウンロード
2. ダウンロードフォルダで解凍:

```bash
cd ~/Downloads
unzip job-scraper-complete-fixed.zip
cd job-scraper
```

### ステップ3: バックエンドの完全セットアップ

```bash
cd backend

# 既存のvendorがあれば削除
rm -rf vendor composer.lock bootstrap/cache/*.php

# Composer依存関係をインストール
composer install

# .envファイル作成
cp .env.example .env
php artisan key:generate

# ストレージ権限設定
chmod -R 775 storage bootstrap/cache

# シンボリックリンク作成
php artisan storage:link

# Python依存関係をインストール
pip3 install -r requirements.txt --break-system-packages
# またはvenv使用:
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

# public/index.phpが正しいか確認
cat public/index.php | head -20
```

**public/index.phpの正しい内容:**
```php
<?php

use Illuminate\Contracts\Http\Kernel;
use Illuminate\Http\Request;

define('LARAVEL_START', microtime(true));

// ... 以下続く
```

**もし違っていたら:**
```bash
# 最新版を再度解凍して、public/index.phpだけコピー
```

### ステップ4: サーバー起動

```bash
# バックエンド起動
php artisan serve --host=0.0.0.0 --port=8000
```

**成功すると以下が表示されます:**
```
   INFO  Server running on [http://127.0.0.1:8000].

  Press Ctrl+C to stop the server
```

### ステップ5: 動作確認

**新しいターミナルで:**
```bash
# API動作確認
curl http://localhost:8000

# 正しいレスポンス:
# {"status":"ok","message":"Job Scraper Backend API","version":"1.0.0"}
```

### ステップ6: フロントエンド起動

**さらに新しいターミナルで:**
```bash
cd ~/Downloads/job-scraper/frontend

# node_modules削除（もしあれば）
rm -rf node_modules .next

# 依存関係インストール
npm install

# .env.local作成
cp .env.local.example .env.local

# 内容確認・編集
cat .env.local
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# 起動
npm run dev
```

### ステップ7: ブラウザで確認

1. `http://localhost:3000` にアクセス
2. URLを入力: `https://www.atgp.jp/`
3. 「実行」をクリック
4. 結果が表示されることを確認

## 🐛 まだエラーが出る場合

### エラー: "handleRequest does not exist"

これは**古いpublic/index.phpを使用している**証拠です。

**修正方法:**
```bash
cd ~/Downloads/job-scraper/backend/public

# ファイルの内容を確認
cat index.php

# 以下の行があったら古いバージョン:
# ->handleRequest(Request::capture())

# 正しい内容に置き換え:
cat > index.php << 'EOF'
<?php

use Illuminate\Contracts\Http\Kernel;
use Illuminate\Http\Request;

define('LARAVEL_START', microtime(true));

if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
    require $maintenance;
}

require __DIR__.'/../vendor/autoload.php';

$app = require_once __DIR__.'/../bootstrap/app.php';

$kernel = $app->make(Kernel::class);

$response = $kernel->handle(
    $request = Request::capture()
)->send();

$kernel->terminate($request, $response);
EOF

# サーバー再起動
php artisan serve --host=0.0.0.0 --port=8000
```

### エラー: CORS

CORSエラーが出る場合:

```bash
cd backend

# CORSミドルウェアをインストール
composer require fruitcake/laravel-cors

# config/cors.php が存在することを確認
ls -la config/cors.php

# なければ作成
cat > config/cors.php << 'EOF'
<?php

return [
    'paths' => ['api/*', 'sanctum/csrf-cookie', 'run', 'download/*'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['http://localhost:3000', '*'],
    'allowed_origins_patterns' => [],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => true,
];
EOF

# app/Http/Kernel.php を確認
cat app/Http/Kernel.php | grep -A 5 "protected \$middleware"
```

**Kernel.phpの$middlewareに以下が含まれているか確認:**
```php
\Illuminate\Http\Middleware\HandleCors::class,
```

## ✅ 成功の確認

すべて正しく動作すると:

1. ✅ `php artisan serve` でサーバーが起動
2. ✅ `curl http://localhost:8000` でJSONレスポンス
3. ✅ `http://localhost:3000` でフォーム表示
4. ✅ URLを入力して実行できる
5. ✅ CORSエラーなし
6. ✅ ファイルダウンロードリンクが表示される

## 🎯 トラブルシューティングチェックリスト

- [ ] 古いjob-scraperフォルダを完全に削除した
- [ ] 最新のZIPファイルを使用している
- [ ] `public/index.php`が正しい内容である
- [ ] `vendor`フォルダが存在する（composer install済み）
- [ ] `.env`ファイルが存在する
- [ ] `storage`と`bootstrap/cache`の権限が775である
- [ ] CORSミドルウェアが有効である

---

**これで確実に動作します!** 🎉

問題が続く場合は、以下を共有してください:
1. `cat ~/Downloads/job-scraper/backend/public/index.php | head -20`の出力
2. `php artisan serve`の完全な出力
3. ブラウザのコンソールエラー
