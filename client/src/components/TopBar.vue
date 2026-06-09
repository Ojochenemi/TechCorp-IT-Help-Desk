<template>
  <header class="top-bar">
    <div class="top-bar-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>
    <div class="top-bar-right">
      <button class="icon-btn" @click="$emit('show-tasks')" title="Tasks">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
        </svg>
      </button>
      <button class="icon-btn" @click="$emit('show-profile-details')" title="Profile">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'

defineEmits(['show-profile-details', 'show-tasks'])

const route = useRoute()
const { t } = useI18n()

const pageTitles = {
  '/': 'nav.dashboard',
  '/tickets': 'nav.tickets',
  '/agents': 'nav.agents',
  '/sla': 'nav.sla',
  '/escalations': 'nav.escalations',
  '/reports': 'nav.reports'
}

const pageTitle = computed(() => {
  const key = pageTitles[route.path] || 'nav.dashboard'
  return t(key)
})
</script>

<style scoped>
.top-bar {
  height: 56px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
}

.icon-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}
</style>
