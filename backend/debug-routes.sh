#!/bin/bash

# Laravel ルートデバッグスクリプト

echo "=================================="
echo "  Laravel Route Debugging"
echo "=================================="
echo ""

# カレントディレクトリ確認
if [ ! -f "artisan" ]; then
    echo "❌ エラー: このスクリプトはbackendディレクトリで実行してください"
    exit 1
fi

echo "✓ 正しいディレクトリです"
echo ""

# キャッシュクリア
echo "[1/4] キャッシュをクリア中..."
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
echo "✓ キャッシュクリア完了"
echo ""

# ルート一覧表示
echo "[2/4] 登録されているルートを確認中..."
php artisan route:list | grep -E "POST.*run|GET.*download"
echo ""

# 設定確認
echo "[3/4] APP_URL確認..."
grep APP_URL .env || echo "APP_URL が設定されていません"
echo ""

# CSRF除外確認
echo "[4/4] CSRF除外設定を確認..."
cat app/Http/Middleware/VerifyCsrfToken.php | grep -A 5 "protected \$except"
echo ""

echo "=================================="
echo "  デバッグ情報"
echo "=================================="
echo ""

# curlでテスト
echo "テスト1: GET / (ルートページ)"
curl -s http://localhost:8000/ | head -3
echo ""
echo ""

echo "テスト2: POST /run (CSRFトークンなし)"
curl -s -X POST http://localhost:8000/run -d "link=https://example.com" | head -5
echo ""
echo ""

echo "=================================="
echo "  推奨アクション"
echo "=================================="
echo ""
echo "1. サーバーを再起動してください:"
echo "   Ctrl+C で停止"
echo "   php artisan serve --host=0.0.0.0 --port=8000"
echo ""
echo "2. ブラウザのキャッシュをクリアしてください"
echo ""
echo "3. フロントエンドを再起動してください:"
echo "   cd frontend"
echo "   npm run dev"
