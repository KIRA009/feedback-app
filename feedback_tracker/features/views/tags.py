from django.db.models import Count

from feedback_tracker.common.base_views import (
    BaseCreateView,
    BaseEditView,
    BaseListView,
)
from feedback_tracker.features.models import Tag


class TagListView(BaseListView):
    model = Tag
    template_name = "features/components/tag_list_table.html"
    context_object_name = "tags"
    default_ordering = "-num_features"
    default_ordering_preference = {"num_features": "-", "name": ""}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(num_features=Count("feature"))
            .order_by(self.ordering_details[2])
        )


class TagCreateView(BaseCreateView):
    model = Tag
    fields = ["name", "color"]
    template_name = "features/components/tag_add.html"
    hx_trigger_header = "tagListChanged"


class TagEditView(BaseEditView):
    model = Tag
    fields = ["name", "color"]
    template_name = "features/components/tag_edit.html"
    hx_trigger_header = "tagListChanged"
