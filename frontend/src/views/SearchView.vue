<template>
  <div class="search-page">
    <h1 class="page-title">Поиск</h1>

    <div class="search-section">
      <SearchBar v-model="query" placeholder="Поиск по товарам и отзывам..." />
      <div class="filters-bar" style="margin-top: 12px;">
        <select v-model="sort" @change="doSearch">
          <option value="">По релевантности</option>
          <option value="price_asc">Цена: по возрастанию</option>
          <option value="price_desc">Цена: по убыванию</option>
          <option value="rating">По рейтингу</option>
          <option value="newest">Сначала новые</option>
        </select>
        <select v-model="categoryId" @change="doSearch">
          <option value="">Все категории</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">Поиск...</div>

    <div v-else-if="searched && !hasResults" class="empty-state">
      <h3>Ничего не найдено</h3>
      <p>Попробуйте изменить запрос</p>
    </div>

    <div v-else-if="searched">
      <div v-if="results.products.length > 0" class="results-section">
        <h2>Товары ({{ results.products.length }})</h2>
        <div class="grid grid-3">
          <ProductCard v-for="p in results.products" :key="p.id" :product="p" />
        </div>
      </div>

      <div v-if="results.reviews.length > 0" class="results-section">
        <h2>Отзывы ({{ results.reviews.length }})</h2>
        <ReviewCard
          v-for="r in results.reviews"
          :key="r.id"
          :review="r"
          :showProduct="true"
          @vote="handleVote"
        />
      </div>
    </div>

    <div v-else class="empty-state">
      <h3>Введите запрос для поиска</h3>
      <p>Поиск по названиям товаров, описаниям и текстам отзывов</p>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import SearchBar from '../components/SearchBar.vue'
import ProductCard from '../components/ProductCard.vue'
import ReviewCard from '../components/ReviewCard.vue'

export default {
  name: 'SearchView',
  components: { SearchBar, ProductCard, ReviewCard },
  data() {
    return {
      query: '',
      sort: '',
      categoryId: '',
      categories: [],
      results: { products: [], reviews: [] },
      loading: false,
      searched: false,
      searchTimeout: null
    }
  },
  async created() {
    try {
      const res = await api.getCategories()
      this.categories = res.data
    } catch (e) { console.error(e) }
  },
  watch: {
    query(val) {
      clearTimeout(this.searchTimeout)
      if (val.length >= 2) {
        this.searchTimeout = setTimeout(() => this.doSearch(), 400)
      } else if (val.length === 0) {
        this.searched = false
        this.results = { products: [], reviews: [] }
      }
    }
  },
  computed: {
    hasResults() {
      return this.results.products.length > 0 || this.results.reviews.length > 0
    }
  },
  methods: {
    async doSearch() {
      if (!this.query || this.query.length < 2) return
      this.loading = true
      this.searched = true
      try {
        const params = { q: this.query }
        if (this.sort) params.sort = this.sort
        if (this.categoryId) params.category_id = this.categoryId
        const res = await api.search(params)
        this.results = res.data
      } catch (e) { console.error(e) }
      this.loading = false
    },
    async handleVote(reviewId, isHelpful) {
      try {
        await api.voteReview(reviewId, isHelpful)
        await this.doSearch()
      } catch (e) { console.error(e) }
    }
  }
}
</script>

<style scoped>
.search-section {
  margin-bottom: 24px;
}

.results-section {
  margin-bottom: 32px;
}

.results-section h2 {
  font-size: 20px;
  margin-bottom: 16px;
  color: #e8e8f0;
}
</style>
