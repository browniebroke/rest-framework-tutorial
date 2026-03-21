from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from snippets.models import Profile, Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import ProfileSerializer, SnippetSerializer, UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet to reproduce issue #6234.

    Try a PATCH request with multipart/form-data that only sends `name`
    (not `metadata`). The bug causes `metadata` to appear in
    validated_data as an empty dict, wiping out any existing value.

    To test:
        # Create a profile with metadata
        curl -X POST http://localhost:8000/profiles/ \
            -H "Content-Type: application/json" \
            -d '{"name": "test", "metadata": {"key": "value"}}'

        # Partial update with only name via multipart/form-data — BUG: metadata gets wiped
        curl -X PATCH http://localhost:8000/profiles/1/ \
            -F "name=updated"

        # Partial update with only name via JSON — works correctly
        curl -X PATCH http://localhost:8000/profiles/1/ \
            -H "Content-Type: application/json" \
            -d '{"name": "updated"}'
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
