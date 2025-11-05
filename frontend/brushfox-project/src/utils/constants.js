// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export const MEDIA_BASE_URL = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8000';

/**
 * Build full media URL from relative path
 * @param {string} path - Relative path (e.g., '/media/photo.jpg')
 * @returns {string|null} - Full URL or null if path is empty
 */
export const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http')) return path; // Already full URL
  return `${MEDIA_BASE_URL}${path.startsWith('/') ? path : '/' + path}`;
};

// API Endpoints - zgodne z backend/brashfox_app/api/urls.py
export const API_ENDPOINTS = {
  // Blog
  POSTS: '/blog-posts/',
  POST_DETAIL: (slug) => `/blog-posts/${slug}/`,
  POST_COMMENTS: (slug) => `/blog-posts/${slug}/comments/`,
  POST_CATEGORIES: '/post-categories/',  // FIXED: was blog-categories
  
  // Portfolio
  PHOTOS: '/photos/',
  PHOTO_DETAIL: (id) => `/photos/${id}/`,
  PHOTO_CATEGORIES: '/photo-categories/',
  
  // About
  ABOUT: '/about/',
  
  // Comments (all)
  COMMENTS: '/comments/',
  
  // Contact
  CONTACT: '/contact/',
  
  // Auth & Users
  USERS: '/users/',
  USER_ME: '/users/me/',
  LOGIN: '/token/',  // JWT login
  REFRESH: '/token/refresh/',  // JWT refresh
  REGISTER: '/users/',
};

// UI Constants
export const ITEMS_PER_PAGE = 10;
export const TOAST_DURATION = 3000;

// Navigation Items
export const NAV_ITEMS = [
  { path: '/', label: 'Strona główna' },
  { path: '/portfolio', label: 'Portfolio' },
  { path: '/blog', label: 'Blog' },
  { path: '/about', label: 'O mnie' },
  { path: '/contact', label: 'Kontakt' },
];
