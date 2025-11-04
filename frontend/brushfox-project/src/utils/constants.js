// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// API Endpoints
export const API_ENDPOINTS = {
  // Blog
  POSTS: '/posts/',
  POST_DETAIL: (slug) => `/posts/${slug}/`,
  POST_COMMENTS: (postId) => `/post-comments/?blog_post=${postId}`,
  POST_CATEGORIES: '/post-categories/',
  
  // Portfolio
  PHOTOS: '/fotos/',
  PHOTO_DETAIL: (id) => `/fotos/${id}/`,
  PHOTO_CATEGORIES: '/foto-categories/',
  PHOTO_TAGS: '/foto-tags/',
  
  // Contact
  MESSAGES: '/messages/',
  
  // Auth
  USERS: '/users/',
  LOGIN: '/api-auth/login/',
  LOGOUT: '/api-auth/logout/',
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
