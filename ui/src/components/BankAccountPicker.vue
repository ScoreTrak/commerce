<template>
  <v-select
    label="Accounts"
    v-model="selectedId"
    :items="accountList"
    item-text="name"
    item-value="id"
    no-data-text="No accounts"
    filled
  />
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters('bank', ['accountById', 'accountList']),
    account() {
      return this.accountById(this.selectedId);
    },
  },
  created() {
    this.$store.dispatch('bank/fetchAccounts');
    this.selectOnlyAccount();
  },
  data: () => ({
    selectedId: null,
  }),
  methods: {
    selectOnlyAccount() {
      if (this.accountList.length !== 1) return;
      this.selectedId = this.accountList[0].id;
    },
  },
  props: {
    value: Object,
  },
  watch: {
    account() {
      this.$emit('input', this.account);
    },
    accountList() {
      this.selectOnlyAccount();
    },
    selectedId() {
      this.$store.dispatch('bank/fetchAccount', this.selectedId);
    },
  },
};
</script>
