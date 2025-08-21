import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie

class Command(BaseCommand):
    help = 'Load movies from CSV file'

    def handle(self, *args, **options):
        csv_file = os.path.join(settings.BASE_DIR, 'movies_intial.csv')
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file}'))
            return
        
        movies_created = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                movie, created = Movie.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'description': row['description'],
                        'genre': row['genre'],
                        'year': int(row['year']) if row['year'] else None,
                        'image': 'movie/images/default.jpg',
                        'url': row.get('image_url', '')
                    }
                )
                
                if created:
                    movies_created += 1
                    self.stdout.write(f'Created movie: {movie.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {movies_created} movies to database')
        )