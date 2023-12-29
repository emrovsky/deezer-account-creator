import threading
import time

from textual.widgets import Input, Label, Pretty, Button
from textual.app import App, ComposeResult
from rich_pixels import Pixels
import capsolver
import requests
import string
import random
import json













class DeezerUi(App):
    CSS_PATH = "button.tcss"
    def generate(self,capsolver_key,account_domain):
        try:
            session = requests.session()
            proxy = random.choice(open("proxies.txt","r").readlines()).strip()
            session.proxies = {'http': 'http://' + proxy.strip(), 'https': 'http://' + proxy.strip()}
            session.headers = {
                'authority': 'www.deezer.com',
                'accept': '*/*',
                'accept-language': 'tr-TR,tr;q=0.5',
                'cache-control': 'no-cache',
                'content-type': 'text/plain;charset=UTF-8',
                'origin': 'https://www.deezer.com',
                'pragma': 'no-cache',
                'referer': 'https://www.deezer.com/us/register',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'same-origin',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            capsolver.api_key = capsolver_key


            cid = str(random.randint(100000000, 999999999)) #random
            username = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            email = (username+"@"+account_domain).lower()

            session.get("https://www.deezer.com/us/register")
            params = {
                'method': 'deezer.getUserData',
                'input': '3',
                'api_version': '1.0',
                'api_token': '',
                'cid': cid,
            }



            response = session.post('https://www.deezer.com/ajax/gw-light.php', params=params, data = '{}')
            api_token = response.json()["results"]["checkForm"]

            params = {
                'method': 'deezer.emailCheck',
                'input': '3',
                'api_version': '1.0',
                'api_token': api_token,
                'cid': cid,
            }

            data = json.dumps({"EMAIL":email})

            response = session.post('https://www.deezer.com/ajax/gw-light.php', params=params, data=data)
            print(response.text)

            recaptcha_token = capsolver.solve({
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://www.deezer.com",
                "websiteKey": "6Ld3MwwbAAAAAKrvn3uSoG60t1A0owdX3ByEstx8",
                "apiDomain":"http://www.google.com/",
                "isInvisible":True
            })["gRecaptchaResponse"]

            session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            session.headers['sec-fetch-mode'] = 'cors'



            data = {
                'type': 'register',
                'email': email,
                'password': password,
                'blogname': username,
                'gender': 'M',
                'birthday_day': '01',
                'birthday_month': '01',
                'birthday_year': '2005',
                'recaptcha': recaptcha_token,
                'is_electron': 'false',
                'checkForm': api_token,
                'EXPLICIT_ALLOW_TRANSFER_DATA_TO_FRANCE': 'true'
            }



            response = session.post('https://www.deezer.com/ajax/action.php', data=data)
            self.notify(severity="information",message=f"{response.text} account created {email}")
            open("accounts.txt","a").write(f"{email}:{password}\n")
        except Exception as E:
            self.notify(severity="error",message=f"{E}")


    def compose(self) -> ComposeResult:
        pixels = Pixels.from_image_path("deezer.png", (60,23))
        yield Label(pixels)


        yield Label("How many account you want to open?")
        self.how_many_acc = Input(
            placeholder="Enter a number...",


        )
        yield self.how_many_acc

        yield Label("how many new threads per every second?")
        self.thread_time = Input(
            placeholder="0.3",
            validate_on=["submitted"]

        )
        yield self.thread_time


        yield Label("Domain of accounts?")
        self.domain = Input(
            placeholder="emrovsky.software",


        )
        yield self.domain

        yield Label("Capsolver api key?")
        self.capsolver_key = Input(
            placeholder="CAP-XXXXXXXXXXXX",


        )
        yield self.capsolver_key



        self.genbutton =  Button.success("generate!")
        yield self.genbutton


    def on_button_pressed(self) -> None:
        self.notify(severity="information",message="account creation process started!")
        time.sleep(1)
        self.genbutton.disabled = True

        for _ in range(int(self.how_many_acc.value)):
            t = threading.Thread(target=self.generate,args=[self.capsolver_key.value,self.domain.value]).start()
            time.sleep(float(self.thread_time.value))















if __name__ == "__main__":
    app = DeezerUi()
    app.run()

