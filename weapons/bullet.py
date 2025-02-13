import glm
from basilisk import Node


COOLDOWN = 0.01
BULLET_SPEED = 50

class Bullet():
    
    def __init__(self, ricochet_remaining: int, damage: int, radius: float, color: str, node: Node=None, path: glm.vec3=None, position: glm.vec3=None, owner: str='enemy') -> None:
        self.ricochet_remaining = ricochet_remaining
        self.damage = damage
        self.radius = radius
        self.color  = color
        
        self.position = position
        self.last_hit = glm.vec3(position) if position else glm.vec3(0, 0, 0)
        self.path = path
        self.node = node
        self.owner = owner
        
        self.time = 0
        self.life_time = 0
        
    def update(self, dt: float) -> None:
        """
        Moves the bullet by the descrete time step
        """
        self.position += dt * self.path * BULLET_SPEED
        self.time += dt
        self.life_time += dt
        
        if self.node:
            self.node.position = self.midpoint
            self.node.scale.y = glm.length(self.position - self.last_hit) / 2
        
    def get_particle_position(self) -> glm.vec3|None:
        """
        Gets the next particle position of the bullet
        """
        if self.time < COOLDOWN: return None
        self.time = 0
        
        return self.position
        
    def ricochet(self, normal: glm.vec3) -> None:
        """
        Checks to see if the bullet is still alive after collision, updates moving vector if so
        """
        # if glm.dot(self.path, normal) > 0: 
        #     self.ricochet_remaining = -1
        #     return
        self.path = glm.reflect(self.path, normal)
        self.ricochet_remaining -= 1
        
    def __repr__(self) -> str:
        return f'Bullet - ricochet: {self.ricochet_remaining}, damage: {self.damage}, radius: {self.radius}'
    
    @property
    def is_dead(self): return self.ricochet_remaining < 0 or self.life_time > 10
    @property
    def midpoint(self): return (self.position + self.last_hit) / 2
    @property
    def node(self): return self._node
    @property
    def path(self): return self._path
    
    @path.setter
    def path(self, value):
        self._path = glm.normalize(value)
    
    @node.setter
    def node(self, value):
        self._node = value
        if self.node: self.node.rotation = glm.normalize(glm.angleAxis(glm.pi() / 2, (1, 0, 0)) * glm.conjugate(glm.quatLookAt(self.path, (0, 1, 0))))