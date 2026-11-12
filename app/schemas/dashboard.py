from pydantic import BaseModel
from typing import List


class StageCount(BaseModel):
    stage: str
    count: int


class DashboardSummary(BaseModel):
    total_clients: int
    total_leads: int
    won_value: float
    pipeline_value: float
    conversion_rate: float
    opportunities_by_stage: List[StageCount]