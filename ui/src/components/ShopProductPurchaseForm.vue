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
        <v-text-field
          v-for="question in product.questions"
          :key="question.id"
          :label="question.text"
          v-model="challenges[question.id]"
          filled
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          :disabled="!isFormValid"
          :loading="isRequestInProgress"
          color="primary"
          text
          type="submit"
        >
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
  computed: {
    isFormValid() {
      return (
        this.account !== null
        && Object.values(this.challenges).filter((a) => a.length > 0).length
            === this.product.questions.length
      );
    },
  },
  data: () => ({
    account: null,
    challenges: {},
    error: '',
    isRequestInProgress: false,
    rules: {
      required: (value) => !!value || 'This field is required.',
    },
  }),
  methods: {
    async onSubmit() {
      this.error = '';
      this.isRequestInProgress = true;
      const response = await HttpClient.post('/api/shop/orders/', {
        account: this.account.id,
        product: this.product.id,
        challenges: Object.entries(this.challenges).map(
          ([question, answer]) => ({ question, answer }),
        ),
      });
      if (!response.ok) {
        const error = await response.json();
        console.log(error);
        if (error instanceof Array) {
          this.error = error.join('. ');
        }
        this.isRequestInProgress = false;
        return;
      }

      // TODO: Better success handling!
      this.error = 'Success';
      setTimeout(() => {
        this.$emit('success');
        this.isRequestInProgress = false;

        this.error = '';
        // this.account = null;
        this.challenges = {};
      }, 3000);
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
