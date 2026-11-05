import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse


DATA_FILE = Path(__file__).with_name("characters.json")
IMAGES_DIR = Path(__file__).with_name("images")
GAME_IMAGES_DIR = IMAGES_DIR / "games"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
DEFAULT_PORT = 8001


def load_characters():
    with DATA_FILE.open(encoding="utf-8") as file:
        characters = json.load(file)

    if not isinstance(characters, list) or not all(
        isinstance(character, dict) for character in characters
    ):
        raise ValueError("characters.json debe contener una lista de personajes.")

    return characters


GAMES = [
    {
        "id": "danganronpa-1",
        "name": "Danganronpa: Trigger Happy Havoc",
    },
]
GAME_IDS = {game["id"] for game in GAMES}
IMAGE_GAME_IDS = GAME_IDS
CHARACTERS = load_characters()


def game_image_path(game_id):
    return next(
        (
            GAME_IMAGES_DIR / ("game-{}".format(game_id) + extension)
            for extension in IMAGE_EXTENSIONS
            if (GAME_IMAGES_DIR / ("game-{}".format(game_id) + extension)).is_file()
        ),
        None,
    )


def cover_image_path():
    return next(
        (
            path
            for extension in IMAGE_EXTENSIONS
            if (path := IMAGES_DIR / ("foto_index" + extension)).is_file()
        ),
        None,
    )


for game in GAMES:
    game["image"] = (
        "/images/games/{}".format(game["id"])
        if game_image_path(game["id"]) is not None
        else None
    )


def image_path(character_id, image_name):
    image_directory = IMAGES_DIR / character_id
    image_names = [image_name]
    if image_name == "sprite-danganronpa-1":
        image_names.append("sprites")
    elif image_name == "sprites":
        image_names.append("sprite-danganronpa-1")

    return next(
        (
            image_directory / (name + extension)
            for name in image_names
            for extension in IMAGE_EXTENSIONS
            if (image_directory / (name + extension)).is_file()
        ),
        None,
    )


def photo_image_path(character_id):
    return image_path(character_id, "foto") or image_path(character_id, character_id)


def additional_image_files(character_id):
    character_directory = IMAGES_DIR / character_id
    if not character_directory.is_dir():
        return []

    return sorted(
        (
            path
            for path in character_directory.iterdir()
            if path.is_file()
            and path.suffix.casefold() in IMAGE_EXTENSIONS
            and path.stem.casefold()
            not in (
                "portrait",
                "sprite",
                "sprites",
                "death",
                "foto",
                character_id.casefold(),
            )
            and not path.stem.startswith(("portrait-", "sprite-"))
            and not (
                path.stem.startswith("execution-")
                and path.stem.removeprefix("execution-").isdigit()
            )
        ),
        key=lambda path: path.name.casefold(),
    )


def additional_image_path(character_id, filename):
    if Path(filename).name != filename:
        return None

    return next(
        (
            path
            for path in additional_image_files(character_id)
            if path.name == filename
        ),
        None,
    )


