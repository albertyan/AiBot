import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'launch',
      component: () => import('../views/Launch.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/ai-sales',
      name: 'ai-sales',
      component: () => import('../views/AiSales.vue')
    },
    {
      path: '/customer-management',
      name: 'customer-management',
      component: () => import('../views/CustomerManagement.vue')
    },
    {
      path: '/moments',
      name: 'moments',
      component: () => import('../views/Moments.vue')
    },
    {
      path: '/automation-sop',
      name: 'automation-sop',
      component: () => import('../views/AutomationSOP.vue')
    },
    {
      path: '/config',
      name: 'config',
      component: () => import('../views/Config.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue')
    }
  ]
})

export default router
