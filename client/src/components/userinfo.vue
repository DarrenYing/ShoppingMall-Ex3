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
          <el-input v-model="form.username" auto-complete="on" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="性别：" size="small">
          <el-input v-model="form.gender" auto-complete="on" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="生日：" size="small">
          <el-input v-model="form.birthday" auto-complete="on" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="职业：" size="small">
          <el-input v-model="form.profession" auto-complete="on" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="个性标签：" size="small">
          <div class="tag-group" v-if="edit">
          <el-tag
            v-for="tag in form.key_word"
            :key="tag"
            type=""
            effect="dark">
            {{ tag }}
          </el-tag>
          </div>
          <div v-if="!edit">
            <el-input v-model="form.key_word" auto-complete="off" class="input" :placeholder="form.key_word"></el-input>
          </div>
        </el-form-item>
        <el-form-item label="注册时间：" size="small">
          <span>{{ form.create_time }}</span>
        </el-form-item>
      </el-form>
      <el-button type="primary" size="small" icon="el-icon-edit" @click="openEdit"></el-button>
      <el-button type="success" size="small" icon="el-icon-check" @click="closeEdit(form)"></el-button>
    </el-col>
    </el-row>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "userinfo",
      data() {
        return {
          fit: 'scale-down',
          url: 'https://s2.ax1x.com/2019/12/27/lVFLGQ.th.png',
          form: {
            username: '',
            gender: '',
            birthday: '',
            profession: '',
            key_word: [],
            create_time: '',
            tags: '',
          },
          edit:true,
          uname: '',
          user_id: '',
        }
      },
      methods: {
          getUserInfo() {
            let user = sessionStorage.getItem('user');
            if (user) {
              this.uname = user;
            }
            let data = {
              username: this.uname,
            };
            const url = "http://localhost:5000/user/userinfo";
            axios.post(url, data).then((res)=>{
              this.form.username = res.data.username;
              this.form.gender = res.data.gender;
              this.form.birthday = res.data.birthday;
              this.form.profession = res.data.profession;
              this.form.key_word = res.data.key_word;
              this.form.create_time = res.data.create_time;
              this.user_id = res.data.user_id;
            })
          },
          openEdit() {
            this.edit = false;
          },
          closeEdit(form) {
            this.edit = true;
            let data = {
              user_id: this.user_id,
              username: form.username,
              gender: form.gender,
              birthday: form.birthday,
              profession: form.profession,
              key_word: form.key_word,
            };
            const url = "http://localhost:5000/user/userinfo/update";
            axios.post(url, data).then((res)=>{
              console.log(res);
              this.getUserInfo();
            })
          },
      },
      created() {
        this.getUserInfo();
      }
    }
</script>

<style scoped>
  .el-tag+.el-tag {
    margin-left: 10px;
  }
</style>
