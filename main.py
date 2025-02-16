import os
os.environ["LANG"] = "en_US.UTF-8"

import userpaths
from nicegui import app, ui
from utils import ConversorCoordernadas
from entities import *

coordenadas = Coordenadas()
baseLevantada = BaseLevantada()
baseCorrigida = BaseLevantamento()
diffs = BaseLevantamento(0, 0, 0)

def update_norte(_):
    norte = baseCorrigida.get_norte() - baseLevantada.get_norte()
    diffs.norte = round(norte, 3)

def update_este(_):
    este = baseCorrigida.get_este() - baseLevantada.get_este()
    diffs.este = round(este, 3)

def update_altura(_):
    altura = baseCorrigida.get_altura() - baseLevantada.get_altura()
    diffs.altura = round(altura, 3)

def converter_coordenadas():
    lat = coordenadas.get_latitude()
    lon = coordenadas.get_longitude()
    baseLevantada.calcular_coordenadas(lat, lon)

async def escolher_arquivos():
    extensoes = ("Arquivos CSV (*.csv)",)
    arquivos = await app.native.main_window.create_file_dialog(
        allow_multiple=True, file_types=extensoes, directory=userpaths.get_downloads()
    )
    if arquivos is None:
        ui.notify('Nenhum arquivo selecionado.')
        return

    for arquivo in arquivos:
        nome_arquivo = os.path.basename(arquivo)
        try:
            ConversorCoordernadas.converter(arquivo, diffs.get_norte(), diffs.get_este(), diffs.get_altura())
            ui.notify(f"Arquivo {nome_arquivo} convertido!", color='green')
        except Exception as erro:
            ui.notify(f'Erro ao tentar converter {nome_arquivo}: {erro}', color='red')

ui.colors(primary="#67538d")
ui.add_head_html('<style>body {background-color: #e2e2e2; }</style>')
with ui.column(align_items="center").classes("fixed-center").classes(
    "w-[80%] max-w-3xl"
):
    with ui.card().classes("mb-[16px]"):
        ui.label(text="👷 Conversor CSV ➡️ Pontos 👷").classes(
            "text-4xl font-extrabold"
        )

    with ui.card().classes("w-full"):
        ui.label("Calcular coordenadas").classes('text-lg')
        with ui.grid(columns=2).classes("w-full"):
            ui.number(
                label="Longitude decimal",
                placeholder="Digite um número",
            ).bind_value(coordenadas, "longitude").props("clearable").classes("w-full")
            ui.number(
                label="Latitude decimal",
                placeholder="Digite um número",
            ).bind_value(coordenadas, "latitude").props("clearable").classes("w-full")

        ui.button(
            "Calcular (SIRGAS2000)",
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
                label="Altura", placeholder="Digite um número", on_change=update_altura
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
                label="Altura", placeholder="Digite um número", on_change=update_altura
            ).bind_value(baseCorrigida, "altura").props("clearable")

        with ui.card().classes("w-full"):
            with ui.grid(columns=3).classes("w-full"):
                ui.label().bind_text_from(diffs, "norte")
                ui.label().bind_text_from(diffs, "este")
                ui.label().bind_text_from(diffs, "altura")

        ui.button("Converter arquivo(s)", on_click=escolher_arquivos).classes("w-full")

ui.run(
    favicon="👷",
    reload=False,
    window_size=(1000, 800),
    title="Conversor CSV ➡️ Pontos",
)
