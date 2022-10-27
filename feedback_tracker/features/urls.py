from django.urls import include, path
from django.views.generic import TemplateView

from feedback_tracker.features.views import (
    FeatureAddTagView,
    FeatureCreateView,
    FeatureEditView,
    FeatureListView,
)
from feedback_tracker.features.views.features import (
    FeatureAddFeedbackView,
    FeatureDetailView,
    FeatureFilterByTag,
    FeatureFilterByUser,
)
from feedback_tracker.features.views.tags import TagCreateView, TagEditView, TagListView

tag_urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="features/tag_index.html"),
        name="tag-index",
    ),
    path("list/", TagListView.as_view(), name="tag-list"),
    path("add/", TagCreateView.as_view(), name="tag-add"),
    path("edit/<int:pk>/", TagEditView.as_view(), name="tag-edit"),
]

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="features/feature_index.html"),
        name="feature-index",
    ),
    path("list/", FeatureListView.as_view(), name="feature-list"),
    path("add/", FeatureCreateView.as_view(), name="feature-add"),
    path("detail/<int:pk>/", FeatureDetailView.as_view(), name="feature-detail"),
    path("edit/<int:pk>/", FeatureEditView.as_view(), name="feature-edit"),
    path("add-tag/<int:pk>/", FeatureAddTagView.as_view(), name="feature-add-tag"),
    path(
        "add-feedback/<int:pk>/",
        FeatureAddFeedbackView.as_view(),
        name="feature-add-feedback",
    ),
    path(
        "filter-by-tag/<int:pk>/",
        FeatureFilterByTag.as_view(),
        name="feature-filter-by-tag",
    ),
    path(
        "filter-by-user/<int:pk>/",
        FeatureFilterByUser.as_view(),
        name="feature-filter-by-user",
    ),
    path("tags/", include(tag_urlpatterns)),
]
