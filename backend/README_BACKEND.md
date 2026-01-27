# Backend README (Render)

## 簡単な使い方
1. このフォルダに `main.py`（元のスクレイパー）を置く（既にある想定）。
2. `pip install -r requirements.txt`
3. `python app.py` でローカル起動（`PORT` 環境変数を使用）。

## Render にデプロイする際の重要注意点（必読）
- **Selenium + Chrome の問題**:
  - `main.py` が Selenium / Chrome を使っている場合、Render のデフォルト環境には Chrome / Chromium 実行環境が用意されていないため、Selenium が失敗する可能性が高いです。
  - 回避策：
    1. **Browserless（外部ヘッドレスブラウザサービス）を使う（推奨）**：
       - browserless.io 等のサービスを契約し、`BROWSERLESS_URL`（例: `wss://chrome.browserless.io?token=...`）を取得してください。
       - そして `main.py` を外部ブラウザに接続するよう **1行だけ修正**する必要があります（下記参照）。  
         > NOTE: `main.py` を「全く変更したくない」とのことですが、Render 非 Docker 環境で Chrome を用意するよりは、「main.py に一行（リモート webdriver に接続するため）」を許容する方が現実的で安定します。
    2. **Docker で Chrome を同梱して Render にデプロイ**（安定だが Docker を使う）：
       - Dockerfile を作り、Chrome と ChromeDriver をインストールしてアプリを動かす方法。安定するが Docker を許容する必要があります。
    3. **自分で Chrome をダウンロードして PATH に置く**（上級者向け、Render では制約あり）。
- **推奨設定（Render Web Service）**:
  - Region: `oregon`（またはお好み）
  - Root Directory: `backend`
  - Build Command:
    ```
    pip install -r requirements.txt
    ```
    （もし browserless を使う場合はそのまま）
  - Start Command:
    ```
    gunicorn app:app -b 0.0.0.0:$PORT --workers=1
    ```
  - Environment Variables:
    - `SCRAPE_TIMEOUT` (optional) — デフォルト `240`
    - `BROWSERLESS_URL` (任意) — 外部ヘッドレスを使う場合
    - その他 API キー等

## main.py を最小修正して remote webdriver（browserless 等）を使うサンプル
（あなたの main.py の webdriver の生成コード付近に以下を条件分岐で入れるイメージです）

```python
# main.py の webdriver を作る箇所の近くに（例示）
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BROWSERLESS_URL = os.environ.get("BROWSERLESS_URL")
if BROWSERLESS_URL:
    # remote webdriver を使う（Browserless 等の URL）
    driver = webdriver.Remote(
        command_executor=BROWSERLESS_URL,
        desired_capabilities=DesiredCapabilities.CHROME
    )
else:
    # 既存のローカル chrome/chromedriver を使う処理（そのまま）
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless=new")
    ...
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

