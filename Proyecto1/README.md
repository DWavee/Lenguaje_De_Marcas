# Danganronpa 1 FanWiki

Wiki no oficial sobre los personajes de Danganronpa: Trigger Happy Havoc. Proyecto 1 de Lenguajes de Marcas (fase 1: estructura HTML).

Autor: Mario García Canca.

## Apartado de la API

- **Nombre:** [`datos/personajes.json`](datos/personajes.json), una API propia creada para este proyecto.
- **Categoría:** no sale de la lista *Public APIs*: la creé con ayuda de Copilot, con el visto bueno del profesor.
- **Origen:** los datos los recopiló una IA (Copilot) tomando como referencia la wiki [Danganronpa Fandom](https://danganronpa.fandom.com/wiki/Danganronpa_Wiki). Cada personaje lleva en `profile.source` la página de la wiki de la que sale.
- **Mantenimiento:** lo mantengo yo en este repositorio.
- **Documentación:** la tabla de campos de la sección siguiente.
- **Condiciones de uso:** el contenido de las wikis de Fandom suele publicarse con una licencia Creative Commons con atribución (CC BY-SA), por eso la web cita la fuente en el pie y en «Sobre los datos». Los personajes y las imágenes pertenecen a sus creadores. Es un proyecto de clase, no oficial y sin ánimo de lucro.
- **Peticiones:** no hay peticiones a una API externa. El JSON se generó con Copilot y se guardó en `datos/`, y el contenido de las páginas sale de ese fichero.

## Tabla de campos

Campos de cada personaje del JSON, con lo que significan para quien lee la web y cómo se marcan en HTML.

| Campo | Tipo | Qué es para quien lee | Cómo se marca |
|---|---|---|---|
| `id` | texto | Identificador del personaje | Nombre de su ficha (`fichas/id.html`) y de la carpeta de sus imágenes |
| `name` | texto | Nombre | `h1` en la ficha, `h3` en las tarjetas, `th` en la comparativa |
| `japaneseName` | texto | Nombre original | `dd` con `lang="ja"` |
| `game` / `gameTitle` | texto | Juego al que pertenece | Solo aparece en los textos de las páginas, porque todos son del mismo juego |
| `talent` | texto | Talento | `dd` bajo «Talento» y `td` en la comparativa |
| `role` | texto | Papel en la historia | `dd` dentro del `details` del destino (puede ser un spoiler) |
| `description` | texto | Descripción | `p` en la ficha y `meta description` de la página |
| `profile.birthday` | texto (día y mes) | Cumpleaños | `time` con `datetime="MM-DD"` |
| `profile.height` | lista de textos | Altura | `dd` en la ficha y `td` numérico en la comparativa |
| `profile.bloodType` | texto o `null` | Grupo sanguíneo | `dd`, con «Desconocido» si es `null` |
| `profile.likes` / `dislikes` | listas de textos | Gustos | `ul` con un `li` por elemento y `td` en la comparativa |
| `profile.personality` | texto | Personalidad | No se muestra (repite la descripción) |
| `profile.source` | URL | Página del personaje en la wiki | `a` con enlace externo |
| `fate.status` | texto | Si sobrevive o muere | `dd` en el `details` y clase `superviviente` o `fallecido` en la comparativa |
| `fate.chapter` | número, texto o `null` | Capítulo | `dd`, con «No aplica» si es `null` |
| `fate.role` | texto | Papel final | `dd` en el `details` |
| `fate.context` | texto o `null` | Contexto | `dd`, con «No aplica» si es `null` |

## Qué hay en cada página

- **`index.html`:** bienvenida, vídeo de presentación incrustado desde YouTube (con enlace alternativo) y cinco personajes destacados con enlace a su ficha.
- **`catalogo.html`:** los 17 personajes en dos grupos (16 estudiantes y el director), cada uno con imagen, nombre, talento, cumpleaños y enlace a su ficha.
- **`fichas/`:** 17 fichas con la misma estructura: aviso de spoilers, datos, gustos, descripción, imagen y, en un `details`, el destino con una foto grande.
- **`comparativa.html`:** tabla de los 16 estudiantes con talento, gustos, altura y destino, dentro de un `details` con aviso de spoilers, y pie con el recuento de supervivientes.
- **`sobre-los-datos.html`:** origen y licencia de los datos, y un fragmento real del JSON junto a la tarjeta HTML que genera.
- **`propuesta.html`:** formulario de 13 campos agrupados en cuatro bloques, con obligatorios y opcionales distinguidos.

## Decisiones de marcado

1. **`dl` o tabla en las fichas.** Dudé porque los datos están en un JSON y la tabla es más directa. Elegí `dl` porque cada dato es un par «nombre: valor», y reservé la tabla para la comparativa, que sí tiene filas y columnas.
2. **Cómo evitar los spoilers.** Puse un aviso al principio y uso `details` y `summary` para esconder el destino en las fichas y la tabla en la comparativa. Así nadie ve un spoiler sin querer.
3. **Vídeo con reproducción automática.** Es la primera vez que incrusto un vídeo, y aprendí que solo arranca solo si va silenciado. Lo dejé así porque tiene controles y un enlace alternativo, y es una decisión de diseño.
4. **Cumpleaños sin año.** Mis datos no tienen año, así que no usé `type="date"`: el formulario pide mes y día, y en las páginas uso `time` con `datetime="MM-DD"`.

## Validación

Las 22 páginas HTML (las cinco principales y las 17 fichas) pasan por el validador del W3C (validator.w3.org) sin errores.