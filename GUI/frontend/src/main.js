// main.js
import { createApp } from 'vue';
import App from './App.vue';
import vuetify from '../plugins/vuetify';

const app = createApp(App);

// Используем Vuetify
app.use(vuetify);

// Монтируем приложение
app.mount('#app');