from rest_framework import viewsets

from lego.app.articles.models import Article
from lego.app.articles.permissions import ArticlePermissions
from lego.app.articles.serializers import ArticleSerializer
from lego.permissions.filters import ObjectPermissionsFilter


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (ObjectPermissionsFilter,)
    permission_classes = (ArticlePermissions,)