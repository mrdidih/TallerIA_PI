from django.core.management.base import BaseCommand
from movie.models import Movie
import os


class Command(BaseCommand):
    help = 'Update movie images using files from media/movie/images'

    def handle(self, *args, **kwargs):

        images_folder = 'media/movie/images/'

        movies = Movie.objects.all()

        self.stdout.write(
            f'Found {movies.count()} movies'
        )

        updated_count = 0
        not_found_count = 0

        for movie in movies:

            image_filename = f"m_{movie.title}.png"

            image_path_full = os.path.join(
                images_folder,
                image_filename
            )

            if os.path.exists(image_path_full):

                movie.image = os.path.join(
                    'movie/images',
                    image_filename
                ).replace('\\', '/')

                movie.save()

                updated_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated image for: {movie.title}'
                    )
                )

            else:

                not_found_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f'Image not found for: {movie.title}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Finished. Updated: {updated_count} - '
                f'Not found: {not_found_count}'
            )
        )