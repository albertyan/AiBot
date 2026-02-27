import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import 'remixicon/fonts/remixicon.css'
import { get_current_user } from './stores/user'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

// Global method to get current user
window.get_current_user = get_current_user;
