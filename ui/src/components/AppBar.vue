<template>
  <div>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="isDrawerOpen = !isDrawerOpen" />
      <div class="d-flex align-center">
        <router-link :to="{ name: 'home' }">
          <v-img
            alt="logo"
            class="shrink mt-1"
            contain
            min-width="100"
            src="https://ubnetdef.org/img/logo.png"
            width="100"
          />
        </router-link>
      </div>

      <v-spacer></v-spacer>

      <!--
      <div class="d-flex align-center">
        <v-switch
          v-model="$vuetify.theme.dark"
          inset
          hide-details
          label="Dark theme"
          color="black"
        />
      </div>
      -->

      <v-btn text v-if="isAuthenticated" @click="logOut">
        Log out
      </v-btn>
      <v-dialog v-else max-width="600px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on" text>
            Log in
          </v-btn>
        </template>
        <LogInForm />
      </v-dialog>
    </v-app-bar>
    <v-navigation-drawer v-model="isDrawerOpen" app bottom temporary>
      <v-list nav>
        <v-subheader>Bank</v-subheader>

        <v-list-item link :to="{ name: 'bank' }">
          <v-list-item-title>Accounts</v-list-item-title>
        </v-list-item>

        <v-divider />

        <v-subheader>Shop</v-subheader>

        <v-list-item link :to="{ name: 'shop-products' }">
          <v-list-item-title>Products</v-list-item-title>
        </v-list-item>

        <v-list-item link :to="{ name: 'shop-orders' }">
          <v-list-item-title>Orders</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import LogInForm from '@/components/LogInForm.vue';

export default {
  components: {
    LogInForm,
  },
  computed: {
    ...mapGetters('users', ['isAuthenticated']),
  },
  data: () => ({
    isDrawerOpen: false,
  }),
  methods: {
    ...mapActions('users', ['logOut']),
  },
};
</script>
