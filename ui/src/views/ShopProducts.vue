<template>
  <v-container>
    <h1>Shop</h1>

    <ShopProductCreate v-if="isStaff" />

    <v-row>
      <v-col
        cols="12"
        sm="6"
        lg="4"
        xl="3"
        v-for="product in publishedProductList"
        :key="product.id"
      >
        <ShopProductCard :product="product" />
      </v-col>
    </v-row>
    <p v-if="publishedProductList.length === 0">No products</p>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import ShopProductCard from '@/components/ShopProductCard.vue';
import ShopProductCreate from '@/components/ShopProductCreate.vue';

export default {
  components: {
    ShopProductCard,
    ShopProductCreate,
  },
  computed: {
    ...mapGetters('shop', ['productList']),
    ...mapGetters('users', ['isStaff']),
    publishedProductList() {
      return this.productList.filter((p) => p.is_published);
    },
  },
};
</script>
