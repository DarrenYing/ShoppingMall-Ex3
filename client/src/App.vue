<template>
  <div id="app">
    <index v-if="showAside"></index>
    <router-view v-if="!showAside"></router-view>
  </div>
</template>

<script>
import index from '@/components/index'

export default {
  name: 'App',
  data() {
    return {
      showAside: false,
    }
  },
  components: {
    index,
  },
  watch: {
    '$route' () {
      this.showAside = (this.$route.name !== 'login' && this.$route.name !== 'register')
    }
  },

  created() {
    console.log(this.$route.name);
    this.showAside = (this.$route.name !== 'login' && this.$route.name !== 'register')
  }


}
</script>

<style>

</style>
