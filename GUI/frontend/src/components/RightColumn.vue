<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">
    <!-- Отображение PDF -->
    <iframe
        v-if="pdfUrl"
        :src="pdfUrl"
        style="flex-grow: 1; border: none;"
        width="100%"
        frameborder="0"
    ></iframe>

    <!-- Кнопка "Скачать PDF" -->
    <v-btn
        v-if="pdfUrl"
        color="primary"
        class="mt-2"
        @click="downloadPdf"
    >
      Скачать PDF
    </v-btn>
  </v-container>
</template>

<script>
export default {
  props: {
    pdfUrl: {
      type: String,
      default: '',
    },
  },
  methods: {
    downloadPdf() {
      if (!this.pdfUrl) return;

      // Создаем ссылку для скачивания
      const link = document.createElement('a');
      link.href = this.pdfUrl;
      link.download = 'output.pdf'; // Имя файла
      link.click();
    },
  },
};
</script>

<style scoped>
/* Стили для правой колонки */
iframe {
  height: calc(100% - 50px); /* Высота минус место для кнопки */
}
</style>