import glm
import random
from entities.entity import Entity
from entities.player import Player
from entities.mist_man import MistMan
from weapons.gun import Gun
from basilisk import Node


class Enemy(Entity):
    
    def __init__(self, game, position: glm.vec3, health: int=1, speed: float=5, spread: float=0.05, gun: Gun=None, ai: str='smart') -> None:
        self.health = health
        self.speed = speed
        self.spread = spread
        
        self.gun = gun if gun else Gun(
            game = game,
            count = 1,
            capacity = 3,
            spread = 0.05,
            cooldown = 3,
            ricochets = 1,
            damage = 1,
            radius = 0,
            color  = 'red',
        )
        
        self.gun.time = -1
        
        self.game = game
        self.player: Player = game.player
        self.mist = MistMan(position)
        self.ai = ai
        
        self.node = Node(
            position + (0, 1, 0),
            scale = (0.5, 1.8, 0.5),
            collision = True,
            physics = True,
            tags = ['enemy'],
            collision_group = 'entity',
            shader=game.invisible_shader
        )
        
        self.gun_node = Node(
            scale = (0.1, 0.1, 0.1),
            mesh = self.game.pistol_mesh,
            material = self.game.red
        )
        
        self.game.sight_scene.add(self.gun_node)
        self.game.sight_scene.add(self.node)
        
        self.position = position # added after bc mistman is used in the position property
        self.y = self.position.y
        
    def update(self, dt: float) -> None:
        """
        Moves the enemt and controls shooting
        """
        self.move(dt)
        self.shoot(dt)
        
        # mist control
        self.mist.update(dt)
        
        direction = self.game.player.position - self.position
        if glm.length2(direction) < 1e-7: return
        direction = glm.normalize(direction)
        
        self.node.position.data.y = self.y + 1.85
        self.node.velocity.y = 0
        self.node.rotation.data = (1, 0, 0, 0)
        
        self.position = self.node.position.data - glm.vec3(0, 1, 0)
        
        # self.gun_node.position = self.mist.chest + direction * 2
        # self.gun_node.rotation = glm.conjugate(glm.angleAxis(glm.pi() / 2, (0, 1, 0))) * glm.conjugate(glm.quatLookAt(direction, (0, 1, 0)))
        
    def move(self, dt: float) -> None:
        """
        Main movement AI for enemies
        """
        if self.ai == 'direct':
            direction = self.player.position - self.position
            if glm.length2(direction) < 1e-7: return
            direction = glm.normalize(direction)
            self.mist.forward = direction
            
            self.node.velocity = self.speed * direction
            
        elif self.ai == 'smart':
            direction = self.player.position - self.position
            direction = glm.vec3(direction.x, 0, direction.y)
            distance = glm.length(direction)
            if distance < 1e-7: return
            direction = glm.normalize(direction)
            self.mist.forward = direction
            if distance < 15: direction *= -1
            self.node.velocity = self.speed * direction
        
    def shoot(self, dt: float) -> None:
        """
        Attempts to fire the gun
        """
        self.gun.update(dt)
        bullets = self.gun.shoot(self.mist.right_hand, self.player.position - (0, 0.5, 0) - self.position)
        if not bullets: return
        self.game.bullet_handler.bullets += bullets
        
    @property
    def position(self): return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
        self.mist.position = value
        # self.node.position.data = value + glm.vec3(0, 1, 0)