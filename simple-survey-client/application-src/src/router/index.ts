import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResponsesView from '@/views/ResponsesView.vue'
import QuestionsView from '@/views/QuestionsView.vue'
import ResponseView from '@/views/ResponseView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsView,
    },
    {
      path: '/responses',
      name: 'responses',
      component: ResponsesView,
    },
    {
      path: '/responses/:id',
      name: 'response',
      component: ResponseView,
      props: true,
    },
  ],
})

export default router
