# Render用Dockerfile - Laravel + Python + Selenium
# htmx CORS対応版

FROM php:8.2-apache

WORKDIR /var/www/html

# システムパッケージとPython、Chrome、依存関係をインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    python3 \
    python3-pandas \
    python3-numpy \
    python3-pip \
    python3-venv \
    python3-dev \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Google Chromeをインストール
RUN mkdir -p /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/google-chrome.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && chmod 644 /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# PHP拡張をインストール
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd zip

# Composerをインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Apacheの設定（htmx CORS対応）
RUN a2enmod rewrite headers
RUN sed -i 's!/var/www/html!/var/www/html/public!g' /etc/apache2/sites-available/000-default.conf
RUN echo '<Directory /var/www/html/public>\n\
    Options Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
    \n\
    # CORS設定（htmx対応）\n\
    Header always set Access-Control-Allow-Origin "*"\n\
    Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE"\n\
    Header always set Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With, HX-Request, HX-Trigger, HX-Trigger-Name, HX-Target, HX-Current-URL, HX-Boosted, HX-History-Restore-Request, HX-Prompt"\n\
    Header always set Access-Control-Expose-Headers "Content-Disposition, HX-Location, HX-Push-Url, HX-Redirect, HX-Refresh, HX-Replace-Url, HX-Reswap, HX-Retarget, HX-Reselect, HX-Trigger, HX-Trigger-After-Settle, HX-Trigger-After-Swap"\n\
    Header always set Access-Control-Allow-Credentials "true"\n\
    \n\
    # OPTIONSリクエストへの対応\n\
    RewriteEngine On\n\
    RewriteCond %{REQUEST_METHOD} OPTIONS\n\
    RewriteRule ^(.*)$ $1 [R=204,L]\n\
</Directory>' >> /etc/apache2/apache2.conf

# アプリケーションファイルをコピー
COPY . /var/www/html

# .env が無ければ .env.example をコピー
RUN if [ ! -f /var/www/html/.env ]; then \
      if [ -f /var/www/html/.env.example ]; then \
        cp /var/www/html/.env.example /var/www/html/.env; \
      else \
        touch /var/www/html/.env; \
      fi; \
    fi

# Pythonパッケージをインストール（pandas 2.2.3を使用）
RUN pip3 install --break-system-packages --no-cache-dir \
    selenium==4.15.2 \
    pandas==2.2.3 \
    openpyxl==3.1.2 \
    webdriver-manager==4.0.1

# Composer の安全なインストール
ENV COMPOSER_ALLOW_SUPERUSER=1
RUN composer install --no-dev --prefer-dist --no-interaction --no-progress --optimize-autoloader --no-scripts

# ディレクトリ構造と権限の事前設定
RUN mkdir -p bootstrap/cache \
             storage/framework/cache/data \
             storage/framework/sessions \
             storage/framework/views \
             storage/app/public/downloads \
             storage/logs \
 && chown -R www-data:www-data bootstrap storage vendor \
 && chmod -R 775 bootstrap storage

# アプリケーションキーの生成
RUN php artisan key:generate --force

# シンボリックリンク作成
RUN php artisan storage:link || true

# キャッシュ最適化
RUN php artisan config:cache || true \
 && php artisan route:cache || true \
 && php artisan view:cache || true

# 最終権限設定
RUN chown -R www-data:www-data /var/www/html \
 && chmod -R 775 storage bootstrap/cache

# ポート80で起動
EXPOSE 80

# Apacheをフォアグラウンドで起動
CMD ["apache2-foreground"]
