from flet import *
import requests
import json

version = '3.0.0'
DEV = 'ElJoker63'

# Define a link style dict.
link_style = {
    "height": 50,
    "focused_border_color": "#00aa94",
    "border_radius": 5,
    "cursor_height": 16,
    "cursor_color": "white",
    "content_padding": 10,
    "border_width": 1.5,
    "text_size": 14,
    "label_style": TextStyle(color="#00aa94"),
}

def get_token(host, username, password):
    try:
        response = requests.post(f"{host}/login/token.php", {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app"
        })
        data = response.json()
        if "token" in data:
            return data["token"]
        elif "error" in data:
            return f"Error: {data['error']}"
        return "Error: Unknown response from server"
    except Exception as e:
        return f"Error: {str(e)}"

def compare_versions(version1, version2):
    v1_parts = [int(part) for part in version1.split('.')]
    v2_parts = [int(part) for part in version2.split('.')]
    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0

def get_update():
    try:
        url = "https://api.github.com/repos/ElJoker63/GENTOKENPLUS/releases/latest"
        resp = requests.get(url).text
        data = json.loads(resp)
        name = data['name'].replace(data['tag_name'], '')
        return name, data['body'], data['tag_name'], data['assets'][0]['browser_download_url']
    except Exception as e:
        return "Error", str(e), "v0.0.0", "#"

class MainPage(UserControl):
    def __init__(self):
        super().__init__()
        self.logo = Image(
            src="/icon.png",
            width=120,
            height=120,
            fit=ImageFit.CONTAIN
        )
        
        self.title = Text(
            "GENTOKEN+",
            size=32,
            color="white",
            weight=FontWeight.BOLD,
            text_align=TextAlign.CENTER
        )
        
        self.host = TextField(
            label="Moodle",
            border_radius=35,
            min_lines=1,
            max_lines=1,
            width=300,
            height=50,
            border_color="#00aa94"
        )
        
        self.username = TextField(
            label="Usuario",
            border_radius=35,
            min_lines=1,
            max_lines=1,
            width=300,
            height=50,
            border_color="#00aa94"
        )
        
        self.password = TextField(
            label="Contraseña",
            password=True,
            border_radius=35,
            min_lines=1,
            max_lines=1,
            width=300,
            height=50,
            border_color="#00aa94"
        )
        
        self.result_text = Text(
            "",
            size=14,
            color="white",
            text_align="center",
            selectable=True
        )
        
        self.copy_message = Text(
            "",
            size=12,
            color="#00aa94",
            text_align="center"
        )
        
        self.progress_ring = ProgressRing(visible=False)
        self.button_text = Text("GENERAR TOKEN", size=16, weight=FontWeight.BOLD, color='#153333')
        
        self.button = Container(
            content=Stack(
                controls=[
                    self.button_text,
                    self.progress_ring
                ],
            ),
            width=200,
            height=40,
            bgcolor="#00aa94",
            border_radius=35,
            alignment=alignment.center,
            on_click=self.generate_token,
            ink=True,
        )

    def copy_to_clipboard(self, e):
        if (self.result_text.value and 
            not self.result_text.value.startswith("Por favor") and 
            not self.result_text.value.startswith("Error")):
            self.page.set_clipboard(self.result_text.value)
            self.copy_message.value = "¡Token copiado!"
            self.copy_message.update()
            self.page.after(2, self.clear_copy_message)

    def clear_copy_message(self, _=None):
        self.copy_message.value = ""
        self.copy_message.update()

    async def generate_token(self, e):
        if not self.host.value or not self.username.value or not self.password.value:
            self.result_text.value = "Por favor complete todos los campos"
            self.result_text.color = "red"
            self.copy_message.value = ""
            self.result_text.update()
            return

        self.button_text.visible = False
        self.progress_ring.visible = True
        self.button.update()

        token = await self.page.run_async(
            get_token,
            self.host.value,
            self.username.value,
            self.password.value
        )

        if token.startswith("Error"):
            self.result_text.value = token
            self.result_text.color = "red"
            self.copy_message.value = ""
        else:
            self.result_text.value = token
            self.result_text.color = "green"
            self.copy_message.value = "Toca el token para copiarlo"

        self.button_text.visible = True
        self.progress_ring.visible = False
        self.button.update()
        self.result_text.update()
        self.copy_message.update()

    def build(self):
        result_container = GestureDetector(
            content=Column(
                [self.result_text, self.copy_message],
                spacing=5,
                horizontal_alignment=CrossAxisAlignment.CENTER
            ),
            on_tap=self.copy_to_clipboard
        )

        return Container(
            content=Column(
                controls=[
                    Divider(height=30, color='transparent'),
                    self.logo,
                    Divider(height=30, color='transparent'),
                    self.title,
                    Divider(height=30, color='transparent'),
                    self.host,
                    self.username,
                    self.password,
                    Divider(height=30, color='transparent'),
                    self.button,
                    Divider(height=30, color='transparent'),
                    result_container,
                    Divider(height=50, color='transparent'),
                    Row(
                        [Text(f"v{version} by {DEV}", color='#00aa94')],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            ),
            padding=10,
            alignment=alignment.center,
            bgcolor='#153333'
        )

class LandingPage(UserControl):
    def __init__(self, update_info):
        super().__init__()
        self.name, self.body, self.tag, self.download_url = update_info
        
    def build(self):
        return SafeArea(
            expand=True,
            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                scroll=ScrollMode.ALWAYS,
                controls=[
                    Column(
                        controls=[
                            Divider(height=120, color="transparent"),
                            Image(src="/icon.png"),
                            Text(
                                self.name,
                                size=30,
                                weight=FontWeight.BOLD
                            ),
                            Divider(height=5, color="transparent"),
                            Markdown(
                                self.body,
                                selectable=False,
                                on_tap_link=lambda e: self.page.launch_url(e.data)
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    Divider(height=20, color="transparent"),
                    Row(
                        controls=[
                            Container(
                                border_radius=5,
                                expand=True,
                                bgcolor="#00aa94",
                                content=Text(
                                    "ACTUALIZAR",
                                    color="white",
                                    size=18
                                ),
                                padding=padding.only(
                                    left=25,
                                    right=25,
                                    top=10,
                                    bottom=10
                                ),
                                alignment=alignment.center,
                                on_click=lambda _: self.page.launch_url(
                                    self.download_url
                                ),
                            )
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ],
            ),
        )

def main(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    page.theme = Theme(
        color_scheme=ColorScheme(
            primary="#00aa94",
            secondary="#153333"
        ),
        scrollbar_theme=ScrollbarTheme(
            thumb_color={
                MaterialState.DEFAULT: colors.TRANSPARENT
            }
        ),
    )

    update_info = get_update()
    current_version = version
    latest_version = update_info[2].replace('v', '')
    
    # Check if update is available
    if compare_versions(current_version, latest_version) == -1:
        page.add(LandingPage(update_info))
    else:
        page.add(MainPage())

app(target=main, assets_dir="assets")