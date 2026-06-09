<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div class="sidebar-header">
      <div class="logo-area" v-if="!collapsed">
        <span class="logo-text">{{ t('nav.companyName') }}</span>
      </div>
      <div class="logo-area" v-else>
        <span class="logo-text">TC</span>
      </div>
      <button class="collapse-btn" @click="$emit('toggle-collapse')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path v-if="!collapsed" d="M15 18l-6-6 6-6" />
          <path v-else d="M9 18l6-6-6-6" />
        </svg>
      </button>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section-label" v-if="!collapsed">NAVIGATION</div>
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
        :title="collapsed ? t(item.label) : ''"
      >
        <span class="nav-icon" v-html="item.icon"></span>
        <span class="nav-text" v-if="!collapsed">{{ t(item.label) }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <LanguageSwitcher v-if="!collapsed" />
      <div class="user-compact" @click="$emit('show-profile-details')">
        <div class="user-avatar-small">{{ currentUser.initials }}</div>
        <div class="user-info-small" v-if="!collapsed">
          <div class="user-name-small">{{ currentUser.name }}</div>
          <div class="user-role-small">{{ currentUser.jobTitle }}</div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { useAuth } from '../composables/useAuth'
import LanguageSwitcher from './LanguageSwitcher.vue'

defineProps({ collapsed: Boolean })
defineEmits(['toggle-collapse', 'show-profile-details', 'show-tasks'])

const route = useRoute()
const { t } = useI18n()
const { currentUser } = useAuth()

const navItems = [
  { path: '/', label: 'nav.dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>' },
  { path: '/tickets', label: 'nav.tickets', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>' },
  { path: '/agents', label: 'nav.agents', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>' },
  { path: '/sla', label: 'nav.sla', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>' },
  { path: '/escalations', label: 'nav.escalations', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>' },
  { path: '/reports', label: 'nav.reports', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="12" width="4" height="8" rx="1"/><rect x="10" y="8" width="4" height="12" rx="1"/><rect x="17" y="4" width="4" height="16" rx="1"/></svg>' }
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease;
  z-index: 100;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.logo-text {
  color: #ffffff;
  font-weight: 700;
  font-size: 1.125rem;
  white-space: nowrap;
}

.collapse-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.collapse-btn:hover {
  color: #e2e8f0;
  background: rgba(255,255,255,0.05);
}

.sidebar-nav {
  flex: 1;
  padding: 0.75rem 0;
  overflow-y: auto;
}

.nav-section-label {
  color: #475569;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.5rem 1.25rem;
  margin-bottom: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  margin: 2px 8px;
  border-radius: 6px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255,255,255,0.05);
  color: #e2e8f0;
}

.nav-item.active {
  background: rgba(59,130,246,0.1);
  color: #ffffff;
  border-left-color: #3b82f6;
}

.nav-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 0.75rem;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.user-compact {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.user-compact:hover {
  background: rgba(255,255,255,0.05);
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3b82f6;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.user-name-small {
  color: #e2e8f0;
  font-size: 13px;
  font-weight: 500;
}

.user-role-small {
  color: #64748b;
  font-size: 11px;
}

.collapsed .nav-item {
  justify-content: center;
  padding: 0.75rem;
  margin: 2px 4px;
}

.collapsed .sidebar-header {
  justify-content: center;
  padding: 1.25rem 0.5rem;
}

.collapsed .sidebar-footer {
  padding: 0.5rem;
}

.collapsed .user-compact {
  justify-content: center;
}
</style>
