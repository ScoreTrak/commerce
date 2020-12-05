import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

const prefersDarkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

const vuetify = new Vuetify({
  theme: {
    dark: prefersDarkModeMediaQuery.matches,
    themes: {
      light: {
        primary: '#005bbb', // UB Blue
      },
    },
  },
});

prefersDarkModeMediaQuery.addListener((e) => {
  vuetify.framework.theme.dark = e.matches;
});

export default vuetify;
