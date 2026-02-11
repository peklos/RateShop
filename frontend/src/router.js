import { createRouter, createWebHistory } from 'vue-router'
import ProductsView from './views/ProductsView.vue'
import ProductDetailView from './views/ProductDetailView.vue'
import ReviewsView from './views/ReviewsView.vue'
import RatingsView from './views/RatingsView.vue'
import SearchView from './views/SearchView.vue'
import GuideView from './views/GuideView.vue'
import AdminView from './views/AdminView.vue'

const routes = [
  { path: '/', redirect: '/products' },
  { path: '/products', name: 'Products', component: ProductsView },
  { path: '/products/:id', name: 'ProductDetail', component: ProductDetailView },
  { path: '/reviews', name: 'Reviews', component: ReviewsView },
  { path: '/ratings', name: 'Ratings', component: RatingsView },
  { path: '/search', name: 'Search', component: SearchView },
  { path: '/guide', name: 'Guide', component: GuideView },
  { path: '/admin', name: 'Admin', component: AdminView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
