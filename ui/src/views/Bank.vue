<template>
  <v-container>
    <h1>Bank</h1>

    <BankAccountPicker v-model="account" />
    <template v-if="account">
      <!--<div>Last updated: {{ Date() }}</div>-->
      <BankAccountSummary
        :balance="account.balance"
        :pastHourDeposits="account.deposits_in_past_hour"
        :pastHourWithdrawals="account.withdrawals_in_past_hour"
      />
      <BankAccountActivity :transactions="account.transactions" />
    </template>
  </v-container>
</template>

<script>
import BankAccountActivity from '@/components/BankAccountActivity.vue';
import BankAccountPicker from '@/components/BankAccountPicker.vue';
import BankAccountSummary from '@/components/BankAccountSummary.vue';

export default {
  components: {
    BankAccountActivity,
    BankAccountPicker,
    BankAccountSummary,
  },
  data: () => ({
    account: null,
  }),
};
</script>
