import pathlib
import re
import tomllib


ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_alembic_is_project_dependency() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())

    assert "alembic>=1.16.0" in pyproject["project"]["dependencies"]


def test_alembic_ini_points_to_local_migration_package() -> None:
    alembic_ini = ROOT / "alembic.ini"

    assert alembic_ini.exists()

    contents = alembic_ini.read_text()
    assert "script_location = alembic" in contents
    assert "prepend_sys_path = ." in contents


def test_alembic_env_uses_application_metadata_and_database_url() -> None:
    env_py = ROOT / "alembic" / "env.py"

    assert env_py.exists()

    contents = env_py.read_text()
    assert "from app.core.config import settings" in contents
    assert "from app.core.database import Base" in contents
    assert "import app.qna.model" in contents
    assert "target_metadata = Base.metadata" in contents
    assert 'config.set_main_option("sqlalchemy.url", settings.database_url)' in contents
    assert "async_engine_from_config" in contents


def test_initial_revision_creates_questions_table() -> None:
    versions_dir = ROOT / "alembic" / "versions"

    assert versions_dir.exists()

    revision_files = sorted(versions_dir.glob("*.py"))
    assert len(revision_files) == 1

    contents = revision_files[0].read_text()
    assert re.search(r"revision: str = .+", contents)
    assert re.search(r"down_revision: Union\[str, Sequence\[str\], None\] = None", contents)
    assert re.search(r"op\.create_table\(\s+\"questions\"", contents)
    assert 'sa.Column("id", sa.Integer(), nullable=False)' in contents
    assert 'sa.Column("title", sa.String(length=200), nullable=False)' in contents
    assert 'sa.Column("content", sa.Text(), nullable=False)' in contents
    assert 'op.create_index(op.f("ix_questions_id"), "questions", ["id"], unique=False)' in contents
    assert 'op.drop_table("questions")' in contents
