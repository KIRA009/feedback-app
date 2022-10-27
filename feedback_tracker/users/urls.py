from django.urls import path
from django.views.generic import TemplateView

from feedback_tracker.users.views import UserCreateView, UserEditView, UserListView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="users/user_index.html"),
        name="user-index",
    ),
    path("list/", UserListView.as_view(), name="user-list"),
    path("add/", UserCreateView.as_view(), name="user-add"),
    path("edit/<int:pk>/", UserEditView.as_view(), name="user-edit"),
]
