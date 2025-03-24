from contextlib import contextmanager
from nicegui import ui

@contextmanager
def frame(id:str):
    if id=='':
        ui.navigate.to('/setup')

    """Custom page frame to share the same styling and behavior across all pages"""
    with ui.header().classes('justify-center'):
        ui.label('RESELF')
        with ui.link(target='/'):
            ui.icon('home')
        with ui.link(target='/user/'+id):
            ui.icon('account_circle')
        with ui.link(target='/settings'):
            ui.icon('settings')
    with ui.footer().classes('justify-center'):
        ui.link('github', 'https://github.com')
        ui.link("author's link", '/user/k51qzi5uqu5dgwz80ysfut2o4mg9k9gekckbhd2kax8q5ny229v7r1lcsm2dmk')
    with ui.column().classes('absolute-center items-center'):
        yield