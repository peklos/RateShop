<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span class="logo-icon">⭐</span>
        <span class="logo-text">RateShop</span>
      </router-link>
      <nav class="nav">
        <router-link to="/products" class="nav-link" active-class="active">
          <span class="nav-icon">🛒</span> Товары
        </router-link>
        <router-link to="/reviews" class="nav-link" active-class="active">
          <span class="nav-icon">💬</span> Отзывы
        </router-link>
        <router-link to="/ratings" class="nav-link" active-class="active">
          <span class="nav-icon">⭐</span> Рейтинги
        </router-link>
        <router-link to="/search" class="nav-link" active-class="active">
          <span class="nav-icon">🔍</span> Поиск
        </router-link>
        <router-link to="/guide" class="nav-link" active-class="active">
          <span class="nav-icon">📖</span> Памятка
        </router-link>
        <router-link to="/admin" class="nav-link nav-admin" active-class="active">
          <span class="nav-icon">⚙️</span> Админка
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  height: 64px;
  gap: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 28px;
  color: #f1c40f;
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.nav {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 14px;
  color: #a0aec0;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-link:hover {
  color: white;
  background: rgba(255,255,255,0.08);
  text-decoration: none;
}

.nav-link.active {
  color: white;
  background: rgba(74, 144, 217, 0.3);
}

.nav-icon {
  font-size: 16px;
}

.nav-admin {
  margin-left: auto;
  color: #f39c12;
}

.nav-admin:hover {
  color: #f1c40f;
}

.nav-admin.active {
  background: rgba(243, 156, 18, 0.2);
  color: #f1c40f;
}
</style>
