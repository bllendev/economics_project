from django.db import models
from common.models import BaseModel


class AI(BaseModel):
    settings = models.ForeignKey("ai.AISettings", on_delete=models.SET_NULL, null=True)
