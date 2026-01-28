<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ScraperController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
*/

// ヘルスチェックエンドポイント
Route::get('/', function () {
    return response()->json([
        'status' => 'ok',
        'message' => 'Job Scraper Backend API',
        'version' => '1.0.0',
        'timestamp' => now()->toIso8601String()
    ]);
});

// スクレイピング実行エンドポイント (POSTのみ)
Route::post('/run', [ScraperController::class, 'run'])
    ->withoutMiddleware([\App\Http\Middleware\VerifyCsrfToken::class]);

// ファイルダウンロードエンドポイント
Route::get('/download/{filename}', [ScraperController::class, 'download'])
    ->name('download')
    ->where('filename', '[A-Za-z0-9_\-\.]+');

// デバッグ用 (本番では削除推奨)
Route::get('/test', function () {
    return response()->json([
        'app_env' => env('APP_ENV'),
        'app_url' => env('APP_URL'),
        'frontend_url' => env('FRONTEND_URL'),
        'storage_path' => storage_path('app/public/downloads'),
        'storage_exists' => is_dir(storage_path('app/public/downloads')),
        'php_version' => PHP_VERSION,
        'laravel_version' => app()->version()
    ]);
});
