# API local de personajes de Danganronpa

API REST sencilla, escrita con Python y sin dependencias externas. Incluye 70 personajes de los cuatro juegos, incluidos Izuru Kamukura, Genocide Jack, Monokuma, Monomi, los cinco Monokubs, Kurokuma, Shirokuma y Hiroko Hagakure. Es una API fan-made y no oficial.

Las descripciones y la personalidad son resúmenes breves en español, no textos del juego. Las fichas enlazan a una wiki comunitaria como referencia para algunos datos de perfil. La API sirve imágenes locales añadidas por quien la use; no incluye ni redistribuye imágenes oficiales.

## Requisitos y puesta en marcha

Necesitas Python 3.9 o posterior. Desde esta carpeta, ejecuta:

```powershell
py server.py
```

La API estará disponible en `http://127.0.0.1:8000/api`. Para usar otro puerto, define la variable de entorno `PORT` antes de iniciar el servidor.

Para consumirla desde el navegador, sirve tu proyecto HTML con una extensión como Live Server y deja el servidor Python en marcha. La API permite solicitudes CORS desde cualquier origen.

## Endpoints

| Método | Ruta | Respuesta |
| --- | --- | --- |
| `GET` | `/api` | Información y rutas disponibles |
| `GET` | `/api/health` | Estado del servidor |
| `GET` | `/api/characters` | Lista de personajes |
| `GET` | `/api/characters/{id}` | Un personaje por su identificador |
| `GET` | `/api/games` | Lista de juegos incluidos |
| `GET` | `/api/games/{id}/characters` | Personajes de un juego |
| `GET` | `/images/games/{game_id}` | Imagen de presentación de un juego |
| `GET` | `/images/{id}/portrait` | Retrato local del personaje |
| `GET` | `/images/{id}/portrait/{variant}` | Retrato alternativo local |
| `GET` | `/images/{id}/sprite/{game_id}` | Sprite local del personaje en un juego |
| `GET` | `/images/{id}/sprite/variant/{variant}` | Sprite alternativo local |
| `GET` | `/images/{id}/death` | Imagen del fallecimiento o descubrimiento del cuerpo |
| `GET` | `/images/{id}/execution/{number}` | Imagen numerada de la ejecución |
| `GET` | `/images/monokubs/collective` | Imagen colectiva de los cinco Monokubs |

Cada personaje incluye `images.portrait`, `images.portraits` (retratos alternativos disponibles), `images.sprites` (sprites por juego), `images.spriteVariants` (sprites alternativos), `images.death` y `images.executions`. Guarda el retrato principal como `images/{id}/portrait.{ext}`, un retrato alternativo como `images/{id}/portrait-{variant}.{ext}` y cada sprite como `images/{id}/sprite-{game_id}.{ext}`, usando el identificador del personaje y del juego. Para la versión 2x2, usa `danganronpa-2x2` como identificador, por ejemplo `sprite-danganronpa-2x2.webp`. Para sprites de formas o apariciones alternativas, usa `sprite-{variant}.{ext}`, por ejemplo `sprite-mechamaru.webp`; la API los incluirá en `images.spriteVariants`.

Kiibo usa la carpeta `images/k1b0/` por su nombre original; la API mantiene el identificador `kiibo` en sus fichas y rutas.

Para imágenes de fallecimientos, guarda una imagen como `images/{id}/death.{ext}`. Para las ejecuciones, usa `images/{id}/execution-1.{ext}`, `execution-2.{ext}` y así sucesivamente; la API las devuelve ordenadas en `images.executions`. Las URL siguen el patrón `/images/{id}/death` y `/images/{id}/execution/{number}`. Los campos serán `null` o una lista vacía si no hay imágenes de ese tipo.

Se aceptan las extensiones `.png`, `.jpg`, `.jpeg` y `.webp`. Si el archivo aún no existe, la API responde `404`. Reinicia el servidor después de añadir imágenes para que aparezcan en la respuesta del personaje.

Las imágenes de presentación de los juegos van en `images/games/` con el nombre `game-{id}.{ext}`, usando el identificador del juego, por ejemplo `game-danganronpa-1.webp` o `game-ultra-despair-girls.jpg`. `/api/games` incluye el campo `image` con la ruta correspondiente; será `null` si no hay imagen. La ruta `/images/games/{game_id}` sirve la imagen en su formato original.

Ejemplo de estructura:

```text
images/
└── hajime-hinata/
    ├── portrait.webp
    ├── sprite-danganronpa-2.webp
    └── sprite-danganronpa-2x2.webp
```

Si un personaje tiene retratos adicionales, usa un sufijo descriptivo, por ejemplo `portrait-kiyondo.webp`; la API lo incluirá en `images.portraits`.

