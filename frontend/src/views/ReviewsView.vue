<template>
  <div class="reviews-page">
    <h1 class="page-title">Все отзывы</h1>

    <div class="filters-bar">
      <select v-model="filters.sort" @change="loadReviews">
        <option value="newest">Сначала новые</option>
        <option value="oldest">Сначала старые</option>
        <option value="rating_high">Высокий рейтинг</option>
        <option value="rating_low">Низкий рейтинг</option>
        <option value="helpful">Самые полезные</option>
      </select>
      <select v-model="filters.rating" @change="loadReviews">
        <option value="">Все оценки</option>
        <option v-for="s in [5,4,3,2,1]" :key="s" :value="s">{{ s }} ★</option>
      </select>
      <span class="results-count">Всего: {{ reviews.length }}</span>
    </div>

    <div v-if="loading" class="loading">Загрузка отзывов...</div>

    <div v-else-if="reviews.length === 0" class="empty-state">
      <h3>Отзывы не найдены</h3>
      <p>Попробуйте изменить фильтры</p>
    </div>

    <div v-else>
      <ReviewCard
        v-for="review in reviews"
        :key="review.id"
        :review="review"
        :showProduct="true"
        @vote="handleVote"
      />
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import ReviewCard from '../components/ReviewCard.vue'

export default {
  name: 'ReviewsView',
  components: { ReviewCard },
  data() {
    return {
      reviews: [],
      loading: true,
      filters: {
        sort: 'newest',
        rating: ''
      }
    }
  },
  async created() {
    await this.loadReviews()
  },
  methods: {
    async loadReviews() {
      this.loading = true
      try {
        const params = { sort: this.filters.sort }
        if (this.filters.rating) params.rating = this.filters.rating
        const res = await api.getReviews(params)
        this.reviews = res.data
      } catch (e) { console.error(e) }
      this.loading = false
    },
    async handleVote(reviewId, isHelpful) {
      try {
        await api.voteReview(reviewId, isHelpful)
        await this.loadReviews()
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
