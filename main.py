from os        import system, path, name
from core      import Log, Run
from time      import sleep

import   tls_client.response
import   concurrent.futures
import   tls_client
import   websocket
import   keyboard
import   random
import   string
import   json


system('cls' if name == 'nt' else 'clear')

def between(text: str, a: str, b: str, i: int = 1) -> str:
    """Extract a substring between two strings."""
    return text.split(a)[i].split(b)[0]

class Main:
    
    
    def __init__(self) -> None:
        
        self.session: tls_client.sessions.Session = tls_client.Session(client_identifier="chrome_120")
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://skribbl.io',
            'Pragma': 'no-cache',
            'Prefer': 'safe',
            'Referer': 'https://skribbl.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        with open("core/config.json", "r") as f:
            settings_json = f.read()
            settings: dict = json.loads(settings_json)
            
            proxy: str = settings["proxy"]
            self.debug: bool = settings["debug"]
            
        if proxy != None:
            self.proxy_host: str = proxy.split("@")[1].split(":")[0]
            self.proxy_port: int = int(proxy.split("@")[1].split(":")[1])
            self.proxy_auth: tuple = tuple(proxy.split("@")[0].split("://")[1].split(":"))
        else:
            self.proxy_host = None
            self.proxy_port = None
            self.proxy_auth = None

    @Run.Error
    def join(self, code: str, choice: str) -> websocket._core.WebSocket:
        
        if choice == "1":
            data: dict = {
                'id': code,
            }
            
            play_request: tls_client.response.Response = self.session.post('https://skribbl.io/api/play', data=data)
            wss_url: str = f"wss:{play_request.text.split(":")[1]}/{play_request.text.split(":")[2]}/?EIO=4&transport=websocket"
            
            if self.debug:
                Log.Success(f"Got WSS url: {wss_url}")
            
            headers: dict = {
                'accept-encoding': 'gzip, deflate, br, zstd',
                'Origin': 'https://skribbl.io',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            }
                
            ws: websocket._core.WebSocket = websocket.create_connection(
                wss_url,
                header=[
                    f"{key}: {value}" for key, value in headers.items()
                    ],
                http_proxy_host=self.proxy_host,
                http_proxy_port=self.proxy_port,
                http_proxy_auth=self.proxy_auth
            )
            
            if self.debug:
                Log.Success("Connected to WSS")
            
            chunk1: str = str(ws.recv())
            sid1: str = between(chunk1, '"sid":"', '"')
            
            if self.debug:
                Log.Success(f"Got SID: {sid1}")
            
            ws.send("40")
            
            chunk2: str = str(ws.recv())
            sid2: str = between(chunk2, '"sid":"', '"')
            
            if self.debug:
                Log.Success(f"Got SID2: {sid2}")
            
            name: str = "".join(random.choices(string.ascii_letters, k=10))
            ws.send('42["login",{"join":"' + code + '","create":0,"name":"' + name + '","lang":"0","avatar":[' + str(random.randint(0, 40)) + ',' + str(random.randint(0, 40)) + ',' + str(random.randint(0, 40)) + ',-1]}]')
            
            chunk3: str = str(ws.recv())
            
            if self.debug:
                Log.Success(f"Joined room")
            
            return ws
        else:   
            headers: dict = {
                'accept-encoding': 'gzip, deflate, br, zstd',
                'Origin': 'https://skribbl.io',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            }
                
            ws: websocket._core.WebSocket = websocket.create_connection(
                code,
                header=[
                    f"{key}: {value}" for key, value in headers.items()
                    ],
                http_proxy_host=self.proxy_host,
                http_proxy_port=self.proxy_port,
                http_proxy_auth=self.proxy_auth
                )
            
            if self.debug:
                Log.Success("Connected to WSS")
            
            chunk1: str = str(ws.recv())
            sid1: str = between(chunk1, '"sid":"', '"')
            
            if self.debug:
                Log.Success(f"Got SID: {sid1}")
            
            ws.send("40")
            
            chunk2: str = str(ws.recv())
            sid2: str = between(chunk2, '"sid":"', '"')
            
            if self.debug:
                Log.Success(f"Got SID2: {sid2}")
            
            name: str = "".join(random.choices(string.ascii_letters, k=10))
            ws.send('42["login",{"join":"' + code + '","create":0,"name":"' + name + '","lang":"0","avatar":[' + str(random.randint(0, 40)) + ',' + str(random.randint(0, 40)) + ',' + str(random.randint(0, 40)) + ',-1]}]')
            
            chunk3: str = str(ws.recv())
            
            if self.debug:
                Log.Success(f"Joined room")
            
            return ws

    @Run.Error
    def spam(self, ws: websocket._core.WebSocket, message: str) -> None:
        while True:
            if keyboard.is_pressed('x'):
                exit()
            
            ws.send('42["data",{"id":30,"data":"' + message + '"}]')
            Log.Success("Sent Message")
            sleep(1)

@Run.Error
def config() -> bool:
        
    system("pip install -r requirements.txt")
        
    config: dict = {}
    proxyusage: str = input("Do you want to use Proxies? y/n (you can change that later in config.json): ")
        
    if proxyusage == "y":
        proxy: str = input("Input Proxy (http://user:pass@domain:port format): ")
        config["proxy"] = proxy
    else:
        config["proxy"] = None
        
    debug: str = input("Activate Debug mode? (y/n): ")
        
    if debug == "y":
        config["debug"] = True
    else:
        config["debug"] = False
        
    with open("core/config.json", "a") as file:
        file.write(json.dumps(config, indent=4))
    
    return True
             
        
if __name__ == "__main__":
    
    if not path.exists("core/config.json"):
        print("Setting up config...")
        if config():
            print("Setup completed, continueing...")
            sleep(2)
            system('cls' if name == 'nt' else 'clear')
            
    print("""
    [1] Spam chat (Private Lobby)
    [2] Spam chat (Public Lobby, check if Lobby is full)
          """)
    
    choice: str = input("Choice: ")
    
    if choice == "1":
        code: str = input("Code: ")
        
    elif choice == "2":
        code: str = input("Enter WSS url: ")
        
    bots: int = int(input("How many Bots: "))
    connections: list = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as thread:
        for i in range(bots):
            thr = thread.submit(Main().join, code, choice)
            ws = thr.result()
            connections.append(ws)
            sleep(2)

    if choice == "1" or choice == "2":
        message: str = input("Message to spam: ")
    
    Log.Info("Press x to cancel spamming")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as thread:
        for i in range(len(connections)):
            thr = thread.submit(Main().spam, connections[i], message)
    
