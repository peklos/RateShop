<template>
  <div class="star-rating" :class="{ interactive: interactive }">
    <span
      v-for="star in 5"
      :key="star"
      class="star"
      :class="{ filled: star <= displayValue, half: star === Math.ceil(displayValue) && displayValue % 1 >= 0.3 && displayValue % 1 <= 0.7 }"
      @click="interactive && $emit('update:modelValue', star)"
      @mouseenter="interactive && (hoverValue = star)"
      @mouseleave="interactive && (hoverValue = 0)"
    >&#9733;</span>
    <span v-if="showValue" class="rating-value">{{ Number(modelValue).toFixed(1) }}</span>
    <span v-if="showCount" class="rating-count">({{ count }})</span>
  </div>
</template>

<script>
export default {
  name: 'StarRating',
  props: {
    modelValue: { type: Number, default: 0 },
    interactive: { type: Boolean, default: false },
    showValue: { type: Boolean, default: false },
    showCount: { type: Boolean, default: false },
    count: { type: Number, default: 0 },
    size: { type: String, default: 'medium' }
  },
  emits: ['update:modelValue'],
  data() {
    return { hoverValue: 0 }
  },
  computed: {
    displayValue() {
      if (this.interactive && this.hoverValue > 0) return this.hoverValue
      return Math.round(this.modelValue)
    }
  }
}
</script>

<style scoped>
.star-rating {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.star {
  color: #ddd;
  font-size: 20px;
  transition: color 0.15s;
  line-height: 1;
}

.star.filled {
  color: #f1c40f;
}

.interactive .star {
  cursor: pointer;
}

.interactive .star:hover {
  transform: scale(1.2);
}

.rating-value {
  margin-left: 6px;
  font-weight: 600;
  font-size: 15px;
  color: #333;
}

.rating-count {
  margin-left: 4px;
  font-size: 13px;
  color: #999;
}
</style>
