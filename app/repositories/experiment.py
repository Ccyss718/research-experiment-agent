from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment import Experiment

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

