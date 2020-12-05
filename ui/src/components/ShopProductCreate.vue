<template>
  <v-dialog v-model="isDialogOpen" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        fab
        fixed
        bottom
        right
        color="primary"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-form ref="form" v-model="isFormValid" @submit.prevent="onSubmit">
      <v-card>
        <v-card-title>
          <span class="headline">
            New product
          </span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            outlined
            label="Name"
            v-model="fields.name"
            required
            :rules="[rules.required]"
          />
          <v-textarea
            outlined
            label="Description"
            v-model="fields.description"
            required
            :rules="[rules.required]"
          />
          <v-text-field
            outlined
            label="Price"
            v-model="fields.price"
            required
            :rules="[rules.required, rules.validPrice]"
            prefix="$"
          />
          <v-switch
            label="Publish now"
            v-model="fields.isPublished"
          />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn
            @click="isDialogOpen = false"
            text
          >
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            text
            type="submit"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import HttpClient from '@/utils/http-client';

export default {
  data: () => ({
    isDialogOpen: false,
    isFormValid: true,
    fields: {
      name: '',
      description: '',
      price: '',
      isPublished: true,
    },
    rules: {
      required: (value) => !!value || 'This field is required.',
      validPrice: (price) => /^\d+(\.\d\d)?$/.test(price) || 'Enter a valid price.',
    },
  }),
  methods: {
    async onSubmit() {
      if (!this.$refs.form.validate()) return;
      const response = await HttpClient.post('/api/shop/products/', {
        ...this.fields,
        is_published: this.fields.isPublished,
      });
      if (response.ok) {
        this.isDialogOpen = false;
        this.$store.dispatch('shop/loadProducts');
      }
    },
  },
  watch: {
    isDialogOpen(value) {
      if (value) return;
      this.$refs.form.resetValidation();
      this.$set(this, 'fields', this.$options.data().fields);
    },
  },
};
</script>
