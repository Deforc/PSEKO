<template>
  <v-container style="height: 100%; display: flex; flex-direction: column;">
    <!-- Toggle "Полный формат" -->
    <div class="toggle-container">
      <span class="toggle-label">Упрощенный формат</span>
      <v-switch
          v-model="isFullFormat"
          color="primary"
          inset
          hide-details
      ></v-switch>
      <span class="toggle-label">Полный формат</span>
    </div>

    <!-- Поле для ввода имени файла -->
    <div>
      <v-textarea
          v-model="fileName"
          label="Имя файла (.tex)"
          outlined
          rows="1"
          auto-grow
          dense
          placeholder="Введите имя файла"
          append-inner-icon="mdi-file-document"
          @keydown.enter="downloadTexFile"
          class="compact-textarea mb-4"
      ></v-textarea>
    </div>


    <!-- Отображение LaTeX-кода -->
    <v-textarea
        readonly
        :value="displayedLatexCode"
        label="Результат работы бэкенда"
        outlined
        style="flex-grow: 1;"
    ></v-textarea>

    <!-- Кнопка "Compile" -->
    <v-btn
        color="success"
        @click="compileLatex"
    >
      Compile
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
      isFullFormat: false, // Флаг для toggle
      fileName: '', // Имя файла
    };
  },
  computed: {
    displayedLatexCode() {
      if (this.isFullFormat || !this.latexCode) {
        return this.latexCode; // Возвращаем полный код, если toggle активен
      }

      // Оставляем только строки с "Program" и нумерованными строками
      const lines = this.latexCode.split('\n');
      const filteredLines = lines.filter((line) => {
        return line.includes('Program') || /^\d+:/.test(line.trim());
      });

      return filteredLines.join('\n'); // Возвращаем отфильтрованный код
    },
  },
  methods: {
    compileLatex() {
      const requestData = {
        filename: this.fileName.trim() || 'output', // Имя файла по умолчанию
        latexCode: this.displayedLatexCode, // Текущий отображаемый LaTeX-код
      };

      // Передаем данные на бэкэнд через событие
      this.$emit('compile-latex', requestData);
    },
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
/* Стили для переключателя */
.toggle-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.toggle-label {
  font-size: 14px;
  color: #555;
}

/* Компактное текстовое поле */
.compact-textarea .v-input__control {
  min-height: 32px !important; /* Минимальная высота */
}

.compact-textarea textarea {
  padding-top: 4px !important; /* Уменьшение внутренних отступов */
  padding-bottom: 4px !important;
  resize: none; /* Отключение изменения размера */
}

.compact-textarea .v-label {
  top: 4px !important; /* Корректировка позиции лейбла */
}
</style>