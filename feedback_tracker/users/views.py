from django.db.models import Count

from feedback_tracker.common.base_views import (
    BaseCreateView,
    BaseEditView,
    BaseListView,
)
from feedback_tracker.users.models import User


class UserListView(BaseListView):
    model = User
    template_name = "users/components/user_list_table.html"
    context_object_name = "users"
    default_ordering = "-num_features"
    default_ordering_preference = {"num_features": "-", "username": "", "email": ""}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(num_features=Count("feedback__feature"))
            .order_by(self.ordering_details[2])
        )


class UserCreateView(BaseCreateView):
    model = User
    fields = ["username", "email"]
    template_name = "users/components/user_add.html"
    hx_trigger_header = "userListChanged"


class UserEditView(BaseEditView):
    model = User
    fields = ["username", "email"]
    template_name = "users/components/user_edit.html"
    hx_trigger_header = "userListChanged"
