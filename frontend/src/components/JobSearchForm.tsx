'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';

interface JobSearchFormProps {
  onSearchComplete: (result: any) => void;
  onSearchStart: () => void;
}

export default function JobSearchForm({ onSearchComplete, onSearchStart }: JobSearchFormProps) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const validateUrl = (url: string): boolean => {
    try {
      new URL(url);
      const supportedSites = ['atgp', 'litalico', 'mynavi', 'snabi'];
      return supportedSites.some(site => url.includes(site));
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!url.trim()) {
      setError('URLを入力してください / Please enter a URL');
      return;
    }

    if (!validateUrl(url)) {
      setError('対応していない求人サイトのURLです / Unsupported job site URL');
      return;
    }

    try {
      onSearchStart();
      const result = await apiClient.scrapeJobs(url);
      onSearchComplete(result);
    } catch (err: any) {
      setError(err.message || 'スクレイピングに失敗しました / Scraping failed');
      onSearchComplete(null);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
          求人サイトURL / Job Site URL
        </label>
        <input
          type="text"
          id="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.atgp.jp/... or https://snabi.jp/... or https://mynavi.jp/..."
          className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <p className="mt-2 text-sm text-gray-500">
          対応サイト / Supported sites: atgp, LITALICO仕事ナビ, マイナビ系 / Mynavi series
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <button
        type="submit"
        className="w-full bg-primary-600 text-white py-3 px-6 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors font-medium"
      >
        スクレイピング開始 / Start Scraping
      </button>
    </form>
  );
}
