import basilisk as bsk
import glm
from entities.player import Player, get_player_node
from entities.enemy_handler import EnemyHandler
from weapons.bullet_handler import BulletHandler
from weapons.gun import Gun
from weapons.bullet import Bullet
from scenes.game_scene import GameScene, get_plain_nodes
from scenes.levels import *
from render.render_handler import RenderHandler
from ui.ui import UI
# import cudart


class Game():  
    
    def __init__(self) -> None:
        self.engine = bsk.Engine(win_size=(1000, 700),  max_fps=60, title="Emulsion")

        self.default_scene = bsk.Scene()
        self.plain_scene = bsk.Scene()
        self.sight_scene = bsk.Scene()
        self.dimension_scene = bsk.Scene()

        self.engine.scene = self.plain_scene
        self.engine.scene = self.sight_scene
        self.engine.scene = self.dimension_scene 
        self.engine.scene = self.default_scene
        
        self.sight_scene.physics_engine.accelerations = [glm.vec3(0, -25, 0)]
        
        self.default_shader = self.engine.shader
        self.particle_shader = bsk.Shader(self.engine, 'shaders/particle_sight.vert', 'shaders/particle_sight.frag')
        self.invisible_shader = bsk.Shader(self.engine, 'shaders/invisible.vert', 'shaders/invisible.frag')
        self.sight_scene.particle = bsk.ParticleHandler(self.sight_scene, self.particle_shader)
        
        self.load_meshes()
        self.load_materials()
        self.load_sounds()
        
        self.levels = [level1, level2, level3, level4, level5, level6, level7]

        self.pistol = Gun(
            game = self,
            count = 1,
            capacity = 7,
            cooldown = 0.2,
            spread = 0.02,
            ricochets = 2,
            damage = 1,
            radius = 0.2,
            color  = 'black',
            owner  = 'player'
        )
        
        self.shotgun = Gun(
            game = self,
            count = 7,
            capacity = 3,
            cooldown = 0.6,
            spread = 0.1,
            ricochets = 1,
            damage = 1,
            radius = 0.125,
            color = 'black',
            owner = 'player'
        )
        
        self.smg = Gun(
            game = self,
            count = 1,
            capacity = 3,
            cooldown = 0.1,
            spread = 0.1,
            ricochets = 0,
            damage = 1,
            radius = 0.03,
            color = 'black',
            owner = 'player'
        )

        # add player to scene
        player_node = get_player_node()
        
        self.player_gun = bsk.Node(
            scale = (0.1, 0.1, 0.1),
            mesh = self.pistol_mesh,
            material = self.blue
        )
        self.default_scene.add(self.player_gun)
        
        self.player = Player(
            position = glm.vec3(0, 0, 0), 
            health = 3,
            speed = 10,
            gun = self.pistol,
            node = player_node,
            game = self
        )
        
        self.sight_scene.add(player_node)
        self.sight_scene.camera = bsk.FollowCamera(player_node, offset=(0, 1, 0))
        self.plain_scene.camera = self.sight_scene.camera
        self.dimension_scene.camera = self.sight_scene.camera
        self.default_scene.camera = self.sight_scene.camera
        self.sky = self.sight_scene.sky
        
        # add handlers
        self.enemy_handler = EnemyHandler(self)
        self.bullet_handler = BulletHandler(self)
        self.gun_nodes = []

        #UI
        self.ui = UI(self)
        
    def load_sounds(self):
        self.pin1 = bsk.Sound('sounds/pin1.wav')
        self.pin2 = bsk.Sound('sounds/pin2.wav')
        self.kill = bsk.Sound('sounds/kill.wav')
        self.shot = bsk.Sound('sounds/shot.wav')
        
    def spawn_gun(self, type: str, position: glm.vec3):
        
        mesh = None
        match type:
            case 'pistol': mesh = self.pistol_mesh
            case 'shotgun': mesh = self.shotgun_mesh
            case 'smg': mesh = self.smg_mesh
            
        hitbox = bsk.Node(
            scale=(0.5, 0.5, 0.5),
            position=glm.vec3(position),
            collision=True,
            # physics=True,
            shader=game.invisible_shader,
            tags=[type]
        )
        
        gun = bsk.Node(
            position=position + (0.2, 0, 0),
            scale=(0.1, 0.1, 0.1),
            material=game.blue,
            mesh=mesh,
            tags=[type],
        )
        
        self.gun_nodes.append(gun)
        self.gun_nodes.append(hitbox)
        
        self.default_scene.add(gun)
        self.sight_scene.add(hitbox)

    def load_meshes(self):
        self.pistol_mesh = bsk.Mesh('meshes/pistol.obj')
        self.shotgun_mesh = bsk.Mesh('meshes/shotgun.obj')
        self.smg_mesh = bsk.Mesh('meshes/smg.obj')
        self.wedge_mesh = bsk.Mesh('meshes/wedge.obj')
        self.health_cube_mesh = bsk.Mesh('meshes/health_cube.obj')
        self.cylinder_mesh = bsk.Mesh('meshes/cylinder.obj')

    def load_level(self, game_scene: GameScene) -> None:
        """
        Add all nodes to the scene
        """ 
        # plain scene
        self.plain_scene.remove(*self.plain_scene.nodes)
        self.plain_scene.add(*get_plain_nodes(game_scene))
        #UI
        self.ui = UI(self)

    def load_level(self, game_scene: GameScene) -> None:
        """
        Add all nodes to the scene
        """ 
        self.level_complete = False
        
        for i in range(0, len(self.gun_nodes), 2): self.default_scene.remove(self.gun_nodes[i])
        self.gun_nodes = []
        
        # plain scene
        self.plain_scene.remove(*self.plain_scene.nodes)
        self.plain_scene.add(*get_plain_nodes(game_scene))
        
        # sight scene
        self.sight_scene.remove(*self.sight_scene.node_handler.nodes)
        self.sight_scene.add(*game_scene.nodes, self.player.node)
        for enemy in game_scene.enemies: self.sight_scene.add(enemy.node)
        
        self.bullet_handler.bullets = []
        self.enemy_handler.enemies = []
        self.enemy_handler.enemies = game_scene.enemies[:]
        
        # dimensions scene
        self.dimension_scene.remove(*self.dimension_scene.nodes)
        for gun in game_scene.guns:
            self.spawn_gun(*gun)
            
        
        
        self.player.position = glm.vec3(0, 1, 0)
        self.player.health = self.player.max_health
        # self.sight_scene.camera.yaw = 0.1
        self.sight_scene.camera.pitch = 0

    def load_materials(self):

        self.e_key = bsk.Image('images/e_key.png')

        saturation = 80
        self.red = bsk.Material(color=(255, saturation - 50, saturation - 50), roughness=.8, metallicness=0.0, specular=0.25)
        self.green = bsk.Material(color=(saturation, 255, saturation), roughness=.8, metallicness=0.0, specular=0.25)
        self.blue = bsk.Material(color=(saturation, saturation, 255), roughness=.8, metallicness=0.0, specular=0.25)
        self.yellow = bsk.Material(color=(255, 255, saturation - 50), roughness=.8, metallicness=0.0, specular=0.25)
        self.cyan = bsk.Material(color=(saturation, 255, 255), roughness=.8, metallicness=0.0, specular=0.25)
        self.white = bsk.Material(color=(255, 255, 255))
        self.black = bsk.Material(color=(30, 30, 30))
        self.purple = bsk.Material(color=(255, saturation, 255), roughness=.8, metallicness=0.0, specular=0.25)

        for scene in [self.default_scene, self.plain_scene, self.dimension_scene, self.sight_scene]:
            self.engine.scene = scene
            scene.material_handler.add(self.red)
            scene.material_handler.add(self.green)
            scene.material_handler.add(self.blue)
            scene.material_handler.add(self.yellow)
            scene.material_handler.add(self.cyan)
            scene.material_handler.add(self.white)
            scene.material_handler.add(self.black)
            scene.material_handler.add(self.purple)

        self.materials = [self.green, self.purple, self.cyan, self.yellow]

    def start(self) -> None:
        """
        Starts the engine and the game
        """
        
        self.render_handler = RenderHandler(self)
        self.level_complete = False
        self.load_level(self.levels[0](self))

        while self.engine.running:
            
            for i in range(0, len(self.gun_nodes), 2):
                self.gun_nodes[i].position.data = self.gun_nodes[i + 1].position.data + (0.2, 0, 0)
                
            is_looking_at_gun = False
            if len(self.gun_nodes) > 0:
                cast = self.sight_scene.raycast(self.sight_scene.camera.position + self.sight_scene.camera.forward * 2, self.sight_scene.camera.forward)
                if cast.node and any([tag in cast.node.tags for tag in ('pistol', 'smg', 'shotgun')]) and glm.length(cast.position - self.player.camera.position) < 5: is_looking_at_gun = True
            
            if is_looking_at_gun:
                box_w, box_h = 80, 80
                outline_w, outline_h = 84, 84
                win_w, win_h = self.engine.win_size
                rect = (win_w // 2 - box_w // 2, win_h - box_h - 10, box_w, box_h)
                rect_outline = (win_w // 2 - outline_w // 2, win_h - outline_h - 8, outline_w, outline_h)
                bsk.draw.blit(self.engine, self.e_key, rect)
                bsk.draw.rect(self.engine, 0, rect_outline)

            if self.engine.event_resize: self.render_handler.resize()

            bsk.pg.display.flip()

            if len(self.enemy_handler.enemies) < 1 and not self.level_complete:
                self.levels.pop(0)
                if not len(self.levels):
                    print('you win')
                    break
                
                self.ui.add_transition()
                self.ui.add_transition(duration=1.5, callback= lambda: self.load_level(self.levels[0](self)))
                self.level_complete = True
                
            if self.player.health < 1: self.load_level(self.levels[0](self))

            if self.engine.keys[bsk.pg.K_2] and not self.engine.previous_keys[bsk.pg.K_2]:
                self.player.health -= 1

            self.bullet_handler.update(self.engine.delta_time)
            self.enemy_handler.update(self.engine.delta_time)
            self.player.update(self.engine.delta_time)

            self.render_handler.render()

            self.engine.update(render=False)

game = Game()
game.start()