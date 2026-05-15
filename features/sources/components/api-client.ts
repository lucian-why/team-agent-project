/**
 * 资料源 API 客户端
 */

import type {
  Source,
  SourceList,
  SourceCreate,
  SourceUpdate,
  SourceInsight,
  CreateInsightRequest,
  InsightCreationResponse,
  SourceStatusResponse,
} from './source-types'

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

// ==================== 资料源 API ====================

export async function getSources(
  token?: string,
  notebookId?: string,
  limit = 50,
  offset = 0,
  sortBy = 'updated',
  sortOrder = 'desc'
): Promise<SourceList[]> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
    sort_by: sortBy,
    sort_order: sortOrder,
  })
  if (notebookId) {
    params.set('notebook_id', notebookId)
  }
  return fetchAPI<SourceList[]>(
    `/sources?${params}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function getSource(
  sourceId: string,
  token?: string
): Promise<Source> {
  return fetchAPI<Source>(
    `/sources/${encodeURIComponent(sourceId)}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function createSource(
  data: SourceCreate,
  token?: string
): Promise<Source> {
  return fetchAPI<Source>(
    '/sources',
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function updateSource(
  sourceId: string,
  data: SourceUpdate,
  token?: string
): Promise<Source> {
  return fetchAPI<Source>(
    `/sources/${encodeURIComponent(sourceId)}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function deleteSource(
  sourceId: string,
  token?: string
): Promise<void> {
  await fetchAPI(
    `/sources/${encodeURIComponent(sourceId)}`,
    {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function getSourceStatus(
  sourceId: string,
  token?: string
): Promise<SourceStatusResponse> {
  return fetchAPI<SourceStatusResponse>(
    `/sources/${encodeURIComponent(sourceId)}/status`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function retrySource(
  sourceId: string,
  token?: string
): Promise<Source> {
  return fetchAPI<Source>(
    `/sources/${encodeURIComponent(sourceId)}/retry`,
    {
      method: 'POST',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

// ==================== 洞察 API ====================

export async function getSourceInsights(
  sourceId: string,
  token?: string
): Promise<SourceInsight[]> {
  return fetchAPI<SourceInsight[]>(
    `/sources/${encodeURIComponent(sourceId)}/insights`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function createSourceInsight(
  sourceId: string,
  data: CreateInsightRequest,
  token?: string
): Promise<InsightCreationResponse> {
  return fetchAPI<InsightCreationResponse>(
    `/sources/${encodeURIComponent(sourceId)}/insights`,
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}
