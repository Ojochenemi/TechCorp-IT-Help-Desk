<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal modal-lg">
      <div class="modal-header">
        <div>
          <h3>{{ ticket?.subject }}</h3>
          <span class="ticket-id">{{ ticket?.id }}</span>
        </div>
        <button class="close-btn" @click="$emit('close')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="modal-body" v-if="ticket">
        <div class="detail-grid">
          <div class="detail-section">
            <h4>Details</h4>
            <div class="detail-row"><span class="label">Status</span><span class="badge" :class="statusClass">{{ ticket.status }}</span></div>
            <div class="detail-row"><span class="label">Priority</span><span class="badge" :class="priorityClass">{{ ticket.priority }}</span></div>
            <div class="detail-row"><span class="label">Category</span><span>{{ ticket.category }}</span></div>
            <div class="detail-row"><span class="label">Assigned To</span><span>{{ ticket.agent_name || ticket.assigned_to }}</span></div>
            <div class="detail-row"><span class="label">Created</span><span>{{ formatDateTime(ticket.created_at) }}</span></div>
            <div class="detail-row"><span class="label">Updated</span><span>{{ formatDateTime(ticket.updated_at) }}</span></div>
            <div class="detail-row" v-if="ticket.resolved_at"><span class="label">Resolved</span><span>{{ formatDateTime(ticket.resolved_at) }}</span></div>
          </div>
          <div class="detail-section">
            <h4>Requester</h4>
            <div class="detail-row"><span class="label">Name</span><span>{{ ticket.requester_name }}</span></div>
            <div class="detail-row"><span class="label">Email</span><span>{{ ticket.requester_email }}</span></div>
            <div class="detail-row"><span class="label">Department</span><span>{{ ticket.requester_department }}</span></div>
          </div>
        </div>
        <div class="detail-section" v-if="ticket.description">
          <h4>Description</h4>
          <p class="description-text">{{ ticket.description }}</p>
        </div>
        <div class="detail-section" v-if="ticket.sla_status">
          <h4>SLA Status</h4>
          <div class="sla-grid">
            <div class="sla-item" v-if="ticket.sla_status.response_met !== null">
              <span class="label">Response</span>
              <span class="badge" :class="ticket.sla_status.response_met ? 'success' : 'danger'">
                {{ ticket.sla_status.response_met ? 'Met' : 'Breached' }}
              </span>
            </div>
            <div class="sla-item" v-if="ticket.sla_status.resolution_met !== null">
              <span class="label">Resolution</span>
              <span class="badge" :class="ticket.sla_status.resolution_met ? 'success' : 'danger'">
                {{ ticket.sla_status.resolution_met ? 'Met' : 'Breached' }}
              </span>
            </div>
          </div>
        </div>
        <div class="detail-section" v-if="ticket.tags && ticket.tags.length">
          <h4>Tags</h4>
          <div class="tags">
            <span class="tag" v-for="tag in ticket.tags" :key="tag">{{ tag }}</span>
          </div>
        </div>
        <div class="detail-section comments-section">
          <h4>{{ t('comments.title') }}</h4>
          <div v-if="commentsLoading" class="comments-loading">{{ t('common.loading') }}</div>
          <div v-else>
            <div v-if="comments.length === 0" class="no-comments">{{ t('comments.noComments') }}</div>
            <div v-else class="comments-list">
              <div class="comment" v-for="comment in comments" :key="comment.id">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.author_name }}</span>
                  <span class="comment-date">{{ formatDateTime(comment.created_at) }}</span>
                </div>
                <p class="comment-body">{{ comment.body }}</p>
              </div>
            </div>
            <form class="comment-form" @submit.prevent="submitComment">
              <div class="comment-form-row">
                <input v-model="newComment.author_name" :placeholder="t('comments.namePlaceholder')" required />
                <input v-model="newComment.author_email" :placeholder="t('comments.emailPlaceholder')" type="email" required />
              </div>
              <textarea v-model="newComment.body" :placeholder="t('comments.placeholder')" rows="3" required></textarea>
              <button type="submit" class="post-btn" :disabled="submitting">{{ t('comments.post') }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { formatDateTime } from '../utils/formatters'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

const props = defineProps({ isOpen: Boolean, ticket: Object })
defineEmits(['close'])

const { t } = useI18n()

const comments = ref([])
const commentsLoading = ref(false)
const submitting = ref(false)
const newComment = ref({ author_name: '', author_email: '', body: '' })

watch(() => props.ticket?.id, async (id) => {
  if (!id) return
  commentsLoading.value = true
  try {
    comments.value = await api.getComments(id)
  } finally {
    commentsLoading.value = false
  }
}, { immediate: true })

async function submitComment() {
  submitting.value = true
  try {
    const comment = await api.createComment(props.ticket.id, newComment.value)
    comments.value.push(comment)
    newComment.value = { author_name: '', author_email: '', body: '' }
  } finally {
    submitting.value = false
  }
}

const statusClass = computed(() => {
  if (!props.ticket) return ''
  const map = { 'Open': 'info', 'In Progress': 'warning', 'Waiting on Customer': 'warning', 'Escalated': 'danger', 'Resolved': 'success', 'Closed': 'neutral' }
  return map[props.ticket.status] || ''
})

const priorityClass = computed(() => {
  if (!props.ticket) return ''
  const map = { 'Critical': 'danger', 'High': 'warning', 'Medium': 'info', 'Low': 'neutral' }
  return map[props.ticket.priority] || ''
})
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

.modal-lg {
  background: #ffffff;
  border-radius: 12px;
  width: 640px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
}

.ticket-id {
  font-size: 0.8125rem;
  color: #64748b;
  font-weight: 500;
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
  padding: 1.5rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.detail-section {
  margin-bottom: 1.25rem;
}

.detail-section h4 {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.375rem 0;
  font-size: 0.875rem;
}

.label {
  color: #64748b;
  font-weight: 500;
}

.description-text {
  font-size: 0.875rem;
  color: #334155;
  line-height: 1.6;
}

.badge {
  display: inline-block;
  padding: 0.188rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.success { background: #d1fae5; color: #065f46; }
.badge.warning { background: #fed7aa; color: #92400e; }
.badge.danger { background: #fecaca; color: #991b1b; }
.badge.info { background: #dbeafe; color: #1e40af; }
.badge.neutral { background: #e2e8f0; color: #475569; }

.sla-grid {
  display: flex;
  gap: 1.5rem;
}

.sla-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.tags {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.188rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.comments-section { border-top: 1px solid #e2e8f0; padding-top: 1.25rem; }

.comments-loading, .no-comments {
  font-size: 0.875rem;
  color: #94a3b8;
  padding: 0.5rem 0;
}

.comments-list { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.25rem; }

.comment {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.375rem;
}

.comment-author { font-size: 0.8125rem; font-weight: 600; color: #0f172a; }
.comment-date { font-size: 0.75rem; color: #94a3b8; }
.comment-body { font-size: 0.875rem; color: #334155; line-height: 1.5; margin: 0; }

.comment-form { display: flex; flex-direction: column; gap: 0.625rem; }

.comment-form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.625rem; }

.comment-form input,
.comment-form textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #0f172a;
  background: #ffffff;
  box-sizing: border-box;
  font-family: inherit;
  resize: vertical;
}

.comment-form input:focus,
.comment-form textarea:focus {
  outline: none;
  border-color: #94a3b8;
}

.post-btn {
  align-self: flex-end;
  background: #0f172a;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
}

.post-btn:hover:not(:disabled) { background: #1e293b; }
.post-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
