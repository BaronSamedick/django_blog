from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from utils.mixins import AuthorRequiredMixin

from .forms import ArticleCreateForm, ArticleUpdateForm
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """

    model = Article
    template_name = "blog/articles_create.html"
    form_class = ArticleCreateForm
    login_url = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статьи на сайт"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("articles_detail", kwargs={"slug": self.object.slug})


class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """

    model = Article
    template_name = "blog/articles_update.html"
    context_object_name = "article"
    form_class = ArticleUpdateForm
    login_url = "home"
    success_message = "Статья была успешно обновлена"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление статьи: {self.object.title}"
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("articles_detail", kwargs={"slug": self.object.slug})


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """

    model = Article
    success_url = reverse_lazy("home")
    context_object_name = "article"
    template_name = "blog/articles_delete.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление статьи: {self.object.title}"
        return context
