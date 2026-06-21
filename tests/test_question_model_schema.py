from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from sqlalchemy import String, Text, inspect

from app.qna.model import Question
from app.qna.schema import QuestionCreate, QuestionRead, QuestionUpdate


def test_question_model_table_definition() -> None:
    mapper = inspect(Question)
    columns = mapper.columns

    assert Question.__tablename__ == "questions"
    assert columns["id"].primary_key
    assert not columns["title"].nullable
    assert isinstance(columns["title"].type, String)
    assert columns["title"].type.length == 200
    assert not columns["content"].nullable
    assert isinstance(columns["content"].type, Text)
    assert not columns["created_at"].nullable
    assert not columns["updated_at"].nullable


def test_question_create_validates_required_fields() -> None:
    question = QuestionCreate(title="FastAPI question", content="What does Pydantic do?")

    assert question.model_dump() == {
        "title": "FastAPI question",
        "content": "What does Pydantic do?",
    }

    with pytest.raises(ValidationError):
        QuestionCreate(title="", content="body")


def test_question_update_allows_partial_payload() -> None:
    assert QuestionUpdate().model_dump(exclude_unset=True) == {}
    assert QuestionUpdate(title="Updated title").model_dump(exclude_unset=True) == {
        "title": "Updated title"
    }


def test_question_read_serializes_from_orm_model() -> None:
    now = datetime(2026, 6, 21, 12, 0, tzinfo=UTC)
    question = Question(
        id=1,
        title="ORM question",
        content="Why separate SQLAlchemy and Pydantic?",
        created_at=now,
        updated_at=now,
    )

    response = QuestionRead.model_validate(question)

    assert response.model_dump() == {
        "id": 1,
        "title": "ORM question",
        "content": "Why separate SQLAlchemy and Pydantic?",
        "created_at": now,
        "updated_at": now,
    }
