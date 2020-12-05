<template>
  <v-form @submit.prevent="logIn">
    <v-card>
      <v-card-title>
        <span class="headline">Log in</span>
      </v-card-title>
      <v-card-text>
        <v-alert type="error" v-if="error">
          {{ error }}
        </v-alert>
        <v-text-field
          label="Username"
          v-model="fields.username"
          :rules="[rules.required]"
        />
        <v-text-field
          label="Password"
          v-model="fields.password"
          :rules="[rules.required]"
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" text type="submit">
          Log in
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
export default {
  data: () => ({
    error: '',
    fields: {
      username: '',
      password: '',
    },
    rules: {
      required: (value) => !!value || 'This field is required.',
    },
    showPassword: false,
  }),
  methods: {
    async logIn() {
      this.error = '';
      try {
        await this.$store.dispatch('users/logIn', this.fields);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
