from app.schemas.experiment import ExperimentCreate, ExperimentUpdate

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

    def create(
            self,
            db: Session,
            data: ExperimentCreate,
) -> Experiment:
        try:
            experiment = self.repository.create(db, data)
            db.commit()
            db.refresh(experiment)
            return experiment
        except Exception:
            db.rollback()
            raise

    def list(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Experiment]:
        return self.repository.list(
            db,
            skip=skip,
            limit=limit,
        )

    def update(
            self,
            db: Session,
            experiment_id: int,
            data: ExperimentUpdate
    ) -> Experiment:
        try:
            experiment = self.get_by_id(db, experiment_id)
            experiment = self.repository.update(db,experiment, data)
            db.commit()
            db.refresh(experiment)
            return experiment
        except Exception:
            db.rollback()
            raise

    def delete(
            self,
            db: Session,
            experiment_id: int,
    ) -> None:
        try:
            experiment = self.get_by_id(db, experiment_id)
            self.repository.delete(db,experiment)
            db.commit()
        except Exception:
            db.rollback()
            raise
        
