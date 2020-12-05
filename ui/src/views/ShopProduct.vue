<template>
  <v-container>
    <h1>Shop</h1>

    <!-- TODO: Edit for staff? -->

    <ShopProductCard v-if="product" :product="product" />
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import ShopProductCard from '@/components/ShopProductCard.vue';

export default {
  components: {
    ShopProductCard,
  },
  computed: {
    ...mapGetters('shop', ['productById']),
    product() {
      return this.productById(this.$route.params.productId);
    },
  },
};
</script>
