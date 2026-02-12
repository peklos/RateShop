<template>
  <div class="product-detail" v-if="product">
    <div class="back-link">
      <router-link to="/products">&larr; Назад к каталогу</router-link>
    </div>

    <div class="product-main card">
      <div class="product-gallery">
        <img :src="mainImage" :alt="product.name" class="main-image" />
        <div class="thumbnails" v-if="product.images && product.images.length > 1">
          <img
            v-for="img in product.images"
            :key="img.id"
            :src="img.image_url"
            class="thumb"
            :class="{ active: img.image_url === mainImage }"
            @click="mainImage = img.image_url"
          />
        </div>
      </div>
      <div class="product-info">
        <div class="product-category" v-if="product.category_name">{{ product.category_name }}</div>
        <h1 class="product-name">{{ product.name }}</h1>
        <div class="product-brand" v-if="product.brand_name">{{ product.brand_name }}</div>
        <div class="product-rating-big">
          <StarRating :modelValue="product.avg_rating || 0" :showValue="true" :showCount="true" :count="product.review_count || 0" />
        </div>
        <p class="product-description">{{ product.description }}</p>
        <div class="product-price-big">{{ formatPrice(product.price) }} ₽</div>

        <!-- Rating distribution -->
        <div class="rating-dist" v-if="product.rating_distribution">
          <h3>Распределение оценок</h3>
          <div v-for="star in [5,4,3,2,1]" :key="star" class="dist-row">
            <span class="dist-label">{{ star }} ★</span>
            <div class="dist-bar">
              <div class="dist-fill" :style="{ width: getDistPercent(star) + '%' }"></div>
            </div>
            <span class="dist-count">{{ product.rating_distribution[star] || 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Form -->
    <div class="review-form-section card">
      <h2>Оставить отзыв</h2>
      <form @submit.prevent="submitReview" class="review-form">
        <div class="form-row">
          <label>Ваше имя *</label>
          <input v-model="newReview.reviewer_name" type="text" required placeholder="Введите ваше имя" />
        </div>
        <div class="form-row">
          <label>Email</label>
          <input v-model="newReview.reviewer_email" type="email" placeholder="email@example.com" />
        </div>
        <div class="form-row">
          <label>Оценка *</label>
          <StarRating v-model="newReview.rating" :interactive="true" />
        </div>
        <div class="form-row">
          <label>Заголовок</label>
          <input v-model="newReview.title" type="text" placeholder="Кратко о впечатлении" />
        </div>
        <div class="form-row">
          <label>Отзыв</label>
          <textarea v-model="newReview.text" rows="4" placeholder="Расскажите подробнее..."></textarea>
        </div>
        <div class="form-row-pair">
          <div class="form-row">
            <label>Достоинства</label>
            <textarea v-model="newReview.pros" rows="2" placeholder="Что понравилось"></textarea>
          </div>
          <div class="form-row">
            <label>Недостатки</label>
            <textarea v-model="newReview.cons" rows="2" placeholder="Что не понравилось"></textarea>
          </div>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="!newReview.reviewer_name || !newReview.rating">
          Отправить отзыв
        </button>
        <span v-if="submitMessage" class="submit-message">{{ submitMessage }}</span>
      </form>
    </div>

    <!-- Reviews List -->
    <div class="reviews-section">
      <h2>Отзывы ({{ product.reviews ? product.reviews.length : 0 }})</h2>
      <div v-if="product.reviews && product.reviews.length > 0">
        <ReviewCard
          v-for="review in product.reviews"
          :key="review.id"
          :review="review"
          @vote="handleVote"
        />
      </div>
      <div v-else class="empty-state">
        <h3>Пока нет отзывов</h3>
        <p>Будьте первым, кто оставит отзыв!</p>
      </div>
    </div>
  </div>
  <div v-else class="loading">Загрузка...</div>
</template>

<script>
import api from '../api.js'
import StarRating from '../components/StarRating.vue'
import ReviewCard from '../components/ReviewCard.vue'

export default {
  name: 'ProductDetailView',
  components: { StarRating, ReviewCard },
  data() {
    return {
      product: null,
      mainImage: '',
      newReview: {
        reviewer_name: '',
        reviewer_email: '',
        rating: 0,
        title: '',
        text: '',
        pros: '',
        cons: ''
      },
      submitMessage: ''
    }
  },
  async created() {
    await this.loadProduct()
  },
  methods: {
    async loadProduct() {
      try {
        const res = await api.getProduct(this.$route.params.id)
        this.product = res.data
        this.mainImage = this.product.image_url || (this.product.images && this.product.images[0]?.image_url) || ''
      } catch (e) {
        console.error(e)
      }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU').format(price)
    },
    getDistPercent(star) {
      if (!this.product.rating_distribution || !this.product.review_count) return 0
      return (this.product.rating_distribution[star] / this.product.review_count) * 100
    },
    async submitReview() {
      if (!this.newReview.rating) {
        this.submitMessage = 'Пожалуйста, поставьте оценку'
        return
      }
      try {
        await api.createReview({
          product_id: this.product.id,
          ...this.newReview
        })
        this.submitMessage = 'Отзыв отправлен!'
        this.newReview = { reviewer_name: '', reviewer_email: '', rating: 0, title: '', text: '', pros: '', cons: '' }
        await this.loadProduct()
        setTimeout(() => { this.submitMessage = '' }, 3000)
      } catch (e) {
        this.submitMessage = 'Ошибка при отправке'
        console.error(e)
      }
    },
    async handleVote(reviewId, isHelpful) {
      try {
        await api.voteReview(reviewId, isHelpful)
        await this.loadProduct()
      } catch (e) { console.error(e) }
    }
  }
}
</script>

<style scoped>
.back-link {
  margin-bottom: 16px;
}

.back-link a {
  font-size: 14px;
  color: #5a9fe6;
}

.product-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

.product-gallery {
  text-align: center;
}

.main-image {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 8px;
  background: #16162a;
}

.thumbnails {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  justify-content: center;
}

.thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumb.active, .thumb:hover {
  border-color: #4a90d9;
}

.product-category {
  font-size: 13px;
  color: #5a9fe6;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.product-name {
  font-size: 28px;
  font-weight: 700;
  color: #e8e8f0;
  margin-bottom: 4px;
}

.product-brand {
  font-size: 15px;
  color: #888;
  margin-bottom: 12px;
}

.product-rating-big {
  margin-bottom: 16px;
}

.product-description {
  font-size: 15px;
  color: #b0b0c0;
  margin-bottom: 20px;
  line-height: 1.7;
}

.product-price-big {
  font-size: 32px;
  font-weight: 700;
  color: #ff6b6b;
  margin-bottom: 24px;
}

.rating-dist h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: #e0e0e0;
}

.dist-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.dist-label {
  width: 40px;
  font-size: 13px;
  color: #999;
  text-align: right;
}

.dist-bar {
  flex: 1;
  height: 10px;
  background: #252540;
  border-radius: 5px;
  overflow: hidden;
}

.dist-fill {
  height: 100%;
  background: #f1c40f;
  border-radius: 5px;
  transition: width 0.3s;
}

.dist-count {
  width: 24px;
  font-size: 13px;
  color: #888;
}

/* Review Form */
.review-form-section {
  margin-bottom: 32px;
}

.review-form-section h2 {
  font-size: 22px;
  margin-bottom: 20px;
  color: #e8e8f0;
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row label {
  font-size: 14px;
  font-weight: 600;
  color: #c0c0d0;
}

.form-row input,
.form-row textarea {
  padding: 10px 14px;
  border: 2px solid #2a2a40;
  border-radius: 8px;
  font-size: 14px;
  background: #16162a;
  color: #e0e0e0;
  transition: border-color 0.2s;
}

.form-row input:focus,
.form-row textarea:focus {
  outline: none;
  border-color: #4a90d9;
}

.form-row input::placeholder,
.form-row textarea::placeholder {
  color: #555;
}

.form-row-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.submit-message {
  color: #4caf50;
  font-weight: 500;
  font-size: 14px;
}

.reviews-section {
  margin-bottom: 32px;
}

.reviews-section h2 {
  font-size: 22px;
  margin-bottom: 20px;
  color: #e8e8f0;
}

@media (max-width: 768px) {
  .product-main {
    grid-template-columns: 1fr;
  }
  .form-row-pair {
    grid-template-columns: 1fr;
  }
}
</style>
