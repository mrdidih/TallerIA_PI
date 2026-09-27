import os
import numpy as np

from django.core.management.base import BaseCommand
from movie.models import Movie

from google import genai
from google.genai import types
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Compare two movies and a prompt using Gemini embeddings"

    def handle(self, *args, **kwargs):

        # Cargar API key de Gemini
        load_dotenv('../gemini.env')

        client = genai.Client(
            api_key=os.environ.get('GEMINI_API_KEY')
        )

        # Películas a comparar
        movie1 = Movie.objects.get(
            title="La captura"
        )

        movie2 = Movie.objects.get(
            title="Castillo medieval"
        )

        # Obtener embedding de un texto
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

        # Calcular similitud de coseno
        def cosine_similarity(a, b):

            return np.dot(a, b) / (
                np.linalg.norm(a) *
                np.linalg.norm(b)
            )

        # Generar embeddings de las dos películas
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        # Calcular similitud entre películas
        similarity = cosine_similarity(
            emb1,
            emb2
        )

        self.stdout.write(
            f"🎬 Similaridad entre "
            f"'{movie1.title}' y "
            f"'{movie2.title}': "
            f"{similarity:.4f}"
        )

        # Prompt libre
        prompt = "película sobre la Segunda Guerra Mundial"

        prompt_emb = get_embedding(prompt)

        # Comparar prompt con las dos películas
        sim_prompt_movie1 = cosine_similarity(
            prompt_emb,
            emb1
        )

        sim_prompt_movie2 = cosine_similarity(
            prompt_emb,
            emb2
        )

        self.stdout.write(
            f"📝 Similitud prompt vs "
            f"'{movie1.title}': "
            f"{sim_prompt_movie1:.4f}"
        )

        self.stdout.write(
            f"📝 Similitud prompt vs "
            f"'{movie2.title}': "
            f"{sim_prompt_movie2:.4f}"
        )