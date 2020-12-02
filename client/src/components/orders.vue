<template>
<div>
  订单信息
  <div>
  <br/>
  <el-container>
    <el-main>
      <el-table :data="tableData">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="收货地址">
                <span>{{ props.row.addr }}</span>
              </el-form-item>
              <el-form-item label="发货时间">
                <span>{{ props.row.send_time }}</span>
              </el-form-item>
              <el-form-item label="付款时间">
                <span>{{ props.row.pay_time }}</span>
              </el-form-item>
              <el-form-item label="结算时间">
                <span>{{ props.row.finish_time }}</span>
              </el-form-item>
              <el-form-item label="创建时间">
                <span>{{ props.row.create_time }}</span>
              </el-form-item>
              <el-form-item label="支付方式">
                <span>{{ props.row.payment_method }}</span>
              </el-form-item>
              <el-form-item label="支付流水号">
                <span>{{ props.row.payment_no }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="order_id" label="订单ID" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="order_no" label="订单号" align="center" min-width="80">
        </el-table-column>
        <el-table-column prop="payment" label="结算金额" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="carriage" label="运费" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="status" label="订单状态" align="center" min-width="40">
        </el-table-column>
        <el-table-column label="操作" align="center" v-if="isManager">
          <template slot-scope="scope">
<!--            <el-button type="primary" size="mini" @click="addRecord">添加</el-button>-->
<!--            <el-button type="primary" size="mini" @click="updateRecord">修改</el-button>-->
            <el-button type="primary" size="mini" @click="orderDetails(scope.row)">详情</el-button>
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
      name: "orders",
      data() {
        return {
          order_id: '',
          username: '',
          tableData: '',
          isManager: true,
        }
      },
      methods: {
        onSubmit() {
          let user = sessionStorage.getItem('user');
          if (user) {
            this.username = user;
          }
          let data = {
            username: this.username
          };
          const url = "http://localhost:5000/order/order";
          axios.post(url, data).then((res)=>{
            this.tableData = res.data
          })
        },
        orderDetails(row) {
          this.$router.push({path:'details/'+row.order_no})
        },
      },

      created() {
        this.onSubmit()
      }

    }
</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
