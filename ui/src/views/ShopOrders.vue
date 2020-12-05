<template>
  <v-container>
    <h1>Orders</h1>

    <v-data-table
      :headers="tableHeaders"
      :items="tableItems"
      :loading="isLoading"
    >
      <template v-slot:top>
        <v-switch v-model="isPendingOnly" label="Only show pending orders" />
      </template>
      <template v-slot:item.time="{ item }">
        <small>{{ formatDate(item.sale.created_at) }}</small>
        <br>
        {{ formatTime(item.sale.created_at) }}
      </template>
      <template v-slot:item.product="{ item }">
        <router-link :to="{ name: 'shop-product', params: { productId: item.product.id }}">
          {{ item.product.name }}
        </router-link>
      </template>
      <template v-slot:item.actions="{ item: order }">
        <v-btn
          v-if="order.completed_at === null"
          @click="openDialog(order, 'complete')"
          outlined
        >
          Completed
        </v-btn>
        <v-btn
          v-if="order.refund === null"
          @click="openDialog(order, 'refund')"
          outlined
        >
          Refund
        </v-btn>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog.isOpen" max-width="600px">
      <v-card>
        <v-card-title class="headline">
          Are you sure you want to {{ dialog.action }} this order?
        </v-card-title>
        <v-card-actions>
          <v-btn text @click="dialog.isOpen = false">Cancel</v-btn>
          <v-spacer />
          <v-btn text color="primary" @click="performDialogAction">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import HttpClient from '@/utils/http-client';

export default {
  created() {
    this.isLoading = true;
    this.fetchOrders();
  },
  computed: {
    ...mapGetters('users', ['isStaff']),
    tableHeaders() {
      const headers = [
        { text: 'Time', value: 'time' },
        { text: 'Account', value: 'sale.source', sortable: false },
        { text: 'Product', value: 'product', sortable: false },
        { text: 'Status', value: 'status', sortable: false },
      ];
      const staffHeaders = [
        ...headers,
        { text: 'Actions', value: 'actions', sortable: false },
      ];
      return this.isStaff ? staffHeaders : headers;
    },
    tableItems() {
      return (this.orders
        .map((o) => ({ ...o, status: this.orderStatus(o) }))
        .filter((o) => !this.isPendingOnly || o.status === 'Pending')
      );
    },
  },
  data: () => ({
    dialog: {
      isOpen: false,
      order: null,
      action: null,
    },
    isLoading: false,
    isPendingOnly: false,
    orders: [],
  }),
  methods: {
    async fetchOrders() {
      const response = await fetch('/api/shop/orders/');
      if (!response.ok) {
        console.log('Could not fetch orders.');
        this.orders = [];
      } else {
        this.orders = await response.json();
      }
      this.isLoading = false;
    },
    formatDate(dateTime) {
      return new Date(dateTime).toLocaleDateString();
    },
    formatTime(dateTime) {
      return new Date(dateTime).toLocaleTimeString();
    },
    orderStatus(order) {
      if (order.refund !== null) return 'Refunded';
      if (order.completed_at !== null) return 'Completed';
      return 'Pending';
    },
    openDialog(order, action) {
      this.dialog.isOpen = true;
      this.dialog.action = action;
      this.dialog.order = order;
    },
    async performDialogAction() {
      this.isLoading = true;
      this.dialog.isOpen = false;
      await HttpClient.post(`/api/shop/orders/${this.dialog.order.id}/${this.dialog.action}/`);
      this.fetchOrders();
    },
  },
};
</script>
