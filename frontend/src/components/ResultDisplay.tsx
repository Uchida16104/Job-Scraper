'use client';

export default function ResultDisplay({ result }: { result: any }) {
  if (!result || !result.jobs || result.jobs.length === 0) {
    return (
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
        <p className="text-yellow-700">
          求人情報が見つかりませんでした / No job listings found
        </p>
      </div>
    );
  }

  const downloadCSV = () => {
    if (result.csv_url) {
      window.open(result.csv_url, '_blank');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              スクレイピング結果 / Scraping Results
            </h2>
            <p className="text-gray-600 mt-1">
              {result.job_count || result.jobs.length} 件の求人が見つかりました / {result.job_count || result.jobs.length} jobs found
            </p>
          </div>
          {result.csv_url && (
            <button
              onClick={downloadCSV}
              className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              CSVダウンロード / Download CSV
            </button>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  会社名 / Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  職種 / Position
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  雇用形態 / Employment
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  給与 / Salary
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  勤務地 / Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  詳細 / Details
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {result.jobs.map((job: any, index: number) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {job.company_name || '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {job.job_type || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {job.employment_type || '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {job.salary || '-'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {job.work_location || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {job.job_url && (
                      <a
                        href={job.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-900"
                      >
                        詳細を見る / View
                      </a>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">取得データサマリー / Data Summary</h3>
        <dl className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg">
            <dt className="text-sm text-gray-500">求人数 / Total Jobs</dt>
            <dd className="text-2xl font-bold text-gray-900">{result.job_count || result.jobs.length}</dd>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <dt className="text-sm text-gray-500">収集日時 / Collected At</dt>
            <dd className="text-lg font-semibold text-gray-900">
              {new Date(result.scraped_at || Date.now()).toLocaleString('ja-JP')}
            </dd>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <dt className="text-sm text-gray-500">ソースURL / Source URL</dt>
            <dd className="text-sm text-gray-900 truncate">{result.source_url || '-'}</dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
