<template>
  <section>
    <h2>Account summary</h2>

    <v-sheet rounded elevation="1">
      <v-container>
        <v-row>
          <v-col>
            <h3>Balance</h3>
            <span>{{ formatCurrency(balance) }}</span>
          </v-col>
          <v-spacer />
          <v-col>
            <h3>Deposits this hour</h3>
            <span>{{ formatCurrency(pastHourDeposits) }}</span>
          </v-col>
          <v-col>
            <h3>Withdrawals this hour</h3>
            <span>{{ formatCurrency(pastHourWithdrawals) }}</span>
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>
  </section>
</template>

<script>
import currencyMixin from '@/mixins/currency';

export default {
  mixins: [currencyMixin],
  props: {
    balance: {
      type: String,
      required: true,
    },
    pastHourDeposits: String,
    pastHourWithdrawals: String,
  },
};
</script>
