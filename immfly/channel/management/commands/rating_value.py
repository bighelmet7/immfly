import csv

from django.core.management.base import BaseCommand, CommandError

from channel.models import TreeChannel

class Command(BaseCommand):
    help = 'Calculate the ratings of all the channels'

    def add_arguments(self, parser):
        parser.add_argument('name')

    def handle(self, *args, **options):
        name = options['name']
        try:
            tree = TreeChannel.objects.get(name=name)
        except TreeChannel.DoesNotExist:
            raise CommandError('TreeChannel "%s" does not exist' % name)
        root_nodes = tree.root.all()

        with open('rates.csv', 'w', newline='') as file:
            csv_wr = csv.writer(file, quoting=csv.QUOTE_NONE)
            csv_wr.writerow(['Channel title', 'Average rating'])
            for root in root_nodes:
                _, history = root.rating_value
                elements = list(history.items())
                elements.sort(key=lambda elem: elem[1], reverse=True)
                for element in elements:
                    csv_wr.writerow([element[0], element[1]])

        self.stdout.write(
            self.style.SUCCESS('Successfully created the rate values of the tree "%s"' % name)
        )
