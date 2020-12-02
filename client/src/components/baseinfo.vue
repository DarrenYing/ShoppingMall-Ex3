<template>
<div>
    <el-row>
    <div class="demo-image">
      <div class="block" align="center">
        <el-image style="width: 80px; height: 80px"
                  :src="url"
                  :fit="fit">
        </el-image>
      </div>
    </div>
    </el-row>
    <br/>
    <el-row>
    <el-col :span="15" :offset="3">
      <el-form label-position="left" label-width="100px">
        <el-form-item label="用户名：" size="small">
          <el-input v-model="username" auto-complete="off" :disabled="true" class="input"></el-input>
        </el-form-item>
        <el-form-item label="旧密码：" size="small">
          <el-input v-model="oldpassword" type="password" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="新密码：" size="small">
          <el-input v-model="newpassword" type="password" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="新密码确认：" size="small">
          <el-input v-model="newpasswordck" type="password" :disabled="edit" class="input"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" size="small" icon="el-icon-edit" @click="openEdit"></el-button>
      <el-button type="success" size="small" icon="el-icon-check" @click="closeEdit()"></el-button>
    </el-col>
    </el-row>
</div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "baseinfo",
      data() {
        return {
          fit: 'scale-down',
          url: 'https://s2.ax1x.com/2019/12/27/lVFLGQ.th.png',
          username: '',
          oldpassword: '',
          newpassword: '',
          newpasswordck: '',
          edit: true,
        }
      },
      methods: {
        getUser() {
          let user = sessionStorage.getItem('user');
          if (user) {
            this.username = user;
          }
        },

        openEdit() {
            this.edit = false;
          },
        closeEdit() {
          this.edit = true;
          let data = {
            username: this.username,
            oldpassword: this.$md5(this.oldpassword),
            newpassword: this.$md5(this.newpassword),
            newpasswordck: this.$md5(this.newpasswordck),
          };
          const url = "http://localhost:5000/user/password/update";
          axios.post(url, data).then((res)=>{
            if(parseInt(res.data.code)===200)
            {
              this.$message({
                  message: "密码修改成功,请重新登录",
                  type: 'success'
              });
              sessionStorage.clear();
              setTimeout(() => {
                  this.$router.push("/auth/login");
              }, 1000);
            }
            else if(parseInt(res.data.code)===400)
            {
                this.$message.error({
                    message: '修改失败，请填写表格相关信息',
                });
            }
            else if(parseInt(res.data.code)===301)
            {
                this.$message.error({
                    message: '旧密码输入错误！',
                });
            }
            else if(parseInt(res.data.code)===300)
            {
                this.$message.error({
                    message: '两次新密码输入不一致！',
                });
            }
            this.oldpassword='';
            this.newpassword='';
            this.newpasswordck='';
          })
        },
      },

      created() {
        this.getUser();
      }

    }
</script>

<style scoped>

</style>
