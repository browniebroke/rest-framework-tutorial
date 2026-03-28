from rest_framework import status
from rest_framework.test import APITestCase


class ListFieldPartialUpdateTest(APITestCase):
    """Reproduce issue #6202: ListField does not respect ordered sequence
    in form data with partial updates."""

    def test_partial_update_with_ordered_list_field(self):
        """PATCH with indexed form data (colors[0], colors[1]) should
        return the colors in validated_data, preserving order."""
        response = self.client.patch(
            '/communities/1/',
            data={'colors[0]': '#ffffff', 'colors[1]': '#000000'},
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('colors', response.data)
        self.assertEqual(response.data['colors'], ['#ffffff', '#000000'])

    def test_partial_update_with_unordered_list_field(self):
        """PATCH with repeated key form data (colors, colors) should work
        as it matches the field name directly."""
        response = self.client.patch(
            '/communities/1/',
            data={'colors': ['#ffffff', '#000000']},
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('colors', response.data)
        self.assertEqual(response.data['colors'], ['#ffffff', '#000000'])
