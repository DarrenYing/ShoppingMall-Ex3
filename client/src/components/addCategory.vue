<template>
<div>
  增加商品类别
  <br/>
  <br/>
  <el-row>
    <el-col :span="15" :offset="3">
      <el-form ref="form" label-width="130px" size="mini">
        <el-form-item label="类别名称">
          <el-input v-model="form.cname"></el-input>
        </el-form-item>
        <el-form-item label="类别描述">
          <el-input v-model="form.info"></el-input>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="onSubmit">提交</el-button>
          <el-button @click="turnback">取消</el-button>
        </el-form-item>
      </el-form>
      <el-dialog title="提交成功！" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
          <span>商品类别已添加</span>
          <span slot="footer" class="dialog-footer">
            <el-button type="danger" @click="turnback">确 定</el-button>
          </span>
      </el-dialog>
    </el-col>
  </el-row>
</div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "addCategory",
      data() {
        return {
          form: {
            cname: '',
            info: '',
          },

          dialogVisible: false,

        }
      },
      methods: {
        onSubmit() {
          let data = {
            cname: this.form.cname,
            info: this.form.info,
          };
          const url = "http://localhost:5000/category/add";
          axios.post(url, data).then((res)=>{
            console.log(res);
            this.dialogVisible=true;
          })
        },

        turnback() {
          this.dialogVisible=false;
          //回到商品界面
          this.$router.push({
            path:'add/',
            name: 'addProduct',
          })
        },
      },

    }
</script>

<style scoped>

</style>
