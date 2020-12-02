<template>
  <div>
    <el-row>
    <el-col :span="10" :offset="1">
      <el-card :body-style="{ padding: '0px' }">
        <img :src=image_url class="image">
        <div style="padding: 14px;">
          <span>{{ pname }}</span>
        </div>
      </el-card>
    </el-col>
    <el-col :span="10" :offset="1">
      <el-form label-position="left" class="item">
        <el-form-item label="商品名称：" size="small">
          <span>{{ pname }}</span>
        </el-form-item>
        <el-form-item label="所属类别：" size="small">
          <span>{{ cname }}</span>
        </el-form-item>
        <el-form-item label="商品单价：" size="small">
          <span>{{ price }}</span>
        </el-form-item>
        <el-form-item label="商品描述：" size="small">
          <span>{{ product_info }}</span>
        </el-form-item>
        <el-form-item label="类别描述：" size="small">
          <span>{{ category_info }}</span>
        </el-form-item>
        <el-form-item label="商品状态：" size="small">
          <span>{{ status }}</span>
        </el-form-item>
      </el-form>
    </el-col>
    </el-row>
  </div>
</template>

<script>
    import axios from 'axios'
    export default {
        name: "product_details",
        data() {
          return {
            id: '',
            pname: '',
            cname: '',
            price: '',
            product_info: '',
            category_info: '',
            status: '',
            image_url: '',
          }
        },
        methods: {
          getProduct() {
            this.id = this.$route.params && this.$route.params.id;
            let data = {
              id: this.id,
            };
            const url = "http://localhost:5000/product/details";
            axios.post(url, data).then((res)=>{
              this.pname = res.data.pname;
              this.cname = res.data.cname;
              this.price = res.data.price;
              this.product_info = res.data.product_info;
              this.category_info = res.data.category_info;
              this.status = res.data.status;
              this.image_url = res.data.image_url;
            })
          }
        },

        created() {
          this.getProduct()
        }

    }
</script>

<style scoped>
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .item {
    margin-bottom: 18px;
  }

  .image {
    width: 100%;
    display: block;
  }


</style>
