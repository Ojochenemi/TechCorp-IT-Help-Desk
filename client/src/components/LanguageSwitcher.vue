<template>
  <button class="lang-btn" @click="toggleLocale">
    {{ currentLocale === 'en' ? 'EN' : 'JA' }}
  </button>
</template>

<script setup>
import { useI18n } from '../composables/useI18n'

const { currentLocale, toggleLocale } = useI18n()
</script>

<style scoped>
.lang-btn {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  color: #94a3b8;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.025em;
}

.lang-btn:hover {
  background: rgba(255,255,255,0.12);
  color: #e2e8f0;
}
</style>
