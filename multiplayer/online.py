from interface import Interface

                  
interface = Interface()

while interface.engine.running:
    
    interface.broadcast_timer += interface.engine.delta_time
    
    interface.get_ui()
    interface.engine.update()