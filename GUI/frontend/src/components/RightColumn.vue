<template>
  <v-container>
    <iframe v-if="pdfUrl" :src="pdfUrl" width="100%" height="500px"></iframe>
    <v-btn v-if="pdfUrl" @click="downloadPdf">Скачать PDF</v-btn>
  </v-container>
</template>

<script>
export default {
  props: {
    pdfUrl: {
      type: String,
      default: '',
    },
  },
  methods: {
    downloadPdf() {
      const link = document.createElement('a');
      link.href = this.pdfUrl;
      link.download = 'output.pdf';
      link.click();
    },
  },
};
</script>