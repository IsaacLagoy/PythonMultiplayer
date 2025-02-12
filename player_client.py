

class PlayerClient():
    
    def __init__(self, socket) -> None:
        self.socket = socket
        self.name = ''
        
    def __repr__(self) -> str:
        return f'Player Client: {self.name}'