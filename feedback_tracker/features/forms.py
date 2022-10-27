from django.forms import Form, fields, widgets

from feedback_tracker.features.models import Tag
from feedback_tracker.users.models import User


def get_tag_choices():
    for name in Tag.objects.values_list("name", flat=True).iterator(chunk_size=1000):
        yield (name, name)


def get_user_choices():
    for username, email in User.objects.values_list("username", "email").iterator(
        chunk_size=1000
    ):
        display_string = username
        if email:
            display_string += f" ({email})"

        yield (username, display_string)


class MultiSelectWidget(widgets.SelectMultiple):
    def create_option(
        self, name: str, value, label, selected, index: int, subindex, attrs
    ):
        selected = selected or value in self.tags
        return super().create_option(
            name, value, label, selected, index, subindex, attrs
        )


class TagForm(Form):
    tags = fields.CharField(max_length=100, widget=MultiSelectWidget)

    def __init__(self, *args, **kwargs):
        related_tags = kwargs.pop("tags", [])
        super().__init__(*args, **kwargs)
        tags_widget = self.fields["tags"].widget
        tags_widget.tags = related_tags
        tags_widget.choices = list(get_tag_choices())


class FeedbackForm(Form):
    comment = fields.CharField(widget=widgets.Textarea)
    user = fields.CharField(max_length=100, widget=widgets.Select)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].widget.choices = list(get_user_choices())
