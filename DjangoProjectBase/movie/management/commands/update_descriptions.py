from django.core.management.base import BaseCommand
from movie.models import Movie

from google import genai
from dotenv import load_dotenv
import os


# Cargar la API Key desde gemini.env
load_dotenv('../gemini.env')

# Crear el cliente de Gemini
client = genai.Client(
    api_key=os.environ.get('GEMINI_API_KEY')
)


def get_completion(prompt):
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=prompt
    )

    return response.text.strip()


class Command(BaseCommand):
    help = 'Update movie descriptions using Gemini'

    def handle(self, *args, **kwargs):

        instruction = (
    "Generate an improved description for the following movie. "
    "Keep it concise and clear. "
    "Return only the new movie description. "
    "Do not include explanations, labels, introductions, quotation marks, "
    "or the original description."
)

        movies = Movie.objects.all()

        for movie in movies:

            prompt = (
                f"{instruction} "
                f"Update the description '{movie.description}' "
                f"of the movie '{movie.title}'"
            )

            response = get_completion(prompt)

            movie.description = response
            movie.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated description for: {movie.title}'
                )
            )

            break