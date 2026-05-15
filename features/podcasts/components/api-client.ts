/**
 * 播客 API 客户端
 */

import type {
  PodcastEpisode,
  PodcastGenerationRequest,
  PodcastGenerationResponse,
  PodcastJobStatus,
} from './podcast-types'

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

// ==================== 剧集 API ====================

export async function getPodcastEpisodes(
  token?: string,
  limit = 50,
  offset = 0
): Promise<PodcastEpisode[]> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  })
  return fetchAPI<PodcastEpisode[]>(
    `/podcasts/episodes?${params}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function getPodcastEpisode(
  episodeId: string,
  token?: string
): Promise<PodcastEpisode> {
  return fetchAPI<PodcastEpisode>(
    `/podcasts/episodes/${encodeURIComponent(episodeId)}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function deletePodcastEpisode(
  episodeId: string,
  token?: string
): Promise<void> {
  await fetchAPI(
    `/podcasts/episodes/${encodeURIComponent(episodeId)}`,
    {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

// ==================== 生成 API ====================

export async function generatePodcast(
  data: PodcastGenerationRequest,
  token?: string
): Promise<PodcastGenerationResponse> {
  return fetchAPI<PodcastGenerationResponse>(
    '/podcasts/generate',
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function getPodcastJobStatus(
  jobId: string,
  token?: string
): Promise<PodcastJobStatus> {
  return fetchAPI<PodcastJobStatus>(
    `/podcasts/jobs/${encodeURIComponent(jobId)}`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function retryPodcastEpisode(
  episodeId: string,
  token?: string
): Promise<PodcastGenerationResponse> {
  return fetchAPI<PodcastGenerationResponse>(
    `/podcasts/episodes/${encodeURIComponent(episodeId)}/retry`,
    {
      method: 'POST',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}
