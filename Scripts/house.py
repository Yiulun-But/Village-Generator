from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
import random

class House:
    def __init__(self, pos: Vec3, mc: Minecraft):
        self.pos = pos
        self.mc = mc
        self.scale = self.determine_size()
        self.materials = {'wall': 5, 'corner': 17}
        self.door_front = self.make_house_front()
    
    def determine_size(self):
        # Note that width refers to x_axis and length refers to z_axis
        width = random.randint(11, 16)
        length = random.randint(16, 21)
        height = 6
        self.w = width
        self.l = length
        self.h = height
        if width % 2 == 1:
            x_lower = self.pos.x - (width // 2)
            x_upper = self.pos.x + (width // 2)
        else:
            x_lower = self.pos.x - (width // 2) + 1
            x_upper = self.pos.x + (width // 2)
            
        if length % 2 == 1:
            z_lower = self.pos.z - (length // 2)
            z_upper = self.pos.z + (length // 2)
        else:
            z_lower = self.pos.z - (length // 2) + 1
            z_upper = self.pos.z + (length // 2)
        y_lower = self.pos.y
        y_upper = self.pos.y + height
        corner1 = Vec3(x_lower, y_lower, z_lower)
        corner2 = Vec3(x_upper, y_upper, z_upper)
        return corner1, corner2
    
    def make_house_front(self):
        house_front = None
        x_lower, y_lower, z_lower = self.scale[0].x, self.scale[0].y, self.scale[0].z
        x_upper, y_upper, z_upper = self.scale[1].x, self.scale[1].y, self.scale[1].z
        direction = random.sample([x_lower, x_upper, z_lower, z_upper], 1)[0]
        
        if direction == x_lower:
            house_front = Vec3(x_lower - 4, self.pos.y, self.pos.z)
        elif direction == x_upper:
            house_front = Vec3(x_upper + 4, self.pos.y, self.pos.z)
        elif direction == z_lower:
            house_front = Vec3(self.pos.x, self.pos.y, z_lower - 4)
        elif direction == z_upper:
            house_front = Vec3(self.pos.x, self.pos.y, z_upper + 4)
        return house_front
    
    def create_rooms(self, w, l, h, starting_pos):
        for i in range(w):
            for j in range(h):
                for k in range(l):
                    if (i == 0 and k == 0) or (i == w-1 and k == 0) or (i == 0 and k == l-1) or (i == w-1 and k == l-1):  # Check if the current block is a corner
                        self.mc.setBlock(starting_pos.x+i, starting_pos.y+j, starting_pos.z+k, self.materials['corner'])  # Set the material to corner_material
                    elif i == 0 or i == w-1 or j == 0 or j == h-1 or k == 0 or k == l-1:
                        self.mc.setBlock(starting_pos.x+i, starting_pos.y+j, starting_pos.z+k, self.materials['wall'])

    def _test_create_room(self):
        self.create_rooms(self.w, self.l, self.h, self.scale[0])
        # print(self.w, self.l, self.h)