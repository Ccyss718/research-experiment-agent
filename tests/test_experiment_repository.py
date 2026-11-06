from email.errors import NonPrintableDefect

from app.models.experiment import ExperimentStatus
from app.repositories.experiment import ExperimentRepository
from app.schemas.experiment import ExperimentCreate, ExperimentUpdate

def test_repository_can_create_and_get_experiment(db):
    repository = ExperimentRepository()

    payload = ExperimentCreate(
        name="Repository test",
        description="Test description",
        hypothesis="The repository should save the experiment",
    )

    created = repository.create(db, payload)
    found = repository.get_by_id(db, created.id)

    assert created.id is not None
    assert found is not None
    assert found.name == "Repository test"

def test_repository_returns_none_for_missing_id(db):
    repository = ExperimentRepository()

    result = repository.get_by_id(db, 99999)

    assert result is None

def test_repository_list_experiments(db):
    repository = ExperimentRepository()

    repository.create(db, ExperimentCreate(name="Experiment A"))
    repository.create(db, ExperimentCreate(name="Experiment B"))

    experiments = repository.list(db)

    assert len(experiments) == 2
    assert experiments[0].name == "Experiment A"
    assert experiments[1].name == "Experiment B"

def test_repository_list_supports_pagination(db):
    repository = ExperimentRepository()

    repository.create(db, ExperimentCreate(name="Experiment A"))
    repository.create(db, ExperimentCreate(name="Experiment B"))
    repository.create(db, ExperimentCreate(name="Experiment C"))

    experiments = repository.list(
        db,
        skip=1,
        limit=1,
    )

    assert len(experiments) == 1
    assert experiments[0].name == "Experiment B"

def test_repository_updates_experiment(db):
    repository = ExperimentRepository()

    experiment = repository.create(
        db,
        ExperimentCreate(
            name="Original experiment",
            description="Original description"
        ),
    )

    updated = repository.update(
        db,
        experiment,
        ExperimentUpdate(
            name="Updated experiment",
            status=ExperimentStatus.RUNNING,
        )
    )

    assert updated.id == experiment.id
    assert updated.name == "Updated experiment"
    assert updated.status == ExperimentStatus.RUNNING
    assert updated.description == "Original description"

def test_repository_deletes_experiment(db):
    repository = ExperimentRepository()

    experiment = repository.create(
        db,
        ExperimentCreate(name="Experiment to delete")
    )

    repository.delete(db, experiment)

    result = repository.get_by_id(db, experiment.id)

    assert result is None