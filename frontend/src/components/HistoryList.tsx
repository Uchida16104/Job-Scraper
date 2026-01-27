'use client';

import { format } from 'date-fns';

interface History {
  id: string;
  source_url: string;
  job_count: number;
  scraped_at: string;
  site_name: string;
}

interface HistoryListProps {
  histories: History[];
  onDownload: (historyId: string) => void;
}

export default function HistoryList({ histories, onDownload }: HistoryListProps) {
  if (histories.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          履歴がありません / No history found
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          スクレイピングを実行すると、ここに履歴が表示されます / History will appear here after scraping
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <ul className="divide-y divide-gray-200">
        {histories.map((history) => (
          <li key={history.id} className="p-6 hover:bg-gray-50 transition-colors">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3">
                  <span className="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-primary-100 text-primary-800">
                    {history.site_name}
                  </span>
                  <h3 className="text-lg font-medium text-gray-900">
                    {history.job_count} 件の求人 / {history.job_count} jobs
                  </h3>
                </div>
                <p className="mt-2 text-sm text-gray-600 truncate">
                  {history.source_url}
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  {format(new Date(history.scraped_at), 'yyyy年MM月dd日 HH:mm / MMM dd, yyyy HH:mm')}
                </p>
              </div>
              <div className="ml-4">
                <button
                  onClick={() => onDownload(history.id)}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  ダウンロード / Download
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
