<template>
  <div class="admin-page">
    <!-- Login Form -->
    <div v-if="!isLoggedIn" class="login-section">
      <div class="login-card card">
        <h1 class="login-title">&#9881; Панель администратора</h1>
        <p class="login-subtitle">Введите логин и пароль для входа</p>
        <form @submit.prevent="login" class="login-form">
          <div class="form-row">
            <label>Логин</label>
            <input v-model="credentials.username" type="text" required placeholder="admin" />
          </div>
          <div class="form-row">
            <label>Пароль</label>
            <input v-model="credentials.password" type="password" required placeholder="Введите пароль" />
          </div>
          <div v-if="loginError" class="error-msg">{{ loginError }}</div>
          <button type="submit" class="btn btn-primary" style="width: 100%;">Войти</button>
        </form>
        <p class="test-hint">Тестовые данные — логин: <strong>admin</strong>, пароль: <strong>admin123</strong></p>
      </div>
    </div>

    <!-- Admin Dashboard -->
    <div v-else>
      <div class="admin-header">
        <h1 class="page-title">Панель администратора</h1>
        <div class="admin-user">
          <span>&#128100; {{ admin.username }} ({{ admin.role }})</span>
          <button class="btn btn-outline btn-sm" @click="logout">Выйти</button>
        </div>
      </div>

      <!-- Tabs -->
      <div class="admin-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="admin-tab"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >{{ tab.icon }} {{ tab.label }}</button>
      </div>

      <!-- Stats Tab -->
      <div v-if="activeTab === 'stats'" class="tab-content">
        <div class="stats-grid" v-if="stats">
          <div class="stat-card card">
            <div class="stat-value">{{ stats.products_count }}</div>
            <div class="stat-label">Товаров</div>
          </div>
          <div class="stat-card card">
            <div class="stat-value">{{ stats.reviews_count }}</div>
            <div class="stat-label">Отзывов</div>
          </div>
          <div class="stat-card card">
            <div class="stat-value">{{ stats.reviewers_count }}</div>
            <div class="stat-label">Авторов</div>
          </div>
          <div class="stat-card card">
            <div class="stat-value">{{ stats.avg_rating }}</div>
            <div class="stat-label">Средний рейтинг</div>
          </div>
        </div>
        <div v-if="stats && stats.recent_reviews" class="card">
          <h3>Последние отзывы</h3>
          <table class="admin-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Товар</th>
                <th>Автор</th>
                <th>Оценка</th>
                <th>Дата</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in stats.recent_reviews" :key="r.id">
                <td>{{ r.id }}</td>
                <td>{{ r.product_name }}</td>
                <td>{{ r.reviewer_name }}</td>
                <td>{{ r.rating }} &#9733;</td>
                <td>{{ r.created_at }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Reviews Tab -->
      <div v-if="activeTab === 'reviews'" class="tab-content">
        <h2>Управление отзывами ({{ adminReviews.length }})</h2>
        <table class="admin-table card">
          <thead>
            <tr>
              <th>ID</th>
              <th>Товар</th>
              <th>Автор</th>
              <th>Оценка</th>
              <th>Заголовок</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in adminReviews" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.product_name }}</td>
              <td>{{ r.reviewer_name }}</td>
              <td>{{ r.rating }} &#9733;</td>
              <td>{{ r.title || '-' }}</td>
              <td>{{ r.created_at }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="deleteReview(r.id)">Удалить</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Products Tab -->
      <div v-if="activeTab === 'products'" class="tab-content">
        <div class="tab-header">
          <h2>Управление товарами ({{ adminProducts.length }})</h2>
          <button class="btn btn-success" @click="showProductForm = !showProductForm">
            {{ showProductForm ? 'Отмена' : '+ Добавить товар' }}
          </button>
        </div>

        <!-- Add Product Form -->
        <div v-if="showProductForm" class="card form-card">
          <h3>{{ editingProduct ? 'Редактировать товар' : 'Новый товар' }}</h3>
          <form @submit.prevent="saveProduct" class="product-form">
            <div class="form-grid">
              <div class="form-row">
                <label>Название *</label>
                <input v-model="productForm.name" type="text" required />
              </div>
              <div class="form-row">
                <label>Цена *</label>
                <input v-model.number="productForm.price" type="number" step="0.01" required />
              </div>
              <div class="form-row">
                <label>Категория</label>
                <select v-model="productForm.category_id">
                  <option value="">Без категории</option>
                  <option v-for="c in adminCategories" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
              </div>
              <div class="form-row">
                <label>Бренд</label>
                <select v-model="productForm.brand_id">
                  <option value="">Без бренда</option>
                  <option v-for="b in adminBrands" :key="b.id" :value="b.id">{{ b.name }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <label>Описание</label>
              <textarea v-model="productForm.description" rows="3"></textarea>
            </div>
            <div class="form-row">
              <label>URL изображения</label>
              <input v-model="productForm.image_url" type="text" placeholder="https://..." />
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">{{ editingProduct ? 'Сохранить' : 'Добавить' }}</button>
              <button type="button" class="btn btn-outline" @click="cancelEdit">Отмена</button>
            </div>
          </form>
        </div>

        <table class="admin-table card">
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Категория</th>
              <th>Бренд</th>
              <th>Цена</th>
              <th>Рейтинг</th>
              <th>Отзывов</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in adminProducts" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.name }}</td>
              <td>{{ p.category_name || '-' }}</td>
              <td>{{ p.brand_name || '-' }}</td>
              <td>{{ formatPrice(p.price) }} &#8381;</td>
              <td>{{ Number(p.avg_rating).toFixed(1) }} &#9733;</td>
              <td>{{ p.review_count }}</td>
              <td class="actions-cell">
                <button class="btn btn-outline btn-sm" @click="editProduct(p)">&#9998;</button>
                <button class="btn btn-danger btn-sm" @click="deleteProduct(p.id)">&#10005;</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  name: 'AdminView',
  data() {
    return {
      isLoggedIn: false,
      admin: null,
      credentials: { username: '', password: '' },
      loginError: '',
      activeTab: 'stats',
      tabs: [
        { id: 'stats', icon: '&#128202;', label: 'Статистика' },
        { id: 'reviews', icon: '&#128172;', label: 'Отзывы' },
        { id: 'products', icon: '&#128722;', label: 'Товары' },
      ],
      stats: null,
      adminReviews: [],
      adminProducts: [],
      adminCategories: [],
      adminBrands: [],
      showProductForm: false,
      editingProduct: null,
      productForm: {
        name: '', description: '', price: 0, image_url: '', category_id: '', brand_id: ''
      }
    }
  },
  watch: {
    activeTab(tab) {
      if (tab === 'stats') this.loadStats()
      if (tab === 'reviews') this.loadReviews()
      if (tab === 'products') this.loadProducts()
    }
  },
  methods: {
    async login() {
      try {
        this.loginError = ''
        const res = await api.adminLogin(this.credentials.username, this.credentials.password)
        this.admin = res.data
        this.isLoggedIn = true
        await this.loadStats()
      } catch (e) {
        this.loginError = 'Неверный логин или пароль'
      }
    },
    logout() {
      this.isLoggedIn = false
      this.admin = null
      this.credentials = { username: '', password: '' }
    },
    async loadStats() {
      try {
        const res = await api.getAdminStats()
        this.stats = res.data
      } catch (e) { console.error(e) }
    },
    async loadReviews() {
      try {
        const res = await api.getAdminReviews()
        this.adminReviews = res.data
      } catch (e) { console.error(e) }
    },
    async loadProducts() {
      try {
        const [products, categories, brands] = await Promise.all([
          api.getAdminProducts(),
          api.getAdminCategories(),
          api.getAdminBrands()
        ])
        this.adminProducts = products.data
        this.adminCategories = categories.data
        this.adminBrands = brands.data
      } catch (e) { console.error(e) }
    },
    async deleteReview(id) {
      if (!confirm('Удалить этот отзыв?')) return
      try {
        await api.deleteAdminReview(id)
        await this.loadReviews()
      } catch (e) { console.error(e) }
    },
    async deleteProduct(id) {
      if (!confirm('Удалить этот товар и все его отзывы?')) return
      try {
        await api.deleteProduct(id)
        await this.loadProducts()
      } catch (e) { console.error(e) }
    },
    editProduct(product) {
      this.editingProduct = product.id
      this.productForm = {
        name: product.name,
        description: product.description || '',
        price: product.price,
        image_url: product.image_url || '',
        category_id: product.category_id || '',
        brand_id: product.brand_id || ''
      }
      this.showProductForm = true
    },
    cancelEdit() {
      this.editingProduct = null
      this.productForm = { name: '', description: '', price: 0, image_url: '', category_id: '', brand_id: '' }
      this.showProductForm = false
    },
    async saveProduct() {
      try {
        const data = { ...this.productForm }
        if (!data.category_id) data.category_id = null
        if (!data.brand_id) data.brand_id = null
        if (!data.image_url) data.image_url = `https://placehold.co/400x400?text=${encodeURIComponent(data.name)}`

        if (this.editingProduct) {
          await api.updateProduct(this.editingProduct, data)
        } else {
          await api.createProduct(data)
        }
        this.cancelEdit()
        await this.loadProducts()
      } catch (e) { console.error(e) }
    },
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU').format(price)
    }
  }
}
</script>

<style scoped>
.login-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 8px;
  color: #e8e8f0;
}

