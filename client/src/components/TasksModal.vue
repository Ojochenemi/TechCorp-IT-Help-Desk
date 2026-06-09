<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ t('common.tasks') }}</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <div v-if="tasks.length === 0" class="no-tasks">{{ t('common.noData') }}</div>
        <div v-for="task in tasks" :key="task.id" class="task-item" :class="{ completed: task.status === 'completed' }">
          <button class="task-check" @click="$emit('toggle-task', task.id)">
            <svg v-if="task.status === 'completed'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            <div v-else class="check-empty"></div>
          </button>
          <span class="task-title">{{ task.title }}</span>
          <button class="task-delete" @click="$emit('delete-task', task.id)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from '../composables/useI18n'

defineProps({ isOpen: Boolean, tasks: { type: Array, default: () => [] } })
defineEmits(['close', 'add-task', 'delete-task', 'toggle-task'])

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
  width: 480px;
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

.close-btn:hover { background: #f1f5f9; color: #0f172a; }

.modal-body {
  padding: 1rem 1.5rem 1.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.no-tasks {
  color: #94a3b8;
  text-align: center;
  padding: 2rem;
  font-size: 0.875rem;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.task-item.completed .task-title {
  text-decoration: line-through;
  color: #94a3b8;
}

.task-check {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
}

.check-empty {
  width: 16px;
  height: 16px;
  border: 2px solid #cbd5e1;
  border-radius: 4px;
}

.task-title {
  flex: 1;
  font-size: 0.875rem;
  color: #334155;
}

.task-delete {
  background: none;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  padding: 2px;
  opacity: 0;
  transition: opacity 0.15s;
}

.task-item:hover .task-delete {
  opacity: 1;
}

.task-delete:hover {
  color: #ef4444;
}
</style>
