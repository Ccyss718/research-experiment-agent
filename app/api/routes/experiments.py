from fastapi import Query, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.experiment import ExperimentResponse, ExperimentCreate, ExperimentUpdate
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

@router.post(
    "/",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_experiment(
        data: ExperimentCreate,
        db: Session = Depends(get_db)
):
    service = ExperimentService()
    return service.create(db, data)

@router.get(
    "/",
    response_model=list[ExperimentResponse]
)
def list_experiment(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=1, le=100),
        db: Session = Depends(get_db),
):
    service = ExperimentService()
    return service.list(
        db,
        skip=skip,
        limit=limit
    )

@router.patch(
    "/{experiment_id}",
    response_model=ExperimentResponse,
)
def update_experiment(
        experiment_id: int,
        data: ExperimentUpdate,
        db: Session = Depends(get_db)
):
    service = ExperimentService()

    try:
        return service.update(
            db,
            experiment_id,
            data,
        )
    except ExperimentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )from exc

@router.delete(
    "/{experiment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_experiment(
        experiment_id: int,
        db: Session = Depends(get_db)
) -> None:
    service = ExperimentService()

    try:
        service.delete(db, experiment_id)
    except ExperimentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )from exc




