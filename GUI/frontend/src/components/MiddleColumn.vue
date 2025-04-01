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
        @click="$emit('compile-latex')"
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
</style>