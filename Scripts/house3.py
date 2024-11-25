from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
import random

class House:
    def __init__(self, pos: Vec3, mc: Minecraft):
        self.mc = mc
        self.materials = [block.COBBLESTONE, block.BRICK_BLOCK, block.WOOD_PLANKS]
        self.air = 0
        self.roof_material = block.WOOD_PLANKS
        self.window = 102
        self.stairs = block.STAIRS_WOOD
        self.stair = block.STAIRS_WOOD.withData(1)
        self.pos = pos
        self.scale = self.determine_size()
        self.door_front = self.deter_front()
        
    
    def deter_front(self):
        return Vec3(self.scale[0].x - 3, self.scale[0].y - 1, self.scale[0].z + 2)
    
    def construct(self):
        x, y, z = self.scale[0].x, self.scale[0].y + 1, self.scale[0].z
        self.generate_house(x, y, z, self.w, self.l, self.h)
        
    def determine_size(self):
        # Note that width refers to x_axis and length refers to z_axis
        width = random.randint(8, 10)
        length = random.randint(12, 15)
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

    def generate_house(self, x, y, z, width, length, height):
        # set material
        material = random.choice(self.materials)

        # level 1 houses
        self.mc.setBlocks(x, y, z, x + width, y + height, z + length, material)
        self.mc.setBlocks(x + 1, y + 1, z + 1, x + width - 1, y + height - 1, z + length - 1, block.AIR)

        # door
        self.mc.setBlock(x , y + 2, z + 2, block.DOOR_WOOD.withData(8))
        self.mc.setBlock(x , y + 1, z + 2, block.DOOR_WOOD.withData(0))
        self.mc.setBlock(x - 1 , y, z + 2, block.STAIRS_WOOD.withData(0))
        self.mc.setBlock(x - 1 , y, z + 1, block.STAIRS_WOOD.withData(0))
        self.mc.setBlock(x - 1 , y, z + 3, block.STAIRS_WOOD.withData(0))
        self.mc.setBlocks(x - 2, y - 1, z + 1, x - 4, y - 1, z + 3, 179, 2)
        generate_2nd_floor = random.choice([True, False])

        if generate_2nd_floor:
            self.mc.setBlocks(x, y + height, z, x + width, y + height + height, z + length, material)
            # Hollow out the top floor
            self.mc.setBlocks(x + 1, y + height + 1, z + 1, x + width -1, y + height + height - 1, z + length -1, block.AIR)
            # Make a hole in first floor roof to allow for stair
            self.mc.setBlocks(x + 2 , y + height, z + length - 1, x + width - 1, y + height, z + length - 1,self.air)
            # stairs
            for i in range(height):
                self.mc.setBlock(x + width - height + i, y + 1 + i, z + length - 1,self.stairs)
            # Windows
            midz = length // 2
            self.mc.setBlocks(x + width, y + 1, z + 1, x + width, y + 2, z + midz - 1, self.window) # back bottom left window
            self.mc.setBlocks(x + width, y + height + 1, z + 1, x + width, y + height + 2, z + length -1, self.window) # back top window
            self.mc.setBlocks(x + 3, y + 1, z, x + width - 1, y + 2, z, self.window) # left side bottom window
            self.mc.setBlocks(x + 3, y + height + 1, z + length, x + width -1 , y + height + 2, z + length, self.window) # right side top window
            self.mc.setBlocks(x, y + 1, z + midz, x, y + 2, z + length -1, self.window) # front bottom window
            self.mc.setBlocks(x, y + height + 1, z + 1, x, y + height + 2, z + midz - 1, self.window) # front top window
            # roof
            midwidth = width / 2
            top = height + height

            for i in range(length + 1):
                for j in range(4):
                    self.mc.setBlock(x - 1 + j, y + top + j, z + i, self.stairs)

            for i in range(4):
                self.mc.setBlock(x - 1 + i, y + top + i, z - 1, self.stairs)

            for i in range(4):
                self.mc.setBlock(x - 1 + i, y + top + i, z + length + 1, self.stairs)

            if width % 2 != 0:
                self.mc.setBlocks(x + 1, y + top + 1, z, x + width, y + top + 1, z + length, self.roof_material)
                self.mc.setBlocks(x + 2, y + top + 2, z, x + width - 1, y + top + 2, z + length, self.roof_material)
                self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + width - 2, y + top + 3, z + length + 1, self.roof_material)
                
                # self.mc.setBlocks(x + 3, y + top + 1, z, x + 6, y + top + 3, z + length, self.roof_material)
                # self.mc.setBlocks(x + 2, y + top + 1, z, x + 2, y + top + 2, z + length, self.roof_material)
                # self.mc.setBlocks(x + 1, y + top + 1, z, x + 1, y + top + 1, z + length, self.roof_material)
                # self.mc.setBlocks(x + 7, y + top + 1, z, x + 7, y + top + 2, z + length, self.roof_material)
                # self.mc.setBlocks(x + 8, y + top + 1, z, x + 8, y + top + 1, z + length, self.roof_material)
                # self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + 6, y + top + 3, z - 1, self.roof_material)
                # self.mc.setBlocks(x + 3, y + top + 3, z + length + 1, x + 6, y + top + 3, z + length + 1, self.roof_material)
            else:
                self.mc.setBlocks(x + 1, y + top + 1, z, x + width, y + top + 1, z + length, self.roof_material)
                self.mc.setBlocks(x + 2, y + top + 2, z, x + width - 1, y + top + 2, z + length, self.roof_material)
                self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + width - 2, y + top + 3, z + length + 1, self.roof_material)
                
                # self.mc.setBlocks(x + 3, y + top + 1, z, x + 5, y + top + 3, z + length, self.roof_material)
                # self.mc.setBlocks(x + 2, y + top + 1, z, x + 2, y + top + 2, z + length, self.roof_material)
                # self.mc.setBlocks(x + 1, y + top + 1, z, x + 1, y + top + 1, z + length, self.roof_material)      
                # self.mc.setBlocks(x + 6, y + top + 1, z, x + 6, y + top + 2, z + length, self.roof_material)
                # self.mc.setBlocks(x + 6, y + top + 1, z, x + 7, y + top + 1, z + length, self.roof_material)
                # self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + 5, y + top + 3, z - 1, self.roof_material)
                # self.mc.setBlocks(x + 3, y + top + 3, z + length + 1, x + 5, y + top + 3, z + length + 1, self.roof_material)
            for i in range(length + 1): 
                for j in range(4):
                    self.mc.setBlock(x + width + 1 - j, y + top + j, z + i, self.stair)

            for i in range(4):
                self.mc.setBlock(x + width + 1 - i, y + top + i, z - 1, self.stair)

            for i in range(4):
                self.mc.setBlock(x + width + 1 - i, y + top + i, z + length + 1, self.stair)
        else:
            # Windows
            midz = length // 2
            self.mc.setBlocks(x + width, y + 1, z + 1, x + width, y + 2, z + midz - 1, self.window) # back bottom left window
            self.mc.setBlocks(x + 3, y + 1, z, x + width - 1, y + 2, z, self.window) # left side bottom window
            self.mc.setBlocks(x, y + 1, z + midz, x, y + 2, z + length -1, self.window) # front bottom window
            # roof
            top = height

            for i in range(length + 1):
                for j in range(4):
                    self.mc.setBlock(x - 1 + j, y + height + j, z + i, self.stairs)

            for i in range(4):
                self.mc.setBlock(x - 1 + i, y + height + i, z - 1, self.stairs)

            for i in range(4):
                self.mc.setBlock(x - 1 + i, y + height + i, z + length + 1, self.stairs)

            if width % 2 != 0:
                self.mc.setBlocks(x + 1, y + top + 1, z, x + width, y + top + 1, z + length, self.roof_material)
                self.mc.setBlocks(x + 2, y + top + 2, z, x + width - 1, y + top + 2, z + length, self.roof_material)
                self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + width - 2, y + top + 3, z + length + 1, self.roof_material)
            else:
                self.mc.setBlocks(x + 1, y + top + 1, z, x + width, y + top + 1, z + length, self.roof_material)
                self.mc.setBlocks(x + 2, y + top + 2, z, x + width - 1, y + top + 2, z + length, self.roof_material)
                self.mc.setBlocks(x + 3, y + top + 3, z - 1, x + width - 2, y + top + 3, z + length + 1, self.roof_material)
            for i in range(length + 1): 
                for j in range(4):
                    self.mc.setBlock(x + width + 1 - j, y + height + j, z + i, self.stair)

            for i in range(4):
                self.mc.setBlock(x + width + 1 - i, y + height + i, z - 1, self.stair)

            for i in range(4):
               self.mc.setBlock(x + width + 1 - i, y + height + i, z + length + 1, self.stair)




    # Define minimum room size and randomness
    min_room_size = random.randint(3, 3)
    randomness = 0.2

    def generate_room(self, mc, x1, y1, z1, x2, y2, z2, material, stop_prob=0.1):
        # Define minimum room size and randomness
        min_room_size = random.randint(3, 3)
        def split_room(horizontal=True, min_size=min_room_size):
            nonlocal x1, y1, z1, x2, y2, z2
            if horizontal:
                # split vertically
                if x2 - x1 < min_size * 2:
                    return
                wall_x = random.randint(x1 + min_size, x2 - min_size)
                mc.setBlocks(wall_x, y1, z1, wall_x, y2, z2, material)
                door_x = wall_x + random.choice([-1, 1])
                mc.setBlock(door_x, y1, z1 + 1, block.AIR)
                mc.setBlock(door_x, y1 + 1, z1 + 1, block.AIR)
                x2 = wall_x
                if random.random() > stop_prob:
                    split_room(not horizontal, min_size)
                    split_room(horizontal, min_size)
            else:
                # split horizontally
                if z2 - z1 < min_size * 2:
                    return
                wall_z = random.randint(z1 + min_size, z2 - min_size)
                mc.setBlocks(x1, y1, wall_z, x2, y2, wall_z, material)
                door_z = wall_z + random.choice([-1, 1])
                mc.setBlock(x1 + 1, y1, door_z, block.AIR)
                mc.setBlock(x1 + 1, y1 + 1, door_z, block.AIR)
                z2 = wall_z
                if random.random() > stop_prob:
                    split_room(not horizontal, min_size)
                    split_room(horizontal, min_size)

        split_room()





# # test
# mc = Minecraft.create()
# hg = House(mc.player.getTilePos(), mc)
# hg.construct()

# # Define the coordinates of the bounding box
# x1, y1, z1 = 0, 0, 0
# x2, y2, z2 = 10, 10, 10

# # Generate the room
# # hg.generate_room(mc, x1, y1, z1, x2, y2, z2, block.STONE)