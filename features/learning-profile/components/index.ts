/**
 * 学习画像组件导出

 * 统一导出所有学习画像相关的组件、类型和工具函数。
 */

// 组件
export { default as LearningProfilePage } from './LearningProfilePage'
export { ProfileMetric, WrongQuestionItem, WrongQuestionGroupCard } from './LearningProfileCard'

// 类型
export type {
  WrongQuestion,
  WrongQuestionGroup,
  StudentProfile,
  StudentProfileCreate,
  StudentProfileUpdate,
  LearningPathNode,
  LearningPath,
  LearningPathCreate,
  LearningPathUpdate,
} from './learning-profile-types'

// 工具函数
export { buildWrongQuestionGroups } from './learning-profile-utils'
