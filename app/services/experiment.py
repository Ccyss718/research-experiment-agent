
from sqlalchemy.orm import Session

from app.models.experiment import Experiment

from app.repositories.experiment import ExperimentRepository

class ExperimentNotFoundError(Exception):
    pass

class ExperimentService:
    def __init__(self, repository: ExperimentRepository | None = None):
        self.repository = repository or ExperimentRepository()
    def get_by_id(
            self,
            db: Session,
            experiment_id: int,
    ) -> Experiment:
        result = self.repository.get_by_id(db, experiment_id)
        if result is not None:
            return result

        raise ExperimentNotFoundError(
            f"Experiment {experiment_id} not found")
