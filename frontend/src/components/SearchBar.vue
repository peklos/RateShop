<template>
  <div class="search-bar">
    <span class="search-icon">&#128269;</span>
    <input
      type="text"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      class="search-input"
    />
    <button v-if="modelValue" class="clear-btn" @click="$emit('update:modelValue', '')">&#10005;</button>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    modelValue: { type: String, default: '' },
    placeholder: { type: String, default: 'Поиск...' }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 100%;
}

.search-icon {
  position: absolute;
  left: 14px;
  font-size: 18px;
  color: #777;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 42px;
  border: 2px solid #2a2a40;
  border-radius: 12px;
  font-size: 15px;
  background: #16162a;
  color: #e0e0e0;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4a90d9;
  box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.2);
}

.search-input::placeholder {
  color: #666;
}

.clear-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  font-size: 16px;
  color: #777;
  cursor: pointer;
  padding: 4px;
}

.clear-btn:hover {
  color: #e0e0e0;
}
</style>
