from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.urls.exceptions import NoReverseMatch

from common.forms import BaseCreateForm
from ..views.notification_mixin import NotificationMixin

import logging

logger = logging.getLogger(__name__)


class BaseCreateUpdateView(LoginRequiredMixin, NotificationMixin, CreateView):
    """Base Creation View used to create HTMX Creation Forms, leveraging Django Crispy Forms and HTMX
    ... POST saves a view using crispy forms
    ... GET gets the form of existing object in form of modal
    ... form_valid: success notification, form reset, and new object created
    ... form_invalid: error message of django crispy form is returned
    """

    template_name = "partials/form_template.html"
    form_class = BaseCreateForm
    success_url = "/success/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification = f"{self.model_name} successfully updated!"
        self.form_html_get = "partials/form_modal_template.html"
        self.form_html_post = "partials/form_template.html"

    @property
    def model_name(self):
        """creates a predicatble lower case model name
        ex. "due diligence report"
        """
        return self.model._meta.verbose_name.lower()

    @property
    def model_name_id(self):
        """creates a generic reusable id to be used in html to name divs and forms
        ex. "due-diligence-report"
        """
        return self.model_name.replace(" ", "-")

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    @property
    def user(self):
        return get_user_model().objects.get(id=self.request.user.id)

    def get_form_kwargs(self):
        """
        Adds the user to the form kwargs (and instance if update form - pk passed and is get request)
        ... overwrite this method if custom kwargs needed for form
        """
        logger.info(f"calling ... get_form_kwargs: self.kwargs: {self.kwargs}")
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.user})
        object = self.get_object()
        if self.request.method == "GET" and object:
            kwargs.update({"instance": object})

        # else assume create (no existing obj)
        elif not object:
            kwargs.update({"created_by": self.request.user.profile})

        logger.debug(f"BaseCreateUpdateView.get_form_kwargs... {kwargs}")
        return kwargs

    def get_form_html(self, form=None):
        """form html which builds the form portion of the form_template
        (allows us to leverage htmx replacing only the form portion of the html)
        """
        return render_to_string(
            f"{self.form_html_post}", self.get_context_data(), request=self.request
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # logger.info(f"get - context: {context}")
        return render(request, f"{self.form_html_get}", context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            logger.info("post - form is valid")
            return self.form_valid(form)
        else:
            logger.info(f"post - form is invalid: {form.errors}")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """where we add context needed for create/update forms
        ... overwrite this method form_url if custom kwargs needed
        """
        logger.info(f"get_context_data - kwargs: {kwargs}")
        self.object = self.get_object()
        object = self.object
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["model_name_id"] = self.model_name_id
        context["pk"] = object.pk if object else None

        try:
            if object:
                context["form_url"] = reverse(
                    f"{self.model_name_id}-update", kwargs={"pk": object.pk}
                )
            else:
                context["form_url"] = reverse(f"{self.model_name_id}-create")
        except NoReverseMatch:
            create_update_txt = "create" if not object else "update"
            logging.warning(
                f"no reverse match for {self.model_name_id} during {create_update_txt} - check the url of your view and ensure you override get_context_data to provide the form_url."
            )

        logging.info(f"get_context_data: {context}")
        return context

    def form_valid(self, form):
        self.object = form.save()

        # determine if we need a new form (for create) or the same form (for update)
        if form.instance.pk:
            # For update, use the same form with the updated instance
            form_html = self.get_form_html(form=form)
        else:
            # For create, generate a fresh form
            form_html = self.get_form_html()

        # Construct and return the response
        response = HttpResponse(
            self.get_notification() + form_html, content_type="text/html"
        )
        response["HX-Trigger"] = "refresh-forms"
        response["HX-Trigger-After-Settle"] = "close-modal"
        response["HX-Trigger-After-Swap"] = (
            "notification-added"  # TODO: fix notification system to use jquery
        )
        return response

    def form_invalid(self, form):
        """invalid form case...
        ... produces form with error messages (leveraging django forms)
        """
        form_html = self.get_form_html(form)
        return HttpResponse(form_html, content_type="text/html", status=201)
