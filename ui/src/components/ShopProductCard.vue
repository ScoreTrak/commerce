<template>
  <v-card>
    <v-img v-if="product.image" :src="product.image" height="250px" />
    <v-card-title>{{ product.name }}</v-card-title>
    <!--
    <v-card-subtitle v-if="remaining">
      Remaining: {{ remaining }}
    </v-card-subtitle>
    -->
    <v-card-text>{{ product.description }}</v-card-text>
    <v-divider />
    <v-card-actions>
      <v-card-text>Price: {{ formatCurrency(product.price) }}</v-card-text>
      <v-spacer />
      <v-dialog v-model="isFormVisible" max-width="500px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-bind="attrs"
            v-on="on"
            text
          >
            Buy
          </v-btn>
        </template>
        <ShopProductPurchaseForm
          :product="product"
          @success="isFormVisible = false"
        />
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
import currencyMixin from '@/mixins/currency';
import ShopProductPurchaseForm from '@/components/ShopProductPurchaseForm.vue';

export default {
  components: {
    ShopProductPurchaseForm,
  },
  data: () => ({
    isFormVisible: false,
  }),
  mixins: [currencyMixin],
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
};
</script>
