from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.experiment import ExperimentStatus

class ExperimentCreate(BaseModel):
    # 去除首尾空格
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    hypothesis: str | None = None
    status: ExperimentStatus = ExperimentStatus.PLANNED

class ExperimentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    hypothesis: str | None = None
    status: ExperimentStatus | None = None

class ExperimentResponse(BaseModel):
    # 允许Pydantic从SQLalchemyORM对象中读取属性如experiment.id
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    hypothesis: str | None
    status: ExperimentStatus
    created_at: datetime
    updated_at: datetime