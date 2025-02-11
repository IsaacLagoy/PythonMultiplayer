import basilisk as bsk
from host import Host
from client import Client

class Game():
    
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
        self.numbers = [bsk.pg.K_0, bsk.pg.K_1, bsk.pg.K_2, bsk.pg.K_3, bsk.pg.K_4, bsk.pg.K_5, bsk.pg.K_6, bsk.pg.K_7, bsk.pg.K_8, bsk.pg.K_9]
    
    def get_ui(self):
        match self.mode:
            case 'main menu':
                bsk.draw.text(self.engine, 'host', (200, 200), 1)
                bsk.draw.text(self.engine, 'join', (200, 400), 1)
                
                if self.engine.mouse.left_click and 100 < self.engine.mouse.x < 300:
                    if 150 < self.engine.mouse.y < 250: 
                        self.mode = 'host menu'
                        self.host_game()
                        
                    elif 350 < self.engine.mouse.y < 450: 
                        self.join_game()
                        self.mode = 'client menu'
                        self.text_input = '' # reset text input for erntering ip, this line is redundant
                        
            case 'host menu':
                bsk.draw.text(self.engine, self.host.host, (300, 200), 1)
                bsk.draw.text(self.engine, f'joined: {len(self.host.clients)}', (300, 400), 1)
            
            case 'client menu':
                bsk.draw.text(self.engine, 'enter host ip', (200, 200), 1)
                bsk.draw.text(self.engine, self.text_input, (200, 400), 1)
                for i, key in enumerate(self.numbers):
                    if self.key_down(key): self.text_input += str(i)
                if self.key_down(bsk.pg.K_DELETE) or self.key_down(bsk.pg.K_BACKSPACE): self.text_input = self.text_input[:-1]
                if self.key_down(bsk.pg.K_PERIOD): self.text_input += '.'
                if self.key_down(bsk.pg.K_RETURN): 
                    self.client.join(self.text_input)
                    self.mode = 'lobby'
                    
            case 'lobby':
                ...
            
    def host_game(self):
        self.host = Host(self.engine)
        
    def join_game(self):
        self.client = Client()
        
    def key_down(self, key):
        return self.engine.keys[key] and not self.engine.previous_keys[key]