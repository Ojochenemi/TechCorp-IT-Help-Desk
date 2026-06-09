# Client - Vue 3 Frontend

## Stack
- Vue 3 + Composition API (`<script setup>`)
- Vue Router 4
- Axios for API calls
- Vite dev server (port 3000)

## Patterns
- Use `<script setup>` for all new components
- Filter state from `useFilters()` composable (singleton)
- Translations from `useI18n()`, never hardcode user-facing text
- User data from `useAuth()` composable
- API calls through `api.js`, never use fetch/axios directly in views

## Key Rules
- Unique keys in v-for: `:key="ticket.id"` not `:key="index"`
- Computed for derived data, not methods in templates
- Validate dates before calling `.getMonth()`, `.toLocaleDateString()` etc.
- Scoped styles, avoid global CSS in components
