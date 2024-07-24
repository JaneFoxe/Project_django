from django.shortcuts import render

from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    """Конкретный блог"""
    model = Blog

    def get(self, request, *args, **kwargs):
        article = self.get_object()

        article.count_of_view += 1
        article.save()

        return super().get(request, *args, **kwargs)