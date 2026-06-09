import { ref, computed } from 'vue'
import en from '../locales/en'
import ja from '../locales/ja'

const currentLocale = ref('en')
const translations = { en, ja }

export function useI18n() {
  const t = (key, params = {}) => {
    const keys = key.split('.')
    let value = translations[currentLocale.value]

    for (const k of keys) {
      if (value === undefined || value === null) break
      value = value[k]
    }

    // Fallback to English
    if ((value === undefined || value === null) && currentLocale.value !== 'en') {
      value = translations.en
      for (const k of keys) {
        if (value === undefined || value === null) break
        value = value[k]
      }
    }

    if (value === undefined || value === null) return key

    if (typeof value === 'string' && Object.keys(params).length > 0) {
      return Object.entries(params).reduce(
        (str, [paramKey, paramValue]) => str.replace(`{${paramKey}}`, paramValue),
        value
      )
    }

    return value
  }

  const toggleLocale = () => {
    currentLocale.value = currentLocale.value === 'en' ? 'ja' : 'en'
  }

  const selectedCurrency = computed(() => currentLocale.value === 'ja' ? 'JPY' : 'USD')

  return { t, currentLocale, toggleLocale, selectedCurrency }
}
