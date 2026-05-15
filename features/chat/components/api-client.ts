/**
 * 聊天 API 客户端
 */

import type {
  ChatSession,
  ChatSessionCreate,
  ChatSessionUpdate,
  ChatSessionWithMessages,
  ExecuteChatRequest,
  ExecuteChatResponse,
  BuildContextRequest,
  BuildContextResponse,
} from './chat-types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5055'

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(error.detail || 'API request failed')
  }

  return response.json()
}

// ==================== 会话 API ====================

export async function getChatSessions(
  notebookId: string,
  token?: string,
  limit = 50,
  offset = 0
): Promise<ChatSession[]> {
  const params = new URLSearchParams({
    notebook_id: notebookId,
    limit: limit.toString(),
    offset: offset.toString(),
  })
  return fetchAPI<ChatSession[]>(
    `/chat/sessions?${params}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function createChatSession(
  data: ChatSessionCreate,
  token?: string
): Promise<ChatSession> {
  return fetchAPI<ChatSession>(
    '/chat/sessions',
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function getChatSession(
  sessionId: string,
  token?: string
): Promise<ChatSessionWithMessages> {
  return fetchAPI<ChatSessionWithMessages>(
    `/chat/sessions/${encodeURIComponent(sessionId)}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function updateChatSession(
  sessionId: string,
  data: ChatSessionUpdate,
  token?: string
): Promise<ChatSession> {
  return fetchAPI<ChatSession>(
    `/chat/sessions/${encodeURIComponent(sessionId)}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function deleteChatSession(
  sessionId: string,
  token?: string
): Promise<void> {
  await fetchAPI(
    `/chat/sessions/${encodeURIComponent(sessionId)}`,
    {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

// ==================== 聊天执行 API ====================

export async function executeChat(
  data: ExecuteChatRequest,
  token?: string
): Promise<ExecuteChatResponse> {
  return fetchAPI<ExecuteChatResponse>(
    '/chat/execute',
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function buildContext(
  data: BuildContextRequest,
  token?: string
): Promise<BuildContextResponse> {
  return fetchAPI<BuildContextResponse>(
    '/chat/context',
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}
