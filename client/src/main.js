import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Dashboard from './views/Dashboard.vue'
import Tickets from './views/Tickets.vue'
import Agents from './views/Agents.vue'
import SLACompliance from './views/SLACompliance.vue'
import Escalations from './views/Escalations.vue'
import Reports from './views/Reports.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/tickets', component: Tickets },
    { path: '/agents', component: Agents },
    { path: '/sla', component: SLACompliance },
    { path: '/escalations', component: Escalations },
    { path: '/reports', component: Reports }
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