def add_image_routes(character):
    character_id = character["id"]
    character_directory = IMAGES_DIR / character_id
    portrait_variants = {
        path.stem.removeprefix("portrait-"): "/images/{}/portrait/{}".format(
            character_id,
            path.stem.removeprefix("portrait-"),
        )
        for path in character_directory.glob("portrait-*")
        if path.suffix.casefold() in IMAGE_EXTENSIONS and path.is_file()
    }
    sprite_variants = {
        path.stem.removeprefix("sprite-"): "/images/{}/sprites/variant/{}".format(
            character_id,
            path.stem.removeprefix("sprite-"),
        )
        for path in character_directory.glob("sprite-*")
        if path.suffix.casefold() in IMAGE_EXTENSIONS
        and path.is_file()
        and path.stem.removeprefix("sprite-") not in IMAGE_GAME_IDS
    }
    execution_images = sorted(
        (
            path
            for path in character_directory.glob("execution-*")
            if path.suffix.casefold() in IMAGE_EXTENSIONS
            and path.is_file()
            and path.stem.removeprefix("execution-").isdigit()
        ),
        key=lambda path: int(path.stem.removeprefix("execution-")),
    )
    character["images"] = {
        "portrait": "/images/{}/portrait".format(character_id),
        "photo": (
            "/images/{}/photo".format(character_id)
            if photo_image_path(character_id) is not None
            else None
        ),
        "portraits": portrait_variants,
        "spriteVariants": sprite_variants,
        "death": (
            "/images/{}/death".format(character_id)
            if image_path(character_id, "death") is not None
            else None
        ),
        "executions": [
            "/images/{}/execution/{}".format(
                character_id,
                path.stem.removeprefix("execution-"),
            )
            for path in execution_images
        ],
        "sprites": (
            "/images/{}/sprites".format(character_id)
            if image_path(character_id, "sprites") is not None
            else None
        ),
        "additional": [
            {
                "name": path.name,
                "url": "/images/{}/file/{}".format(
                    character_id,
                    quote(path.name, safe=""),
                ),
            }
            for path in additional_image_files(character_id)
        ],
    }
for character in CHARACTERS:
    add_image_routes(character)


class APIHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = unquote(parsed_url.path).rstrip("/")
        query = parse_qs(parsed_url.query)

        if path == "/api":
            self.send_json(
                200,
                {
                    "name": "Danganronpa 1 Characters API",
                    "cover": "/images/cover" if cover_image_path() else None,
                    "endpoints": [
                        "/api/characters",
                        "/api/characters/{id}",
                        "/api/games",
                        "/api/games/{id}/characters",
                        "/images/cover",
                        "/images/{id}/portrait",
                        "/images/{id}/portrait/{variant}",
                        "/images/{id}/photo",
                        "/images/{id}/sprites",
                        "/images/{id}/sprites/{game_id}",
                        "/images/{id}/sprites/variant/{variant}",
                        "/images/{id}/death",
                        "/images/{id}/execution/{number}",
                        "/images/{id}/file/{filename}",
                        "/images/games/{game_id}",
                    ],
                },
            )
            return

        if path == "/api/health":
            self.send_json(200, {"status": "ok"})
            return

        if path.startswith("/images/"):
            if path == "/images/cover":
                image_file = cover_image_path()
                if image_file is None:
                    self.send_json(404, {"error": "Imagen de portada no encontrada."})
                    return

                image = image_file.read_bytes()
                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    mimetypes.guess_type(image_file.name)[0]
                    or "application/octet-stream",
                )
                self.send_header("Content-Length", str(len(image)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(image)
                return

            if path.startswith("/images/games/"):
                game_id = path.removeprefix("/images/games/")
                if game_id not in GAME_IDS:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return

                image_file = game_image_path(game_id)
                if image_file is None:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return

                image = image_file.read_bytes()
                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    mimetypes.guess_type(image_file.name)[0]
                    or "application/octet-stream",
                )
                self.send_header("Content-Length", str(len(image)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(image)
                return

            image_parts = path.strip("/").split("/")
            if len(image_parts) not in (3, 4, 5):
                self.send_json(404, {"error": "Imagen no encontrada."})
                return

            _, character_id, image_type, *variant_part = image_parts
            character = next(
                (item for item in CHARACTERS if item["id"] == character_id),
                None,
            )
            if character is None or image_type not in (
                "portrait",
                "photo",
                "sprite",
                "sprites",
                "death",
                "execution",
                "file",
            ):
                self.send_json(404, {"error": "Imagen no encontrada."})
                return

            image_file = None
            if image_type == "photo" and not variant_part:
                image_file = photo_image_path(character_id)
                if image_file is None:
                    self.send_json(404, {"error": "Foto no encontrada."})
                    return
            elif image_type == "file" and len(variant_part) == 1:
                image_file = additional_image_path(character_id, variant_part[0])
                if image_file is None:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
            elif image_type == "death" and not variant_part:
                image_name = "death"
            elif image_type == "execution" and len(variant_part) == 1:
                execution_number = variant_part[0]
                if not execution_number.isdigit() or int(execution_number) < 1:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                image_name = "execution-{}".format(int(execution_number))
            elif image_type in ("sprite", "sprites") and len(variant_part) == 1:
                image_game_id = variant_part[0]
                if image_game_id not in IMAGE_GAME_IDS:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                image_name = "sprite-{}".format(image_game_id)
            elif (
                image_type in ("sprite", "sprites")
                and len(variant_part) == 2
                and variant_part[0] == "variant"
            ):
                variant = variant_part[1]
                if not variant or any(
                    character not in "abcdefghijklmnopqrstuvwxyz0123456789-"
                    for character in variant
                ):
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                image_name = "sprite-{}".format(variant)
                if variant in IMAGE_GAME_IDS:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
            elif image_type == "portrait" and variant_part:
                if len(variant_part) != 1:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                variant = variant_part[0]
                if not variant or any(
                    character not in "abcdefghijklmnopqrstuvwxyz0123456789-"
                    for character in variant
                ):
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                image_name = "portrait-{}".format(variant)
            elif image_type in ("sprite", "sprites"):
                if variant_part:
                    self.send_json(404, {"error": "Imagen no encontrada."})
                    return
                image_name = "sprites"
            elif image_type == "portrait" and not variant_part:
                image_name = "portrait"
            else:
                self.send_json(404, {"error": "Imagen no encontrada."})
                return

            if image_type not in ("file", "photo"):
                image_file = image_path(character_id, image_name)
            if image_file is None:
                self.send_json(404, {"error": "Imagen no encontrada."})
                return

            image = image_file.read_bytes()
            self.send_response(200)
            self.send_header(
                "Content-Type",
                mimetypes.guess_type(image_file.name)[0] or "application/octet-stream",
            )
            self.send_header("Content-Length", str(len(image)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(image)
            return

        if path == "/api/games":
            self.send_json(200, GAMES)
            return

        if path.startswith("/api/games/") and path.endswith("/characters"):
            game_id = path.removeprefix("/api/games/").removesuffix("/characters")
            game_id = game_id.strip("/")
            if not any(game["id"] == game_id for game in GAMES):
                self.send_json(404, {"error": "Juego no encontrado."})
                return
            results = [character for character in CHARACTERS if character["game"] == game_id]
            self.send_json(200, results)
            return

        if path == "/api/characters":
            results = CHARACTERS
            game_id = query.get("game", [""])[0].casefold()
            role = query.get("role", [""])[0].casefold()
            search = query.get("search", [""])[0].casefold()

            if game_id:
                results = [character for character in results if character["game"] == game_id]
            if role:
                results = [character for character in results if character["role"].casefold() == role]
            if search:
                results = [
                    character
                    for character in results
                    if search
                    in " ".join(
                        (
                            character["name"],
                            character["talent"],
                            character["description"],
                            *(
                                value
                                for value in character.get("profile", {}).values()
                                if isinstance(value, str)
                            ),
                            *(
                                value
                                for key in ("height", "likes", "dislikes")
                                for value in character.get("profile", {}).get(key, [])
                                if isinstance(value, str)
                            ),
                        )
                    ).casefold()
                ]

            self.send_json(200, results)
            return

        if path.startswith("/api/characters/"):
            character_id = path.removeprefix("/api/characters/")
            character = next(
                (item for item in CHARACTERS if item["id"] == character_id),
                None,
            )
            if character is None:
                self.send_json(404, {"error": "Personaje no encontrado."})
                return
            self.send_json(200, character)
            return

        self.send_json(404, {"error": "Ruta no encontrada."})

    def do_POST(self):
        self.send_json(405, {"error": "Método no permitido. Usa GET."})

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


def main():
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    server = ThreadingHTTPServer(("127.0.0.1", port), APIHandler)
    print("API disponible en http://127.0.0.1:{}/api".format(port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando API...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
