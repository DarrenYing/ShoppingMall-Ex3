<template>
<div>
  结算界面
  <br/>
  <br/>
  <el-row>
    <el-col :span="15" :offset="3">
      <el-form ref="form" label-width="130px" size="mini">
        <div v-if="useNewAddr">
        <el-form-item label="收货人">
          <el-input v-model="form.rname"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="form.phone"></el-input>
        </el-form-item>
        <el-row>
          <el-form-item label="省份">
            <el-input v-model="form.province"></el-input>
          </el-form-item>
          <el-form-item label="城市">
            <el-input v-model="form.city"></el-input>
          </el-form-item>
        </el-row>
        <el-form-item label="详细地址">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
        </div>
        <el-form-item label="选择常用收货地址" v-if="!useNewAddr" >
          <el-select v-model="addr_id" placeholder="请选择收货地址">
            <el-option
              v-for="item in receivers"
              :key="item.addr_id"
              :label="item.address"
              :value="item.addr_id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="useNewAddr=true" v-if="!useNewAddr">新建收货地址</el-button>
          <el-button type="success" size="small" @click="useNewAddr=false" v-if="useNewAddr">返回</el-button>
        </el-form-item>
        <el-form-item label="支付方式">
          <el-radio-group v-model="form.method" size="medium">
            <el-radio border label="支付宝"></el-radio>
            <el-radio border label="微信"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item size="large">
          <el-button type="primary" @click="payCart">提交</el-button>
          <el-button @click="turnback">取消</el-button>
        </el-form-item>
      </el-form>
      <el-dialog title="提交成功！" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
          <span>订单已提交</span>
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
      name: "product_cart_payment",
      data() {
        return {
          user_id: '',
          total_price: '',

          form: {
            rname: '',
            phone: '',
            province: '',
            city: '',
            address: '',
            method: '',
          },

          addr_id: '',
          receivers: '', //已有的收货地址
          useNewAddr: false,

          dialogVisible: false,
        }
      },
      methods: {
        payCart() {
          this.user_id = this.$route.params.user_id;
          this.total_price = this.$route.params.total_price;
          if (this.useNewAddr){
            this.addr_id = '';
          }
          let data = {
            user_id: this.user_id,
            total_price: this.total_price,
            addr_id: this.addr_id,
            rname: this.form.rname,
            phone: this.form.phone,
            province: this.form.province,
            city: this.form.city,
            address: this.form.address,
            method: this.form.method,
          };
          const url = "http://localhost:5000/cart/payment";
          axios.post(url, data).then((res)=>{
            console.log(res);
            this.dialogVisible=true;
          })
        },

        turnback() {
          this.dialogVisible = false;
          //回到购物车界面，购物车清空
          this.$router.push({
            path:'cart/',
            name: 'product_cart',
          })
        },

        getReceivers() {
          this.user_id = this.$route.params.user_id;
          let data = {
            user_id: this.user_id,
          };
          const url = "http://localhost:5000/address/query";
          axios.post(url, data).then((res)=>{
            this.receivers = res.data;

            console.log(res.data[0])
          })
        },

        handleClose() {
          this.dialogVisible = false
        },
      },
      created() {
        // this.payCart();
        this.getReceivers();
      }


    }
</script>

<style scoped>

</style>
