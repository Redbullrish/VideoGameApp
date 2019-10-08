import os

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FormTestCase(TestCase):
    def test_genre_read(self):
        genre_file = os.path.join(BASE_DIR, "Query/data/genre.txt")
        genre_set = set()

        with open(genre_file) as fp:
            line = fp.readline()
            while line:
                genre_set.add(line[:-1])
                line = fp.readline()
        
        print(genre_set)
        self.assertEqual(len(genre_set), 12)
