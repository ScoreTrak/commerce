import Vue from 'vue';

export default {
  namespaced: true,
  state: () => ({
    // TODO: Remove this.
    catalog: {
      2: {
        name: 'Irrelevant banker advice',
        description: 'Banker provides advice that is not relevant to the competition.',
        price: '500',
      },
      3: {
        name: 'Console access',
        description: 'Direct console access to any machine.',
        price: '3_000',
        remaining: 1,
      },
      5: {
        name: 'Consultant advice',
        description: '',
        price: '7_500',
        remaining: 2,
      },
      8: {
        name: 'Security Engineer advice',
        description: '',
        price: '13.37',
      },
      9: {
        name: 'Server bill',
        description: 'Pay for an hour of "hosting" for your DMZ machines.',
        price: '20_000',
      },
      11: {
        name: 'Red Team immunity (15 minutes)',
        description: 'Your team will not be actively attacked for 15 minutes.',
        price: '25_000',
      },
      12: {
        name: 'Machine revert',
        description: 'Revert a machine to a pre-competition snapshot.',
        price: '30_000',
      },
    },
    productsById: {},
  }),
  getters: {
    productById: (state) => (id) => state.productsById[id],
    productList: (state) => Object.values(state.productsById),
  },
  mutations: {
    setProducts(state, products) {
      const byId = Object.fromEntries(products.map((p) => [p.id, p]));
      Vue.set(state, 'productsById', byId);
    },
  },
  actions: {
    async loadProducts({ commit }) {
      const response = await fetch('/api/shop/products/');
      const products = await response.json();
      commit('setProducts', products);
    },
  },
};
