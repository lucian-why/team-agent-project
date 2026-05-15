/**
 * 资料源组件导出
 */

// 类型
export type {
  Asset,
  Source,
  SourceList,
  SourceCreate,
  SourceUpdate,
  SourceInsight,
  CreateInsightRequest,
  InsightCreationResponse,
  SourceStatusResponse,
} from './source-types'

// API 客户端
export {
  getSources,
  getSource,
  createSource,
  updateSource,
  deleteSource,
  getSourceStatus,
  retrySource,
  getSourceInsights,
  createSourceInsight,
} from './api-client'
