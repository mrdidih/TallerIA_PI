from django.core.management.base import BaseCommand
from movie.models import Movie

from google import genai
from dotenv import load_dotenv
import os
import base64
import re


# Cargar la API key desde gemini.env
load_dotenv('../gemini.env')

# Crear cliente de Gemini
client = genai.Client(
    api_key=os.environ.get('GEMINI_API_KEY')
)


class Command(BaseCommand):
    help = 'Generate movie images using Gemini and update the database'

    def generate_and_save_image(self, movie_title, save_folder):
        prompt = f"Create a movie poster for the film '{movie_title}'"

        interaction = client.interactions.create(
            model='gemini-3.1-flash-image',
            input=prompt,
        )

        image_data = interaction.output_image.data

        # Limpiar el nombre del archivo
        safe_title = re.sub(r'[\\/*?:"<>|]', '', movie_title)
        image_filename = f"m_{safe_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        with open(image_path_full, 'wb') as f:
            f.write(base64.b64decode(image_data))

        return os.path.join('movie/images', image_filename).replace('\\', '/')

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            image_relative_path = self.generate_and_save_image(
                movie.title,
                images_folder
            )

            movie.image = image_relative_path
            movie.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Saved and updated image for: {movie.title}"
                )
            )

            break