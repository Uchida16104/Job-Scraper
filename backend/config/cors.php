<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Cross-Origin Resource Sharing (CORS) Configuration
    |--------------------------------------------------------------------------
    */

    'paths' => ['api/*', 'sanctum/csrf-cookie', '/', 'run', 'download/*', 'test'],

    'allowed_methods' => ['*'],

    'allowed_origins' => [
        env('FRONTEND_URL', 'http://localhost:3000'),
        'http://localhost:3000',
        'https://*.vercel.app',
        'https://job-scraper-indol-nine.vercel.app',
    ],

    'allowed_origins_patterns' => [
        '/^https:\/\/.*\.vercel\.app$/',
        '/^http:\/\/localhost(:\d+)?$/',
    ],

    'allowed_headers' => ['*'],

    'exposed_headers' => ['Content-Disposition'],

    'max_age' => 0,

    'supports_credentials' => true,

];
