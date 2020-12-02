<template>
<div>
  用户管理
  <div>
  <br/>
  <el-container>
    <el-header style="text-align: right" label-width="20px" height="50px">
      <el-col :span="8" style="padding-left: 10px; padding-right: 10px;">
      <el-input v-model="username" placeholder="搜索用户名"></el-input>
      </el-col>
      <el-col :span="4" style="padding-left: 10px; padding-right: 10px;">
      <el-button type="primary" size="medium" icon="el-icon-search" @click="onSubmit">查询</el-button>
      </el-col>
    </el-header>
    <el-main>
      <el-table :data="tableData">
        <el-table-column prop="user_id" label="ID" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="username" label="用户名" align="center" min-width="60">
        </el-table-column>
        <el-table-column prop="authority" label="权限" align="center" min-width="60">
        </el-table-column>
        <el-table-column prop="create_time" label="注册时间" align="center" min-width="60">
        </el-table-column>
        <el-table-column prop="state" label="账号启禁" align="center">
          <template slot-scope="scope">
            <el-switch
                       v-model="scope.row.state"
                       active-color="#13ce66"
                       inactive-color="#ff4949"
                       :active-value="0"
                       :inactive-value="1"
                       @change="changeSwitch(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="权限变更" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="check(scope.row)">修改权限</el-button>
            <el-dialog title="请选择用户权限" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
              <el-radio v-model="radio" label="1">提升为管理员</el-radio>
              <el-radio v-model="radio" label="2">降为普通用户</el-radio>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="danger" @click="updateAuthority(scope.row)">确 定</el-button>
              </span>
            </el-dialog>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
  </div>

</div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "user_manage",
      data() {
        return {
          username: '',
          tableData: '',
          dialogVisible: false,
          radio: '',
          selected_id: '',
        }
      },
      methods: {
        getUsers() {
          const url = "http://localhost:5000/user/manage";
          axios.post(url).then((res)=>{
            this.tableData = res.data
          })
        },

        onSubmit() {
          let data = {
            username: this.username
          };
          const url = "http://localhost:5000/user/query";
          axios.post(url, data).then((res)=>{
            this.tableData = res.data
          })
        },

        check(row) {
          this.dialogVisible = true;
          this.selected_id = row.user_id;
        },

        updateAuthority(row) {
          let data = {
            user_id: this.selected_id,
            radio: this.radio,
          };
          const url = "http://127.0.0.1:5000/user/authority/update";
          axios.post(url,data).then((res)=>{
              if(parseInt(res.data.code)===200){
                this.$message({
                    message: "修改成功!",
                    type: 'success'
                });
              }
              else if(parseInt(res.data.code)===400)
              {
                this.$message.error({
                    message: '该用户已被禁用，不可修改',
                });
              }
              console.log(res);
              this.dialogVisible = false;
              this.getUsers();
          })
          .catch((error)=>{
              console.error(error);
          })
        },

        changeSwitch(row) {
          let data = {
            user_id: row.user_id
          };
          const url = "http://localhost:5000/user/forbidden";
          axios.post(url, data).then((res)=>{
            this.getUsers();
            console.log(res);
          })
        },

        handleClose() {
          this.dialogVisible = false
        },

      },

      created() {
        this.getUsers();
      }

    }
</script>

<style scoped>

</style>
