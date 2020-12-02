<template>
<div>
  增加商品
  <br/>
  <br/>
  <el-row>
    <el-col :span="15" :offset="3">
      <el-form ref="form" label-width="130px" size="mini">
        <el-form-item label="商品名称">
          <el-input v-model="form.pname"></el-input>
        </el-form-item>
        <el-form-item label="商品描述">
          <el-input v-model="form.info"></el-input>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="form.price"></el-input>
        </el-form-item>
        <el-form-item label="图片链接">
          <el-input v-model="form.image_url"></el-input>
        </el-form-item>
        <el-form-item label="商品类别">
          <el-select v-model="category_id" placeholder="请选择所属类别">
            <el-option
              v-for="item in categories"
              :key="item.category_id"
              :label="item.cname"
              :value="item.category_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="addCategory">新建商品类别</el-button>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="onSubmit">提交</el-button>
          <el-button @click="turnback">取消</el-button>
        </el-form-item>
      </el-form>
      <el-dialog title="提交成功！" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
          <span>商品已添加</span>
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
      name: "addProduct",
      data() {
        return {

          form: {
            pname: '',
            info: '',
            price: '',
            image_url: '',
          },

          categories: '',
          category_id: '',
          dialogVisible: false,
          useNewCategory: false,
        }
      },
      methods: {
        onSubmit() {
          let data = {
            pname: this.form.pname,
            category_id: this.category_id,
            info: this.form.info,
            price: this.form.price,
            image_url: this.form.image_url,
          };
          const url = "http://localhost:5000/product/add";
          axios.post(url, data).then((res)=>{
            console.log(res);
            this.dialogVisible=true;
          })
        },

        addCategory() {
          this.$router.push({
            path:'/category/add',
            name: 'addCategory',
          })
        },

        turnback() {
          this.dialogVisible=false;
          //回到商品界面
          this.$router.push({
            path:'item/',
            name: 'product_item',
          })
        },

        getCategories() {
          const url = "http://localhost:5000/category/query";
          axios.post(url).then((res)=>{
            this.categories = res.data;

            console.log(res.data[0])
          })
        },

        handleClose() {
          this.dialogVisible = false
        },
      },

      created() {
        this.getCategories();
      }

    }
</script>

<style scoped>

</style>
