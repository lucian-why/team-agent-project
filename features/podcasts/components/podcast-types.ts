/**
 * 播客前端类型定义
 */

// ==================== 剧集相关 ====================

export interface PodcastEpisode {
  id: string
  name: string
  episodeProfile: Record<string, unknown>
  speakerProfile: Record<string, unknown>
  briefing: string
  content?: string
  audioFile?: string
  audioUrl?: string
  transcript?: Record<string, unknown>
  outline?: Record<string, unknown>
  created?: string
  jobStatus?: string
  errorMessage?: string
  commandId?: string
}

export interface PodcastEpisodeCreate {
  name: string
  episodeProfile: Record<string, unknown>
  speakerProfile: Record<string, unknown>
  briefing: string
  content?: string
  notebookId?: string
  episodeProfileName?: string
  speakerProfileName?: string
  briefingSuffix?: string
}

// ==================== 生成相关 ====================

export interface PodcastGenerationRequest {
  episodeProfile: string
  speakerProfile: string
  episodeName: string
  notebookId?: string
  content?: string
  briefingSuffix?: string
}

export interface PodcastGenerationResponse {
  jobId: string
  status: string
  message: string
  episodeProfile: string
  episodeName: string
}

// ==================== 任务状态 ====================

export interface PodcastJobStatus {
  jobId: string
  status: string
  message?: string
  errorMessage?: string
  startedAt?: string
  completedAt?: string
}
