// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import md5 from 'js-md5'

Vue.use(ElementUI);
Vue.config.productionTip = false;
Vue.prototype.$md5 = md5;

router.beforeEach((to,from,next) => {
  // 如果即将进入的路由对象是登录页，则进行跳转，否则验证是否携带accessToken,如果有，则进
  // 行跳转，没有，则不允许跳转
  if(to.path === "/auth/login" || to.path==="/auth/register")
  {
      next();
  }
  else{
    if (sessionStorage.getItem('token') && sessionStorage.getItem('user'))
    {
        if(to.path === '/product/add' || to.path === '/category/add')
        {
          if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'0')
          ||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'1')){
            next();
          }
          else
          {
            ElementUI.Message.error({
              message: '您不具有权限浏览',
            });
            next("/index");
          }
        }
        else if(to.path==="/user/usermanage")
        {
            if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'0'))
                next();
            else
            {
              ElementUI.Message.error({
                message: '您不具有权限浏览',
              });
              next("/index")
            }
        }
        else
        {
           if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'0')
             ||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'1')
              ||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'2'))
           {
             next();
           }
           else if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'3'))
           {
             ElementUI.Message.error({
               message: '该账户已被禁用',
             });
             setTimeout(() => {
               next("/auth/register");
             }, 1000);
           }
           else
           {
             ElementUI.Message.error({
               message: '您还未登录',
             });
             setTimeout(() => {
               next("/auth/login");
             }, 1000);
           }
        }
    }
    else
    {
        ElementUI.Message.error({
          message: '您还未登录',
        });
        setTimeout(() => {
            next("/auth/login");
        }, 1000);

    }
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});


