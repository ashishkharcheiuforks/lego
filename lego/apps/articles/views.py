from rest_framework import viewsets

from lego.apps.articles.models import Article
from lego.apps.articles.serializers import DetailedArticleSerializer, PublicArticleSerializer
from lego.apps.permissions.api.views import AllowedPermissionsMixin


class ArticlesViewSet(AllowedPermissionsMixin, viewsets.ModelViewSet):

    queryset = Article.objects.all()
    ordering = '-created_at'

    def get_queryset(self):
        queryset = self.queryset.select_related('created_by').prefetch_related('tags')

        if self.action == 'list':
            return queryset

        return queryset.prefetch_related(
            'comments',
            'comments__created_by',
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicArticleSerializer

        return DetailedArticleSerializer
