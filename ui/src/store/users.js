import router from '@/router/index';

export default {
  namespaced: true,
  state: () => ({
    currentUser: null,
  }),
  getters: {
    isAuthenticated: (state) => state.currentUser !== null,
    isStaff: (state, getters) => getters.isAuthenticated && state.currentUser.is_staff,
  },
  mutations: {
    setCurrentUser(state, user) {
      state.currentUser = user;
    },
  },
  actions: {
    async fetchCurrentUser({ commit }) {
      const response = await fetch('/api/users/current/');
      const user = response.ok ? await response.json() : null;
      commit('setCurrentUser', user);
    },
    async logIn(_, fields) {
      const response = await fetch('/api/users/log-in/', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(fields),
      });
      if (!response.ok) throw new Error('Authentication failed.');
      router.go(0);
    },
    async logOut() {
      await fetch('/api/users/log-out/');
      router.go(0);
    },
  },
};
