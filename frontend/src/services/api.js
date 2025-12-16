import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  testLogin: () => api.post('/test/login'),
  googleLogin: () => window.location.href = `${API_URL}/auth/google`,
  appleLogin: () => window.location.href = `${API_URL}/auth/apple`,
};

export const transactions = {
  create: (data) => api.post('/transactions', data),
  getAll: () => api.get('/transactions'),
  getDashboard: () => api.get('/transactions/dashboard'),
  deleteByCategory: (type, category) => api.delete(`/transactions/category/${type}/${category}`),
};

export default api;