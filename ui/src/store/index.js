import Vue from 'vue';
import Vuex from 'vuex';

import bank from '@/store/bank';
import shop from '@/store/shop';
import users from '@/store/users';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    bank,
    shop,
    users,
  },
});
