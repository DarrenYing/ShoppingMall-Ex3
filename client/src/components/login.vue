<template>
  <body id="login">
    <el-card class="box-card">
        <div slot="header" class="clearfix" align="center">
          <span>电商平台</span>
        </div>
        <el-col :span="15" :offset="3">
          <el-form label-position="right" label-width="100px">
            <el-form-item label="用户名：" size="small">
              <el-input v-model="model.username" auto-complete="off" class="input"></el-input>
            </el-form-item>
            <el-form-item label="密码：" size="small">
              <el-input type="password" v-model="model.password" auto-complete="off" class="input"></el-input>
            </el-form-item>
          </el-form>
          <el-button type="primary" size="medium" @click="jump">尚未注册</el-button>
<!--          <el-button type="success" size="medium" @click="toindex">主页</el-button>-->
          <el-button type="success" size="medium" @click="login">登录</el-button>
        </el-col>
    </el-card>

  </body>
</template>

<script>
  import axios from "axios"
  import qs from "qs"

  export default {
    name:"login",
    data: () => ({
    model: {
      username: '',
      password: '',
    },
  }),

  methods: {
    login() {
      let data={
        username: this.model.username,
        password: this.$md5(this.model.password),
      };
      const url = "http://localhost:5000/login";
      axios
        .post(url,qs.stringify(data))
        .then((res)=>{
          if(parseInt(res.data.code)===200)
          {
            this.$message({
                message: "登录成功!",
                type: 'success'
            });

            sessionStorage.setItem("token",res.data.token);
            sessionStorage.setItem("user",this.model.username);
            setTimeout(() => {
                this.$router.push("/index");
            }, 1000);

          }
          else if(parseInt(res.data.code)===400)
          {
            this.$message.error({
                message: '登录失败，请检查你的用户名和密码',
            });
            // this.win_visible=false;
          }
        })
        .catch((error)=>{
            console.error(error);
        })
    },
    jump(){
      this.$message("跳转中……");
      setTimeout(() => {
        this.$router.push({
          path:'register/',
          name: 'register',
        })
      }, 1000);
    },
  },
}
</script>
<style scoped>
  #login {
    background:url("../assets/background.jpg") no-repeat;
    background-position: center;
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }
  body{
    margin: -8px;
    padding: 0;
  }

  .box-card {
    width: 480px;
    height: 250px;
    margin-left: 25%;
    margin-top: 8%;
  }
  .el-button {
    margin-left: 60px;
  }
  .el-button+.el-button {
    margin-left: 20px;
  }
</style>
