<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">

    <!-- Отображение LaTeX-кода -->
    <v-textarea
        readonly
        :value="latexCode"
        label="Результат работы бэкенда"
        outlined
        style="flex-grow: 1;"
    ></v-textarea>

    <!-- Кнопка "Compile" -->
    <v-btn
        color="success"
        @click="$emit('compile-latex')"
    >
      Compile
    </v-btn>

    <!-- Поле для ввода имени файла -->
    <v-text-field
        v-model="fileName"
        label="Имя файла"
        outlined
        placeholder="Введите имя файла"
        append-inner-icon="mdi-file-document"
        class="mt-4"
        @keydown.enter="downloadTexFile"
    ></v-text-field>

    <!-- Кнопка "Скачать .tex" -->
    <v-btn
        color="green"
        class="mb-4"
        @click="downloadTexFile"
    >
      Скачать .tex
    </v-btn>

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
  data() {
    return {
      fileName: '', // Имя файла
    };
  },
  methods: {
    downloadTexFile() {
      if (!this.latexCode) {
        alert('Нет данных для скачивания!');
        return;
      }

      const fileName = this.fileName.trim()
          ? `${this.fileName}.tex`
          : 'output.tex'; // Если имя не указано, используем "output.tex"

      // Создаем Blob с содержимым LaTeX-кода
      const blob = new Blob([this.latexCode], { type: 'text/plain' });

      // Создаем ссылку для скачивания
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = fileName;
      link.click();

      // Очищаем URL после скачивания
      URL.revokeObjectURL(link.href);
    },
  },
};
</script>

<style scoped>
/* Стили для компонента */
.v-textarea {
  height: calc(100% - 120px); /* Высота минус место для поля и кнопок */
}
</style>