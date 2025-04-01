<template>
  <v-app>
    <!-- Хедер -->
    <Header />

    <!-- Основной контент -->
    <v-main style="flex-grow: 1; overflow: hidden;">
      <v-container fluid style="height: 100%; display: flex; flex-direction: column;">
        <v-row style="flex-grow: 1; overflow: hidden;">
          <!-- Левая колонка -->
          <v-col cols="4" style="overflow: auto;">
            <LeftColumn @update-latex="updateLatex" />
          </v-col>

          <!-- Средняя колонка -->
          <v-col cols="4" style="overflow: auto;">
            <MiddleColumn
                :latexCode="latexCode"
                @compile-latex="compileLatex"
            />
          </v-col>

          <!-- Правая колонка -->
          <v-col cols="4" style="overflow: auto;">
            <RightColumn :pdfUrl="pdfUrl" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Футер -->
    <Footer />
  </v-app>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import LeftColumn from './components/LeftColumn.vue';
import MiddleColumn from './components/MiddleColumn.vue';
import RightColumn from './components/RightColumn.vue';
import axios from 'axios';

export default {
  components: { Header, Footer, LeftColumn, MiddleColumn, RightColumn },
  data() {
    return {
      latexCode: '', // LaTeX-код, полученный с бэкэнда
      pdfUrl: '', // URL PDF-файла
    };
  },
  methods: {
    // Обновление LaTeX-кода из левой колонки
    updateLatex(code) {
      this.latexCode = code;
    },

    // Компиляция LaTeX-кода в PDF
    async compileLatex(requestData) {
      try {
        const response = await axios.post('/api/compile', requestData);
        this.pdfUrl = response.data.pdfUrl; // Сохраняем URL PDF-файла
      } catch (error) {
        console.error('Ошибка при компиляции LaTeX:', error);
      }
    },
  },
};
</script>

<style>
/* Глобальные стили */
html,
body {
  height: 100%;
  margin: 0;
}

#app {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>