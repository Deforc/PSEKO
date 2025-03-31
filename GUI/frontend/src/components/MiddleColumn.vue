<template>
  <v-container>
    <v-textarea readonly :value="latexCode" label="Результат работы бэкенда"></v-textarea>
    <v-btn @click="$emit('compile-latex')">Compile</v-btn>
  </v-container>
</template>

<script>
export default {
  props: {
    latexCode: {
      type: String,
      default: '',
    },
  },
};
</script>