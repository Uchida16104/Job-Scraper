'use client';

import { useState } from 'react';
import JobSearchForm from '@/components/JobSearchForm';
import ResultDisplay from '@/components/ResultDisplay';

export default function Home() {
  const [searchResult, setSearchResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearchComplete = (result: any) => {
    setSearchResult(result);
    setIsLoading(false);
  };

  const handleSearchStart = () => {
    setIsLoading(true);
    setSearchResult(null);
  };

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          求人情報スクレイピング / Job Information Scraping
        </h1>
        <p className="text-gray-600 mb-6">
          求人サイトのURLを入力して、情報を自動収集します / Enter job site URL to automatically collect information
        </p>
        <JobSearchForm 
          onSearchComplete={handleSearchComplete}
          onSearchStart={handleSearchStart}
        />
      </div>

      {isLoading && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-blue-700">
                スクレイピング処理中です。しばらくお待ちください... / Scraping in progress. Please wait...
              </p>
            </div>
          </div>
        </div>
      )}

      {searchResult && <ResultDisplay result={searchResult} />}
    </div>
  );
}
