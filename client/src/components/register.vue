<template>
  <body id="register">
    <el-card class="box-card">
        <div slot="header" class="clearfix" align="center">
          <span>电商平台</span>
        </div>
        <el-col :span="15" :offset="3">
          <el-form label-position="right" label-width="100px">
            <el-form-item label="用户名：" size="small">
              <el-input v-model="model.username" auto-complete="off" class="input"></el-input>
            </el-form-item>
            <el-form-item label="邮箱：" size="small">
              <el-input v-model="model.email" auto-complete="off" class="input"></el-input>
            </el-form-item>
            <el-form-item label="密码：" size="small">
              <el-input type="password" v-model="model.password" auto-complete="off" class="input"></el-input>
            </el-form-item>
            <el-form-item label="确认密码：" size="small">
              <el-input type="password" v-model="model.pswrd_ck" auto-complete="off" class="input"></el-input>
            </el-form-item>
          </el-form>
          <el-button type="primary" size="medium" @click="jump">直接登录</el-button>
          <el-button type="success" size="medium" @click="register">注册</el-button>
        </el-col>
    </el-card>

  </body>
</template>

<script>
    import axios from "axios"
    import qs from "qs"
    export default {
        name: "register",
        data() {
          return {
            model:{
              username: "",
              email:"",
              password: "",
              pswrd_ck: "",
              authority:'2',
            }
          }
        },
        methods:{
          register() {
            let data={
                username: this.model.username,
                password: this.$md5(this.model.password),
                pswrd_ck: this.$md5(this.model.pswrd_ck),
                email: this.model.email,
                authority: this.model.authority
            };
            const url = "http://localhost:5000/register";
            axios
              .post(url, qs.stringify(data))
              .then((res) => {
                if (parseInt(res.data.code)===200)
                {
                  this.$message({
                      message: "注册成功!",
                      type: 'success'
                  });
                  setTimeout(() => {
                      this.$router.push("login/");
                  }, 1000);
                }
                else if(parseInt(res.data.code)===400)
                {
                  this.$message.error({
                      message: '两次密码输入不一致！',
                  });
                  const ac=res.data.account;
                  this.model.username=ac["username"];
                  this.model.password=ac["password"];
                  this.model.pswrd_ck=''
                }
                else if (parseInt(res.data.code)===500)
                {
                  this.$message.error({
                      message: "所有填写信息均不能为空！",
                  });
                }
                else if (parseInt(res.data.code)===300)
                {
                  this.$message.error({
                      message: "用户已存在!",
                  });
                }
              })
              .catch((error) => {
                console.log(error);
              });
          },
          jump(){
            this.$message("跳转中……");
            setTimeout(() => {
              this.$router.push({
                path:'login/',
                name: 'login',
              })
            }, 1000);
          },
          channelInputLimit (e){
                let key = e.key;
                // 不允许输入'e'和'.'
                if (key === 'e' || key === '.') {
                    e.returnValue = false;
                    return false
                }
                return true
          },
        }
    }
</script>
<style scoped>
  #register {
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
    height: 350px;
    margin-left: 25%;
    margin-top: 2%;
  }
  .el-button {
    margin-left: 60px;
  }
  .el-button+.el-button {
    margin-left: 20px;
  }
</style>
