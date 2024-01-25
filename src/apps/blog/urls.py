from django.urls import path

from .views import ArticleByCategoryListView, ArticleDetailView, ArticleListView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="home"),
    path("articles/<str:slug>/", ArticleDetailView.as_view(), name="articles_detail"),
    path("category/<str:slug>/", ArticleByCategoryListView.as_view(), name="articles_by_category"),
]
