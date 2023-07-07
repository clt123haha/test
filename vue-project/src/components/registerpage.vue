<template>
  <div class="register" ref="father">
<!--    <div id="Verification" v-text="Verification" @click="randomNum"></div>-->
    <img id="Verification" :src="Verification" alt="Base64 Image" @click="randomNum">

    <span id="passwordjudge">两次输入不一致</span>
    <van-nav-bar title="注册" left-arrow @click-left="onClickLeft" />
    <van-field
      v-model="phone"
      label="手机号"
      placeholder="请输入手机号"
      required
      autocompleted="off"
      clearable
      @blur="phonejudge1()"
      ref="phone"
    />
    <van-field
      v-model="password"
      type="password"
      label="密码"
      placeholder="请输入密码"
      required
      autocompleted="off"
      clearable
    />
    <van-field
        v-model="password2"
        type="password"
        label="密码"
        placeholder="请再次输入密码"
        required
        autocompleted="off"
        @blur="passwordjudge1()"
        clearable
    />

    <van-field
      v-model="VerificationCode"
      label="验证码"
      placeholder="请输入验证码"
      autocomplete="off"
      required
      @blur="codejudge1()"
    />
    <van-button type="primary" size="large" @click="showPopup()">下一步</van-button>
    <van-popup v-model="show">
      <p :class="{
        mess : true,
      }" :style="messStyle">{{mess}}</p>
    </van-popup>
  </div>
</template>
<script>
export default {
  methods: {
    data() {
      return {
        messStyle:"#58bc58"
      };
    },
    onClickLeft() {
      window.location.hash = "#/";
      console.log(window.location.hash);
    },
    async randomNum() {
      let codeData = await this.$axios({
        method: "get",
        url: "http://localhost:5000/user/get_Indonesia",
      });
      this.Verification = "data:image/jpg;base64,"+codeData.data;
    },
    //判断手机号
    phonejudge1() {
      let reg = /^1[3-9]\d{9}$/;
      this.phonejudge = reg.test(this.phone);
      let a = this.$refs.phone.$el;
      let b = a.querySelector("input");
      if (!this.phonejudge) {
        //格式不正确
        b.style.color = "red";
      } else {
        b.style.color = "#000";
      }
    },
    passwordjudge1() {
      if (this.password != this.password2) {
        this.$refs.father.querySelector("#passwordjudge").style.display =
          "block";
      } else {
        this.$refs.father.querySelector("#passwordjudge").style.display =
          "none";
        this.passwordjudge = true;
      }
    },
    codejudge1() {
      if (this.VerificationCode == this.Verification) {
        this.codejudge = true;
      }
    },
    //单击下一步
    async showPopup() {
      let repData = await this.$axios({
        method: "post",
        url: "http://localhost:5000/user/register",
        data: {
          phone: this.phone,
          password: this.password,
          checkpassword: this.password2,
          Indonesia: this.VerificationCode,
        }
      });
      this.mess = repData.data.message;
      this.messStyle = repData.data.code == 200?'color:#58bc58':'color:red'
      this.show = true;
    }
  },
  data() {
    return {
      password: "",
      Verification: "",
      show: false,
      //输入框
      phone: "",
      password2: "",
      VerificationCode: "",
      phonejudge: "",
      passwordjudge: "",
      codejudge: "",
      //注册是否成功内容
      mess: "注册失败"
    };
  },
  created() {
    this.randomNum();
    // console.log(this);
  },
  mounted() {}
};
</script>
<style scoped>
.register {
  background: #efeff4;
  height: 100%;
}
.register .van-nav-bar {
  background: #3993cf;
}
.register .van-nav-bar__title {
  color: #fff;
}
.register .van-nav-bar__arrow {
  font-size: 20px;
  color: #fff;
}
.register .van-button--large {
  width: 90%;
  margin-left: 0.5rem;
  margin-top: 0.6rem;
  background-color: #3993cf;
  border-radius: 0.1rem;
  height: 1.4rem;
  line-height: 1.4rem;
}

.register #Verification {
  width: 3rem;
  height: 1.3rem;
  position: absolute;
  background: #3993cf;
  top: 5.6rem;
  right: 0.2rem;
  z-index: 999;
  line-height: 1.3rem;
  text-align: center;
  font-size: 18px;
  color: white;
}
.register #passwordjudge {
  color: red;
  position: absolute;
  top: 4.5rem;
  right: 0.1rem;
  z-index: 999;
  display: none;
}
.register .mess {
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
.register .mess.err {
  color: red;
}
</style>


