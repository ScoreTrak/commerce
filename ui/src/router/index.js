import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/bank',
    name: 'bank',
    component: () => import(/* webpackChunkName: "bank" */ '../views/Bank.vue'),
  },
  {
    path: '/shop',
    name: 'shop',
    component: () => import(/* webpackChunkName: "shop" */ '../views/Shop.vue'),
    children: [
      {
        path: 'orders',
        name: 'shop-orders',
        component: () => import(/* webpackChunkName: "shop" */ '../views/ShopOrders.vue'),
      },
      {
        path: 'products/:productId',
        name: 'shop-product',
        component: () => import(/* webpackChunkName: "shop" */ '../views/ShopProduct.vue'),
      },
      {
        path: 'products',
        name: 'shop-products',
        component: () => import(/* webpackChunkName: "shop" */ '../views/ShopProducts.vue'),
      },
    ],
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
