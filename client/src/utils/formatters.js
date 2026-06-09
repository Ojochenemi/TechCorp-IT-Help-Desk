/**
 * Format an ISO date string to a readable date.
 * @param {string} isoString - ISO 8601 date string
 * @returns {string} Formatted date (e.g., "Mar 15, 2026")
 */
export function formatDate(isoString) {
  if (!isoString) return '—'
  const date = new Date(isoString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

/**
 * Format an ISO date string to a readable date and time.
 * @param {string} isoString - ISO 8601 date string
 * @returns {string} Formatted datetime (e.g., "Mar 15, 2026 2:30 PM")
 */
export function formatDateTime(isoString) {
  if (!isoString) return '—'
  const date = new Date(isoString)
  return date.toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: 'numeric', minute: '2-digit'
  })
}

/**
 * Format minutes into a human-readable duration.
 * @param {number} minutes - Duration in minutes
 * @returns {string} Formatted duration (e.g., "2h 30m", "1d 4h")
 */
export function formatDuration(minutes) {
  if (minutes === null || minutes === undefined) return '—'
  if (minutes < 60) return `${Math.round(minutes)}m`
  if (minutes < 1440) {
    const h = Math.floor(minutes / 60)
    const m = Math.round(minutes % 60)
    return m > 0 ? `${h}h ${m}m` : `${h}h`
  }
  const d = Math.floor(minutes / 1440)
  const h = Math.round((minutes % 1440) / 60)
  return h > 0 ? `${d}d ${h}h` : `${d}d`
}

/**
 * Format hours into a human-readable duration.
 * @param {number} hours - Duration in hours
 * @returns {string} Formatted duration
 */
export function formatHours(hours) {
  if (hours === null || hours === undefined || hours === 0) return '—'
  return formatDuration(hours * 60)
}

/**
 * Get a relative time string from an ISO date.
 * @param {string} isoString - ISO 8601 date string
 * @returns {string} Relative time (e.g., "3 hours ago")
 */
export function timeAgo(isoString) {
  if (!isoString) return '—'
  const now = new Date()
  const date = new Date(isoString)
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins}m ago`
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 30) return `${diffDays}d ago`
  const diffMonths = Math.floor(diffDays / 30)
  return `${diffMonths}mo ago`
}
