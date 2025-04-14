<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">
    <!-- Отображение PDF -->
    <div
        v-if="isFullFormat && isValidPdfUrl"
        ref="pdfContainer"
        style="flex-grow: 1; overflow: auto; position: relative;"
    >
      <!-- Контейнер для страниц PDF -->
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
import { getDocument } from 'pdfjs-dist';
import { GlobalWorkerOptions } from 'pdfjs-dist';

// Указываем путь к worker через new URL
GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.mjs',
  import.meta.url
).toString();
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
      const currentUrl = window.location.href;
      return this.pdfUrl !== currentUrl;
    },
  },
  methods: {
    async renderPdf(url) {
      try {
        // Загрузка PDF-документа
        const loadingTask = getDocument(url);
        const pdf = await loadingTask.promise;

        // Очистка контейнера
        this.$refs.pdfContainer.innerHTML = '';

        // Отображение всех страниц PDF
        for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
          const page = await pdf.getPage(pageNumber);
          const viewport = page.getViewport({ scale: 1.5 });

          // Создание canvas для каждой страницы
          const canvas = document.createElement('canvas');
          const context = canvas.getContext('2d');
          canvas.width = viewport.width;
          canvas.height = viewport.height;

          // Добавление canvas в контейнер
          this.$refs.pdfContainer.appendChild(canvas);

          // Рендеринг страницы
          await page.render({
            canvasContext: context,
            viewport: viewport,
          }).promise;
        }
      } catch (error) {
        console.error('Ошибка при загрузке PDF:', error);
      }
    },
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
  watch: {
    pdfUrl(newVal) {
      if (newVal && this.isFullFormat && this.isValidPdfUrl) {
        this.renderPdf(newVal); // Загружаем и отображаем PDF
      }
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