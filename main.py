import os

os.environ["LANG"] = "en_US.UTF-8"

import userpaths
from nicegui import app, ui
from utils import CalculadoraGeografica, ConversorCoordernadas

class Decimal:
    lat: float  # y
    lon: float  # x

diffs = {"norte": 0, "este": 0, "altura": 0}


class BaseLevantamento:
    norte: float  # y
    este: float  # x
    altura: float

    def calcular_coordenadas(self, lat, lon):
        calc = CalculadoraGeografica()
        x, y = calc.geo_para_utm(lat, lon)
        self.norte = y
        self.este = x


decimal = Decimal()
baseLevantada = BaseLevantamento()
baseCorrigida = BaseLevantamento()


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


def converter_coordenadas():
    lat = decimal.lat if decimal.lat is not None else 0
    lon = decimal.lon if decimal.lon is not None else 0
    baseLevantada.calcular_coordenadas(lat, lon)


async def pick_file():
    file_types = ("Arquivos CSV (*.csv)",)
    files = await app.native.main_window.create_file_dialog(
        allow_multiple=True, file_types=file_types, directory=userpaths.get_my_documents()
    )
    if files is None:
        return

    for file in files:
        ConversorCoordernadas.converter(file, diffs["norte"], diffs["este"], diffs["altura"])
        ui.notify(f"Arquivo {os.path.basename(file)} convertido!")


ui.colors(primary="#67538d")
ui.add_head_html('<style>body {background-color: #e2e2e2; }</style>')
with ui.column(align_items="center").classes("fixed-center").classes(
    "w-[80%] max-w-3xl"
):
    ui.label(text="👷 Conversor CSV -> Pontos 👷").classes(
        "text-4xl font-extrabold mb-[16px]"
    )

    with ui.card().classes("w-full"):
        ui.label("Calcular coordenadas").classes('text-lg')
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
            "Calcular",
            on_click=converter_coordenadas,
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

        ui.button("Calcular arquivo(s)", on_click=pick_file).classes("w-full")

ui.run(
    favicon="👷",
    reload=False,
    window_size=(1000, 800),
    title="Conversor CSV -> Pontos",
)
