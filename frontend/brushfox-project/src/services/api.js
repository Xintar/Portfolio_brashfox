import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for CSRF and session cookies
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Service Methods
export const apiService = {
  // Generic methods
  get: (url, config) => api.get(url, config),
  post: (url, data, config) => api.post(url, data, config),
  put: (url, data, config) => api.put(url, data, config),
  patch: (url, data, config) => api.patch(url, data, config),
  delete: (url, config) => api.delete(url, config),

  // Blog Posts
  getPosts: (page = 1) => api.get(`/posts/?page=${page}`),
  getPostBySlug: (slug) => api.get(`/posts/${slug}/`),
  createPost: (data) => api.post('/posts/', data),
  updatePost: (id, data) => api.patch(`/posts/${id}/`, data),
  deletePost: (id) => api.delete(`/posts/${id}/`),

  // Comments
  getComments: (postId) => api.get(`/post-comments/?blog_post=${postId}`),
  createComment: (data) => api.post('/post-comments/', data),

  // Portfolio Photos
  getPhotos: (page = 1) => api.get(`/fotos/?page=${page}`),
  getPhotoById: (id) => api.get(`/fotos/${id}/`),
  uploadPhoto: (formData) => api.post('/fotos/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  updatePhoto: (id, data) => api.patch(`/fotos/${id}/`, data),
  deletePhoto: (id) => api.delete(`/fotos/${id}/`),

  // Photo Categories
  getPhotoCategories: () => api.get('/foto-categories/'),

  // Contact Messages
  sendMessage: (data) => api.post('/messages/', data),

  // Auth
  login: (credentials) => api.post('/api-auth/login/', credentials),
  logout: () => api.post('/api-auth/logout/'),
  register: (userData) => api.post('/users/', userData),
};

export default api;
