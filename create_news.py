import os
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviereviews.settings')
django.setup()

from news.models import News

# Crear noticias de ejemplo
news_data = [
    {
        'headline': 'Oppenheimer arrasa en la temporada de premios',
        'body': 'La película biográfica dirigida por Christopher Nolan sobre el físico J. Robert Oppenheimer ha sido aclamada por crítica y público, posicionándose como favorita para los premios de la industria cinematográfica.',
        'date': date.today() - timedelta(days=1)
    },
    {
        'headline': 'Netflix anuncia nuevas producciones originales para 2024',
        'body': 'La plataforma de streaming reveló su catálogo de películas originales para el próximo año, incluyendo colaboraciones con directores reconocidos y nuevos talentos emergentes.',
        'date': date.today() - timedelta(days=3)
    },
    {
        'headline': 'El revival del cine de terror independiente',
        'body': 'Las películas de terror de bajo presupuesto están experimentando un renacimiento, con varios títulos independientes superando las expectativas en taquilla y recibiendo elogios de la crítica.',
        'date': date.today() - timedelta(days=5)
    },
    {
        'headline': 'Parasite celebra 5 años de su estreno mundial',
        'body': 'La película surcoreana de Bong Joon-ho que hizo historia al ganar el Oscar a Mejor Película cumple cinco años desde su premiere en el Festival de Cannes, marcando un antes y después en el cine internacional.',
        'date': date.today() - timedelta(days=7)
    },
    {
        'headline': 'La industria del cine adopta nuevas tecnologías de IA',
        'body': 'Los estudios cinematográficos están incorporando inteligencia artificial en diversos aspectos de la producción, desde la escritura de guiones hasta los efectos visuales, generando debate sobre el futuro del cine.',
        'date': date.today() - timedelta(days=10)
    },
    {
        'headline': 'Festival de Cine de Sundance anuncia selecciones 2024',
        'body': 'El prestigioso festival independiente reveló su lineup oficial, destacando una mayor diversidad en directores y temáticas, con especial énfasis en historias de comunidades subrepresentadas.',
        'date': date.today() - timedelta(days=12)
    }
]

# Limpiar noticias existentes
News.objects.all().delete()

# Crear nuevas noticias
for news_item in news_data:
    News.objects.create(**news_item)
    print(f"Creada noticia: {news_item['headline']}")

print(f"Se crearon {len(news_data)} noticias exitosamente.")