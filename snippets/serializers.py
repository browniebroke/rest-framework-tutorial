from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Profile, Snippet


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to reproduce issue #6234.

    The `metadata` DictField always appears in validated_data for
    multipart/form-data requests, even when the field was not sent,
    because `parse_html_dict` returns an empty dict instead of
    an empty sentinel value.
    """
    metadata = serializers.DictField(child=serializers.CharField(), required=False)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'metadata')

    def update(self, instance, validated_data):
        # This is the pattern from the issue: trying to skip fields
        # that weren't provided during a partial update.
        # With the bug, "metadata" is ALWAYS in validated_data for
        # multipart/form-data, even when the client didn't send it.
        if not self.partial or "metadata" in validated_data:
            instance.metadata = validated_data.get("metadata", {})
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


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
