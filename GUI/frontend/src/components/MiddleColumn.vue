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
    <div
        class="latex-output"
        v-html="highlightedLatexCode"
        style="flex-grow: 1; overflow: auto; white-space: pre-wrap; font-family: monospace;"
    ></div>

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
    defaultFileName: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      isFullFormat: true, // Флаг для toggle
      fileName: '', // Имя файла
      internalLatexCode: '', // Внутренняя переменная для хранения LaTeX-кода
    };
  },
  watch: {
    // Отслеживаем изменения пропса latexCode
    latexCode(newVal) {
      console.log('LaTeX Code Updated:', newVal);
      this.internalLatexCode = newVal;
    },
    defaultFileName(newVal) {
      if (newVal && !this.fileName) {
        this.fileName = newVal;
      }
    },
  },
  computed: {
    displayedLatexCode() {
      if (!this.internalLatexCode) {
        return ''; // Если latexCode пустой, возвращаем пустую строку
      }

      if (this.isFullFormat) {
        return this.internalLatexCode; // Возвращаем полный код, если toggle активен
      }

      // Оставляем только блок с алгоритмом
      const lines = this.internalLatexCode.split('\n');
      let algorithmBlock = [];
      let inAlgorithmBlock = false;

      for (const line of lines) {
        if (line.includes('\\begin{algorithm}')) {
          inAlgorithmBlock = true; // Начало блока
        }

        if (inAlgorithmBlock) {
          algorithmBlock.push(line); // Добавляем строки блока
        }

        if (line.includes('\\end{algorithm}')) {
          break; // Конец блока
        }
      }

      return algorithmBlock.join('\n'); // Возвращаем отфильтрованный код
    },
    highlightedLatexCode() {
      // Простое подсвечивание синтаксиса (если нужно)
      return this.displayedLatexCode
          .replace(/\\[a-zA-Z]+/g, '<span style="color: blue;">$&</span>') // Команды LaTeX
          .replace(/\{.*?\}/g, '<span style="color: green;">$&</span>'); // Аргументы команд
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
      if (!this.internalLatexCode) {
        alert('Нет данных для скачивания!');
        return;
      }

      const fileName = this.fileName.trim()
          ? `${this.fileName}.tex`
          : 'output.tex'; // Если имя не указано, используем "output.tex"

      // Создаем Blob с содержимым LaTeX-кода
      const blob = new Blob([this.internalLatexCode], { type: 'text/plain' });

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

/* Стиль для отображения LaTeX-кода */
.latex-output {
  border: 1px solid #ccc;
  padding: 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}
</style>