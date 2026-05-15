import type { WrongQuestion, WrongQuestionGroup } from './learning-profile-types'

/**
 * 学习画像工具函数

 * 从现有项目迁移并重构为垂直切片架构。
 */

// 模拟错题数据（实际项目中应从 API 获取）
const MOCK_WRONG_QUESTIONS: WrongQuestion[] = [
  {
    id: 'expert-system-vs-llm',
    question: '专家系统和大语言模型的核心区别是什么？',
    userAnswer: '专家系统也是通过大量数据训练出来的模型。',
    correctAnswer: '专家系统主要依赖人工编写规则和知识库，大语言模型主要依赖大规模数据预训练。',
    mistakeType: '发展阶段混淆',
    sourceLabel: 'AI 发展简史讲义 第 2 段',
  },
  {
    id: 'rag-reduces-hallucination',
    question: 'RAG 为什么能降低大模型幻觉？',
    userAnswer: '因为 RAG 会让模型变得更聪明。',
    correctAnswer: 'RAG 会先检索外部知识，再让模型基于可追溯资料回答，从而减少无依据生成。',
    mistakeType: '机制理解不清',
    sourceLabel: '大语言模型科普材料 第 2 段',
  },
  {
    id: 'supervised-learning-label',
    question: '监督学习中的"标签"指什么？',
    userAnswer: '模型自动生成的答案。',
    correctAnswer: '标签是训练数据中给出的正确结果或目标值，用来指导模型学习。',
    mistakeType: '基础概念错误',
    sourceLabel: '机器学习与深度学习入门 第 1 段',
  },
]

interface NotebookResponse {
  id: string
  name: string
  source_count: number
}

/**
 * 构建错题分组
 *
 * @param notebooks 笔记本列表
 * @returns 错题分组数组
 */
export function buildWrongQuestionGroups(notebooks: NotebookResponse[]): WrongQuestionGroup[] {
  return notebooks.map((notebook, index) => {
    const hasEnoughLearningContext = notebook.source_count > 0 && index === 0

    return {
      notebookId: notebook.id,
      notebookName: notebook.name,
      sourceCount: notebook.source_count,
      wrongQuestions: hasEnoughLearningContext ? MOCK_WRONG_QUESTIONS : [],
      frequentMistakes: hasEnoughLearningContext ? ['发展阶段混淆', '机制理解不清', '基础概念错误'] : [],
      quizHref: `/notebooks/${encodeURIComponent(notebook.id)}?studioTool=quiz`,
    }
  })
}
