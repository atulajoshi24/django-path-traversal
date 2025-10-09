from django.test import TestCase
from django.urls import reverse

class FileServerAppTests(TestCase):
    def test_file_content(self):
        # Assuming you have a file named 'test_file.txt' in the root directory
        filename = 'test_file.txt'
        response = self.client.get(reverse('serve_file', args=[filename]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expected content of the file')  # Replace with actual expected content

    def test_file_not_found(self):
        filename = 'non_existent_file.txt'
        response = self.client.get(reverse('serve_file', args=[filename]))
        self.assertEqual(response.status_code, 404)