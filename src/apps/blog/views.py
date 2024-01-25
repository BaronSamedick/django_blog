from django.views.generic import DetailView, ListView

from .models import Article, Category

PAGINATION_SIZE = 5


class ArticleListView(ListView):
    model = Article
    template_name = "blog/articles_list.html"
    context_object_name = "articles"
    paginate_by = PAGINATION_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/articles_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class ArticleByCategoryListView(ListView):
    model = Article
    template_name = "blog/articles_list.html"
    context_object_name = "articles"
    paginate_by = PAGINATION_SIZE
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        queryset = Article.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Статьи из категории: {self.category.title}"
        return context
