<template>
  <section>
    <h2>Account activity</h2>
    <v-simple-table v-if="transactions.length > 0">
      <thead>
        <tr>
          <th>Time</th>
          <th>Amount</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.id">
          <td>
            <small>{{ formatDate(transaction.created_at) }}</small>
            <br>
            {{ formatTime(transaction.created_at) }}
          </td>
          <!-- TODO: Right-align -->
          <td>{{ formatCurrency(transaction.amount) }}</td>
          <td>{{ transaction.description }}</td>
        </tr>
      </tbody>
    </v-simple-table>
    <p v-else>No activity</p>
  </section>
</template>

<script>
import currencyMixin from '@/mixins/currency';

export default {
  methods: {
    formatDate(dateTime) {
      return new Date(dateTime).toLocaleDateString();
    },
    formatTime(dateTime) {
      return new Date(dateTime).toLocaleTimeString();
    },
  },
  mixins: [currencyMixin],
  props: {
    transactions: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
