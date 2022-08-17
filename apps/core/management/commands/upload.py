from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from io import BytesIO

from resources.models import Resource

data = {'Resources': [{'title': 'test resource 1', 'content': 'this resource helps you to do something', 'tags': ['resource', 'useful']},
                      {'title': 'test resource 2', 'content': 'this resource points you to an external project', 'tags': ['resource', 'organisation']}],
        'Case Studies': [{'title': 'test case study 1', 'summary': 'a case study of studying cases', 'image': 'ignore/example1.webp', 'body': '<body text>', 'tags': ['case study', 'not useful']}]}

class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='?', type=int, default=0)

    def handle(self, *args, **options):
        for new_resource_data in data['Resources']:
            print(new_resource_data)
            new_resource = Resource.objects.create(title = new_resource_data['title'], content = new_resource_data['content'])
            for tag in new_resource_data['tags']:
                new_resource.tags.add(tag)
            new_resource.save()
