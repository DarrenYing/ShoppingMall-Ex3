<template>
<div>
  商品信息

  <div>
  <br/>
  <el-container>
    <el-header style="text-align: left" label-width="20px" height="50px">
      <el-form>
        <el-row style="margin-left: -10px; margin-right: -10px;">
          <el-col :span="4" style="padding-left: 10px; padding-right: 10px;">
          <el-form-item size="small">
            <el-input v-model="pname" placeholder="商品名称:"></el-input>
          </el-form-item>
          </el-col>
          <el-col :span="4" style="padding-left: 10px; padding-right: 10px;">
          <el-form-item size="small">
            <el-input v-model="cname" placeholder="商品类别:"></el-input>
          </el-form-item>
          </el-col>
          <el-col :span="4" style="padding-left: 10px; padding-right: 10px;">
          <el-form-item size="small">
            <el-input v-model="minprice" placeholder="价格下限:"></el-input>
          </el-form-item>
          </el-col>
          <el-col :span="4" style="padding-left: 10px; padding-right: 10px;">
          <el-form-item size="small">
            <el-input v-model="maxprice" placeholder="价格上限:"></el-input>
          </el-form-item>
          </el-col>
          <el-col :span="4" style="padding-left: 30px; padding-right: 10px;">
          <el-form-item>
            <el-button type="primary" size="small" @click="onSubmit">查询</el-button>
          </el-form-item>
          </el-col>
          <el-col :span="4" style="padding-left: 0px; padding-right: 10px;">
          <el-form-item>
            <el-button type="primary" size="small" @click="addRecord" v-if="isManager">添加</el-button>
          </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-header>
    <el-main>
      <el-table :data="tableData">
        <el-table-column prop="id" label="编号" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="pname" label="商品名称" align="center" min-width="60">
        </el-table-column>
        <el-table-column prop="cname" label="商品类别" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="price" label="商品价格" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="info" label="商品描述" align="center" min-width="80">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="120">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="updateRecord(scope.row)" v-if="isManager">修改</el-button>
            <el-button type="primary" size="small" @click="delRecord(scope.row)" v-if="isManager">删除</el-button>
            <el-button type="primary" size="small" @click="productDetails(scope.row)">详情</el-button>
            <el-button type="primary" size="small" @click="addToCart(scope.row)" v-if="!isManager">加购</el-button>
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
      name: "product_item",
      data() {
        return {
          id: '',
          pname: '',
          cname: '',
          minprice: '',
          maxprice: '',
          tableData: '',
          isManager: false,
          username: '',
        }
      },
      methods: {
        getIsManager(){
          let user = sessionStorage.getItem('user');
          if (user) {
            this.username = user;
          }
          let data = {
            username: this.username,
          };
          const url = "http://localhost:5000/authority/query";
          axios.post(url, data).then((res)=>{
            console.log(res.data);
            this.isManager = Boolean(res.data);
            console.log(this.isManager);
          })
        },
        getAllItems() {
          const url = "http://localhost:5000/product/all";
          axios.post(url).then((res)=>{
            this.tableData = res.data
          })
        },
        onSubmit() {
          let data = {
            pname: this.pname,
            cname: this.cname,
            minprice: this.minprice,
            maxprice: this.maxprice,
          };
          const url = "http://localhost:5000/product/item";
          axios.post(url, data).then((res)=>{
            this.tableData = res.data
          })
        },
        addRecord() {
          this.$router.push({
            path:'add/',
            name: 'addProduct',
          })
        },
        delRecord(row) {
          let data = {
            product_id: row.id,
          };
          const url = "http://localhost:5000/product/delete";
          axios.post(url, data).then((res)=>{
            console.log(res);
            this.getAllItems();
          })
        },
        updateRecord(row) {
          this.$router.push({path:'update/'+row.id})
        },
        productDetails(row) {
          this.$router.push({path:'details/'+row.id})
        },
        addToCart(row) {
          // let user = sessionStorage.getItem('user');
          // if (user) {
          //   this.username = user;
          // }
          let data = {
            username: this.username,
            product_id: row.id,
          };
          const url = "http://localhost:5000/product/cart/add";
          axios.post(url, data).then((res)=>{
            console.log(res)
          })
        }

      },
      created() {
        this.getIsManager();
        this.getAllItems(); //默认展示全部商品
      }
    }
</script>

<style scoped>

</style>
