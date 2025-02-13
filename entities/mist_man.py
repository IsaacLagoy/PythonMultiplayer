import glm
import random


HEAD_RADIUS = 0.2
FOOT_RADIUS = 0.4

TORSO_LENGTH = 1
LEG_LENGTH = 1
NECK_LENGTH = 0.5
ARM_LENGTH = 0.5
SHOULDER_WIDTH = 0.5

FORWARD_OFFSET = 0.1
DIFFUSE_STRENGTH = 0.2

class MistMan():
    
    def __init__(self, position: glm.vec3, cooldown: float=0.001) -> None:
        
        self.right_foot = glm.vec3(1e5)
        self.left_foot = glm.vec3(1e5)
        
        self.forward  = glm.vec3(0, 0, -1)
        self.position = position

        self.right_hand = self.chest
        self.left_hand = self.chest
        
        self.cooldown = cooldown
        self.time = 0
        
    def update(self, dt: float) -> None:
        """
        Updates particle timer
        """
        self.time += dt
        
    def get_particle_position(self) -> glm.vec3|None:
        """
        Creates particles on the mist figure
        """
        if self.time < self.cooldown: return None
        self.time = 0
        
        diffuse = DIFFUSE_STRENGTH * glm.normalize([random.uniform(-1, 1) for _ in range(3)])
        choice = random.randint(0, 7)
        if not choice: # spawn on head
            offset = glm.normalize([random.uniform(-1, 1) for _ in range(3)])
            offset *= HEAD_RADIUS
            return self.head + offset + diffuse

        # if the particle spawns on the body
        percent = random.uniform(0, 1)
        match choice:
            case 1: return self.hip + (self.chest      - self.hip) * percent + diffuse # chest
            case 2: return self.hip + (self.right_foot - self.hip) * percent + diffuse # r leg
            case 3: return self.hip + (self.left_foot  - self.hip) * percent + diffuse # l leg
            case 4: return self.chest + (self.right_shoulder - self.chest) * percent + diffuse # r shoulder
            case 5: return self.chest + (self.left_shoulder  - self.chest) * percent + diffuse # l shoulder
            case 6: return self.right_shoulder + (self.right_hand - self.right_shoulder) * percent + diffuse # r arm
            case 7: return self.left_shoulder + (self.left_hand   - self.left_shoulder) * percent + diffuse # l arm
    
    @property
    def position(self): return self._position
    @property
    def hip(self): return self.position + (0, LEG_LENGTH, 0)
    @property
    def chest(self): return self.hip + (0, TORSO_LENGTH, 0)
    @property
    def head(self): return self.chest + (0, NECK_LENGTH, 0)
    @property
    def right_shoulder(self): return self.chest + self.right * SHOULDER_WIDTH
    @property
    def left_shoulder(self): return self.chest - self.right * SHOULDER_WIDTH
    @property
    def forward(self): return self._forward
    @property
    def right(self): return glm.normalize(glm.cross(self.forward, (0, 1, 0)))
    
    
    @position.setter
    def position(self, value): 
        self._position = value
        
        # compute the positions of the feet
        center = self._position
        
        if (center.x - self.right_foot.x) ** 2 + (center.z - self.right_foot.z) ** 2 > FOOT_RADIUS ** 2:
            self.right_foot = self.position + self.right * FOOT_RADIUS
            
        if (center.x - self.left_foot.x) ** 2 + (center.z - self.left_foot.z) ** 2 > FOOT_RADIUS ** 2:
            self.left_foot = self.position - self.right * FOOT_RADIUS
            
        self.right_hand = self.left_hand = self.chest + self.forward * ARM_LENGTH

            
    @forward.setter
    def forward(self, value):
        self._forward = glm.normalize(value)