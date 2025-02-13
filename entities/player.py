import glm
from basilisk import Node, Engine, pg, FollowCamera
from entities.entity import Entity
from weapons.gun import Gun
import basilisk as bsk
import random


class Player(Entity):
    
    def __init__(self, position: glm.vec3, health: int, speed: float, gun: Gun, node: Node, game) -> None:
        self.node = node
        super().__init__(position, health, speed)
        
        self.game = game
        self.gun = gun
        self.jumping = False
        self.max_health = self.health
        
        self.fov = 70
        self.target_fov = 80
        self.fov_time = 0

        self.health_cube = bsk.Node(mesh=game.health_cube_mesh, scale=.15)
        self.health_level = bsk.Node(scale=.1, material=game.red)
        self.game.default_scene.add(self.health_level, self.health_cube)
        
        self.shake_time = 0
        self.shake_intensity = 0
        
    def update(self, dt: float) -> None:
        """
        
        """
        self.node.rotation = glm.conjugate(glm.quatLookAt(glm.vec3(self.camera.forward.x, 0, self.camera.forward.z), self.camera.UP))
        self.game.player_gun.rotation = glm.normalize(glm.conjugate(glm.angleAxis(glm.pi() / 2, (0, 1, 0))) * self.game.sight_scene.camera.rotation)
        self.game.player_gun.position = self.node.position.data + glm.vec3(0, 0.35, 0) + self.camera.right * 0.75 + self.camera.forward * 1.5

        self.health_cube.rotation = glm.normalize(glm.conjugate(glm.angleAxis(glm.pi() / 2, (0, 1, 0))) * self.game.sight_scene.camera.rotation)
        self.health_cube.position = self.node.position.data + glm.vec3(0, 0.5, 0) - self.camera.right * 0.4 + self.camera.forward * 0.75
        
        self.health_level.scale.y = (self.health / self.max_health + .5) * .1
        self.health_level.rotation = glm.normalize(glm.conjugate(glm.angleAxis(glm.pi() / 2, (0, 1, 0))) * self.game.sight_scene.camera.rotation)
        self.health_level.position = self.node.position.data + glm.vec3(0, 0.5, 0) - self.camera.right * 0.4 + self.camera.forward * 0.75


        if self.position.y < 1.1: 
            self.position.y = 1.1
            if not self.jumping: self.node.velocity.y = 0
            elif self.node.velocity.y < 0: self.jumping = False
            
        self.move(dt)
        self.shoot(dt)
        self.pick()
        
        # controls fov
        self.fov_time += dt
        if self.fov_time > 0.01 and self.fov != self.target_fov:
            self.fov_time = 0
            self.fov += 1 if self.fov < self.target_fov else -1
            
        # controls camera shake
        if self.shake_time > 0: 
            self.game.sight_scene.camera.offest = glm.vec3(0, 1, 0) + self.shake_intensity * glm.normalize([random.uniform(-1, 1) for _ in range(3)])
            self.shake_time -= dt
        else: self.game.sight_scene.camera.offest = glm.vec3(0, 1, 0)
        
    def pick(self) -> None:
        if not (self.game.engine.keys[pg.K_e] and not self.game.engine.previous_keys[pg.K_e]): return
        cast = self.game.sight_scene.raycast(self.camera.position + self.camera.forward * 2, self.camera.forward)
        if not cast.node or not any([tag in cast.node.tags for tag in ('pistol', 'smg', 'shotgun')]): return
        if glm.length(self.camera.position - cast.position) > 5: return
        
        tag = ''
        match self.game.player_gun.mesh:
            case self.game.pistol_mesh: tag = 'pistol'
            case self.game.shotgun_mesh: tag = 'shotgun'
            case self.game.smg_mesh: tag = 'smg'
        
        for i in range(0, len(self.game.gun_nodes), 2):
            if not (cast.node == self.game.gun_nodes[i] or cast.node == self.game.gun_nodes[i + 1]): continue
            self.game.gun_nodes[i].mesh = self.game.player_gun.mesh
        
        match cast.node.tags[0]:
            case 'pistol':
                self.gun = self.game.pistol
                self.game.player_gun.mesh = self.game.pistol_mesh
            case 'shotgun':
                self.gun = self.game.shotgun
                self.game.player_gun.mesh = self.game.shotgun_mesh
            case 'smg':
                self.gun = self.game.smg
                self.game.player_gun.mesh = self.game.smg_mesh
                
        cast.node.tags = [tag]
        
    def camera_shake(self, time: float, intensity: float) -> None:
        self.shake_time = time
        self.shake_intensity = intensity
        
    def move(self, dt) -> None:
        """
        Sets the player's node's velocity to the input keys (wasd)
        """
        self._position = self.node.position.data - glm.vec3(0, 1, 0)
        
        # contraol the player's position by adding velocity to the node
        keys = self.engine.keys
        x, z = self.camera.forward.x, self.camera.forward.z
        movement = self.camera.right * (keys[pg.K_d] - keys[pg.K_a]) # should change fov when sprinting
        if x != 0 or z != 0: movement += glm.vec3(x, 0, z) * (keys[pg.K_w] - keys[pg.K_s])
        if glm.length2(movement) > 0: movement = self.speed * glm.normalize(movement)
        if keys[pg.K_LSHIFT] and not keys[pg.K_s] and (keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_d]): 
            movement *= 1.5
            self.target_fov = 80
        else:
            self.target_fov = 70
        if keys[pg.K_SPACE] and (not self.jumping or any(glm.dot(collision.normal, (0, 1, 0)) > 0.2 for collision in self.node.collisions)):
            self.node.velocity.y = 15
            self.jumping = True
            
        if glm.length2(movement) == 0 and glm.length2((self.node.velocity.x, 0, self.node.velocity.z)) > 1: 
            movement = glm.vec3(self.node.velocity.x, 0, self.node.velocity.z) * (1 - dt * 10)
        
        self.node.velocity.x = movement.x
        self.node.velocity.z = movement.z
        
    def shoot(self, dt: float) -> None:
        """
        Attemps to fire the player gun if the player is left clicking
        """
        self.gun.update(dt)
        if not self.engine.mouse.left_click and not (self.gun == self.game.smg and self.engine.mouse.left_down): return
        
        fire_position = self.game.player_gun.position.data + self.camera.forward * 1.25
        cast = self.game.sight_scene.raycast(self.camera.position + self.camera.forward * 2, self.camera.forward)
        target = cast.position if cast.node else self.camera.forward * 1e3
        
        bullets = self.gun.shoot(fire_position, glm.normalize(target - fire_position))
        if not bullets: return
        
        self.game.bullet_handler.bullets += bullets
        self.camera_shake(self.gun.cooldown / 10, self.gun.cooldown / 10)
        
    @property
    def position(self): return self._position
    @property
    def camera(self) -> FollowCamera: return self.game.sight_scene.camera
    @property
    def engine(self) -> Engine: return self.game.engine
    @property
    def fov(self): return self.camera.fov
    
    @position.setter
    def position(self, value):
        self._position = value
        self.node.position.data = self._position + glm.vec3(0, 1, 0)
        
    @fov.setter
    def fov(self, value):
        self.camera.fov = value
        
        
def get_player_node() -> Node:
    player_node = Node(
        physics = True,
        collision = True,
        scale = (0.5, 2, 0.5),
        tags = ['player'],
        collision_group = 'entity'
    )
    
    return player_node