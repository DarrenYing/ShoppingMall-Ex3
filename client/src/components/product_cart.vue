<template>
<div>
  购物车
  <div>
  <br/>
  <el-container>
    <el-main>
      <el-table :data="tableData">
        <el-table-column type="expand">
          <template slot-scope="scope">
            <el-table :data="scope.row.items">
              <el-table-column prop="pname" label="商品名称" align="center" min-width="50">
              </el-table-column>
              <el-table-column prop="cname" label="商品类别" align="center" min-width="50">
              </el-table-column>
              <el-table-column prop="unit_price" label="单价" align="center" min-width="50">
              </el-table-column>
              <el-table-column label="数量" align="center" min-width="60">
                <template slot-scope="scope">
                  <el-button type="warning" @click="subQuantity(scope)" icon="el-icon-minus" circle size="mini"></el-button>
                  <span>{{scope.row.quantity}}</span>
                  <el-button type="success" @click="addQuantity(scope)" icon="el-icon-plus" circle size="mini"></el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="cart_id" label="购物车ID" align="center" min-width="40">
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" align="center" min-width="80">
        </el-table-column>
        <el-table-column label="结算金额" align="center" min-width="40">
          <template slot-scope="scope">
            <span>{{ total_price }}</span>
          </template>
        </el-table-column>
<!--        <el-table-column label="操作" align="center">-->
<!--          <template slot-scope="scope">-->
<!--            <el-button type="danger" size="mini" @click="delCart(scope.row)">删除</el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
      </el-table>
      <br/>
      <el-button-group>
        <el-button type="success" size="mini" @click="submitCart()">结算</el-button>
        <el-button type="danger" size="mini" @click="dialogVisible=true">清空购物车</el-button>
      </el-button-group>
      <el-dialog title="确定清空购物车？" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
          <span>即将清空购物车</span>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="danger" @click="emptyCart">确 定</el-button>
          </span>
      </el-dialog>
    </el-main>
  </el-container>
  </div>
</div>
</template>

<script>
    import axios from 'axios'
    export default {
      name: "product_cart",
      data() {
        return {
          tableData: '',
          username: '',
          user_id: '',
          items: [],
          dialogVisible: false,
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
          const url = "http://localhost:5000/product/cart";
          axios.post(url, data).then((res)=>{
            this.tableData = res.data;
            this.items = this.tableData[0].items;
            // console.log(res.data[0].user_id)
            this.user_id = res.data[0].user_id;
          })
        },

        submitCart() {
          this.$router.push({
            path:'cart/payment',
            name: 'product_cart_payment',
            params: {
              user_id: this.user_id,
              total_price: this.total_price,
            }
          })
        },

        subQuantity(scope) {
          scope.row.quantity--;
          var that = this;
          if(scope.row.quantity<=0){
            // console.log(that.tableData[0].items)
            that.updateCart(scope.row.pname, 0);
            that.tableData[0].items.splice(that.tableData[0].items.indexOf(scope.row), 1)
          }
          else{
            that.updateCart(scope.row.pname, scope.row.quantity);
          }
        },
        addQuantity(scope) {
          scope.row.quantity++;
          this.updateCart(scope.row.pname, scope.row.quantity);
        },
        updateCart(pname, quantity) {
          let data = {
            pname: pname,
            quantity: quantity,
          };
          const url = "http://localhost:5000/product/cart/update";
          axios.post(url, data).then((res)=>{
            console.log(res)
          })
        },
        handleClose() {
          this.dialogVisible = false
        },
        emptyCart(){
          this.items = []
        },
      },
      computed: {
        total_price: function() {
          let totalCost = 0;
          for(var index in this.items){
            let item = this.items[index];
            // console.log(item.quantity);
            totalCost += item.unit_price * item.quantity;
          }
          console.log(totalCost);
          return totalCost
        }
      },

      created() {
        this.onSubmit();
      }
    }
</script>

<style scoped>
  .el-button+.el-button {
    margin-left: 10px;
  }
</style>
