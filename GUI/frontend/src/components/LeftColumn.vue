<template>
  <v-container>
    <v-textarea v-model="inputText" label="Введите текст"></v-textarea>
    <v-btn @click="sendToBackend">Отправить на бэкэнд</v-btn>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputText: '',
    };
  },
  methods: {
    async sendToBackend() {
      try {
        const response = await axios.post('/api/latex', { text: this.inputText });
        this.$emit('update-latex', response.data.latexCode);
      } catch (error) {
        console.error('Ошибка при отправке данных:', error);
      }
    },
  },
};
</script>