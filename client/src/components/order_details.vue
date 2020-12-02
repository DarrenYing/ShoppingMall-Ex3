<template>
<div>
  订单详情
  <div>
  <br/>
  <el-container>
    <el-main>
      <el-table :data="tableData">
        <el-table-column prop="pname" label="商品名称" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="cname" label="商品类别" align="center" min-width="80">
        </el-table-column>
        <el-table-column prop="unit_price" label="商品单价" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="quantity" label="购买数量" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="total_price" label="结算价格" align="center" min-width="40">
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
      name: "order_details",
      data() {
        return {
          id: '',
          tableData: '',
        }
      },
      methods: {
        getOrderDetails() {
          this.id = this.$route.params && this.$route.params.id;
          let data = {
            id: this.id,
          };
          const url = "http://localhost:5000/order/details";
          axios.post(url, data).then((res)=>{
            console.log(res);
            this.tableData = res.data;
          })
        }
      },
      created() {
        this.getOrderDetails()
      }
    }
</script>

<style scoped>

</style>
