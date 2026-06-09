<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ t('common.profile') }}</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <div class="profile-header">
          <div class="profile-avatar">{{ currentUser.initials }}</div>
          <div>
            <div class="profile-name">{{ currentUser.name }}</div>
            <div class="profile-title">{{ currentUser.jobTitle }}</div>
          </div>
        </div>
        <div class="profile-details">
          <div class="detail-row"><span class="detail-label">Email</span><span>{{ currentUser.email }}</span></div>
          <div class="detail-row"><span class="detail-label">Department</span><span>{{ currentUser.department }}</span></div>
          <div class="detail-row"><span class="detail-label">Location</span><span>{{ currentUser.location }}</span></div>
          <div class="detail-row"><span class="detail-label">Phone</span><span>{{ currentUser.phone }}</span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuth } from '../composables/useAuth'
import { useI18n } from '../composables/useI18n'

defineProps({ isOpen: Boolean })
defineEmits(['close'])

const { currentUser } = useAuth()
const { t } = useI18n()
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal {
  background: #ffffff;
  border-radius: 12px;
  width: 420px;
  max-width: 90vw;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
}

.close-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-body {
  padding: 1.5rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #3b82f6;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
}

.profile-name {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
}

.profile-title {
  font-size: 0.875rem;
  color: #64748b;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.detail-label {
  color: #64748b;
  font-weight: 500;
}
</style>
