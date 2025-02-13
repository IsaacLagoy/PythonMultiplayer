import glm
import random
from entities.enemy import Enemy
from basilisk import Scene, pg
from weapons.gun import Gun


class EnemyHandler():
    
    def __init__(self, game) -> None:
        self.game = game
        self.enemies: list[Enemy] = []
        
    def update(self, dt: float) -> None:
        """
        Updates all nodes and checks for death
        """
        to_remove = []
        
        for enemy in self.enemies:
            
            # run code if enemy has been killed
            if enemy.is_dead:
                enemy.on_death()
                to_remove.append(enemy)
                continue
            
            # enemy update and particles
            enemy.update(dt)
            
            particle_position = enemy.mist.get_particle_position()
            if not particle_position: continue
            self.sight_scene.particle.add(
                position = particle_position,
                material = self.game.red,
                scale = random.uniform(.8, 1.2),
                life = 0.2,
            )
            
        for enemy in to_remove:
            self.enemies.remove(enemy)
            self.game.sight_scene.remove(enemy.node, enemy.gun_node)
            self.game.kill.play()
            
    def get_enemy_by_node(self, node) -> Enemy:
        for enemy in self.enemies:
            if enemy.node == node: return enemy
        return None
        
    @property
    def sight_scene(self) -> Scene: return self.game.sight_scene