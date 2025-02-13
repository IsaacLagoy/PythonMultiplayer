import glm


class Entity():
    
    def __init__(self, position: glm.vec3, health: int, speed: float) -> None:
        self.position = position
        self.health = health
        self.speed = speed

        
    def update(self, dt: float) -> None: ... # abstract function for children
    
    def on_death(self) -> None: ...
    
    @property
    def is_dead(self): return self.health <= 0