<template>
  <div class="guide-page">
    <h1 class="page-title">Памятка пользователя</h1>
    <p class="guide-subtitle">Подробная инструкция по использованию RateShop. Здесь вы найдёте ответы на все вопросы!</p>

    <div class="guide-search">
      <SearchBar v-model="searchQuery" placeholder="Поиск по памятке... (например: 'как оставить отзыв')" />
    </div>

    <div class="guide-sections">
      <div v-for="section in filteredSections" :key="section.id" class="guide-section card">
        <div class="section-header" @click="toggleSection(section.id)">
          <span class="section-icon">{{ section.icon }}</span>
          <h2 class="section-title">{{ section.title }}</h2>
          <span class="section-toggle">{{ openSections.includes(section.id) ? '&#9660;' : '&#9654;' }}</span>
        </div>
        <div v-show="openSections.includes(section.id)" class="section-content">
          <div v-for="(step, i) in section.steps" :key="i" class="guide-step">
            <div class="step-number">{{ i + 1 }}</div>
            <div class="step-content">
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-text" v-html="step.text"></p>
            </div>
          </div>
          <div v-if="section.tips" class="tips-box">
            <h4>&#128161; Полезные советы:</h4>
            <ul>
              <li v-for="(tip, i) in section.tips" :key="i">{{ tip }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div v-if="showFAQ" class="guide-section card">
        <div class="section-header" @click="toggleSection('faq')">
          <span class="section-icon">&#10067;</span>
          <h2 class="section-title">Часто задаваемые вопросы (FAQ)</h2>
          <span class="section-toggle">{{ openSections.includes('faq') ? '&#9660;' : '&#9654;' }}</span>
        </div>
        <div v-show="openSections.includes('faq')" class="section-content">
          <div v-for="(item, i) in faqItems" :key="i" class="faq-item">
            <h3 class="faq-question">&#10069; {{ item.q }}</h3>
            <p class="faq-answer">{{ item.a }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'

export default {
  name: 'GuideView',
  components: { SearchBar },
  data() {
    return {
      searchQuery: '',
      openSections: ['products'],
      sections: [
        {
          id: 'products',
          icon: '&#128722;',
          title: 'Как просматривать товары',
          steps: [
            {
              title: 'Откройте раздел "Товары"',
              text: 'Нажмите на вкладку <strong>"Товары"</strong> в верхнем меню. Она самая первая слева. Вы увидите карточки всех доступных товаров с фотографиями, ценами и звёздочками рейтинга.'
            },
            {
              title: 'Используйте фильтры',
              text: 'Над карточками товаров есть <strong>выпадающие списки</strong> — можно выбрать категорию (например, "Электроника") и бренд (например, "Samsung"). Также можно отсортировать по цене или рейтингу.'
            },
            {
              title: 'Откройте карточку товара',
              text: 'Нажмите на любую карточку товара. Откроется полная страница с <strong>подробным описанием</strong>, фотографиями, средним рейтингом, распределением оценок и всеми отзывами.'
            },
            {
              title: 'Посмотрите фотографии',
              text: 'На странице товара сверху есть <strong>большая фотография</strong>. Если у товара несколько фото — под главным фото будут маленькие картинки (миниатюры). Нажмите на любую, чтобы увеличить.'
            }
          ],
          tips: [
            'Звёздочки показывают средний рейтинг: чем больше закрашенных звёзд, тем лучше оценки',
            'Цифра в скобках рядом со звёздами — это количество отзывов',
            'Цена отображается в рублях'
          ]
        },
        {
          id: 'reviews',
          icon: '&#128172;',
          title: 'Как оставить отзыв',
          steps: [
            {
              title: 'Перейдите на страницу товара',
              text: 'Нажмите на карточку товара в каталоге. Пролистайте страницу вниз до раздела <strong>"Оставить отзыв"</strong>.'
            },
            {
              title: 'Заполните имя',
              text: 'В поле <strong>"Ваше имя"</strong> напишите, как вас зовут. Это обязательное поле — без имени отзыв не отправится.'
            },
            {
              title: 'Поставьте оценку',
              text: 'Нажмите на <strong>звёздочки</strong>. 1 звезда — ужасно, 5 звёзд — отлично. Просто нажмите на нужную звезду. Это тоже обязательно.'
            },
            {
              title: 'Напишите текст отзыва',
              text: 'Заполните <strong>заголовок</strong> (кратко о впечатлении), <strong>основной текст</strong> (подробности), <strong>достоинства</strong> и <strong>недостатки</strong>. Всё это необязательно, но помогает другим покупателям.'
            },
            {
              title: 'Нажмите "Отправить отзыв"',
              text: 'Внизу формы есть синяя кнопка <strong>"Отправить отзыв"</strong>. Нажмите на неё. Если всё заполнено правильно — появится сообщение "Отзыв отправлен!" и ваш отзыв появится в списке.'
            }
          ],
          tips: [
            'Если кнопка "Отправить" серая и не нажимается — проверьте, что вы указали имя и поставили оценку',
            'Ваш отзыв появится сразу после отправки',
            'Вы можете оставить несколько отзывов на один и тот же товар'
          ]
        },
        {
          id: 'all-reviews',
          icon: '&#128196;',
          title: 'Как просматривать все отзывы',
          steps: [
            {
              title: 'Откройте раздел "Отзывы"',
              text: 'Нажмите на вкладку <strong>"Отзывы"</strong> в верхнем меню (вторая слева). Вы увидите ленту всех отзывов ко всем товарам.'
            },
            {
              title: 'Отсортируйте отзывы',
              text: 'Сверху есть выпадающий список сортировки. Вы можете выбрать: <strong>Сначала новые</strong>, <strong>Сначала старые</strong>, <strong>Высокий рейтинг</strong>, <strong>Низкий рейтинг</strong> или <strong>Самые полезные</strong>.'
            },
            {
              title: 'Фильтруйте по оценке',
              text: 'Второй выпадающий список позволяет показать только отзывы с определённым количеством звёзд. Например, только 5-звёздочные или только 1-звёздочные.'
            },
            {
              title: 'Оцените полезность',
              text: 'Под каждым отзывом есть кнопки <strong>&#128077;</strong> (полезно) и <strong>&#128078;</strong> (не полезно). Нажмите, чтобы помочь другим понять, какие отзывы самые полезные.'
            }
          ],
          tips: [
            'Зелёная метка "Проверенная покупка" означает, что автор действительно купил товар',
            'Нажав на название товара в отзыве, вы перейдёте на его страницу'
          ]
        },
        {
          id: 'ratings',
          icon: '&#11088;',
          title: 'Как пользоваться рейтингами',
          steps: [
            {
              title: 'Откройте раздел "Рейтинги"',
              text: 'Нажмите на вкладку <strong>"Рейтинги"</strong> в верхнем меню. Здесь собрана статистика по всем товарам.'
            },
            {
              title: 'Посмотрите общую статистику',
              text: 'Вверху страницы три карточки: <strong>количество товаров</strong>, <strong>количество отзывов</strong> и <strong>общий средний рейтинг</strong>. Далее — диаграмма распределения оценок.'
            },
            {
              title: 'Изучите топ товаров',
              text: 'Два блока: <strong>"Топ-5 лучших"</strong> (товары с самым высоким рейтингом) и <strong>"Топ-5 с низким рейтингом"</strong>. Нажмите на название товара, чтобы перейти к нему.'
            },
            {
              title: 'Таблица рейтингов',
              text: 'Внизу страницы — полная таблица всех товаров с рейтингами. Можно сортировать по рейтингу или количеству отзывов.'
            }
          ]
        },
        {
          id: 'search',
          icon: '&#128269;',
          title: 'Как пользоваться поиском',
          steps: [
            {
              title: 'Откройте раздел "Поиск"',
              text: 'Нажмите на вкладку <strong>"Поиск"</strong> в верхнем меню.'
            },
            {
              title: 'Введите запрос',
              text: 'В строке поиска наберите то, что ищете. Например: <strong>"Samsung"</strong>, <strong>"камера"</strong>, <strong>"удобные"</strong>. Поиск начнётся автоматически после ввода 2 букв.'
            },
            {
              title: 'Посмотрите результаты',
              text: 'Результаты делятся на два блока: <strong>Товары</strong> (карточки найденных товаров) и <strong>Отзывы</strong> (отзывы, в которых нашлось ваше слово).'
            },
            {
              title: 'Используйте фильтры',
              text: 'Можно дополнительно отфильтровать по <strong>категории</strong> и выбрать <strong>сортировку</strong> (по цене, рейтингу или дате).'
            }
          ],
          tips: [
            'Поиск ищет по названиям товаров, описаниям, текстам отзывов, достоинствам и недостаткам',
            'Чтобы очистить строку поиска, нажмите крестик справа',
            'Минимум 2 символа для начала поиска'
          ]
        }
      ],
      faqItems: [
        { q: 'Нужно ли регистрироваться, чтобы оставить отзыв?', a: 'Нет, регистрация не требуется. Просто укажите ваше имя при написании отзыва.' },
        { q: 'Могу ли я удалить свой отзыв?', a: 'Удалять отзывы может только администратор. Если вы хотите удалить свой отзыв, обратитесь к администратору.' },
        { q: 'Что значит "Проверенная покупка"?', a: 'Это означает, что автор отзыва действительно приобрёл данный товар. Таким отзывам можно доверять больше.' },
        { q: 'Как работает рейтинг?', a: 'Рейтинг — это средняя оценка по всем отзывам. Например, если 3 человека поставили 5, 4 и 3 звезды, средний рейтинг будет 4.0.' },
        { q: 'Почему я не могу нажать кнопку "Отправить отзыв"?', a: 'Проверьте, что вы заполнили обязательные поля: имя и оценка (звёздочки). Без них кнопка будет неактивна.' },
        { q: 'Как связаться с администратором?', a: 'Раздел "Админка" доступен по ссылке в правой части верхнего меню. Доступ только с паролем.' }
      ]
    }
  },
  computed: {
    filteredSections() {
      if (!this.searchQuery) return this.sections
      const q = this.searchQuery.toLowerCase()
      return this.sections.filter(s => {
        const inTitle = s.title.toLowerCase().includes(q)
        const inSteps = s.steps.some(step =>
          step.title.toLowerCase().includes(q) || step.text.toLowerCase().includes(q)
        )
        const inTips = s.tips && s.tips.some(t => t.toLowerCase().includes(q))
        return inTitle || inSteps || inTips
      })
    },
    showFAQ() {
      if (!this.searchQuery) return true
      const q = this.searchQuery.toLowerCase()
      return this.faqItems.some(item =>
        item.q.toLowerCase().includes(q) || item.a.toLowerCase().includes(q)
      )
    }
  },
  methods: {
    toggleSection(id) {
      const idx = this.openSections.indexOf(id)
      if (idx >= 0) {
        this.openSections.splice(idx, 1)
      } else {
        this.openSections.push(id)
      }
    }
  }
}
</script>

<style scoped>
.guide-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}

.guide-search {
  margin-bottom: 24px;
  max-width: 600px;
}

.guide-section {
  margin-bottom: 16px;
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 4px 0;
  user-select: none;
}

.section-header:hover {
  opacity: 0.8;
}

.section-icon {
  font-size: 24px;
}

.section-title {
  flex: 1;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0;
}

.section-toggle {
  font-size: 14px;
  color: #999;
}

.section-content {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.guide-step {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #4a90d9;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
}

.step-text {
  font-size: 14px;
  color: #555;
  line-height: 1.7;
}

.tips-box {
  background: #fff8e1;
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
}

.tips-box h4 {
  font-size: 14px;
  margin-bottom: 8px;
  color: #f57f17;
}

.tips-box ul {
  margin: 0;
  padding-left: 20px;
}

.tips-box li {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
  line-height: 1.5;
}

.faq-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.faq-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.faq-question {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.faq-answer {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}
</style>
