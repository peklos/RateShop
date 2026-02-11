<template>
  <div class="ratings-page">
    <h1 class="page-title">Средний рейтинг товаров</h1>

    <!-- Stats summary -->
    <div v-if="stats" class="stats-cards">
      <div class="stat-card card">
        <div class="stat-value">{{ stats.total_products }}</div>
        <div class="stat-label">Товаров</div>
      </div>
      <div class="stat-card card">
        <div class="stat-value">{{ stats.total_reviews }}</div>
        <div class="stat-label">Отзывов</div>
      </div>
      <div class="stat-card card">
        <div class="stat-value">{{ stats.overall_avg_rating }}</div>
        <div class="stat-label">Средний рейтинг</div>
      </div>
    </div>

    <!-- Overall distribution -->
    <div v-if="stats" class="card dist-card">
      <h3>Распределение оценок (все товары)</h3>
      <div class="dist-grid">
        <div v-for="star in [5,4,3,2,1]" :key="star" class="dist-row">
          <span class="dist-label">{{ star }} &#9733;</span>
          <div class="dist-bar">
            <div class="dist-fill" :style="{ width: getDistPercent(star) + '%' }"></div>
          </div>
          <span class="dist-count">{{ stats.rating_distribution[star] || 0 }}</span>
        </div>
      </div>
    </div>

    <!-- Top / Worst -->
    <div v-if="stats" class="top-worst-grid">
      <div class="card">
        <h3 class="section-title top-title">&#127942; Топ-5 лучших товаров</h3>
        <div v-for="(p, i) in stats.top_products" :key="'top-'+p.product_id" class="rank-item">
          <span class="rank-num">{{ i + 1 }}</span>
          <img :src="p.image_url" class="rank-img" />
          <div class="rank-info">
            <router-link :to="`/products/${p.product_id}`" class="rank-name">{{ p.product_name }}</router-link>
            <div class="rank-meta">
              <StarRating :modelValue="p.avg_rating" :showValue="true" />
              <span class="rank-reviews">{{ p.review_count }} отзывов</span>
            </div>
          </div>
        </div>
      </div>
      <div class="card">
        <h3 class="section-title worst-title">&#128308; Топ-5 с низким рейтингом</h3>
        <div v-for="(p, i) in stats.worst_products" :key="'worst-'+p.product_id" class="rank-item">
          <span class="rank-num">{{ i + 1 }}</span>
          <img :src="p.image_url" class="rank-img" />
          <div class="rank-info">
            <router-link :to="`/products/${p.product_id}`" class="rank-name">{{ p.product_name }}</router-link>
            <div class="rank-meta">
              <StarRating :modelValue="p.avg_rating" :showValue="true" />
              <span class="rank-reviews">{{ p.review_count }} отзывов</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Full ratings table -->
    <div class="card table-card">
      <h3 class="section-title">Полная таблица рейтингов</h3>
      <div class="filters-bar">
        <select v-model="sort" @change="loadRatings">
          <option value="rating_high">По рейтингу (высокий)</option>
          <option value="rating_low">По рейтингу (низкий)</option>
          <option value="reviews_count">По кол-ву отзывов</option>
        </select>
      </div>
      <table class="ratings-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Товар</th>
            <th>Категория</th>
            <th>Бренд</th>
            <th>Рейтинг</th>
            <th>Отзывов</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in ratings" :key="r.product_id">
            <td>{{ i + 1 }}</td>
            <td>
              <router-link :to="`/products/${r.product_id}`">{{ r.product_name }}</router-link>
            </td>
            <td>{{ r.category_name || '-' }}</td>
            <td>{{ r.brand_name || '-' }}</td>
            <td>
              <StarRating :modelValue="r.avg_rating" :showValue="true" />
            </td>
            <td>{{ r.review_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>
  </div>
</template>

<script>
import api from '../api.js'
import StarRating from '../components/StarRating.vue'

export default {
  name: 'RatingsView',
  components: { StarRating },
  data() {
    return {
      ratings: [],
      stats: null,
      loading: true,
      sort: 'rating_high'
    }
  },
  async created() {
    await Promise.all([this.loadRatings(), this.loadStats()])
    this.loading = false
  },
  methods: {
    async loadRatings() {
      try {
        const res = await api.getRatings({ sort: this.sort })
        this.ratings = res.data
      } catch (e) { console.error(e) }
    },
    async loadStats() {
      try {
        const res = await api.getRatingStats()
        this.stats = res.data
      } catch (e) { console.error(e) }
    },
    getDistPercent(star) {
      if (!this.stats || !this.stats.total_reviews) return 0
      return ((this.stats.rating_distribution[star] || 0) / this.stats.total_reviews) * 100
    }
  }
}
</script>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  padding: 24px;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #4a90d9;
}

.stat-label {
  font-size: 14px;
  color: #888;
  margin-top: 4px;
}

.dist-card {
  margin-bottom: 24px;
}

.dist-card h3 {
  font-size: 18px;
  margin-bottom: 16px;
}

.dist-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.dist-label {
  width: 45px;
  font-size: 14px;
  color: #666;
  text-align: right;
}

.dist-bar {
  flex: 1;
  height: 14px;
  background: #eee;
  border-radius: 7px;
  overflow: hidden;
}

.dist-fill {
  height: 100%;
  background: linear-gradient(90deg, #f1c40f, #f39c12);
  border-radius: 7px;
}

.dist-count {
  width: 30px;
  font-size: 14px;
  color: #888;
}

.top-worst-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  margin-bottom: 16px;
}

.top-title { color: #27ae60; }
.worst-title { color: #e74c3c; }

.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.rank-item:last-child { border-bottom: none; }

.rank-num {
  font-size: 20px;
  font-weight: 700;
  color: #ccc;
  width: 28px;
  text-align: center;
}

.rank-img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
}

.rank-info { flex: 1; }

.rank-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.rank-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 2px;
}

.rank-reviews {
  font-size: 12px;
  color: #999;
}

.table-card {
  margin-bottom: 24px;
  overflow-x: auto;
}

.ratings-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.ratings-table th {
  text-align: left;
  padding: 12px 8px;
  border-bottom: 2px solid #eee;
  color: #888;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
}

.ratings-table td {
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
}

.ratings-table a {
  color: #4a90d9;
  font-weight: 500;
}

@media (max-width: 768px) {
  .stats-cards { grid-template-columns: 1fr; }
  .top-worst-grid { grid-template-columns: 1fr; }
}
</style>
