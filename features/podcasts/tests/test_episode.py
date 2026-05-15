"""
播客领域模型测试
"""

import pytest
from ..domain.episode import (
    PodcastEpisodeBase,
    PodcastEpisodeCreate,
    PodcastEpisode,
    PodcastGenerationRequest,
    PodcastGenerationResponse,
    PodcastJobStatus,
)


class TestPodcastEpisode:
    """播客剧集模型测试"""

    def test_episode_base_defaults(self):
        """测试基础模型默认值"""
        base = PodcastEpisodeBase(
            name="Test Episode",
        )

        assert base.name == "Test Episode"
        assert base.episode_profile == {}
        assert base.speaker_profile == {}
        assert base.briefing == ""
        assert base.content is None

    def test_episode_create(self):
        """测试创建剧集请求"""
        request = PodcastEpisodeCreate(
            name="Test Episode",
            episode_profile={"style": "interview"},
            speaker_profile={"voice": "male"},
            briefing="This is a test episode.",
            notebook_id="nb-123",
            episode_profile_name="interview",
            speaker_profile_name="male",
        )

        assert request.name == "Test Episode"
        assert request.notebook_id == "nb-123"
        assert request.episode_profile_name == "interview"

    def test_episode_complete(self):
        """测试完整剧集模型"""
        episode = PodcastEpisode(
            id="episode-123",
            name="Test Episode",
            episode_profile={"style": "interview"},
            speaker_profile={"voice": "male"},
            briefing="This is a test episode.",
            content="Episode content here.",
            audio_file="/audio/test.mp3",
            audio_url="/api/podcasts/episodes/episode-123/audio",
            transcript={"text": "Full transcript"},
            outline={"sections": ["Intro", "Main", "Conclusion"]},
            created="2024-01-01T00:00:00",
            job_status="completed",
            error_message=None,
            command_id="cmd-123",
        )

        assert episode.id == "episode-123"
        assert episode.audio_file == "/audio/test.mp3"
        assert episode.job_status == "completed"
        assert episode.transcript is not None

    def test_episode_from_attributes(self):
        """测试从字典创建剧集"""
        data = {
            "id": "episode-123",
            "name": "Test Episode",
            "episode_profile": {"style": "interview"},
            "speaker_profile": {"voice": "male"},
            "briefing": "This is a test episode.",
            "audio_file": "/audio/test.mp3",
            "created": "2024-01-01T00:00:00",
            "job_status": "completed",
        }

        episode = PodcastEpisode.model_validate(data)

        assert episode.id == data["id"]
        assert episode.name == data["name"]
        assert episode.audio_file == data["audio_file"]


class TestPodcastGeneration:
    """播客生成模型测试"""

    def test_generation_request(self):
        """测试生成请求"""
        request = PodcastGenerationRequest(
            episode_profile="interview",
            speaker_profile="male",
            episode_name="Test Episode",
            notebook_id="nb-123",
            content="Optional content.",
            briefing_suffix="Additional info.",
        )

        assert request.episode_profile == "interview"
        assert request.speaker_profile == "male"
        assert request.episode_name == "Test Episode"
        assert request.notebook_id == "nb-123"

    def test_generation_response(self):
        """测试生成响应"""
        response = PodcastGenerationResponse(
            job_id="job-123",
            status="submitted",
            message="Generation started.",
            episode_profile="interview",
            episode_name="Test Episode",
        )

        assert response.job_id == "job-123"
        assert response.status == "submitted"
        assert response.episode_profile == "interview"


class TestPodcastJobStatus:
    """播客任务状态模型测试"""

    def test_job_status(self):
        """测试任务状态"""
        status = PodcastJobStatus(
            job_id="job-123",
            status="running",
            message="Processing...",
            error_message=None,
            started_at="2024-01-01T00:00:00",
            completed_at=None,
        )

        assert status.job_id == "job-123"
        assert status.status == "running"
        assert status.started_at == "2024-01-01T00:00:00"
        assert status.completed_at is None

    def test_job_status_completed(self):
        """测试完成的任务状态"""
        status = PodcastJobStatus(
            job_id="job-123",
            status="completed",
            message="Generation completed.",
            started_at="2024-01-01T00:00:00",
            completed_at="2024-01-01T00:05:00",
        )

        assert status.status == "completed"
        assert status.completed_at == "2024-01-01T00:05:00"

    def test_job_status_failed(self):
        """测试失败的任务状态"""
        status = PodcastJobStatus(
            job_id="job-123",
            status="failed",
            message="Generation failed.",
            error_message="API limit exceeded.",
            started_at="2024-01-01T00:00:00",
            completed_at="2024-01-01T00:01:00",
        )

        assert status.status == "failed"
        assert status.error_message == "API limit exceeded."
