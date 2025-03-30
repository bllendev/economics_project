from django.db import models
from django.utils.module_loading import import_string
from django.urls import path
from simple_history.models import HistoricalRecords
import uuid
import re

import logging

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    created_by = models.ForeignKey(
        "users.User", blank=True, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)

    def get_absolute_url(self):
        return f"/{self.get_model_name_id()}/detail/{self.pk}/"

    def get_update_url(self):
        return f"/{self.get_model_name_id()}/update/{self.pk}/"

    def get_create_url(self):
        return f"/{self.get_model_name_id()}/create/"

    def get_reset_url(self):
        return f"/{self.get_model_name_id()}/reset/{self.pk}/"

    def get_delete_url(self):
        return f"/{self.get_model_name_id()}/delete/{self.pk}/"

    @property
    def form_trigger(self):
        return f"{self.get_model_name_id()}-trigger"

    @classmethod
    def get_urls(cls):
        """
        Generate URL patterns for the following views:
        - DetailView
        - CreateView
        - ResetView
        - DeleteView
        - UpdateView
        """
        app_label = cls._meta.app_label
        base_path = f"{app_label}.views"

        urls = []
        view_suffixes = [
            "DetailView",
            "CreateView",
            "ResetView",
            "DeleteView",
            "UpdateView",
        ]
        url_suffixes = [
            "detail/<uuid:pk>/",
            "create/",
            "reset/<uuid:pk>/",
            "delete/<uuid:pk>/",
            "update/<uuid:pk>/",
        ]

        for view_suffix, url_suffix in zip(view_suffixes, url_suffixes):
            pattern = None
            try:
                view_path = f"{base_path}.{cls.get_model_name()}{view_suffix}"
                view = import_string(view_path)
                _url_name = view_suffix.lower().replace(
                    "view", ""
                )  # DetailView -> detail
                url_name = f"{cls.get_model_name_id()}-{_url_name}"  # report-detail

                pattern = path(
                    f"{cls.get_model_name_id()}/{url_suffix}",
                    view.as_view(),
                    name=url_name,
                )
                urls.append(pattern)
            except ImportError as e:
                logger.warning(
                    f"""
                    {e} | {base_path}.{cls.get_model_name()}{view_suffix}
                    Doesn't Exist yet for the URL pattern:
                    {f"{cls.get_model_name_id()}/{url_suffix}"}
                """
                )
                pass

            logger.debug(f"URL pattern: {pattern}")
        return urls

    @classmethod
    def get_model_name(cls):
        return cls.__name__

    @classmethod
    def get_model_name_id(cls):
        return re.sub(r"(?<!^)(?=[A-Z])", "-", cls.get_model_name()).lower()

    @property
    def model_name_id(self):
        return self.get_model_name_id()

    class Meta:
        abstract = True
