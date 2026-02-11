<template>
  <div class="products-page">
    <h1 class="page-title">Каталог товаров</h1>

    <div class="filters-bar">
      <select v-model="filters.category_id" @change="loadProducts">
        <option value="">Все категории</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
      </select>
      <select v-model="filters.brand_id" @change="loadProducts">
        <option value="">Все бренды</option>
        <option v-for="b in brands" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <select v-model="filters.sort" @change="loadProducts">
        <option value="">По умолчанию</option>
        <option value="price_asc">Цена: по возрастанию</option>
        <option value="price_desc">Цена: по убыванию</option>
        <option value="rating">По рейтингу</option>
        <option value="newest">Сначала новые</option>
      </select>
      <span class="results-count">Найдено: {{ products.length }}</span>
    </div>

    <div v-if="loading" class="loading">Загрузка товаров...</div>

    <div v-else-if="products.length === 0" class="empty-state">
      <h3>Товары не найдены</h3>
      <p>Попробуйте изменить фильтры</p>
    </div>

    <div v-else class="grid grid-3">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import ProductCard from '../components/ProductCard.vue'

export default {
  name: 'ProductsView',
  components: { ProductCard },
  data() {
    return {
      products: [],
      categories: [],
      brands: [],
      loading: true,
      filters: {
        category_id: '',
        brand_id: '',
        sort: ''
      }
    }
  },
  async created() {
    await Promise.all([
      this.loadProducts(),
      this.loadCategories(),
      this.loadBrands()
    ])
  },
  methods: {
    async loadProducts() {
      this.loading = true
      try {
        const params = {}
        if (this.filters.category_id) params.category_id = this.filters.category_id
        if (this.filters.brand_id) params.brand_id = this.filters.brand_id
        if (this.filters.sort) params.sort = this.filters.sort
        const res = await api.getProducts(params)
        this.products = res.data
      } catch (e) {
        console.error('Error loading products:', e)
      }
      this.loading = false
    },
    async loadCategories() {
      try {
        const res = await api.getCategories()
        this.categories = res.data
      } catch (e) { console.error(e) }
    },
    async loadBrands() {
      try {
        const res = await api.getBrands()
        this.brands = res.data
      } catch (e) { console.error(e) }
    }
  }
}
</script>

<style scoped>
.results-count {
  margin-left: auto;
  font-size: 14px;
  color: #888;
}
</style>
