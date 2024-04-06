import './assets/main.css'
import 'primevue/resources/themes/aura-dark-green/theme.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import confirmationservice from 'primevue/confirmationservice'


const app = createApp(App)

app.use(router)
app.use(PrimeVue)
app.use(confirmationservice)

app.mount('#app')
