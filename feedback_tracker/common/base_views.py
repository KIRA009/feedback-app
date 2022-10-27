from django.http import HttpResponse
from django.utils.functional import cached_property
from django.views.generic import CreateView, ListView, UpdateView

from feedback_tracker.common.utils import get_ordering_object


class BaseListView(ListView):
    default_ordering = ""
    default_ordering_preference = {}

    @cached_property
    def ordering_details(self):
        ordering = self.request.GET.get("ordering", self.default_ordering)
        curr_ordering = get_ordering_object(ordering)
        next_ordering = dict()
        for field, direction in curr_ordering.items():
            if direction == "-":
                next_ordering[field] = ""
            else:
                next_ordering[field] = "-"
        return curr_ordering, next_ordering, ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # could use len here since the queryset will eventually be evaluated
        context["total_count"] = len(context[self.context_object_name])
        context["curr_ordering"] = self.ordering_details[0]
        context["next_ordering"] = self.ordering_details[1]
        context["default_ordering_preference"] = self.default_ordering_preference
        return context


class BaseEditCreateView:
    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204, headers={"HX-Trigger": self.hx_trigger_header})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context["form"]:
            field.field.widget.attrs["class"] = "form-control"
        return context


class BaseCreateView(BaseEditCreateView, CreateView):
    pass


class BaseEditView(BaseEditCreateView, UpdateView):
    pass
