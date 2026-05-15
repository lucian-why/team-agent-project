/**
 * 聊天组件导出
 */

// 类型
export type {
  ChatMessage,
  Citation,
  ChatSession,
  ChatSessionWithMessages,
  ChatSessionCreate,
  ChatSessionUpdate,
  ExecuteChatRequest,
  ExecuteChatResponse,
  AgentTrigger,
  ChatContext,
  ContextSource,
  ContextNote,
  BuildContextRequest,
  BuildContextResponse,
} from './chat-types'

// API 客户端
export {
  getChatSessions,
  createChatSession,
  getChatSession,
  updateChatSession,
  deleteChatSession,
  executeChat,
  buildContext,
} from './api-client'
