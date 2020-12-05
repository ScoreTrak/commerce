<template>
  <v-app dark>
    <AppBar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';

export default {
  components: {
    AppBar,
  },
  created() {
    this.$store.dispatch('users/fetchCurrentUser');
  },
};
</script>
