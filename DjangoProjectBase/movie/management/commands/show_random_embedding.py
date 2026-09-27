import random
import numpy as np

from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Show the embedding of a randomly selected movie"

    def handle(self, *args, **kwargs):

        movies = list(Movie.objects.all())

        if not movies:
            self.stdout.write(
                self.style.ERROR(
                    "No movies found in the database."
                )
            )
            return

        # Seleccionar una película al azar
        movie = random.choice(movies)

        # Recuperar el embedding almacenado como binario
        embedding_vector = np.frombuffer(
            movie.emb,
            dtype=np.float32
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Movie: {movie.title}"
            )
        )

        self.stdout.write(
            f"Embedding size: {len(embedding_vector)}"
        )

        self.stdout.write(
            f"First 10 embedding values:"
        )

        self.stdout.write(
            str(embedding_vector[:10])
        )