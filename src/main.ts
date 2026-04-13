import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { router } from '@/core/router'
import App from './App.vue'
import './style.css'

// Import interceptors (side-effect: registers them on apiClient)
import '@/core/api/interceptors'

const app = createApp(App)

// Pinia with persistence
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Router
app.use(router)

// Mount
app.mount('#app')
