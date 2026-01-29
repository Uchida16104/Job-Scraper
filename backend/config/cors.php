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

    'allowed_headers' => [
        '*',
        'Content-Type',
        'X-Requested-With',
        'Authorization',
        'Accept',
        'Origin',
        'Access-Control-Request-Method',
        'Access-Control-Request-Headers',
        // htmx specific headers
        'HX-Request',
        'HX-Trigger',
        'HX-Trigger-Name',
        'HX-Target',
        'HX-Current-URL',
        'HX-Boosted',
        'HX-History-Restore-Request',
        'HX-Prompt',
    ],

    'exposed_headers' => [
        'Content-Disposition',
        'HX-Location',
        'HX-Push-Url',
        'HX-Redirect',
        'HX-Refresh',
        'HX-Replace-Url',
        'HX-Reswap',
        'HX-Retarget',
        'HX-Reselect',
        'HX-Trigger',
        'HX-Trigger-After-Settle',
        'HX-Trigger-After-Swap',
    ],

    'max_age' => 0,

    'supports_credentials' => true,

];
