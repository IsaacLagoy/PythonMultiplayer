import basilisk as bsk
from host import Host
from client import Client
from alphanumeric_storage import NUMBERS, CHARACTERS
import json

class Interface():
    
    def __init__(self):
        self.mode = 'main menu'
        self.host = None
        self.client = None
        
        # set up scene
        self.engine = bsk.Engine()
        scene = bsk.Scene()
        self.engine.scene = scene
        
        # user input
        self.text_input = ''
        self.name = ''
        self.broadcast_timer = 0
        self.broadcast_time = 1 / 30
    
    def get_ui(self):
        self.broadcast_timer += self.engine.delta_time
        
        match self.mode:
            case 'main menu':
                bsk.draw.text(self.engine, 'host', (200, 200), 1)
                bsk.draw.text(self.engine, 'join', (200, 400), 1)
                
                if self.engine.mouse.left_click and 100 < self.engine.mouse.x < 300:
                    if 150 < self.engine.mouse.y < 250: 
                        self.mode = 'host naming'
                        self.host_game()
                        
                    elif 350 < self.engine.mouse.y < 450: 
                        self.join_game()
                        self.mode = 'client menu'
                        self.text_input = '' # reset text input for erntering ip, this line is redundant
                        
            case 'host naming':
                bsk.draw.text(self.engine, 'enter name (lower and _)', (400, 200), 1)
                bsk.draw.text(self.engine, self.text_input, (200, 400), 1)
                for key, char in CHARACTERS.items():
                    if self.key_down(key): self.text_input += char
                if self.key_down(bsk.pg.K_DELETE) or self.key_down(bsk.pg.K_BACKSPACE): self.text_input = self.text_input[:-1]
                if self.key_down(bsk.pg.K_RETURN): 
                    self.name = self.text_input
                    self.text_input = ''
                    self.mode = 'host menu'
                        
            case 'host menu':
                bsk.draw.text(self.engine, self.host.host, (300, 200), 1)
                bsk.draw.text(self.engine, self.name, (300, 300), 1)
                for i, client in enumerate(self.host.clients.values()):
                    bsk.draw.text(self.engine, client.name, (300, 400 + 100 * i), 1)
                if len(self.host.clients):
                    bsk.draw.text(self.engine, 'start', (500, 200), 1)
                    if self.engine.mouse.left_click and 500 < self.engine.mouse.x < 600 and 200 < self.engine.mouse.y < 300:
                        # procedure to start the game
                        ... 
                
                if self.broadcast_timer > self.broadcast_time:
                    self.broadcast_timer = 0
                    self.host.broadcast(json.dumps({'players': [self.name] + [c.name for c in self.host.clients.values()]}))
            
            case 'client menu':
                bsk.draw.text(self.engine, 'enter host ip', (200, 200), 1)
                bsk.draw.text(self.engine, self.text_input, (200, 400), 1)
                for i, key in enumerate(NUMBERS):
                    if self.key_down(key): self.text_input += str(i)
                if self.key_down(bsk.pg.K_DELETE) or self.key_down(bsk.pg.K_BACKSPACE): self.text_input = self.text_input[:-1]
                if self.key_down(bsk.pg.K_PERIOD): self.text_input += '.'
                if self.key_down(bsk.pg.K_RETURN): 
                    self.client.join(self.text_input)
                    self.mode = 'client naming'
                    self.text_input = ''
                    
            case 'client naming':
                bsk.draw.text(self.engine, 'enter name (lower and _)', (400, 200), 1)
                bsk.draw.text(self.engine, self.text_input, (200, 400), 1)
                for key, char in CHARACTERS.items():
                    if self.key_down(key): self.text_input += char
                if self.key_down(bsk.pg.K_DELETE) or self.key_down(bsk.pg.K_BACKSPACE): self.text_input = self.text_input[:-1]
                if self.key_down(bsk.pg.K_RETURN): 
                    self.mode = 'lobby'
                    self.name = self.text_input
                    self.client.send_message(json.dumps({'name': self.text_input}))
                    self.text_input = ''
                    
            case 'lobby':
                if 'players' in self.client.data:
                    for i, name in enumerate(self.client.data['players']):
                        bsk.draw.text(self.engine, name, (300, 400 + 100 * i), 1)
                if self.broadcast_timer > self.broadcast_time:
                    self.broadcast_timer = 0
                    self.client.send_message(json.dumps({'name' : self.name}))
            
    def host_game(self):
        self.host = Host(self.engine)
        
    def join_game(self):
        self.client = Client()
        
    def key_down(self, key):
        return self.engine.keys[key] and not self.engine.previous_keys[key]