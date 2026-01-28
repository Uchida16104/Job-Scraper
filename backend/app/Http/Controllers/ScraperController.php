<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class ScraperController extends Controller
{
    /**
     * スクレイピングを実行してCSV/XLSXファイルを生成
     */
    public function run(Request $request)
    {
        try {
            // URLのバリデーション
            $request->validate([
                'link' => 'required|url',
                'mode' => 'nullable|string'
            ]);

            $url = $request->input('link');
            $mode = $request->input('mode', 'run');

            Log::info('Scraper started', ['url' => $url, 'mode' => $mode]);

            // Pythonスクリプトのパス
            $pythonScript = base_path('main.py');
            
            // Pythonスクリプトが存在するか確認
            if (!file_exists($pythonScript)) {
                Log::error('Python script not found', ['path' => $pythonScript]);
                return response()->json([
                    'success' => false,
                    'message' => 'Pythonスクリプトが見つかりません'
                ], 500);
            }

            // 出力ディレクトリ
            $outputDir = storage_path('app/public/downloads');
            
            // ディレクトリが存在しない場合は作成
            if (!is_dir($outputDir)) {
                mkdir($outputDir, 0775, true);
            }

            // Python実行コマンド (headlessモード、出力ディレクトリ指定)
            $escapedUrl = escapeshellarg($url);
            $escapedOutputDir = escapeshellarg($outputDir);
            $command = sprintf(
                'python3 %s %s --headless --output-dir %s 2>&1',
                escapeshellarg($pythonScript),
                $escapedUrl,
                $escapedOutputDir
            );

            Log::info('Executing command', ['command' => $command]);

            // コマンド実行
            $output = [];
            $returnCode = 0;
            exec($command, $output, $returnCode);

            $outputText = implode("\n", $output);
            Log::info('Command executed', [
                'return_code' => $returnCode,
                'output' => $outputText
            ]);

            // 実行結果を確認
            if ($returnCode !== 0) {
                Log::error('Python script failed', [
                    'return_code' => $returnCode,
                    'output' => $outputText
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'スクレイピング実行に失敗しました',
                    'error' => $outputText
                ], 500);
            }

            // 生成されたファイルを検索
            $files = glob($outputDir . '/data_*.{csv,xlsx}', GLOB_BRACE);
            
            if (empty($files)) {
                Log::warning('No files generated', ['output_dir' => $outputDir]);
                return response()->json([
                    'success' => false,
                    'message' => 'ファイルが生成されませんでした。URLを確認してください。',
                    'output' => $outputText
                ], 400);
            }

            // 最新のファイル2つを取得 (CSV と XLSX)
            usort($files, function($a, $b) {
                return filemtime($b) - filemtime($a);
            });

            $csvFile = null;
            $xlsxFile = null;

            foreach ($files as $file) {
                if (pathinfo($file, PATHINFO_EXTENSION) === 'csv' && !$csvFile) {
                    $csvFile = $file;
                } elseif (pathinfo($file, PATHINFO_EXTENSION) === 'xlsx' && !$xlsxFile) {
                    $xlsxFile = $file;
                }
                
                if ($csvFile && $xlsxFile) {
                    break;
                }
            }

            // ダウンロードURLを生成
            $baseUrl = rtrim(config('app.url'), '/');
            $downloadLinks = [];

            if ($csvFile) {
                $csvFilename = basename($csvFile);
                $downloadLinks['csv'] = [
                    'url' => "{$baseUrl}/download/{$csvFilename}",
                    'filename' => $csvFilename,
                    'size' => $this->formatBytes(filesize($csvFile))
                ];
            }

            if ($xlsxFile) {
                $xlsxFilename = basename($xlsxFile);
                $downloadLinks['xlsx'] = [
                    'url' => "{$baseUrl}/download/{$xlsxFilename}",
                    'filename' => $xlsxFilename,
                    'size' => $this->formatBytes(filesize($xlsxFile))
                ];
            }

            Log::info('Files generated successfully', ['files' => $downloadLinks]);

            // HTMLレスポンスを返す (htmx用)
            $html = '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">';
            $html .= '<h3 class="font-bold mb-2">✓ スクレイピング完了</h3>';
            $html .= '<p class="mb-2">以下のファイルが生成されました:</p>';
            $html .= '<ul class="space-y-2">';
            
            if (isset($downloadLinks['csv'])) {
                $html .= sprintf(
                    '<li><a href="%s" download class="text-blue-600 hover:underline">📄 CSV ファイル (%s)</a></li>',
                    htmlspecialchars($downloadLinks['csv']['url']),
                    htmlspecialchars($downloadLinks['csv']['size'])
                );
            }
            
            if (isset($downloadLinks['xlsx'])) {
                $html .= sprintf(
                    '<li><a href="%s" download class="text-blue-600 hover:underline">📊 Excel ファイル (%s)</a></li>',
                    htmlspecialchars($downloadLinks['xlsx']['url']),
                    htmlspecialchars($downloadLinks['xlsx']['size'])
                );
            }
            
            $html .= '</ul>';
            $html .= '</div>';

            return response($html, 200, ['Content-Type' => 'text/html']);

        } catch (\Illuminate\Validation\ValidationException $e) {
            Log::error('Validation error', ['errors' => $e->errors()]);
            $html = '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">';
            $html .= '<h3 class="font-bold">✗ エラー</h3>';
            $html .= '<p>正しいURLを入力してください</p>';
            $html .= '</div>';
            return response($html, 422, ['Content-Type' => 'text/html']);
            
        } catch (\Exception $e) {
            Log::error('Unexpected error', [
                'message' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            
            $html = '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">';
            $html .= '<h3 class="font-bold">✗ エラー</h3>';
            $html .= '<p>' . htmlspecialchars($e->getMessage()) . '</p>';
            $html .= '</div>';
            return response($html, 500, ['Content-Type' => 'text/html']);
        }
    }

    /**
     * ファイルをダウンロード
     */
    public function download($filename)
    {
        try {
            $filePath = storage_path('app/public/downloads/' . $filename);
            
            // セキュリティチェック: ディレクトリトラバーサル防止
            $realPath = realpath($filePath);
            $allowedDir = realpath(storage_path('app/public/downloads'));
            
            if (!$realPath || strpos($realPath, $allowedDir) !== 0) {
                Log::warning('Invalid file access attempt', ['filename' => $filename]);
                abort(404);
            }
            
            if (!file_exists($filePath)) {
                Log::warning('File not found', ['path' => $filePath]);
                abort(404);
            }

            Log::info('File download', ['filename' => $filename]);

            return response()->download($filePath);
            
        } catch (\Exception $e) {
            Log::error('Download error', [
                'filename' => $filename,
                'message' => $e->getMessage()
            ]);
            abort(500);
        }
    }

    /**
     * バイト数を人間が読みやすい形式に変換
     */
    private function formatBytes($bytes, $precision = 2)
    {
        $units = ['B', 'KB', 'MB', 'GB'];
        $bytes = max($bytes, 0);
        $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
        $pow = min($pow, count($units) - 1);
        $bytes /= (1 << (10 * $pow));
        
        return round($bytes, $precision) . ' ' . $units[$pow];
    }
}
