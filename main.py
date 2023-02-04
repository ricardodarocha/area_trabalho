import subprocess
from typing import Dict

import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    Container,
    icons,
    Image
)
from flet.column import Column


def main(page: Page):
    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()
    select_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent):
        select_button.text = 'Procurar mais arquivos...'
        select_button.current.disabled = False if e.files is None else True
        upload_button.current.visible = False if e.files is None else True
        prog_bars.clear()
        files.current.controls.clear()
        titulo.value = 'clique em processar'
        titulo.update()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = 100
        prog_bars[e.file_name].update()

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=f'/##{f.name}',
                    )
                )
                processar(f.name)
            file_picker.upload(uf)
            
            titulo.value = 'Concluído!'
            select_button.text = 'Procurar mais arquivos...'
            select_button.current.disabled = False
            upload_button.current.visible = False
            page.update()


    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = "0"
        # update text inside drag target control
        e.control.content.content.value = "1"
        page.update()

    # hide dialog in a overlay
    page.overlay.append(file_picker)
    # imagem=Image(src='https://cdn.dribbble.com/users/791530/screenshots/5062062/attachments/1124403/interface_illustration_icons8.png?compress=1&resize=800x600&vertical=top')
    # imagem=Image(src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQo0GfwImo54daQ24cHIW6eUcLvt3Qw6CMfuwJAhQi9Ccn60593yV7Pf-UNrUoskBA0u2A&usqp=CAU')
    imagem=Image(src='https://cdn.dribbble.com/users/690291/screenshots/3507754/untitled-1.gif')
    titulo = flet.Text(
                "Aguardando...",
                size=60,
                color=flet.colors.BLACK,
                weight=flet.FontWeight.W_600,
            )

    def processar(file):
        p = subprocess.Popen(f'"run/iex" {file} Sheet0', stdout=subprocess.PIPE, shell=True)
        r, e = p.communicate()
        if e:
            print('erro', e)
        else:
            import base64
            file_name_string = base64.urlsafe_b64encode(r)
            filename = base64.b64decode(file_name_string)
            print(filename)
        

    botao_procurar = ElevatedButton(
            "Procurar...",
            ref=select_button,
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
            )
    botao_processar = ElevatedButton(
            "processar",
            ref=upload_button,
            icon=icons.PLAY_CIRCLE_ROUNDED,
            on_click=upload_files,
            visible=False,
        )

    container1 = flet.Container(padding=flet.padding.only(left=50), content=botao_procurar)
    selected_files = flet.Container(padding=flet.padding.only(left=50), content=Column(ref=files))
    container2 = flet.Container(padding=flet.padding.only(left=50), content=botao_processar)
    container3 = flet.Container(padding=flet.padding.only(left=50), content=titulo)
    draggable_image  = flet.DragTarget(
                    group="number",
                    content=imagem,
                    on_accept=drag_accept,
                )

    page.add(
        selected_files,
        container1,
        container2,
        container3,
        draggable_image
        )
    
flet.app(target=main, upload_dir="uploads")