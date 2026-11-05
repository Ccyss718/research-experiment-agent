from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentUpdate

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

    def list(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100,
        ) -> list[Experiment]:

        query = (
            select(Experiment)
            .order_by(Experiment.id)
            .offset(skip)
            .limit(limit)
        )

        return list(db.scalars(query).all())

    def update(
            self,
            db: Session,
            experiment: Experiment,
            data: ExperimentUpdate
    )-> Experiment:
        # 只获取用户实际提交的字段
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(experiment, field, value)

        db.flush()
        db.refresh(experiment)
        return experiment

    def delete(
            self,
            db: Session,
            experiment: Experiment,
    ) -> None:
        db.delete(experiment)
        db.flush()
