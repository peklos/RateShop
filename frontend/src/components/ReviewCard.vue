<template>
  <div class="review-card card">
    <div class="review-header">
      <div class="reviewer-info">
        <img :src="review.reviewer_avatar || 'https://placehold.co/40x40?text=U'" class="reviewer-avatar" />
        <div>
          <div class="reviewer-name">{{ review.reviewer_name }}</div>
          <div class="review-date">{{ formatDate(review.created_at) }}</div>
        </div>
      </div>
      <div class="review-rating-badge">
        <StarRating :modelValue="review.rating" />
      </div>
    </div>
    <div v-if="showProduct && review.product_name" class="review-product">
      <router-link :to="`/products/${review.product_id}`">{{ review.product_name }}</router-link>
    </div>
    <h4 v-if="review.title" class="review-title">{{ review.title }}</h4>
    <p v-if="review.text" class="review-text">{{ review.text }}</p>
    <div class="review-pros-cons" v-if="review.pros || review.cons">
      <div v-if="review.pros" class="pros">
        <span class="label">+ Достоинства:</span> {{ review.pros }}
      </div>
      <div v-if="review.cons" class="cons">
        <span class="label">- Недостатки:</span> {{ review.cons }}
      </div>
    </div>
    <div class="review-footer">
      <div class="review-badges">
        <span v-if="review.is_verified" class="badge badge-green">Проверенная покупка</span>
      </div>
      <div class="review-votes">
        <button class="vote-btn" @click="$emit('vote', review.id, true)" title="Полезно">
          &#128077; {{ review.helpful_count || 0 }}
        </button>
        <button class="vote-btn" @click="$emit('vote', review.id, false)" title="Не полезно">
          &#128078; {{ review.not_helpful_count || 0 }}
        </button>
      </div>
      <button v-if="showDelete" class="btn btn-danger btn-sm" @click="$emit('delete', review.id)">
        Удалить
      </button>
    </div>
  </div>
</template>

<script>
import StarRating from './StarRating.vue'

export default {
  name: 'ReviewCard',
  components: { StarRating },
  props: {
    review: { type: Object, required: true },
    showProduct: { type: Boolean, default: false },
    showDelete: { type: Boolean, default: false }
  },
  emits: ['vote', 'delete'],
  methods: {
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        year: 'numeric', month: 'long', day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.review-card {
  margin-bottom: 16px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.reviewer-name {
  font-weight: 600;
  font-size: 14px;
  color: #e0e0e0;
}

.review-date {
  font-size: 12px;
  color: #777;
}

.review-product {
  margin-bottom: 8px;
  font-size: 13px;
}

.review-product a {
  color: #5a9fe6;
  font-weight: 500;
}

.review-title {
  font-size: 16px;
  margin-bottom: 8px;
  color: #e8e8f0;
}

.review-text {
  font-size: 14px;
  color: #b0b0c0;
  margin-bottom: 12px;
  line-height: 1.6;
}

.review-pros-cons {
  margin-bottom: 12px;
  font-size: 13px;
}

.pros {
  color: #4caf50;
  margin-bottom: 4px;
}

.cons {
  color: #ff6b6b;
}

.pros .label, .cons .label {
  font-weight: 600;
}

.review-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.review-votes {
  display: flex;
  gap: 8px;
}

.vote-btn {
  background: #252540;
  border: none;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  color: #b0b0c0;
  cursor: pointer;
  transition: background 0.2s;
}

.vote-btn:hover {
  background: #303050;
}

.review-badges {
  flex: 1;
}
</style>
