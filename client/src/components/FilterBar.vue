<template>
  <div class="filter-bar">
    <div class="filter-group">
      <select v-model="selectedStatus" class="filter-select">
        <option value="all">{{ t('filters.status') }}: {{ t('filters.all') }}</option>
        <option value="Open">{{ t('statuses.open') }}</option>
        <option value="In Progress">{{ t('statuses.inProgress') }}</option>
        <option value="Waiting on Customer">{{ t('statuses.waitingOnCustomer') }}</option>
        <option value="Escalated">{{ t('statuses.escalated') }}</option>
        <option value="Resolved">{{ t('statuses.resolved') }}</option>
        <option value="Closed">{{ t('statuses.closed') }}</option>
      </select>

      <select v-model="selectedPriority" class="filter-select">
        <option value="all">{{ t('filters.priority') }}: {{ t('filters.all') }}</option>
        <option value="Critical">{{ t('priorities.critical') }}</option>
        <option value="High">{{ t('priorities.high') }}</option>
        <option value="Medium">{{ t('priorities.medium') }}</option>
        <option value="Low">{{ t('priorities.low') }}</option>
      </select>

      <select v-model="selectedCategory" class="filter-select">
        <option value="all">{{ t('filters.category') }}: {{ t('filters.all') }}</option>
        <option value="Network">Network</option>
        <option value="Hardware">Hardware</option>
        <option value="Software">Software</option>
        <option value="Access/Permissions">Access/Permissions</option>
        <option value="Email">Email</option>
        <option value="Other">Other</option>
      </select>

      <select v-model="selectedAgent" class="filter-select">
        <option value="all">{{ t('filters.agent') }}: {{ t('filters.all') }}</option>
        <option v-for="agent in agentList" :key="agent.id" :value="agent.id">{{ agent.name }}</option>
      </select>

      <select v-model="selectedPeriod" class="filter-select">
        <option value="all">{{ t('filters.period') }}: {{ t('filters.all') }}</option>
        <option value="2025-11">Nov 2025</option>
        <option value="2025-12">Dec 2025</option>
        <option value="2026-01">Jan 2026</option>
        <option value="2026-02">Feb 2026</option>
        <option value="2026-03">Mar 2026</option>
        <option value="Q4-2025">Q4 2025</option>
        <option value="Q1-2026">Q1 2026</option>
      </select>
    </div>

    <button v-if="hasActiveFilters" class="reset-btn" @click="resetFilters">
      {{ t('filters.reset') }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { api } from '../api'

const { t } = useI18n()
const {
  selectedStatus, selectedPriority, selectedCategory,
  selectedAgent, selectedPeriod, hasActiveFilters, resetFilters
} = useFilters()

const agentList = ref([])

onMounted(async () => {
  try {
    agentList.value = await api.getAgents()
  } catch (err) {
    console.error('Failed to load agents for filter:', err)
  }
})
</script>

<style scoped>
.filter-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-select {
  height: 32px;
  padding: 0 0.625rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  color: #334155;
  background: #ffffff;
  cursor: pointer;
  outline: none;
}

.filter-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
}

.reset-btn {
  height: 32px;
  padding: 0 0.75rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
}

.reset-btn:hover {
  background: #e2e8f0;
  color: #334155;
}
</style>
