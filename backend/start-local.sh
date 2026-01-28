#!/bin/bash

# バックエンドローカル起動スクリプト

echo "==================================="
echo "  Job Scraper Backend - Local Setup"
echo "==================================="

# カレントディレクトリ確認
if [ ! -f "composer.json" ]; then
    echo "エラー: このスクリプトはbackendディレクトリで実行してください"
    exit 1
fi

# Composerの依存関係をインストール
echo "[1/6] Composer依存関係をインストール中..."
composer install

# .envファイルが存在しない場合は作成
if [ ! -f ".env" ]; then
    echo "[2/6] .envファイルを作成中..."
    cp .env.example .env
    php artisan key:generate
else
    echo "[2/6] .envファイルは既に存在します"
fi

# ストレージディレクトリの権限設定
echo "[3/6] ストレージディレクトリの権限を設定中..."
chmod -R 775 storage bootstrap/cache

# シンボリックリンクを作成
echo "[4/6] シンボリックリンクを作成中..."
php artisan storage:link

# Python依存関係をインストール
echo "[5/6] Python依存関係をインストール中..."
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt

# Laravelサーバーを起動
echo "[6/6] Laravelサーバーを起動中..."
echo ""
echo "バックエンドサーバーが http://localhost:8000 で起動します"
echo "停止するには Ctrl+C を押してください"
echo ""
php artisan serve --host=0.0.0.0 --port=8000
