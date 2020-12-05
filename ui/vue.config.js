module.exports = {
  devServer: {
    progress: false,
    proxy: 'http://backend:8000',
  },
  transpileDependencies: [
    'vuetify',
  ],
};
