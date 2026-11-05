from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate

class ExperimentRepository:
    def get_by_id(
            self,
            db: Session,
            experiment_id: int,
    ) -> Experiment | None :
        query = select(Experiment).where(Experiment.id == experiment_id)
        exp = db.scalar(query)
        # scalar找不到会返回None
        return exp

    def create(
            self,
            db: Session,
            data: ExperimentCreate
    ) -> Experiment:
        exp_data = data.model_dump()
        experiment = Experiment(**exp_data)
        db.add(experiment)
        db.flush()
        db.refresh(experiment)
        
        return experiment



