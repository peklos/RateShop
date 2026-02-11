<template>
  <router-link :to="`/products/${product.id}`" class="product-card card">
    <div class="product-image">
      <img :src="product.image_url" :alt="product.name" />
    </div>
    <div class="product-info">
      <div class="product-category" v-if="product.category_name">{{ product.category_name }}</div>
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-brand" v-if="product.brand_name">{{ product.brand_name }}</div>
      <div class="product-rating">
        <StarRating :modelValue="product.avg_rating || 0" :showValue="true" :showCount="true" :count="product.review_count || 0" />
      </div>
      <div class="product-price">{{ formatPrice(product.price) }} &#8381;</div>
    </div>
  </router-link>
</template>

<script>
import StarRating from './StarRating.vue'

export default {
  name: 'ProductCard',
  components: { StarRating },
  props: {
    product: { type: Object, required: true }
  },
  methods: {
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU').format(price)
    }
  }
}
</script>

<style scoped>
.product-card {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  padding: 0;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
  text-decoration: none;
}

.product-image {
  width: 100%;
  height: 200px;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-category {
  font-size: 12px;
  color: #4a90d9;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #1a1a2e;
  line-height: 1.3;
}

.product-brand {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
}

.product-rating {
  margin-bottom: 12px;
  margin-top: auto;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: #e74c3c;
}
</style>
