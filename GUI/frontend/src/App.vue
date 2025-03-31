<template>
  <v-app>
    <Header />
    <v-main style="flex-grow: 1; overflow: hidden;">
      <v-container fluid style="height: 100%; display: flex; flex-direction: column;">
        <v-row style="flex-grow: 1; overflow: hidden;">
          <v-col cols="4" style="overflow: auto;">
            <LeftColumn @update-latex="updateLatex" />
          </v-col>
          <v-col cols="4" style="overflow: auto;">
            <MiddleColumn :latexCode="latexCode" @compile-latex="compileLatex" />
          </v-col>
          <v-col cols="4" style="overflow: auto;">
            <RightColumn :pdfUrl="pdfUrl" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
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
      latexCode: '',
      pdfUrl: '', // URL PDF-файла
    };
  },
  methods: {
    updateLatex(code) {
      this.latexCode = code;
    },
    async compileLatex() {
      try {
        const response = await axios.post('/api/compile', { latex: this.latexCode });
        this.pdfUrl = response.data.pdfUrl; // Получаем URL PDF
      } catch (error) {
        console.error('Ошибка при компиляции LaTeX:', error);
      }
    },
  },
};
</script>