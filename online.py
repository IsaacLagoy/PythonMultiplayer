from game import Game

                  
game = Game()

while game.engine.running:
    
    game.broadcast_timer += game.engine.delta_time
    
    game.get_ui()
    game.engine.update()