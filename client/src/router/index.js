import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import register from '@/components/register'
import login from '@/components/login'
import index from '@/components/index'
import product_item from "@/components/product_item"
import addProduct from "@/components/addProduct"
import addCategory from "@/components/addCategory"
import product_details from "@/components/product_details"
import updateProduct from "@/components/updateProduct"
import product_cart from "@/components/product_cart"
import product_cart_payment from "@/components/product_cart_payment"
import orders from "@/components/orders"
import order_details from "@/components/order_details"
import userinfo from "@/components/userinfo"
import baseinfo from "@/components/baseinfo"
import user_manage from "@/components/user_manage"

Vue.use(Router);


const routes = [
    {
      path: '/',
      redirect: '/auth/login',
    },
    {
      path: '/auth/register',
      name: 'register',
      component: register
    },
    {
      path: '/auth/login',
      name: 'login',
      component: login
    },
    {
      path: '/index',
      name: 'index',
      // component: index
    },
    {
      path: '/product/item',
      name: 'product_item',
      component: product_item
    },
    {
      path: '/product/add',
      name: 'addProduct',
      component: addProduct
    },
  {
      path: '/category/add',
      name: 'addCategory',
      component: addCategory
    },
    {
      path: '/product/details/:id',
      name: 'product_details',
      component: product_details
    },
    {
      path: '/product/update/:id',
      name: 'updateProduct',
      component: updateProduct
    },
    {
      path: '/product/cart/',
      name: 'product_cart',
      component: product_cart
    },
    {
      path: '/product/cart/payment',
      name: 'product_cart_payment',
      component: product_cart_payment
    },
    {
      path: '/order/order',
      name: 'orders',
      component: orders
    },
    {
      path: '/order/details/:id',
      name: 'order_details',
      component: order_details
    },
    {
      path: '/user/userinfo',
      name: 'userinfo',
      component: userinfo
    },
    {
      path: '/user/baseinfo',
      name: 'baseinfo',
      component: baseinfo
    },
    {
      path: '/user/usermanage',
      name: 'user_manage',
      component: user_manage
    },


];

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router


