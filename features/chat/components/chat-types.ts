/**
 * 聊天前端类型定义
 */

// ==================== 消息相关 ====================

export interface ChatMessage {
  id: string
  type: 'human' | 'ai' | 'unknown'
  content: string
  timestamp?: string
  citations: Citation[]
}

export interface Citation {
  sourceId: string
  sourceTitle?: string
  content: string
  relevance?: number
}

// ==================== 会话相关 ====================

export interface ChatSession {
  id: string
  title: string
  notebookId?: string
  modelOverride?: string
  ownerId: string
  created?: string
  updated?: string
  messageCount?: number
}

export interface ChatSessionWithMessages extends ChatSession {
  messages: ChatMessage[]
}

export interface ChatSessionCreate {
  notebookId: string
  title?: string
  modelOverride?: string
}

export interface ChatSessionUpdate {
  title?: string
  modelOverride?: string
}

// ==================== 聊天执行 ====================

export interface ExecuteChatRequest {
  sessionId: string
  message: string
  context: ChatContext
  modelOverride?: string
  notebookId?: string
  assistantId?: string
}

export interface ExecuteChatResponse {
  sessionId: string
  messages: ChatMessage[]
  agentTriggered?: AgentTrigger
}

export interface AgentTrigger {
  intent: string
  agentChain: string[]
  notebookId?: string
}

// ==================== 上下文 ====================

export interface ChatContext {
  sources: ContextSource[]
  notes: ContextNote[]
}

export interface ContextSource {
  id: string
  title: string
  content: string
  insights?: string[]
}

export interface ContextNote {
  id: string
  content: string
}

export interface BuildContextRequest {
  notebookId: string
  contextConfig: Record<string, Record<string, string>>
}

export interface BuildContextResponse {
  context: ChatContext
  tokenCount: number
  charCount: number
}
