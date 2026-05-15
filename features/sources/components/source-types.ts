/**
 * 资料源前端类型定义
 */

// ==================== 资源资产 ====================

export interface Asset {
  filePath?: string
  url?: string
}

// ==================== 资料源 ====================

export interface Source {
  id: string
  title: string
  topics: string[]
  asset?: Asset
  fullText?: string
  ownerId: string
  embedded: boolean
  embeddedChunks: number
  fileAvailable?: boolean
  created?: string
  updated?: string
  commandId?: string
  status?: string
  processingInfo?: Record<string, unknown>
  notebooks: string[]
  insightsCount: number
}

export interface SourceList {
  id: string
  title?: string
  topics: string[]
  asset?: Asset
  embedded: boolean
  embeddedChunks: number
  insightsCount: number
  created?: string
  updated?: string
  commandId?: string
  status?: string
  processingInfo?: Record<string, unknown>
}

export interface SourceCreate {
  type: 'link' | 'upload' | 'text'
  notebookId?: string
  notebooks?: string[]
  url?: string
  content?: string
  title?: string
  filePath?: string
  transformations?: string[]
  embed?: boolean
  deleteSource?: boolean
  asyncProcessing?: boolean
}

export interface SourceUpdate {
  title?: string
  topics?: string[]
}

// ==================== 洞察 ====================

export interface SourceInsight {
  id: string
  sourceId: string
  insightType: string
  content: string
  created?: string
  updated?: string
}

export interface CreateInsightRequest {
  transformationId: string
}

export interface InsightCreationResponse {
  status: string
  message: string
  sourceId: string
  transformationId: string
  commandId?: string
}

// ==================== 状态 ====================

export interface SourceStatusResponse {
  status?: string
  message?: string
  processingInfo?: Record<string, unknown>
  commandId?: string
}
