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
            <RightColumn
                :pdfUrl="pdfUrl"
                :pdfFileName="pdfFileName"
                :texFileName="texFileName"
                :texUrl="texUrl"
                :isFullFormat="true"
                :compilationAttempted="compilationAttempted"
            />
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
      pdfFileName: '', // Имя PDF-файла
      texFileName: '', // Имя .tex файла
      texUrl: '', // URL .tex файла
      compilationAttempted: false, // Флаг, указывающий, была ли попытка компиляции
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
        this.compilationAttempted = true; // Устанавливаем флаг попытки компиляции

        const response = await axios.post('http://127.0.0.1:8000/api/compile', requestData);

        // Проверка на наличие данных в ответе
        if (!response.data || !response.data.pdfUrl || !response.data.texUrl) {
          throw new Error('Сервер не вернул необходимые URL');
        }

        // Сохраняем данные из ответа
        this.pdfUrl = response.data.pdfUrl;
        this.texUrl = response.data.texUrl; // URL .tex файла
        this.pdfFileName = response.data.pdfFileName || 'document.pdf'; // Имя PDF по умолчанию
        this.texFileName = response.data.texFileName || 'document.tex'; // Имя .tex по умолчанию
      } catch (error) {
        console.error('Ошибка при компиляции LaTeX:', error.message);
        alert('Не удалось скомпилировать LaTeX. Попробуйте еще раз.');
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