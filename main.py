from flet import *
import requests
import json

def get_token(host, username, password):
    resp = requests.get(f'{host}/login/token.php?username={username}&password={password}&service=moodle_mobile_app').text
    token = json.loads(resp)['token']
    return token

def main(page: Page):
    token = get_token('https://cursad.jovenclub.cu', 'eljoker63','33805157Jkr63*')
    page.add(SafeArea(Text(f"Hello, Flet!\n{token}")))

app(target=main, assets_dir="assets")