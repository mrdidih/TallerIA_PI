import os
import numpy as np

from django.core.management.base import BaseCommand
from movie.models import Movie

from google import genai
from google.genai import types
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Generate and store embeddings for all movies in the database"

    def handle(self, *args, **kwargs):

        # Cargar API key de Gemini
        load_dotenv('../gemini.env')

        client = genai.Client(
            api_key=os.environ.get('GEMINI_API_KEY')
        )

        # Obtener todas las películas
        movies = Movie.objects.all()

        self.stdout.write(
            f"Found {movies.count()} movies in the database"
        )

        # Función auxiliar para generar embeddings
        def get_embedding(text):

            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="SEMANTIC_SIMILARITY"
                )
            )

            return np.array(
                response.embeddings[0].values,
                dtype=np.float32
            )

        # Recorrer todas las películas
        for movie in movies:

            try:

                emb = get_embedding(
                    movie.description
                )

                # Guardar embedding como binario
                movie.emb = emb.tobytes()

                movie.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Embedding stored for: {movie.title}"
                    )
                )

            except Exception as e:

                self.stderr.write(
                    f"Failed to generate embedding "
                    f"for {movie.title}: {e}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Finished generating embeddings for all movies"
            )
        )