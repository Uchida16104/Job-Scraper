<?php

use Illuminate\Support\Facades\Facade;
use Illuminate\Support\ServiceProvider;

return [

    'name' => env('APP_NAME', 'Laravel'),
    'env' => env('APP_ENV', 'production'),
    
    // デバッグモード: trueにするとエラー詳細が表示される
    // 本番環境では必ずfalseにすること
    'debug' => (bool) env('APP_DEBUG', false),
    
    'url' => env('APP_URL', 'http://localhost'),
    'asset_url' => env('ASSET_URL'),
    'timezone' => 'Asia/Tokyo',
    'locale' => 'ja',
    'fallback_locale' => 'en',
    'faker_locale' => 'ja_JP',
    'key' => env('APP_KEY'),
    'cipher' => 'AES-256-CBC',

    'providers' => ServiceProvider::defaultProviders()->merge([
        App\Providers\AppServiceProvider::class,
        App\Providers\RouteServiceProvider::class,
    ])->toArray(),

    'aliases' => Facade::defaultAliases()->merge([
    ])->toArray(),

];
