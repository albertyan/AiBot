import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PageView from '../views/pageView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/index',
      name: 'index',
      component: PageView,
      redirect: '/index/welcome',
      children:[
        {
          path:'welcome',
          name: 'welcome',
          component: () => import('@/views/welcome.vue')
        },
        {
          path:'ai',
          name: 'ai',
          component: () => import('@/views/ai.vue')
        },
        {
          path:'contacts',
          name: 'contacts',
          component: () => import('@/views/contacts.vue')
        },
        {
          path:'sop',
          name: 'sop',
          component: () => import('@/views/sop.vue')
        },
        {
          path:'setting',
          name: 'setting',
          component: () => import('@/views/setting.vue')
        }
      ]
    },
  ],
})

export default router
