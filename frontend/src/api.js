import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export default {
  // Products
  getProducts(params = {}) {
    return api.get('/products', { params })
  },
  getProduct(id) {
    return api.get(`/products/${id}`)
  },
  createProduct(data) {
    return api.post('/products', data)
  },
  updateProduct(id, data) {
    return api.put(`/products/${id}`, data)
  },
  deleteProduct(id) {
    return api.delete(`/products/${id}`)
  },

  // Categories & Brands
  getCategories() {
    return api.get('/categories')
  },
  getBrands() {
    return api.get('/brands')
  },

  // Reviews
  getReviews(params = {}) {
    return api.get('/reviews', { params })
  },
  getReview(id) {
    return api.get(`/reviews/${id}`)
  },
  createReview(data) {
    return api.post('/reviews', data)
  },
  deleteReview(id) {
    return api.delete(`/reviews/${id}`)
  },
  voteReview(id, isHelpful) {
    return api.post(`/reviews/${id}/vote`, { is_helpful: isHelpful })
  },

  // Ratings
  getRatings(params = {}) {
    return api.get('/ratings', { params })
  },
  getRatingStats() {
    return api.get('/ratings/stats')
  },

  // Search
  search(params) {
    return api.get('/search', { params })
  },

  // Admin
  adminLogin(username, password) {
    return api.post('/admin/login', { username, password })
  },
  getAdminStats() {
    return api.get('/admin/stats')
  },
  getAdminReviews() {
    return api.get('/admin/reviews')
  },
  deleteAdminReview(id) {
    return api.delete(`/admin/reviews/${id}`)
  },
  getAdminProducts() {
    return api.get('/admin/products')
  },
  getAdminCategories() {
    return api.get('/admin/categories')
  },
  getAdminBrands() {
    return api.get('/admin/brands')
  },
}
