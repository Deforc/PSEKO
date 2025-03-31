<template>
  <v-app-bar color="primary" dark app>
    <v-btn @click="showImage('grammar')">Show Grammar</v-btn>
    <v-btn @click="showImage('uml')">Show UML</v-btn>
    <v-dialog v-model="dialog" max-width="800">
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