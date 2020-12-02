<template>
  <div id="app">
<!--    <el-header></el-header>-->
    <el-container style="height: 500px; border: 1px solid #eee">
      <el-aside width="160px" style="background-color: rgb(238, 241, 246)">
        <div class="app-side-logo">
          <img src="@/assets/logo.png"
               :width="isCollapse ? '60' : '60'"
               height="60" />
        </div>
        <el-menu router
                 :default-active="$route.path">
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>商品管理</template>
            <el-menu-item-group>
              <el-menu-item index="/product/item">商品</el-menu-item>
              <el-menu-item index="/product/cart">购物车</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-message"></i>订单管理</template>
            <el-menu-item-group>
              <el-menu-item index="/order/order">订单</el-menu-item>
<!--              <el-menu-item index="/order/item">订单条目</el-menu-item>-->
<!--              <el-menu-item index="/order/payment">支付信息</el-menu-item>-->
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"><i class="el-icon-message"></i>用户管理</template>
            <el-menu-item-group>
              <el-menu-item index="/user/baseinfo">修改密码</el-menu-item>
              <el-menu-item index="/user/userinfo">个人资料</el-menu-item>
              <el-menu-item index="/user/usermanage">用户管理</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
      <el-header>
        <el-row>
        <div align="right">
          <el-dropdown trigger="hover"
                       :hide-on-click="false">
            <span class="el-dropdown-link">
              {{ username }}
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="gotoUserinfo">设置</el-dropdown-item>
              <el-dropdown-item divided
                                @click.native="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div align="left">
          <el-button type="primary" size="mini" icon="el-icon-arrow-left" @click="prev">返回</el-button>
        </div>
        </el-row>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      </el-container>

  </el-container>
</div>
</template>

<script>
export default {
  name: 'index',

  data() {
    return {
      username: '',
      isCollapse: false,
    }
  },
  methods: {
    toggleSideBar() {
      this.isCollapse = !this.isCollapse
    },
    logout: function () {
      this.$confirm('确认退出?', '提示', {})
        .then(() => {
          sessionStorage.removeItem('user');
          this.$router.push('/auth/login');
        })
        .catch(() => { });
    },
    gotoUserinfo() {
      this.$router.push({
        path:'/user/userinfo',
        name: 'userinfo',
      })
    },


    prev() {
      this.$router.go(-1);
    }
  },
  mounted: function () {
    let user = sessionStorage.getItem('user');
    if (user) {
      this.username = user;
    }
  },
}
</script>

<style>
  .el-header{
    height: 60px,

  }
</style>
