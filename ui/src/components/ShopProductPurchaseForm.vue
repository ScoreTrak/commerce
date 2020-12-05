<template>
  <v-form @submit.prevent="onSubmit">
    <v-card>
      <v-card-title>
        <span class="headline">Purchase "{{ product.name }}"</span>
      </v-card-title>
      <v-card-text>
        <v-alert :type="error === 'Success' ? 'success' : 'error'" v-if="error">
          {{ error }}
        </v-alert>
        <BankAccountPicker v-model="account" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" text type="submit" :disabled="account === null">
          Purchase
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import BankAccountPicker from '@/components/BankAccountPicker.vue';
import HttpClient from '@/utils/http-client';

export default {
  components: {
    BankAccountPicker,
  },
  data: () => ({
    account: null,
    error: '',
    rules: {
      required: (value) => !!value || 'This field is required.',
    },
  }),
  methods: {
    async onSubmit() {
      this.error = '';
      const response = await HttpClient.post('/api/shop/orders/', {
        account: this.account.id,
        product: this.product.id,
      });
      if (!response.ok) {
        const error = await response.json();
        console.log(error);
        if (error instanceof Array) {
          this.error = error.join('. ');
        }
        return;
      }
      this.error = 'Success';
    },
  },
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
};
</script>
