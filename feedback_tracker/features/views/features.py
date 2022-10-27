from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import DetailView, FormView

from feedback_tracker.common.base_views import (
    BaseCreateView,
    BaseEditView,
    BaseListView,
)
from feedback_tracker.common.utils import string_is_email
from feedback_tracker.features.forms import FeedbackForm, TagForm
from feedback_tracker.features.models import Feature, Feedback, Tag
from feedback_tracker.users.models import User


class FeatureListView(BaseListView):
    model = Feature
    template_name = "features/components/feature_list_table.html"
    context_object_name = "features"
    default_ordering = "-num_feedback"
    default_ordering_preference = {"num_feedback": "-", "name": ""}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("tags", "feedback")
            .annotate(num_feedback=Count("feedback"))
            .order_by(self.ordering_details[2])
        )


class FeatureCreateView(BaseCreateView):
    model = Feature
    fields = ["name"]
    template_name = "features/components/feature_add.html"
    hx_trigger_header = "featureListChanged"


class FeatureEditView(BaseEditView):
    model = Feature
    fields = ["name"]
    template_name = "features/components/feature_edit.html"
    hx_trigger_header = "featureListChanged"


class FeatureDetailView(DetailView):
    model = Feature
    template_name = "features/components/feature_detail.html"
    context_object_name = "feature"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("feedback", "feedback__user", "tags")
            .annotate(num_feedback=Count("feedback"))
        )


class FeatureAddTagView(FormView):
    form_class = TagForm
    template_name = "features/components/feature_add_tag.html"

    def form_valid(self, form):
        data = form.cleaned_data
        tags = list(map(lambda x: x.strip("'"), data["tags"].strip("[]").split(", ")))
        database_tags = Tag.objects.filter(name__in=tags).values_list("name", flat=True)
        new_tags = list(set(tags) - set(database_tags))
        old_tags = list(set(tags) - set(new_tags))

        new_tags = Tag.objects.bulk_create([Tag(name=tag) for tag in new_tags])
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#bulk-create
        # If the model’s primary key is an AutoField, the primary key attribute can only be retrieved on
        # certain databases (currently PostgreSQL, MariaDB 10.5+, and SQLite 3.35+).
        new_tags = [tag.name for tag in new_tags]
        new_tags.extend(old_tags)
        new_tags = Tag.objects.filter(name__in=new_tags)

        Feature.objects.get(id=self.feature_id).tags.set(new_tags)
        return HttpResponse(status=204, headers={"HX-Trigger": "featureListChanged"})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tags"] = Tag.objects.filter(feature__id=self.feature_id).values_list(
            "name", flat=True
        )
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.feature_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context["form"]:
            field.field.widget.attrs["class"] = "form-control"
        return context


class FeatureFilterByTag(FeatureListView):
    template_name = "features/components/feature_filtered_by_tags_table.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("tags")
            .filter(tags__id=self.tag_id)
            .annotate(num_feedback=Count("feedback"))
            .order_by(self.ordering_details[2])
        )

    def dispatch(self, request, *args, **kwargs):
        self.tag_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(id=self.tag_id)
        return context


class FeatureFilterByUser(FeatureListView):
    template_name = "features/components/feature_filtered_by_users_table.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(feedback__user__id=self.user_id)
            .annotate(num_feedback=Count("feedback"))
            .order_by(self.ordering_details[2])
        )

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.user_id)
        return context


class FeatureAddFeedbackView(FormView):
    form_class = FeedbackForm
    template_name = "features/components/feature_add_feedback.html"

    def form_valid(self, form):
        data = form.cleaned_data
        username = data["user"]
        try:
            if string_is_email(username):
                email = username
                username = username.split("@")[0]
                user = User.objects.get_or_create(username=username, email=email)[0]
            else:
                user = User.objects.get_or_create(username=username)[0]
        except ValueError as e:
            return HttpResponseBadRequest(e)
        Feedback.objects.create(
            user=user,
            feature_id=self.feature_id,
            comment=data["comment"],
        )
        return HttpResponse(status=204, headers={"HX-Trigger": "featureListChanged"})

    def dispatch(self, request, *args, **kwargs):
        self.feature_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context["form"]:
            field.field.widget.attrs["class"] = "form-control"
        context["feature"] = Feature.objects.get(id=self.feature_id)
        return context
