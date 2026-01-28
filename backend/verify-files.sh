#!/bin/bash

# Job Scraper ファイル検証スクリプト

echo "=================================="
echo "  Job Scraper File Verification"
echo "=================================="
echo ""

# カレントディレクトリ確認
if [ ! -f "public/index.php" ]; then
    echo "❌ エラー: このスクリプトはbackendディレクトリで実行してください"
    exit 1
fi

echo "✓ 正しいディレクトリです"
echo ""

# public/index.php のチェック
echo "[1/5] public/index.php をチェック中..."
if grep -q "handleRequest" public/index.php; then
    echo "❌ 古いバージョンのpublic/index.phpです!"
    echo "   修正が必要: handleRequest → kernel->handle"
    echo ""
    echo "修正コマンド:"
    echo "cat > public/index.php << 'EOF'"
    echo '<?php'
    echo ''
    echo 'use Illuminate\Contracts\Http\Kernel;'
    echo 'use Illuminate\Http\Request;'
    echo ''
    echo "define('LARAVEL_START', microtime(true));"
    echo ''
    echo "if (file_exists(\$maintenance = __DIR__.'/../storage/framework/maintenance.php')) {"
    echo '    require $maintenance;'
    echo '}'
    echo ''
    echo "require __DIR__.'/../vendor/autoload.php';"
    echo ''
    echo "\$app = require_once __DIR__.'/../bootstrap/app.php';"
    echo ''
    echo "\$kernel = \$app->make(Kernel::class);"
    echo ''
    echo "\$response = \$kernel->handle("
    echo '    $request = Request::capture()'
    echo ')->send();'
    echo ''
    echo '$kernel->terminate($request, $response);'
    echo "EOF"
    exit 1
else
    echo "✓ public/index.php は正しいバージョンです"
fi

# bootstrap/app.php のチェック
echo "[2/5] bootstrap/app.php をチェック中..."
if grep -q "Application::configure" bootstrap/app.php; then
    echo "❌ 古いバージョンのbootstrap/app.phpです!"
    echo "   Laravel 11の構文が使用されています"
    exit 1
else
    echo "✓ bootstrap/app.php は正しいバージョンです"
fi

# Middlewareファイルのチェック
echo "[3/5] Middlewareファイルをチェック中..."
REQUIRED_MIDDLEWARE=(
    "app/Http/Middleware/VerifyCsrfToken.php"
    "app/Http/Middleware/TrustProxies.php"
    "app/Http/Middleware/EncryptCookies.php"
)

for file in "${REQUIRED_MIDDLEWARE[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file が見つかりません"
        exit 1
    fi
done
echo "✓ すべてのMiddlewareファイルが存在します"

# 設定ファイルのチェック
echo "[4/5] 設定ファイルをチェック中..."
REQUIRED_CONFIG=(
    "config/cors.php"
    "config/session.php"
    "config/cache.php"
)

for file in "${REQUIRED_CONFIG[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file が見つかりません"
        exit 1
    fi
done
echo "✓ すべての設定ファイルが存在します"

# requirements.txt のチェック
echo "[5/5] requirements.txt をチェック中..."
if grep -q "pandas==2.1.3" requirements.txt; then
    echo "⚠️  pandas 2.1.3 が指定されています（Python 3.13と非互換）"
    echo "   pandas 2.2.0 への更新を推奨します"
elif grep -q "pandas==2.2.0" requirements.txt; then
    echo "✓ pandas 2.2.0 が指定されています（Python 3.13互換）"
else
    echo "⚠️  pandasのバージョンが不明です"
fi

echo ""
echo "=================================="
echo "  ✅ 検証完了"
echo "=================================="
echo ""
echo "すべてのファイルが正しいバージョンです!"
echo ""
echo "次のステップ:"
echo "1. composer install"
echo "2. cp .env.example .env"
echo "3. php artisan key:generate"
echo "4. chmod -R 775 storage bootstrap/cache"
echo "5. php artisan storage:link"
echo "6. pip3 install -r requirements.txt --break-system-packages"
echo "7. php artisan serve"