A los cinco Monokubs se les asigna una carpeta compartida `images/monokubs/`. Guarda sus retratos como `monotaro.webp`, `monosuke.webp`, `monophanie.webp`, `monokid.webp` y `monodam.webp`, y la imagen grupal como `collective.webp`. Las fichas individuales exponen sus rutas en `images.portrait` y `images.collective`.

Añade únicamente imágenes que tengas derecho a usar; la carpeta de imágenes no incluye archivos de los juegos.

Se pueden combinar estos filtros en `/api/characters`:

- `game`: identificador del juego (`danganronpa-1`, `danganronpa-2`, `ultra-despair-girls` o `danganronpa-v3`).
- `role`: rol (`protagonista`, `aliado`, `estudiante` o `antagonista`).
- `search`: busca en nombre, talento, descripción y datos del perfil.

Ejemplos:

```text
http://127.0.0.1:8000/api/characters?game=danganronpa-2
http://127.0.0.1:8000/api/characters?role=protagonista
http://127.0.0.1:8000/api/characters?search=detective
http://127.0.0.1:8000/api/characters/kyoko-kirigiri
http://127.0.0.1:8000/api/games/danganronpa-v3/characters
```

## Ejemplo desde JavaScript

```javascript
const respuesta = await fetch("http://127.0.0.1:8000/api/characters");

if (!respuesta.ok) {
  throw new Error(`Error de la API: ${respuesta.status}`);
}

const personajes = await respuesta.json();
console.log(personajes);
```

Cada personaje conserva `id`, `name`, `japaneseName` (nombre escrito en japonés), `game`, `gameTitle`, `talent`, `role` y `description`. También incluye `fate`, `images` con las rutas locales disponibles, y `profile`, con:

- `fate.status`: resultado al final de la historia del juego (`sobrevive`, `muere`, `destruido`, entre otros).
- `fate.chapter`: capítulo del fallecimiento o destrucción; `null` si no corresponde. Mukuro usa `"prólogo"`, ya que muere antes del capítulo 1.
- `fate.role`: papel en el suceso (`víctima`, `culpable`, `superviviente`, etc.).
- `fate.context`: aclaración opcional para casos especiales, como suicidios, condenas erróneas o destrucciones de robots.
- `fate.virtualOutcome`: resultado opcional dentro del Neo World Program. En Danganronpa 2, distingue la muerte del avatar de la supervivencia física del participante; Chiaki y Monomi son IA y tienen casos propios.

Los datos de destino contienen spoilers de los cuatro juegos. Taichi Fujisaki figura con estado `desconocido`: recibe una herida mortal en el capítulo 3, pero su cuerpo desaparece y el juego no confirma su muerte.

- `birthday`: cumpleaños si está documentado; de lo contrario, `null`.
- `height`: medidas publicadas, incluidas sus variantes o unidades.
- `bloodType`: grupo sanguíneo o `null`.
- `likes` y `dislikes`: listas de preferencias documentadas. Ambos campos aparecen en todos los personajes; `[]` indica que falta confirmar esa información.
- `personality`: resumen breve en español.
- `source`: enlace a la ficha comunitaria consultada. No es una fuente oficial; comprueba los datos antes de usarlos como definitivos.

Los datos no confirmados no se rellenan por suposición. La información descriptiva y las preferencias están en español; se conservan los nombres propios, los títulos oficiales de los juegos, las URL de las fuentes y `japaneseName` en japonés. El archivo `characters.json` contiene los datos y se puede ampliar manteniendo esta estructura. La búsqueda también consulta las preferencias y los demás campos de `profile`.

Ejemplo de respuesta:

```json
{
  "id": "makoto-naegi",
  "name": "Makoto Naegi",
  "japaneseName": "苗木 誠",
  "game": "danganronpa-1",
  "gameTitle": "Danganronpa: Trigger Happy Havoc",
  "talent": "Estudiante de preparatoria con suerte",
  "role": "protagonista",
  "description": "Un estudiante optimista que confía en la esperanza y en sus compañeros.",
  "images": {
    "portrait": "/images/makoto-naegi/portrait",
    "portraits": {},
    "spriteVariants": {},
    "death": null,
    "executions": [],
    "sprites": {
      "danganronpa-1": "/images/makoto-naegi/sprite/danganronpa-1",
      "ultra-despair-girls": "/images/makoto-naegi/sprite/ultra-despair-girls"
    }
  },
  "profile": {
    "birthday": "5 de febrero",
    "height": ["160 cm (Japón)", "161 cm (Japón; DR3)", "5'3\" (edición inglesa)"],
    "bloodType": "A",
    "likes": ["Curry", "Cosas de moda"],
    "dislikes": ["Caballa seca", "Tofu seco"],
    "personality": "Un estudiante optimista que confía en la esperanza y en sus compañeros.",
    "source": "https://danganronpa.fandom.com/wiki/Makoto_Naegi"
  }
}
```
