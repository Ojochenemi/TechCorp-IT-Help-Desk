export default {
  nav: {
    companyName: 'TechCorpサポート',
    dashboard: 'ダッシュボード',
    tickets: 'チケット',
    agents: 'エージェント',
    sla: 'SLAコンプライアンス',
    escalations: 'エスカレーション',
    reports: 'レポート'
  },
  dashboard: {
    title: 'ダッシュボード',
    kpi: {
      openTickets: '未解決チケット',
      avgResolution: '平均解決時間',
      slaCompliance: 'SLA準拠率',
      agentUtilization: 'エージェント稼働率',
      hours: '時間'
    },
    statusDistribution: 'ステータス分布',
    priorityBreakdown: '優先度内訳',
    recentTickets: '最近のチケット'
  },
  tickets: {
    title: 'チケット',
    subtitle: 'サポートチケットの管理と追跡',
    id: 'ID',
    subject: '件名',
    status: 'ステータス',
    priority: '優先度',
    category: 'カテゴリ',
    assignedTo: '担当者',
    created: '作成日',
    updated: '更新日',
    requester: '依頼者',
    department: '部門',
    description: '説明',
    tags: 'タグ',
    slaStatus: 'SLAステータス',
    responseTime: '応答時間',
    resolutionTime: '解決時間',
    met: '達成',
    breached: '違反',
    pending: '保留中'
  },
  agents: {
    title: 'エージェント',
    subtitle: 'サポートチームの名簿と作業負荷',
    name: '名前',
    role: '役割',
    status: 'ステータス',
    assigned: '割り当て',
    resolved: '解決済み',
    avgResolution: '平均解決時間',
    satisfaction: '満足度',
    skills: 'スキル',
    workload: '作業負荷分布'
  },
  sla: {
    title: 'SLAコンプライアンス',
    subtitle: 'サービスレベル契約の追跡',
    rules: 'SLAルール',
    compliance: 'コンプライアンスサマリー',
    breaches: 'SLA違反',
    responseTarget: '応答目標',
    resolutionTarget: '解決目標',
    responseCompliance: '応答コンプライアンス',
    resolutionCompliance: '解決コンプライアンス'
  },
  escalations: {
    title: 'エスカレーション',
    subtitle: '注意が必要なエスカレーションチケット',
    ticket: 'チケット',
    from: '元担当',
    to: '新担当',
    reason: '理由',
    escalatedAt: 'エスカレーション日時',
    resolvedAt: '解決日時',
    status: 'ステータス',
    notes: '備考'
  },
  reports: {
    title: 'レポート',
    subtitle: '分析とパフォーマンストレンド',
    monthlyTrends: '月次チケットトレンド',
    agentPerformance: 'エージェントパフォーマンス',
    created: '作成',
    resolved: '解決',
    escalated: 'エスカレーション'
  },
  filters: {
    status: 'ステータス',
    priority: '優先度',
    category: 'カテゴリ',
    agent: 'エージェント',
    period: '期間',
    all: 'すべて',
    reset: 'フィルタをリセット'
  },
  statuses: {
    open: 'オープン',
    inProgress: '対応中',
    waitingOnCustomer: '顧客待ち',
    escalated: 'エスカレーション',
    resolved: '解決済み',
    closed: 'クローズ'
  },
  priorities: {
    critical: '緊急',
    high: '高',
    medium: '中',
    low: '低'
  },
  comments: {
    title: 'コメント',
    noComments: 'コメントはまだありません。',
    placeholder: 'コメントを入力...',
    post: 'コメントを投稿',
    namePlaceholder: '名前',
    emailPlaceholder: 'メールアドレス'
  },
  common: {
    loading: '読み込み中...',
    error: 'エラーが発生しました',
    noData: 'データがありません',
    close: '閉じる',
    save: '保存',
    cancel: 'キャンセル',
    search: '検索...',
    profile: 'プロフィール',
    tasks: 'タスク',
    settings: '設定',
    logout: 'ログアウト'
  }
}
