<template>
  <div class="home">
    <div>
      <img src="./UserHeader.png" alt="logo" id="pic">
    </div>
    <ibanner></ibanner>
  </div>
</template>

<script>
// @ is an alias to /src
import ibanner from "@/components/ibanner.vue";
// import HelloWorld from "@/components/HelloWorld.vue";
export default {
  name: "home",
  components: {
    ibanner
  }
};
</script>
<style>
#pic{
  width: 97%;
}
</style>

