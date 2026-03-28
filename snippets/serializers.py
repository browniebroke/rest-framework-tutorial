from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField, ListField

from snippets.models import Snippet


class CommunitySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    colors = ListField(
        allow_null=True,
        child=CharField(max_length=7),
        required=False,
    )


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code',
                  'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
