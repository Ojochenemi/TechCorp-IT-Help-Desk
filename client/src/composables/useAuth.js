import { computed } from 'vue'
import { useI18n } from './useI18n'

export function useAuth() {
  const { currentLocale } = useI18n()

  const currentUser = computed(() => {
    const isJapanese = currentLocale.value === 'ja'

    return {
      name: isJapanese ? '山田 太郎' : 'Alex Morgan',
      initials: isJapanese ? '山田' : 'AM',
      email: 'alex.morgan@techcorp.com',
      jobTitle: isJapanese ? 'ITサポートマネージャー' : 'IT Support Manager',
      department: isJapanese ? 'ITサポート' : 'IT Support',
      company: 'TechCorp',
      location: isJapanese ? '東京オフィス' : 'San Francisco Office',
      phone: '+1 (555) 234-5678',
      tasks: [
        { id: 'task-1', title: isJapanese ? 'SLA違反レポートの確認' : 'Review SLA breach report', status: 'pending' },
        { id: 'task-2', title: isJapanese ? '新規L2エージェントの割り当て' : 'Assign new L2 agent to network queue', status: 'pending' },
        { id: 'task-3', title: isJapanese ? 'KB記事の更新' : 'Update VPN troubleshooting KB article', status: 'completed' }
      ]
    }
  })

  return { currentUser }
}
