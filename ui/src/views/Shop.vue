<template>
  <router-view />
</template>

<script>
export default {
  created() {
    this.$store.dispatch('shop/loadProducts');
  },
};
</script>
