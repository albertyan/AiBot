import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import './style.css'
import App from './App.vue'
import router from './router'
import 'remixicon/fonts/remixicon.css'
import { get_current_user } from './stores/user'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Antd)
app.mount('#app')

// Global method to get current user
window.get_current_user = get_current_user;
