import { createWebHistory, createRouter } from 'vue-router'
import HomeView from '../views/home/index.vue';
import Setting from '../components/settings.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  },
  { path: '/setting', component: Setting },
];

var router = createRouter({
  history: createWebHistory(),
  routes
})
export default router