<template>
  <v-app-bar color="green" dark app>
    <v-btn @click="showImage('grammar')">Показать грамматику</v-btn>
    <v-btn @click="showImage('uml')">Показать UML</v-btn>
    <v-dialog v-model="dialog" min-width="80%">
      <v-card>
        <v-img :src="imageSrc" contain></v-img>
      </v-card>
    </v-dialog>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      imageSrc: '',
    };
  },
  methods: {
    showImage(type) {
      this.imageSrc = `/${type}.jpeg`;
      this.dialog = true;
    },
  },
};
</script>