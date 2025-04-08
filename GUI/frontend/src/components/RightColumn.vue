<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">
    <!-- Кнопки для скачивания -->
    <div style="display: flex; gap: 10px; margin-top: 10px;">
      <!-- Кнопка "Скачать .tex" -->
      <v-btn
          v-if="isValidTexUrl"
          color="primary"
          @click="downloadTex"
      >
        Скачать {{ texFileName }}
      </v-btn>

      <!-- Кнопка "Скачать PDF" (видна только в полном формате и при наличии PDF) -->
      <v-btn
          v-if="isFullFormat && isValidPdfUrl"
          color="primary"
          @click="downloadPdf"
      >
        Скачать {{ pdfFileName }}
      </v-btn>
    </div>
  </v-container>
</template>

<script>
export default {
  props: {
    pdfUrl: {
      type: String,
      default: '', // URL PDF-файла (может быть пустым)
    },
    texUrl: {
      type: String,
      required: true, // URL .tex файла (обязательный)
    },
    pdfFileName: {
      type: String,
      default: 'document.pdf', // Имя PDF-файла по умолчанию
    },
    texFileName: {
      type: String,
      default: 'document.tex', // Имя .tex файла по умолчанию
    },
    isFullFormat: {
      type: Boolean,
      default: false, // Упрощенный формат по умолчанию
    },
    compilationAttempted: {
      type: Boolean,
      default: false, // Флаг, указывающий, была ли попытка компиляции
    },
  },
  computed: {
    isValidPdfUrl() {
      if (!this.pdfUrl || this.pdfUrl.trim() === '') return false;

      // Получаем текущий URL страницы
      const currentUrl = window.location.href;

      // Проверяем, чтобы `pdfUrl` не совпадал с текущим URL
      return this.pdfUrl !== currentUrl;
    },

    isValidTexUrl() {
      if (!this.texUrl || this.texUrl.trim() === '') return false;

      // Получаем текущий URL страницы
      const currentUrl = window.location.href;

      // Проверяем, чтобы `texUrl` не совпадал с текущим URL и заканчивался на ".tex"
      return this.texUrl !== currentUrl && this.texUrl.endsWith('.tex');
    },
  },
  methods: {
    downloadPdf() {
      if (!this.isValidPdfUrl) return;

      // Создаем ссылку для скачивания PDF
      const link = document.createElement('a');
      link.href = this.pdfUrl;
      link.download = this.pdfFileName; // Используем имя файла из props
      link.click();
    },
    downloadTex() {
      if (!this.isValidTexUrl) return;

      // Создаем ссылку для скачивания .tex
      const link = document.createElement('a');
      link.href = this.texUrl;
      link.download = this.texFileName; // Используем имя файла из props
      link.click();
    },
  },
};
</script>

<style scoped>
/* Стили для правой колонки */
iframe {
  height: calc(100% - 50px); /* Высота минус место для кнопок */
}
</style>