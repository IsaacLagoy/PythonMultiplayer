class PlayerClient():
    
    def __init__(self, address) -> None:
        self.address = address
        self.name = ''
        self.time_since_last_message = 0
        
    def __repr__(self) -> str:
        return f'Player Client: {self.name}'