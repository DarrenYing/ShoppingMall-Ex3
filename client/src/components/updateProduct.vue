<template>
<div>
  商品信息修改
  <br/>
  <br/>
    <el-row>
    <el-col :span="15" :offset="3">
      <el-form label-position="left" label-width="100px">
        <el-form-item label="商品名称：" size="small">
          <el-input v-model="form.pname" auto-complete="off" :disabled="edit" class="input"></el-input>
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
        <el-form-item label="商品价格：" size="small">
          <el-input v-model="form.price" auto-complete="off" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="商品描述：" size="small">
          <el-input v-model="form.product_info" auto-complete="off" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="类别描述：" size="small">
          <el-input v-model="form.category_info" auto-complete="off" :disabled="edit" class="input"></el-input>
        </el-form-item>
        <el-form-item label="图片链接：" size="small">
          <el-input v-model="form.image_url" auto-complete="off" :disabled="edit" class="input"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" size="small" icon="el-icon-edit" @click="openEdit"></el-button>
      <el-button type="success" size="small" icon="el-icon-check" @click="closeEdit(form)"></el-button>
      <el-button @click="turnback">返回</el-button>
    </el-col>
    </el-row>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "updateProduct",
      data() {
        return {
          product_id: '',
          form: {
            pname: '',
            price: '',
            product_info: '',
            category_info: '',
            image_url: '',
          },
          categories: '',
          category_id: '',
          edit:true,
        }
      },
      methods: {
        getProduct() {
          this.product_id = this.$route.params && this.$route.params.id;
          let data = {
            id: this.product_id,
          };
          const url = "http://localhost:5000/product/details";
          axios.post(url, data).then((res)=>{
            this.form.pname = res.data.pname;
            this.category_id = res.data.category_id;
            this.form.price = res.data.price;
            this.form.product_info = res.data.product_info;
            this.form.category_info = res.data.category_info;
            this.form.image_url = res.data.image_url;
          })
        },
        getCategories() {
          const url = "http://localhost:5000/category/query";
          axios.post(url).then((res)=>{
            this.categories = res.data;

            console.log(res.data[0])
          })
        },
        openEdit() {
          this.edit = false;
        },
        closeEdit(form) {
          this.edit = true;
          let data = {
            product_id: this.product_id,
            pname: form.pname,
            category_id: this.category_id,
            price: form.price,
            product_info: form.product_info,
            category_info: form.category_info,
            image_url: form.image_url,
          };
          const url = "http://localhost:5000/product/update";
          axios.post(url, data).then((res)=>{
            console.log(res)
          })
        },
        turnback() {
          //回到商品界面
          this.$router.push({
            path:'item/',
            name: 'product_item',
          })
        },

      },
      created() {
        this.getProduct();
        this.getCategories();
      }

    }
</script>

<style scoped>

</style>
