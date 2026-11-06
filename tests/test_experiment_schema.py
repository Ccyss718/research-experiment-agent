import pytest
from pydantic import ValidationError

from app.models.experiment import ExperimentStatus
from app.schemas.experiment import ExperimentCreate

def test_experiment_create_accepts_valid_data():
    experiment = ExperimentCreate(
        name="Test Experiment",
        description="Schema Test",
        hypothesis="The schema should accept valid data"
    )

    assert experiment.name == "Test Experiment"
    assert experiment.status == ExperimentStatus.PLANNED

def test_experiment_strip_whitespace():
    experiment = ExperimentCreate(
        name="   Test Experiment   ",
        description="Schema Test",
        hypothesis="The schema should accept valid data"
    )
    assert experiment.name == "Test Experiment"

def test_experiment_name_required():
    with pytest.raises(ValidationError):
        ExperimentCreate(name="  ")