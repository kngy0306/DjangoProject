from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        page_context["page"] = "main"
        return page_context
