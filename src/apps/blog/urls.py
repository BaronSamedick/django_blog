from django.urls import path

from .views import (
    ArticleByCategoryListView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
)

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="home"),
    path("articles/create/", ArticleCreateView.as_view(), name="articles_create"),
    path("articles/<str:slug>/update/", ArticleUpdateView.as_view(), name="articles_update"),
    path("articles/<str:slug>/delete/", ArticleDeleteView.as_view(), name="articles_delete"),
    path("articles/<str:slug>/", ArticleDetailView.as_view(), name="articles_detail"),
    path("category/<str:slug>/", ArticleByCategoryListView.as_view(), name="articles_by_category"),
]
