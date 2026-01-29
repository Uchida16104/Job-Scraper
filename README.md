# Job Scraper

求人サイトから情報を自動抽出してCSV/Excel形式でダウンロードできるWebアプリケーション

## 対応サイト

- atgp
- マイナーリーグ
- LITALICO仕事ナビ
- dodaチャレンジ
- Indeed
- マイナビ
- リクナビNEXT

## 技術スタック

### フロントエンド
- HTMX
- Alpine.js
- Tailwind CSS
- Vercel (ホスティング)

### バックエンド
- Python 3.11
- Flask
- BeautifulSoup4
- Pandas
- Render (ホスティング)

## デプロイ方法

### フロントエンド (Vercel)

1. Vercelアカウントにログイン
2. 新規プロジェクト作成
3. GitHubリポジトリを接続
4. Root Directoryを`frontend`に設定
5. デプロイ

### バックエンド (Render)

1. Renderアカウントにログイン
2. 新規Web Service作成
3. GitHubリポジトリを接続
4. Root Directoryを`backend`に設定
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn main:app`
7. デプロイ

## ローカル開発

### フロントエンド
```bash
cd frontend
npm run dev
```

ブラウザで http://localhost:3000 を開く

### バックエンド
```bash
cd backend
pip install -r requirements.txt
python main.py
```

サーバーは http://localhost:10000 で起動

## 使用方法

1. 求人検索結果ページのURLを入力
2. 最大取得件数を設定（デフォルト100件）
3. スクレイピング開始ボタンをクリック
4. 完了後、CSV/Excelファイルをダウンロード

## 抽出される情報

- 会社名
- 職種
- 勤務地
- 雇用形態
- 給与
- 求人URL
- 月給換算（下限）

## 注意
- ***結果データは必ずしも保証されたものではありません。必ず、分析元の求人サイトから直接再確認する事をお勧めします。***

## ライセンス

MIT
