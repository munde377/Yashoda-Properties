import axios from 'axios'

// Configure API base URL
// In development: use localhost:8000 for separate backend server
// In production (Render): use relative path (same domain, FastAPI serves both frontend & API)
const API_URL = import.meta.env.VITE_API_URL || (() => {
  if (typeof window === 'undefined') return 'http://localhost:8000'
  
  // Production: use relative path for same-domain requests
  if (import.meta.env.PROD) {
    return ''
  }
  // Development: use localhost backend
  return 'http://localhost:8000'
})()

const api = axios.create({
  baseURL: API_URL,
})

// Add JWT token to request headers if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle authentication errors and token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status
    if (status === 401) {
      localStorage.removeItem('access_token')
      if (typeof window !== 'undefined') {
        window.location.href = '/'
      }
    }
    return Promise.reject(error)
  }
)

export default api
