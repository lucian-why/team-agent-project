/**
 * 学习画像 API 客户端

 * 封装学习画像相关的 API 调用。
 */

import type {
  StudentProfile,
  StudentProfileCreate,
  StudentProfileUpdate,
  LearningPath,
  LearningPathCreate,
  LearningPathUpdate,
} from './learning-profile-types'

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

// ==================== 学生画像 API ====================

export async function getStudentProfile(
  notebookId: string,
  token?: string
): Promise<StudentProfile> {
  return fetchAPI<StudentProfile>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/profile`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function upsertStudentProfile(
  notebookId: string,
  data: StudentProfileCreate,
  token?: string
): Promise<StudentProfile> {
  return fetchAPI<StudentProfile>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/profile`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function updateStudentProfile(
  notebookId: string,
  data: StudentProfileUpdate,
  token?: string
): Promise<StudentProfile> {
  return fetchAPI<StudentProfile>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/profile`,
    {
      method: 'PATCH',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function deleteStudentProfile(
  notebookId: string,
  token?: string
): Promise<void> {
  await fetchAPI(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/profile`,
    {
      method: 'DELETE',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

// ==================== 学习路径 API ====================

export async function getLearningPath(
  notebookId: string,
  token?: string
): Promise<LearningPath> {
  return fetchAPI<LearningPath>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/learning-path`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function upsertLearningPath(
  notebookId: string,
  data: LearningPathCreate,
  token?: string
): Promise<LearningPath> {
  return fetchAPI<LearningPath>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/learning-path`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}

export async function updateLearningPath(
  notebookId: string,
  data: LearningPathUpdate,
  token?: string
): Promise<LearningPath> {
  return fetchAPI<LearningPath>(
    `/learning/notebooks/${encodeURIComponent(notebookId)}/learning-path`,
    {
      method: 'PATCH',
      body: JSON.stringify(data),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  )
}
