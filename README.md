# Map My World API

## Introducción

Map My World es una API RESTful diseñada para potenciar una aplicación interactiva de mapas que permite a los usuarios explorar y revisar una variedad de ubicaciones y categorías alrededor del mundo, como restaurantes, parques y museos. Con un énfasis en la relevancia y la actualidad, nuestra API garantiza que las recomendaciones se mantengan frescas y atractivas a través de un sistema de revisión constante.

## Características Principales

- **Gestión de Ubicaciones y Categorías**: Los usuarios pueden añadir y gestionar ubicaciones con detalles como longitud y latitud, así como distintas categorías de lugares para explorar.

- **Recomendador de Exploración**: Este endpoint dinámico ofrece sugerencias de 10 combinaciones de ubicación-categoría que no han sido revisadas en los últimos 30 días, dando prioridad a aquellas que nunca han sido revisadas para asegurar la relevancia y calidad del contenido.

## Modelos de Datos

- **Ubicaciones (`locations`)**: Representan puntos específicos en el mapa definidos por longitud y latitud.
  
- **Categorías (`categories`)**: Tipos de lugares que se pueden explorar.
  
- **Revisiones de Ubicación-Categoría (`location_category_reviewed`)**: Registros que aseguran la calidad de las recomendaciones, marcando combinaciones de ubicaciones y categorías como revisadas.

## Tecnologías Utilizadas

- **Flask**: Un microframework de Python que facilita la creación de aplicaciones web de forma rápida y con un núcleo simple, pero extensible.

- **SQLAlchemy**: ORM de Python que permite interactuar con bases de datos de manera eficiente y pythonica.

- **SQLite**: Sistema de gestión de bases de datos relacional ligero, que almacena la base de datos como un archivo en el sistema del usuario.

- **Flask-RESTful**: Extensión de Flask que facilita la creación de APIs REST con prácticas recomendadas mediante la abstracción de la lógica de las rutas y respuestas.

## Instalación

Descripción de los pasos necesarios para instalar y ejecutar la API en un entorno local o de producción.

```sh
git clone https://github.com/tu-usuario/map-my-world.git
cd map-my-world
docker compose up --build
```

## Documentacion Swagger
la documentacion swagger de debe buscar en http://localhost/swagger
