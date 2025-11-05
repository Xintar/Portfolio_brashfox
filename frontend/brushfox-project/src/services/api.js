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
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Try to refresh token
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('authToken', access);
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed - logout
          localStorage.removeItem('authToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
      } else {
        // No refresh token - logout
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
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
  getPosts: (params = {}) => api.get('/blog-posts/', { params }),
  getPostBySlug: (slug) => api.get(`/blog-posts/${slug}/`),
  createPost: (data) => api.post('/blog-posts/', data),
  updatePost: (slug, data) => api.patch(`/blog-posts/${slug}/`, data),
  deletePost: (slug) => api.delete(`/blog-posts/${slug}/`),
  searchPosts: (query) => api.get('/blog-posts/', { params: { search: query } }),

  // Blog Categories
  getPostCategories: () => api.get('/post-categories/'),

  // Comments
  getPostComments: (slug) => api.get(`/blog-posts/${slug}/comments/`),
  getAllComments: (params = {}) => api.get('/comments/', { params }),
  createComment: (data) => api.post('/comments/', data),

  // Portfolio Photos
  getPhotos: (params = {}) => api.get('/photos/', { params }),
  getPhotoById: (id) => api.get(`/photos/${id}/`),
  uploadPhoto: (formData) => api.post('/photos/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  updatePhoto: (id, data) => api.patch(`/photos/${id}/`, data),
  deletePhoto: (id) => api.delete(`/photos/${id}/`),

  // Photo Categories
  getPhotoCategories: () => api.get('/photo-categories/'),

  // About Me
  getAbout: () => api.get('/about/'),

  // Contact Messages
  sendMessage: (data) => api.post('/contact/', data),

  // Auth & Users
  login: (credentials) => api.post('/token/', credentials),
  refreshToken: (refresh) => api.post('/token/refresh/', { refresh }),
  register: (userData) => api.post('/users/', userData),
  getCurrentUser: () => api.get('/users/me/'),
  getUsers: (params = {}) => api.get('/users/', { params }),
};

export default api;
