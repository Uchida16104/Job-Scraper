'use client';

import { useEffect, useState } from 'react';
import HistoryList from '@/components/HistoryList';
import { apiClient } from '@/lib/api';

export default function HistoryPage() {
  const [histories, setHistories] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    site: '',
    startDate: '',
    endDate: '',
  });

  useEffect(() => {
    loadHistories();
  }, []);

  const loadHistories = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await apiClient.getHistory(filters);
      setHistories(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load history');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    loadHistories();
  };

  const handleDownloadCSV = async (historyId: string) => {
    try {
      const blob = await apiClient.downloadCSV(historyId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `job-scraping-${historyId}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert(`ダウンロードエラー / Download error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          スクレイピング履歴 / Scraping History
        </h1>
        <p className="text-gray-600 mb-6">
          過去のスクレイピング結果を確認できます / View past scraping results
        </p>

        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <h2 className="text-lg font-semibold mb-4">
            フィルター / Filters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                求人サイト / Job Site
              </label>
              <select
                value={filters.site}
                onChange={(e) => handleFilterChange('site', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">全て / All</option>
                <option value="atgp">atgp</option>
                <option value="litalico">LITALICO</option>
                <option value="mynavi">マイナビ / Mynavi</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                開始日 / Start Date
              </label>
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) => handleFilterChange('startDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                終了日 / End Date
              </label>
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) => handleFilterChange('endDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <button
            onClick={handleApplyFilters}
            className="mt-4 bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            フィルター適用 / Apply Filters
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">読み込み中... / Loading...</p>
        </div>
      ) : error ? (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-red-700">{error}</p>
        </div>
      ) : (
        <HistoryList histories={histories} onDownload={handleDownloadCSV} />
      )}
    </div>
  );
}
