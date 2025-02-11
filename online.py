from game import Game
                  
game = Game()

while game.engine.running:
    
    game.get_ui()
    game.engine.update()