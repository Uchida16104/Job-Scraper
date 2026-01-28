#!/bin/bash

# フロントエンドローカル起動スクリプト

echo "====================================="
echo "  Job Scraper Frontend - Local Setup"
echo "====================================="

# カレントディレクトリ確認
if [ ! -f "package.json" ]; then
    echo "エラー: このスクリプトはfrontendディレクトリで実行してください"
    exit 1
fi

# npm依存関係をインストール
echo "[1/3] npm依存関係をインストール中..."
npm install

# .env.localファイルが存在しない場合は作成
if [ ! -f ".env.local" ]; then
    echo "[2/3] .env.localファイルを作成中..."
    cp .env.local.example .env.local
    echo "NEXT_PUBLIC_BACKEND_URL を http://localhost:8000 に設定しました"
else
    echo "[2/3] .env.localファイルは既に存在します"
fi

# Next.js開発サーバーを起動
echo "[3/3] Next.js開発サーバーを起動中..."
echo ""
echo "フロントエンドサーバーが http://localhost:3000 で起動します"
echo "停止するには Ctrl+C を押してください"
echo ""
npm run dev