.login-subtitle {
  text-align: center;
  color: #888;
  margin-bottom: 24px;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.test-hint {
  margin-top: 16px;
  text-align: center;
  font-size: 12px;
  color: #666;
}

.test-hint strong {
  color: #999;
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
.form-row select,
.form-row textarea {
  padding: 10px 14px;
  border: 2px solid #2a2a40;
  border-radius: 8px;
  font-size: 14px;
  background: #16162a;
  color: #e0e0e0;
}

.form-row input:focus,
.form-row select:focus,
.form-row textarea:focus {
  outline: none;
  border-color: #4a90d9;
}

.form-row input::placeholder,
.form-row textarea::placeholder {
  color: #555;
}

.error-msg {
  color: #ff6b6b;
  font-size: 14px;
  text-align: center;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #999;
}

.admin-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  border-bottom: 2px solid #252540;
  padding-bottom: 0;
}

.admin-tab {
  padding: 10px 20px;
  border: none;
  background: none;
  font-size: 14px;
  font-weight: 500;
  color: #888;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.admin-tab:hover {
  color: #e0e0e0;
}

.admin-tab.active {
  color: #5a9fe6;
  border-bottom-color: #4a90d9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  padding: 24px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #5a9fe6;
}

.stat-label {
  font-size: 14px;
  color: #888;
  margin-top: 4px;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.admin-table th {
  text-align: left;
  padding: 12px 8px;
  border-bottom: 2px solid #2a2a40;
  color: #888;
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
}

.admin-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #1e1e30;
  color: #c0c0d0;
}

.actions-cell {
  display: flex;
  gap: 4px;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tab-header h2 {
  font-size: 20px;
  color: #e8e8f0;
}

.form-card {
  margin-bottom: 24px;
}

.form-card h3 {
  margin-bottom: 16px;
  color: #e8e8f0;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-actions {
  display: flex;
  gap: 8px;
}

.tab-content h2 {
  margin-bottom: 16px;
  color: #e8e8f0;
}

.tab-content h3 {
  margin-bottom: 12px;
  color: #e0e0e0;
}

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .form-grid { grid-template-columns: 1fr; }
}
</style>
