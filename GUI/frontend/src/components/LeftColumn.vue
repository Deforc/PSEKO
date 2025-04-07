<template>
  <v-container>
    <!-- Выпадающий список для выбора стиля -->
    <v-select
        v-model="selectedStyle"
        :items="styles"
        label="Выберите стиль"
        outlined
    ></v-select>

    <!-- Поле для ввода текста с поддержкой табуляции -->
    <v-textarea
        v-model="inputText"
        label="Введите текст"
        outlined
        @keydown.tab.prevent="insertTab"
    ></v-textarea>

    <!-- Кнопка загрузки файла -->
    <v-btn
        color="green"
        class="mb-4"
        block
        @click="openFileInput"
    >
      Загрузить текст из файла (.txt)
    </v-btn>

    <!-- Скрытый input для выбора файла -->
    <input
        type="file"
        ref="fileInput"
        accept=".txt"
        style="display: none;"
        @change="handleFileUpload"
    />

    <!-- Подписи и цветовые пикеры -->
    <v-row>
      <v-col cols="6">
        <label class="color-picker-label">Цвет ключевых слов</label>
        <v-color-picker
            v-model="colorKeywords"
            mode="hexa"
            hide-canvas
            hide-inputs
            show-swatches
            swatches-max-height="100"
        ></v-color-picker>
      </v-col>
      <v-col cols="6">
        <label class="color-picker-label">Цвет комментариев</label>
        <v-color-picker
            v-model="colorComment"
            mode="hexa"
            hide-canvas
            hide-inputs
            show-swatches
            swatches-max-height="100"
        ></v-color-picker>
      </v-col>
    </v-row>

    <!-- Кнопка отправки -->
    <v-btn
        color="green"
        block
        class="mt-4"
        @click="sendToBackend"
    >
      Публикация
    </v-btn>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedStyle: 'tree', // Стиль по умолчанию
      styles: ['tree', 'ladder', 'line'], // Доступные стили
      inputText: '', // Введенный текст
      colorKeywords: '#0000FF', // Цвет ключевых слов (по умолчанию blue)
      colorComment: '#808080', // Цвет комментариев (по умолчанию gray)
    };
  },
  methods: {
    insertTab(event) {
      const textarea = event.target;

      // Получаем текущую позицию курсора
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      // Вставляем символ табуляции (\t) в текущую позицию
      this.inputText =
          this.inputText.substring(0, start) + '\t' + this.inputText.substring(end);

      // Перемещаем курсор после вставленного таба
      this.$nextTick(() => {
        textarea.setSelectionRange(start + 1, start + 1);
      });
    },
    openFileInput() {
      // Открываем скрытый input для выбора файла
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Проверяем, что файл имеет расширение .txt
      if (!file.name.endsWith('.txt')) {
        alert('Пожалуйста, выберите файл с расширением .txt');
        return;
      }

      // Читаем содержимое файла
      const reader = new FileReader();
      reader.onload = (e) => {
        this.inputText = e.target.result; // Записываем содержимое файла в текстовое поле
      };
      reader.onerror = () => {
        alert('Ошибка при чтении файла');
      };
      reader.readAsText(file);
    },
    async sendToBackend() {
      try {
        const requestData = {
          style: this.selectedStyle, // Выбранный стиль
          text: this.inputText, // Введенный текст
          colorKeywords: this.colorKeywords.slice(1), // Убираем "#" для формата RRGGBB
          colorComment: this.colorComment.slice(1), // Убираем "#" для формата RRGGBB
        };

        // Отправляем запрос на бэкэнд
        const response = await axios.post('http://127.0.0.1:8000/api/latex', requestData);
        this.$emit('update-latex', response.data.latexCode); // Передаем результат в родительский компонент
      } catch (error) {
        console.error('Ошибка при отправке данных:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Стили для подписей */
.color-picker-label {
  display: block;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

/* Ограничение ширины палитры */
.v-color-picker {
  max-width: 100%;
}
</style>