import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    console.error('Response:', error.response);
    const message = error.response?.data?.detail || error.message || 'Unknown error occurred';
    return Promise.reject(new Error(message));
  }
);

export const apiClient = {
  async scrapeJobs(url: string) {
    const response = await axiosInstance.post('/api/scrape', { url });
    return response.data;
  },

  async getHistory(filters: { site?: string; startDate?: string; endDate?: string }) {
    const params = new URLSearchParams();
    if (filters.site) params.append('site', filters.site);
    if (filters.startDate) params.append('start_date', filters.startDate);
    if (filters.endDate) params.append('end_date', filters.endDate);
    
    const response = await axiosInstance.get(`/api/history?${params.toString()}`);
    return response.data;
  },

  async downloadCSV(historyId: string): Promise<Blob> {
    const response = await axiosInstance.get(`/api/download/${historyId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  async getJobDetails(jobId: string) {
    const response = await axiosInstance.get(`/api/jobs/${jobId}`);
    return response.data;
  },
};

export default apiClient;
