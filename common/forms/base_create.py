from django import forms
import logging

logger = logging.getLogger(__name__)


class BaseCreateForm(forms.ModelForm):
    class Meta:
        model = None
        exclude = ["created_by", "created_at", "id", "history"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.created_by = kwargs.pop("created_by", None)
        self.redirect = None
        super(BaseCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        obj = super(BaseCreateForm, self).save(commit=False)

        # ensure created_by is populated
        if self.created_by and not obj.created_by:
            logger.info(f"setting created_by field to {self.created_by}")
            obj.created_by = self.created_by

        # commit !
        if commit:
            obj.save()

        return obj

