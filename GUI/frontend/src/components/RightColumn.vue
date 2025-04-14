<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">
    <!-- Отображение LaTeX с помощью MathJax -->
    <div v-if="isFullFormat && texContent" ref="mathContainer" style="flex-grow: 1; overflow: auto;">
      <p v-html="renderedTex"></p>
    </div>

    <!-- Сообщение об отсутствии PDF (после попытки компиляции) -->
    <div
        v-else-if="isFullFormat && !isValidPdfUrl && compilationAttempted"
        style="flex-grow: 1; display: flex; justify-content: center; align-items: center;"
    >
      <p>PDF-файл недоступен</p>
    </div>

    <!-- Кнопки для скачивания -->
    <div style="display: flex; gap: 10px; margin-top: 10px;">
      <!-- Кнопка "Скачать .tex" -->
      <v-btn
          v-if="texUrl"
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
    texContent: {
      type: String,
      default: '', // Содержимое .tex файла (берется из latexCode)
    },
  },
  computed: {
    /**
     * Проверяет, является ли `pdfUrl` корректным:
     * - Не пустой строкой.
     * - Не совпадает с текущим URL страницы.
     */
    isValidPdfUrl() {
      if (!this.pdfUrl || this.pdfUrl.trim() === '') return false;

      // Получаем текущий URL страницы
      const currentUrl = window.location.href;

      // Проверяем, чтобы `pdfUrl` не совпадал с текущим URL
      return this.pdfUrl !== currentUrl;
    },

    /**
     * Возвращает содержимое .tex файла для отображения.
     * Удаляет команды уровня документа (\documentclass, \begin{document}, \end{document}).
     */
    renderedTex() {
      if (!this.texContent) return '';

      // Удаляем ненужные команды
      let content = this.texContent.replace(/\\documentclass\{.*?\}/g, '');
      content = content.replace(/\\usepackage\{.*?\}/g, '');
      content = content.replace(/\\begin\{document\}/g, '');
      content = content.replace(/\\end\{document\}/g, '');

      return content.trim();
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
      if (!this.texUrl) return;

      // Создаем ссылку для скачивания .tex
      const link = document.createElement('a');
      link.href = this.texUrl;
      link.download = this.texFileName; // Используем имя файла из props
      link.click();
    },
  },
  mounted() {
    // Инициализация MathJax после рендеринга
    if (window.MathJax && this.texContent) {
      window.MathJax.typesetPromise([this.$refs.mathContainer]);
    }
  },
};
</script>

<style scoped>
/* Стили для правой колонки */
iframe {
  height: calc(100% - 50px); /* Высота минус место для кнопок */
}
</style>