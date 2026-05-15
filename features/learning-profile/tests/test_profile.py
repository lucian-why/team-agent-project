"""
学习画像领域模型测试
"""

import pytest
from datetime import datetime

from ..domain.profile import (
    WrongQuestion,
    WrongQuestionGroup,
    StudentProfileBase,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfile,
    LearningPathNode,
    LearningPathBase,
    LearningPathCreate,
    LearningPathUpdate,
    LearningPath,
)


class TestWrongQuestion:
    """错题模型测试"""

    def test_wrong_question_create(self):
        """测试创建错题模型"""
        question = WrongQuestion(
            id="q1",
            question="什么是 Python？",
            userAnswer="一种编程语言",
            correctAnswer="Python 是一种高级编程语言",
            mistakeType="概念模糊",
            sourceLabel="Python 入门 第 1 段",
        )

        assert question.id == "q1"
        assert question.question == "什么是 Python？"
        assert question.mistakeType == "概念模糊"

    def test_wrong_question_group_create(self):
        """测试创建错题分组模型"""
        group = WrongQuestionGroup(
            notebookId="nb-1",
            notebookName="Python 入门",
            sourceCount=5,
            wrongQuestions=[],
            frequentMistakes=["概念模糊", "语法错误"],
            quizHref="/notebooks/nb-1?studioTool=quiz",
        )

        assert group.notebookId == "nb-1"
        assert group.sourceCount == 5
        assert len(group.frequentMistakes) == 2


class TestStudentProfile:
    """学生画像模型测试"""

    def test_student_profile_base_defaults(self):
        """测试基础模型默认值"""
        base = StudentProfileBase()

        assert base.major is None
        assert base.course is None
        assert base.learning_goal is None
        assert base.knowledge_level is None
        assert base.cognitive_style is None
        assert base.weak_points == []
        assert base.interest_tags == []
        assert base.practice_preference is None
        assert base.pace_preference is None
        assert base.resource_preference is None
        assert base.confidence == 0.0
        assert base.evidence_summary is None
        assert base.source_ids == []
        assert base.created_by == "user"
        assert base.metadata == {}

    def test_student_profile_base_with_data(self):
        """测试基础模型带数据"""
        base = StudentProfileBase(
            major="计算机科学",
            course="Python 编程",
            learning_goal="掌握基础语法",
            knowledge_level="初学者",
            cognitive_style="视觉型",
            weak_points=["循环", "函数"],
            interest_tags=["AI", "数据分析"],
            practice_preference="多做练习",
            pace_preference="慢速",
            resource_preference="视频教程",
            confidence=0.8,
            evidence_summary="基于 3 次测验结果",
        )

        assert base.major == "计算机科学"
        assert base.confidence == 0.8
        assert "循环" in base.weak_points

    def test_student_profile_create(self):
        """测试创建画像请求模型"""
        request = StudentProfileCreate(
            notebook_id="nb-123",
            major="计算机科学",
            course="Python 编程",
        )

        assert request.notebook_id == "nb-123"
        assert request.major == "计算机科学"

    def test_student_profile_create_required_fields(self):
        """测试创建画像请求模型必填字段"""
        with pytest.raises(Exception):
            StudentProfileCreate()  # notebook_id 是必填的

    def test_student_profile_update_partial(self):
        """测试更新画像请求模型部分更新"""
        update = StudentProfileUpdate(
            major="数据科学",
            confidence=0.9,
        )

        assert update.major == "数据科学"
        assert update.confidence == 0.9
        assert update.course is None  # 未更新的字段为 None

    def test_student_profile_update_all_none(self):
        """测试更新画像请求模型全部为 None"""
        update = StudentProfileUpdate()

        assert update.major is None
        assert update.course is None
        assert update.learning_goal is None

    def test_student_profile_complete(self):
        """测试完整画像模型"""
        profile = StudentProfile(
            id="profile-123",
            notebook_id="nb-456",
            major="计算机科学",
            course="Python 编程",
            learning_goal="掌握基础语法",
            knowledge_level="初学者",
            cognitive_style="视觉型",
            weak_points=["循环", "函数"],
            interest_tags=["AI", "数据分析"],
            practice_preference="多做练习",
            pace_preference="慢速",
            resource_preference="视频教程",
            confidence=0.8,
            evidence_summary="基于 3 次测验结果",
            source_ids=["src-1", "src-2"],
            created_by="user",
            metadata={"key": "value"},
            schema_version=1,
            created="2024-01-01T00:00:00",
            updated="2024-01-02T00:00:00",
        )

        assert profile.id == "profile-123"
        assert profile.notebook_id == "nb-456"
        assert profile.schema_version == 1
        assert profile.created == "2024-01-01T00:00:00"

    def test_student_profile_from_attributes(self):
        """测试从字典创建画像（from_attributes 模式）"""
        data = {
            "id": "profile-123",
            "notebook_id": "nb-456",
            "major": "计算机科学",
            "course": "Python 编程",
            "learning_goal": "掌握基础语法",
            "knowledge_level": "初学者",
            "cognitive_style": "视觉型",
            "weak_points": ["循环", "函数"],
            "interest_tags": ["AI", "数据分析"],
            "practice_preference": "多做练习",
            "pace_preference": "慢速",
            "resource_preference": "视频教程",
            "confidence": 0.8,
            "evidence_summary": "基于 3 次测验结果",
            "source_ids": ["src-1", "src-2"],
            "created_by": "user",
            "metadata": {"key": "value"},
            "schema_version": 1,
            "created": "2024-01-01T00:00:00",
            "updated": "2024-01-02T00:00:00",
        }

        profile = StudentProfile.model_validate(data)

        assert profile.id == data["id"]
        assert profile.notebook_id == data["notebook_id"]
        assert profile.major == data["major"]


