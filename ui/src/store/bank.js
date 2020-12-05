import Vue from 'vue';

export default {
  namespaced: true,
  state: () => ({
    accountsById: {},
  }),
  getters: {
    accountById: (state) => (id) => state.accountsById[id],
    accountList: (state) => Object.values(state.accountsById),
  },
  mutations: {
    setAccount(state, account) {
      Vue.set(state.accountsById, account.id, account);
    },
    setAccounts(state, accounts) {
      const byId = Object.fromEntries(accounts.map((a) => [a.id, a]));
      Vue.set(state, 'accountsById', byId);
    },
  },
  actions: {
    async fetchAccount({ commit }, accountId) {
      const response = await fetch(`/api/bank/accounts/${accountId}/`);
      if (!response.ok) {
        console.log('Failed to load bank account.');
        return;
      }
      const account = await response.json();
      commit('setAccount', account);
    },
    async fetchAccounts({ commit }) {
      const response = await fetch('/api/bank/accounts/');
      if (!response.ok) {
        console.log('Failed to load bank accounts.');
        return;
      }
      const accounts = await response.json();
      commit('setAccounts', accounts);
    },
  },
};
