import { ref, computed } from 'vue'

const selectedStatus = ref('all')
const selectedPriority = ref('all')
const selectedCategory = ref('all')
const selectedAgent = ref('all')
const selectedPeriod = ref('all')

export function useFilters() {
  const hasActiveFilters = computed(() => {
    return selectedStatus.value !== 'all' ||
           selectedPriority.value !== 'all' ||
           selectedCategory.value !== 'all' ||
           selectedAgent.value !== 'all' ||
           selectedPeriod.value !== 'all'
  })

  const resetFilters = () => {
    selectedStatus.value = 'all'
    selectedPriority.value = 'all'
    selectedCategory.value = 'all'
    selectedAgent.value = 'all'
    selectedPeriod.value = 'all'
  }

  const getCurrentFilters = () => {
    const filters = {}
    if (selectedStatus.value !== 'all') filters.status = selectedStatus.value
    if (selectedPriority.value !== 'all') filters.priority = selectedPriority.value
    if (selectedCategory.value !== 'all') filters.category = selectedCategory.value
    if (selectedAgent.value !== 'all') filters.agent_id = selectedAgent.value
    if (selectedPeriod.value !== 'all') filters.month = selectedPeriod.value
    return filters
  }

  return {
    selectedStatus,
    selectedPriority,
    selectedCategory,
    selectedAgent,
    selectedPeriod,
    hasActiveFilters,
    resetFilters,
    getCurrentFilters
  }
}
