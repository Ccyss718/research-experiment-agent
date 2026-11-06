import pytest

from app.models.experiment import ExperimentStatus
from app.schemas.experiment import ExperimentUpdate

from app.schemas.experiment import ExperimentCreate
from app.services.experiment import ExperimentService, ExperimentNotFoundError

def test_service_creates_experiment(db):
    service = ExperimentService()

    experiment = service.create(
        db,
        ExperimentCreate(
            name="Service test experiment",
            description="Create through service"
        )
    )

    assert experiment.id is not None
    assert experiment.name == "Service test experiment"

    found = service.get_by_id(db, experiment.id)

    assert found.id is not None
    assert found.name == "Service test experiment"

def test_service_raises_when_experiment_not_found(db):
    service = ExperimentService()

    with pytest.raises(ExperimentNotFoundError):
        service.get_by_id(db, 9999)

def test_service_update_experiment(db):
    service = ExperimentService()

    created = service.create(
        db,
        ExperimentCreate(
            name="Original experiment",
            description="Keep this description"
        )
    )

    updated = service.update(
        db,
        created.id,
        ExperimentUpdate(
            name="Updated experiment",
            status=ExperimentStatus.RUNNING,
        )
    )

    assert updated.id == created.id
    assert updated.name == "Updated experiment"
    assert updated.status == ExperimentStatus.RUNNING
    assert updated.description == "Keep this description"

def test_service_deletes_experiment(db):
    service = ExperimentService()

    created = service.create(
        db,
        ExperimentCreate(
            name="Experiment to delete"
        )
    )

    service.delete(db, created.id)

    with pytest.raises(ExperimentNotFoundError):
        service.get_by_id(db, created.id)