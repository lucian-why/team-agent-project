/**
 * 学习画像前端类型定义

 * 从现有项目迁移并重构为垂直切片架构。
 */

// ==================== 错题相关 ====================

export interface WrongQuestion {
  id: string
  question: string
  userAnswer: string
  correctAnswer: string
  mistakeType: string
  sourceLabel: string
}

export interface WrongQuestionGroup {
  notebookId: string
  notebookName: string
  sourceCount: number
  wrongQuestions: WrongQuestion[]
  frequentMistakes: string[]
  quizHref: string
}

// ==================== 学生画像 ====================

export interface StudentProfile {
  id: string
  notebookId: string
  major?: string
  course?: string
  learningGoal?: string
  knowledgeLevel?: string
  cognitiveStyle?: string
  weakPoints: string[]
  interestTags: string[]
  practicePreference?: string
  pacePreference?: string
  resourcePreference?: string
  confidence: number
  evidenceSummary?: string
  sourceIds: string[]
  createdBy: string
  metadata: Record<string, unknown>
  schemaVersion: number
  created?: string
  updated?: string
}

export interface StudentProfileCreate {
  notebookId: string
  major?: string
  course?: string
  learningGoal?: string
  knowledgeLevel?: string
  cognitiveStyle?: string
  weakPoints?: string[]
  interestTags?: string[]
  practicePreference?: string
  pacePreference?: string
  resourcePreference?: string
  confidence?: number
  evidenceSummary?: string
  sourceIds?: string[]
  createdBy?: string
  metadata?: Record<string, unknown>
}

export interface StudentProfileUpdate {
  major?: string
  course?: string
  learningGoal?: string
  knowledgeLevel?: string
  cognitiveStyle?: string
  weakPoints?: string[]
  interestTags?: string[]
  practicePreference?: string
  pacePreference?: string
  resourcePreference?: string
  confidence?: number
  evidenceSummary?: string
  sourceIds?: string[]
  metadata?: Record<string, unknown>
}

// ==================== 学习路径 ====================

export interface LearningPathNode {
  id: string
  title: string
  description: string
  learningObjectives: string[]
  prerequisites: string[]
  recommendedSourceIds: string[]
  recommendedResourceTypes: string[]
  estimatedMinutes: number
  status: 'todo' | 'in_progress' | 'completed' | 'skipped'
  masteryScore: number
}

export interface LearningPath {
  id: string
  notebookId: string
  profileId?: string
  title: string
  course: string
  nodes: LearningPathNode[]
  currentNodeId?: string
  status: 'draft' | 'active' | 'completed' | 'archived'
  sourceIds: string[]
  createdBy: string
  metadata: Record<string, unknown>
  schemaVersion: number
  created?: string
  updated?: string
}

export interface LearningPathCreate {
  notebookId: string
  profileId?: string
  title?: string
  course?: string
  nodes?: LearningPathNode[]
  currentNodeId?: string
  status?: string
  sourceIds?: string[]
  createdBy?: string
  metadata?: Record<string, unknown>
}

export interface LearningPathUpdate {
  profileId?: string
  title?: string
  course?: string
  nodes?: LearningPathNode[]
  currentNodeId?: string
  status?: string
  sourceIds?: string[]
  metadata?: Record<string, unknown>
}
