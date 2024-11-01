from flet import *
import requests
import json

version = '3.0.1'
DEV = 'ElJoker63'

def get_token(host, username, password):
    try:
        resp = requests.get(f'{host}/login/token.php?username={username}&password={password}&service=moodle_mobile_app').text
        token = json.loads(resp)['token']
        return token
    except Exception as e:
        return f"Error: {str(e)}"

def main(page: Page):
    page.theme_mode = "dark"
    page.padding = 0
    page.spacing = 0
    # Configure theme colors
    page.theme = Theme(
        color_scheme=ColorScheme(
            primary="#00aa94",
            secondary="#153333",
            )
        )
    
    # Resultado del token
    result_text = Text("", size=14, color="white", text_align="center", selectable=True)
    copy_message = Text("", size=12, color="#00aa94", text_align="center")
    
    def copy_to_clipboard(e):
        if result_text.value and not result_text.value.startswith("Por favor") and not result_text.value.startswith("Error"):
            # Extraer solo el token del texto completo
            token = result_text.value
            page.set_clipboard(token)
            # Mostrar mensaje de copiado
            copy_message.value = "¡Token copiado!"
            page.update()
            # Limpiar mensaje después de 2 segundos
            page.after(2, lambda _: clear_copy_message())
    
    def clear_copy_message():
        copy_message.value = ""
        page.update()
    
    def generate_token(e):
        if not host.value or not username.value or not password.value:
            result_text.value = "Por favor complete todos los campos"
            result_text.color = "red"
            copy_message.value = ""
        else:
            # Mostrar indicador de carga
            button.content.controls[0].visible = False
            button.content.controls[1].visible = True
            page.update()
            
            # Obtener token
            token = get_token(host.value, username.value, password.value)
            
            # Actualizar resultado
            if token.startswith("Error"):
                result_text.value = token
                result_text.color = "red"
                copy_message.value = ""
            else:
                result_text.value = f"{token}"
                result_text.color = "green"
                copy_message.value = "Toca el token para copiarlo"
            
            # Restaurar botón
            button.content.controls[0].visible = True
            button.content.controls[1].visible = False
        page.update()

    # Componentes de la UI
    logo = Image(
        src="http://192.168.1.161:5500/assets/icon.png",
        width=120,
        height=120,
        fit=ImageFit.CONTAIN
    )
    
    title = Text("GENTOKEN+", 
        size=32, 
        color="white",
        weight=FontWeight.BOLD,
        text_align=TextAlign.CENTER
    )
    
    divider = Divider(height=30, color='transparent')
    divider50 = Divider(height=50, color='transparent')
    
    host = TextField(
        label="Moodle",
        border_radius=35,
        min_lines=1,
        max_lines=1,
        width=300,        
        height=50,
        border_color="#00aa94"
    )
    
    username = TextField(
        label="Usuario",
        border_radius=35,
        min_lines=1,
        max_lines=1,
        width=300,
        height=50,
        border_color="#00aa94"
    )
    
    password = TextField(
        label="Contraseña",
        password=True,
        border_radius=35,
        min_lines=1,
        max_lines=1,
        width=300,
        height=50,
        border_color="#00aa94"
    )
    
    # Botón con indicador de carga
    button = Container(
        content=Stack(
            controls=[
                Text("GENERAR TOKEN", size=16, weight=FontWeight.BOLD, color='#153333'),
                ProgressRing(visible=False)
            ],
        ),
        width=200,
        height=40,
        bgcolor="#00aa94",
        border_radius=35,
        alignment=alignment.center,
        on_click=generate_token,
        ink=True,
    )

    # Hacer el texto del resultado clickeable
    result_container = GestureDetector(
        content=Column([
            result_text,
            copy_message
        ], spacing=5, horizontal_alignment=CrossAxisAlignment.CENTER),
        on_tap=copy_to_clipboard
    )

    copy = Row([Text(spans=[TextSpan(text=f"v{version} by {DEV}")], color='#00aa94')], alignment=MainAxisAlignment.CENTER)

    # Contenedor principal
    cont = Container(
        content=Column(
            controls=[
                divider,
                logo,
                divider,
                title,
                divider,
                host,
                username,
                password,
                divider,
                button,
                divider,
                result_container,
                divider50,
                copy,
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
        ),
        padding=10, alignment=alignment.center, bgcolor='#153333'
    )
    
    page.add(cont)

app(target=main, assets_dir="assets")