class TestLearningPath:
    """学习路径模型测试"""

    def test_learning_path_node_create(self):
        """测试创建学习路径节点"""
        node = LearningPathNode(
            id="node-1",
            title="Python 基础",
            description="学习 Python 基础语法",
            learning_objectives=["变量", "循环", "函数"],
            prerequisites=[],
            recommended_source_ids=["src-1"],
            recommended_resource_types=["video", "article"],
            estimated_minutes=60,
            status="todo",
            mastery_score=0.0,
        )

        assert node.id == "node-1"
        assert node.title == "Python 基础"
        assert node.estimated_minutes == 60
        assert node.status == "todo"
        assert len(node.learning_objectives) == 3

    def test_learning_path_node_defaults(self):
        """测试学习路径节点默认值"""
        node = LearningPathNode(
            id="node-1",
            title="Python 基础",
        )

        assert node.description == ""
        assert node.learning_objectives == []
        assert node.prerequisites == []
        assert node.recommended_source_ids == []
        assert node.recommended_resource_types == []
        assert node.estimated_minutes == 30
        assert node.status == "todo"
        assert node.mastery_score == 0.0

    def test_learning_path_base_defaults(self):
        """测试学习路径基础模型默认值"""
        base = LearningPathBase()

        assert base.profile_id is None
        assert base.title == "学习路径"
        assert base.course == ""
        assert base.nodes == []
        assert base.current_node_id is None
        assert base.status == "draft"
        assert base.source_ids == []
        assert base.created_by == "user"
        assert base.metadata == {}

    def test_learning_path_create(self):
        """测试创建学习路径请求模型"""
        request = LearningPathCreate(
            notebook_id="nb-123",
            title="Python 学习路径",
            course="Python 编程",
        )

        assert request.notebook_id == "nb-123"
        assert request.title == "Python 学习路径"

    def test_learning_path_create_required_fields(self):
        """测试创建学习路径请求模型必填字段"""
        with pytest.raises(Exception):
            LearningPathCreate()  # notebook_id 是必填的

    def test_learning_path_update_partial(self):
        """测试更新学习路径请求模型部分更新"""
        update = LearningPathUpdate(
            title="更新后的路径",
            status="active",
        )

        assert update.title == "更新后的路径"
        assert update.status == "active"
        assert update.course is None

    def test_learning_path_complete(self):
        """测试完整学习路径模型"""
        nodes = [
            LearningPathNode(id="node-1", title="基础"),
            LearningPathNode(id="node-2", title="进阶"),
        ]

        path = LearningPath(
            id="path-123",
            notebook_id="nb-456",
            profile_id="profile-789",
            title="Python 学习路径",
            course="Python 编程",
            nodes=nodes,
            current_node_id="node-1",
            status="active",
            source_ids=["src-1"],
            created_by="user",
            metadata={"difficulty": "beginner"},
            schema_version=1,
            created="2024-01-01T00:00:00",
            updated="2024-01-02T00:00:00",
        )

        assert path.id == "path-123"
        assert path.notebook_id == "nb-456"
        assert len(path.nodes) == 2
        assert path.current_node_id == "node-1"
        assert path.status == "active"

    def test_learning_path_from_attributes(self):
        """测试从字典创建学习路径（from_attributes 模式）"""
        data = {
            "id": "path-123",
            "notebook_id": "nb-456",
            "profile_id": "profile-789",
            "title": "Python 学习路径",
            "course": "Python 编程",
            "nodes": [
                {"id": "node-1", "title": "基础"},
                {"id": "node-2", "title": "进阶"},
            ],
            "current_node_id": "node-1",
            "status": "active",
            "source_ids": ["src-1"],
            "created_by": "user",
            "metadata": {"difficulty": "beginner"},
            "schema_version": 1,
            "created": "2024-01-01T00:00:00",
            "updated": "2024-01-02T00:00:00",
        }

        path = LearningPath.model_validate(data)

        assert path.id == data["id"]
        assert path.notebook_id == data["notebook_id"]
        assert len(path.nodes) == 2
