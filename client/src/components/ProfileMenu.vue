<template>
  <button class="profile-btn" @click="$emit('show-profile-details')">
    <div class="avatar">{{ currentUser.initials }}</div>
  </button>
</template>

<script setup>
import { useAuth } from '../composables/useAuth'

defineEmits(['show-profile-details'])
const { currentUser } = useAuth()
</script>

<style scoped>
.profile-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.avatar {
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
}
</style>
