<template>

  <div class="sign">

    <van-nav-bar title="登陆" left-arrow @click-left="onClickLeft" />

    <van-cell-group>
      <van-field v-model="account" clearable label="账号" placeholder="请输入账号" autocomplete="off" />
      <van-field
          v-model="password"
          type="password"
          label="密码"
          placeholder="请输入密码"
          autocomplete="off"
      />
      <van-field v-model="Indonesia" clearable label="验证码" placeholder="请输入验证码" autocomplete="off" />
      <img id="Verification" :src="Verification" alt="Base64 Image" @click="randomNum">

    </van-cell-group>
    <van-button type="info" size="large" @click="sign1()">登陆</van-button>
    <div class="messageof">
      <a href="#/register" class="register">快速注册</a>
      <a href style="color:#aaa">找回密码</a>
    </div>
    <van-divider
        :style="{ color: '#aaa', borderColor: '#aaa', padding: '0 16px',marginTop:'6rem' }"
    >其他平台登陆</van-divider>

    <van-popup v-model="show">
      <p :class="{
        mess : true,
      }" :style="messStyle">{{mess}}</p>
    </van-popup>
  </div>


</template>
<script>
export default {
  data() {
    return {
      mess:"",
      messStyle:"#58bc58",
      show:false,
      account: "",
      password: "",
      Indonesia:"",
      Verification:"",
      message: '',
      receivedMessage: '',
      socket:null
    };
  },
  created() {
    this.randomNum()
  },
  methods: {
    getCookie(key) {//获取cookie值
        var cookies = document.cookie;//name=malin; pwd=123456
        var arr = cookies.split('; ');//['name=malin','pwd=123456']
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=');//['name','malin'
          if (key == arr2[0]) {
            return arr2[1];
          }
        };
    },
    async randomNum() {
      let codeData = await this.$axios({
        method: "get",
        url: "http://localhost:5000/user/get_Indonesia",
      });
      this.Verification = "data:image/jpg;base64,"+codeData.data;
    },
    onClickLeft() {
      // router.push({ name: "home" });
      window.location.hash = "#/";
      console.log(window.location.hash);
    },
    async sign1() {
      let repData = await this.$axios({
        method: "post",
        url: "http://localhost:5000/user/login/password",
        data: {
          account: this.account,
          password: this.password,
          Indonesia: this.Indonesia
        }
      });
      //登录成功
      if(repData.data.code == 200){
        this.messStyle = 'color:#58bc58'
        this.$router.push({path: "footer/home"});
        document.cookie = "username" + "=" + this.account + ";path=/";
        document.cookie = "password" + "=" + this.password + ";path=/";
        document.cookie = "id" + "=" + repData.data.data.id + ";path=/";
      }else{
        //登录失败
        this.messStyle = 'color:red'
      }
      this.mess = repData.data.message;
      this.show = true;
    }
  },
  sockets:{
    connect: function(){
      console.log('socket 连接成功')
      const data = {
        socketid:this.$socket.id,
        userid:this.getCookie('id')
      }
      console.log('更新用户连接信息',data)
      this.$socket.emit('init',data);
    },
    message: function(val){
      console.log('message:'+val);
    },
    init: function(val){
      console.log('init:'+val);
    },
    sendmessage: function(val){
      console.log('sendmessage:'+val);
    }
  },

};
</script>
<style scoped>
.sign {
  background: #efeff4;
  height: 100%;
}
.sign .van-nav-bar {
  background: #3993cf;
}
.sign .van-nav-bar__title {
  color: #fff;
}
.sign .van-nav-bar__arrow {
  font-size: 20px;
  color: #fff;
}
.sign .van-button--large {
  width: 90%;
  margin-left: 0.5rem;
  margin-top: 0.6rem;
  background-color: #3993cf;
  border-radius: 0.1rem;
  height: 1.4rem;
  line-height: 1.4rem;
}
.sign .messageof {
  width: 100%;
  text-align: center;
  margin-top: 1rem;
}
.sign .messageof .register {
  margin-right: 1rem;
  color: #3993cf;
  padding-right: 1rem;
  border-right: 1px solid #aaa;
}
.sign #Verification {
  width: 3rem;
  height: 1.3rem;
  position: absolute;
  background: #3993cf;
  top: 2.8rem;
  right: 0.2rem;
  z-index: 999;
  line-height: 1.3rem;
  text-align: center;
  font-size: 18px;
  color: white;
}
.sign .mess {
  color: #58bc58;
  font-size: 0.5rem;
  display: block;
  text-align: center;
  margin: 20px;
  /*line-height: 2rem;*/
  /*color: #58bc58;*/
  /*font-size: 0.5rem;*/
  /*display: block;*/
  /*width: 100%;*/
  /*height: 2rem;*/
  /*text-align: center;*/
}
.sign .mess.err {
  color: red;
}

</style>


