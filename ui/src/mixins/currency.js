const CURRENCY_FORMATTER = new Intl.NumberFormat(
  'en-US',
  { style: 'currency', currency: 'USD' },
);

export default {
  methods: {
    formatCurrency(amount) {
      const amountFloat = parseFloat(amount);
      return Number.isNaN(amountFloat)
        ? 'unknown'
        : CURRENCY_FORMATTER.format(amountFloat);
    },
  },
};
