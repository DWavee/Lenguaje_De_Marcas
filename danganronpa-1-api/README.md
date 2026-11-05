# API local de personajes de Danganronpa 1

API REST escrita en Python y sin dependencias externas. Incluye los 16 personajes de Danganronpa: Trigger Happy Havoc y a Monokuma. Es una API fan-made y no oficial.

## Requisitos y puesta en marcha

Necesitas Python 3.9 o posterior. Desde esta carpeta, ejecuta:

```powershell
py server.py
```

La API estará disponible en `http://127.0.0.1:8001/api`. Usa el puerto 8001 para poder ejecutar esta API junto a la API original. Para elegir otro puerto, define la variable de entorno `PORT` antes de iniciar el servidor.

## Endpoints

| Método | Ruta | Respuesta |
| --- | --- | --- |
| `GET` | `/api` | Información y rutas disponibles |
| `GET` | `/api/health` | Estado del servidor |
| `GET` | `/api/characters` | Lista de los 17 personajes |
| `GET` | `/api/characters/{id}` | Un personaje por su identificador |
| `GET` | `/api/games` | El juego incluido |
| `GET` | `/api/games/danganronpa-1/characters` | Personajes del juego |
| `GET` | `/images/cover` | Imagen principal de la página (`images/foto_index.webp`) |
| `GET` | `/images/games/danganronpa-1` | Imagen local del juego, si existe |
| `GET` | `/images/{id}/portrait` | Retrato local del personaje |
| `GET` | `/images/{id}/portrait/{variant}` | Retrato alternativo local |
| `GET` | `/images/{id}/photo` | Foto añadida del personaje (`foto.webp` o `{id}.webp`) |
| `GET` | `/images/{id}/sprites` | Sprite local del personaje |
| `GET` | `/images/{id}/sprites/variant/{variant}` | Sprite alternativo local |
| `GET` | `/images/{id}/death` | Imagen del fallecimiento o descubrimiento del cuerpo |
| `GET` | `/images/{id}/execution/{number}` | Imagen numerada de la ejecución |
| `GET` | `/images/{id}/file/{filename}` | Imagen adicional del personaje |

Se pueden combinar estos filtros en `/api/characters`:

- `role`: rol (`protagonista`, `aliado`, `estudiante` o `antagonista`).
- `search`: busca en nombre, talento, descripción y datos del perfil.

Ejemplos:

```text
http://127.0.0.1:8001/api/characters?role=protagonista
http://127.0.0.1:8001/api/characters?search=detective
http://127.0.0.1:8001/api/characters/makoto-naegi
http://127.0.0.1:8001/api/games/danganronpa-1/characters
```

Cada personaje incluye `id`, `name`, `japaneseName`, `game`, `gameTitle`, `talent`, `role`, `description`, `profile`, `fate` e información sobre las rutas de imágenes locales. Las descripciones son resúmenes breves en español, no textos del juego. Algunos campos de perfil incluyen enlaces a una wiki comunitaria como referencia.

La carpeta `images/` contiene los recursos locales disponibles para los personajes de Danganronpa 1. Los sprites se llaman `sprites.webp` y se exponen mediante `images.sprites` y la ruta `/images/{id}/sprites`. Las rutas antiguas de sprites siguen funcionando por compatibilidad. La imagen principal de la página se sirve desde `images/foto_index.webp` mediante `/images/cover`. Para las fotos añadidas a las carpetas de los personajes, usa `foto.webp` (o `{id}.webp`, por ejemplo `monokuma.webp`). La API las expone como `images.photo`; los demás archivos se listan como `images.additional`. Usa las extensiones `.png`, `.jpg`, `.jpeg` o `.webp` y reinicia el servidor después de añadir archivos.

## Ejemplo desde JavaScript

```javascript
const respuesta = await fetch("http://127.0.0.1:8001/api/characters");

if (!respuesta.ok) {
  throw new Error(`Error de la API: ${respuesta.status}`);
}

const personajes = await respuesta.json();
console.log(personajes);
```
