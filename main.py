import os

os.environ["LANG"] = "en_US.UTF-8"

import userpaths
from nicegui import app, ui
from services import CalculadoraGeografica, ConversorCoordernadas

class Decimal:
    def __init__(self):
        self.lat: float  # y
        self.lon: float  # x


diffs = {"norte": 0, "este": 0, "altura": 0}


class BaseLevantada:
    def __init__(self):
        self.norte: float  # y
        self.este: float  # x
        self.altura: float

    def converterCoordenadas(self, lat, lon):
        calc = CalculadoraGeografica()
        x, y = calc.geo_para_utm(lat, lon)
        self.norte = y
        self.este = x


class BaseCorrigida:
    def __init__(self):
        self.norte: float  # y
        self.este: float  # x
        self.altura: float


decimal = Decimal()
baseLevantada = BaseLevantada()
baseCorrigida = BaseCorrigida()


def update_norte(_):
    cor = 0 if baseCorrigida.norte is None else baseCorrigida.norte
    lev = 0 if baseLevantada.norte is None else baseLevantada.norte
    diffs.update(norte=round(cor - lev, 3))


def update_este(_):
    cor = 0 if baseCorrigida.este is None else baseCorrigida.este
    lev = 0 if baseLevantada.este is None else baseLevantada.este
    diffs.update(este=round(cor - lev, 3))


def update_alt(_):
    cor = 0 if baseCorrigida.altura is None else baseCorrigida.altura
    lev = 0 if baseLevantada.altura is None else baseLevantada.altura
    diffs.update(altura=round(cor - lev, 3))


def converterCoordenadas():
    lat = decimal.lat if hasattr(decimal, "lat") and decimal.lat is not None else 0
    lon = decimal.lon if hasattr(decimal, "lon") and decimal.lon is not None else 0
    baseLevantada.converterCoordenadas(lat, lon)


async def pick_file():
    file_types = ("Arquivos CSV (*.csv)",)
    files = await app.native.main_window.create_file_dialog(
        allow_multiple=True, file_types=file_types, directory=userpaths.get_my_documents()
    )
    if files is None:
        return

    conversor = ConversorCoordernadas()
    for file in files:
        conversor.converter(file, diffs["norte"], diffs["este"], diffs["altura"])
        ui.notify(f"Arquivo {os.path.basename(file)} convertido!")


ui.colors(primary="#67538d")
with ui.column(align_items="center").classes("fixed-center").classes(
    "w-[80%] max-w-3xl"
):
    ui.label(text="👷 Conversor CSV -> Pontos 👷").classes(
        "text-4xl font-extrabold mb-[16px]"
    )

    with ui.card().classes("w-full"):
        ui.label("Converter coordenadas").classes('text-lg')
        with ui.grid(columns=2).classes("w-full"):
            ui.number(
                label="Longitude decimal",
                placeholder="Digite um número",
            ).bind_value(decimal, "lon").props("clearable").classes("w-full")
            ui.number(
                label="Latitude decimal",
                placeholder="Digite um número",
            ).bind_value(decimal, "lat").props("clearable").classes("w-full")

        ui.button(
            "Converter",
            on_click=converterCoordenadas,
        ).classes("w-full")

    with ui.card().classes("w-full"):
        ui.label("Base levantada").classes('text-lg')
        with ui.grid(columns=3).classes("w-full"):
            ui.number(
                label="Norte",
                placeholder="Digite um número",
                format="%.8f",
                on_change=update_norte,
            ).bind_value(baseLevantada, "norte").props("readonly")

            ui.number(
                label="Este",
                placeholder="Digite um número",
                format="%.7f",
                on_change=update_este,
            ).bind_value(baseLevantada, "este").props("readonly")

            ui.number(
                label="Altura", placeholder="Digite um número", on_change=update_alt
            ).bind_value(baseLevantada, "altura").props("clearable")

        ui.separator().classes("my-[16px]")
        ui.label("Base corrigida").classes('text-lg')
        with ui.grid(columns=3).classes("w-full"):
            ui.number(
                label="Norte", placeholder="Digite um número", on_change=update_norte
            ).bind_value(baseCorrigida, "norte").props("clearable")

            ui.number(
                label="Este", placeholder="Digite um número", on_change=update_este
            ).bind_value(baseCorrigida, "este").props("clearable")

            ui.number(
                label="Altura", placeholder="Digite um número", on_change=update_alt
            ).bind_value(baseCorrigida, "altura").props("clearable")

        with ui.card().classes("w-full"):
            with ui.grid(columns=3).classes("w-full"):
                ui.label().bind_text_from(diffs, "norte")
                ui.label().bind_text_from(diffs, "este")
                ui.label().bind_text_from(diffs, "altura")

        ui.button("Selecionar arquivo(s)", on_click=pick_file).classes("w-full")

ui.run(
    favicon="👷",
    reload=False,
    window_size=(1000, 800),
    dark=True,
    title="Conversor CSV -> Pontos",
)
