from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.experiment import ExperimentResponse
from app.services.experiment import (
    ExperimentNotFoundError,
    ExperimentService,
)

router = APIRouter(
    prefix="/experiments",
    tags=["experiments"],
)
# 模块化写法，注册路由模块由main统一挂载

@router.get(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(
        experiment_id: int,
        db: Session = Depends(get_db),
):
    service = ExperimentService()
    try:
        result = service.get_by_id(db, experiment_id)
    except ExperimentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        ) from exc
    # 保留异常原因记录
    return result




