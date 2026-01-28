<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ScraperController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return response()->json([
        'status' => 'ok',
        'message' => 'Job Scraper Backend API',
        'version' => '1.0.0'
    ]);
});

Route::post('/run', [ScraperController::class, 'run']);
Route::get('/download/{filename}', [ScraperController::class, 'download'])->name('download');
