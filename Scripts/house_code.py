from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
import random

class HouseBuilder:
    def __init__(self, pos, mc):
        self.mc = mc
        self.pos = pos
        self.scale = self.determine_size()
        self.door_front = None
        self.materials = [block.COBBLESTONE, block.BRICK_BLOCK, block.WOOD_PLANKS]
        self.air = 0
        self.roof_material = block.WOOD_PLANKS
        self.window = 102
        self.stairs = block.STAIRS_WOOD
        self.stair = block.STAIRS_WOOD.withData(1)
        
        
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

    def build_house(self):
        x, y, z = self.pos.x, self.pos.y, self.pos.z
        width = random.randint(8, 9)
        length = random.randint(11, 15)
        height = random.randint(3, 4)
        material = random.choice(self.materials)

        # Build the house
        self.mc.setBlocks(x, y, z, x + width, y + height, z + length, material)
        self.mc.setBlocks(x + 1, y + 1, z + 1, x + width - 1, y + height - 1, z + length - 1, block.AIR)

        # Divide the house into rooms
        min_room_size = random.randint(3, 4)
        randomness = 0.2
        self.split_room(x, y, z, x + width, y + height, z + length, True, min_room_size, randomness)

    def split_room(self, x1, y1, z1, x2, y2, z2, horizontal=True, min_size=3, stop_prob=0.1):
            if horizontal:
                # split vertically
                if x2 - x1 < min_size * 2:
                    return
                wall_x = random.randint(x1 + min_size, x2 - min_size)
                self.mc.setBlocks(wall_x, y1, z1, wall_x, y2, z2, self.materials[0])
                door_x = wall_x + random.choice([-1, 1])
                self.mc.setBlock(door_x, y1, z1 + 1, self.air)
                self.mc.setBlock(door_x, y1 + 1, z1 + 1, self.air)
                if random.random() > stop_prob:
                    self.split_room(x1, y1, z1, wall_x, y2, z2, not horizontal, min_size, stop_prob)
                    self.split_room(wall_x + 1, y1, z1, x2, y2, z2, not horizontal, min_size, stop_prob)
            else:
                # split horizontally
                if z2 - z1 < min_size * 2:
                    return
                wall_z = random.randint(z1 + min_size, z2 - min_size)
                self.mc.setBlocks(x1, y1, wall_z, x2, y2, wall_z, self.materials[0])
                door_z = wall_z + random.choice([-1, 1])
                self.mc.setBlock(x1 + 1, y1, door_z, self.air)
                self.mc.setBlock(x1 + 1, y1 + 1, door_z, self.air)
                if random.random() > stop_prob:
                    self.split_room(x1, y1, z1, x2, y2, wall_z, not horizontal, min_size, stop_prob)
                    self.split_room(x1, y1, wall_z + 1, x2, y2, z2, not horizontal, min_size, stop_prob)
    
    
    def build_house(mc, x, y, z, width, height, length, material, window, stairs):
        # Build walls
        def build_wall(x1, y1, z1, x2, y2, z2):
            mc.setBlocks(x1, y1, z1, x2, y2, z2, material)

        def split_room(x1, y1, z1, x2, y2, z2):
            build_wall(x1, y1, z1, x2, y2, z1) # front
            build_wall(x1, y1, z1, x1, y2, z2) # left
            build_wall(x2, y1, z1, x2, y2, z2) # right
            build_wall(x1, y1, z2, x2, y2, z2) # back

        build_wall(x, y, z, x + width, y + height, z + length) # outer shell
        split_room(x + 1, y + 1, z + 1, x + width - 1, y + height - 1, z + length - 1) # interior walls

    def build_roof(mc, x, y, z, width, length, height, material, roof_material, window):
        generate_2nd_floor = random.choice([True, False])
        midz = width / 2
        stair = block.STAIRS_WOOD.withData(1)
        if generate_2nd_floor:
            mc.setBlocks(x, y + height, z, x + width, y + height + height, z + length, material)
            # Hollow out the top floor
            mc.setBlocks(x + 1, y + height + 1, z + 1, x + width -1, y + height + height - 1, z + length -1, block.AIR)
            # Make a hole in first floor roof to allow for stair
            mc.setBlocks(x + 2 , y + height, z + length - 1, x + width - 1, y + height, z + length - 1, block.AIR)
            # stairs
            for i in range(height):
                mc.setBlock(x + width - height + i, y + 1 + i, z + length - 1, block.STAIRS_WOOD)
            # Windows
            mc.setBlocks(x + width, y + 1, z + 1, x + width, y + 2, z + length // 2 - 1, window) # back bottom left window
            mc.setBlocks(x + width, y + height + 1, z + 1, x + width, y + height + 2, z + length -1, window) # back top window
            mc.setBlocks(x + 3, y + 1, z, x + width - 1, y + 2, z, window) # left side bottom window
            mc.setBlocks(x + 3, y + height + 1, z + length, x + width -1 , y + height + 2, z + length, window) # right side top window
            mc.setBlocks(x, y + 1, z + length // 2, x, y + 2, z + length -1, window) # front bottom window
            mc.setBlocks(x, y + height + 1, z + 1, x, y + height + 2, z + length // 2 - 1, window) # front top window
            # # roof
            midwidth = width // 2
            top = height + height

            for i in range(length + 1):
                for j in range(4):
                    mc.setBlock(x - 1 + j, y + top + j, z + i, block.STAIRS_WOOD)

            for i in range(4):
                mc.setBlock(x - 1 + i, y + top + i, z - 1, block.STAIRS_WOOD)

            for i in range(4):
                mc.setBlock(x - 1 + i, y + top + i, z + length + 1, block.STAIRS_WOOD)

            if width % 2 != 0:
                mc.setBlocks(x + 3, y + top + 1, z, x + 6, y + top + 3, z + length, roof_material)
                mc.setBlocks(x + 2, y + top + 1, z, x + 2, y + top + 2, z + length, roof_material)
                mc.setBlocks(x + 1, y + top + 1, z, x + 1, y + top + 1, z + length, roof_material)   
                mc.setBlocks(x + 7, y + top + 1, z, x + 7, y + top + 2, z + length, roof_material)
                mc.setBlocks(x + 8, y + top + 1, z, x + 8, y + top + 1, z + length, roof_material)
                mc.setBlocks(x + 3, y + top + 3, z - 1, x + 6, y + top + 3, z - 1, roof_material)
                mc.setBlocks(x + 3, y + top + 3, z + length + 1, x + 6, y + top + 3, z + length + 1, roof_material)
            else:
                mc.setBlocks(x + 3, y + top + 1, z, x + 5, y + top + 3, z + length, roof_material)
                mc.setBlocks(x + 2, y + top + 1, z, x + 2, y + top + 2, z + length, roof_material)
                mc.setBlocks(x + 1, y + top + 1, z, x + 1, y + top + 1, z + length, roof_material)      
                mc.setBlocks(x + 6, y + top + 1, z, x + 6, y + top + 2, z + length, roof_material)
                mc.setBlocks(x + 6, y + top + 1, z, x + 7, y + top + 1, z + length, roof_material)
                mc.setBlocks(x + 3, y + top + 3, z - 1, x + 5, y + top + 3, z - 1, roof_material)
                mc.setBlocks(x + 3, y + top + 3, z + length + 1, x + 5, y + top + 3, z + length + 1, roof_material)
            for i in range(length + 1): 
                for j in range(4):
                    mc.setBlock(x + width + 1 - j, y + top + j, z + i, stair)

            for i in range(4):
                mc.setBlock(x + width + 1 - i, y + top + i, z - 1, stair)

            for i in range(4):
                mc.setBlock(x + width + 1 - i, y + top + i, z + length + 1, stair)


        else:
            # Windows
            mc.setBlocks(x + width, y + 1, z + 1, x + width, y + 2, z + midz - 1, window) # back bottom left window
            mc.setBlocks(x + 3, y + 1, z, x + width - 1, y + 2, z, window) # left side bottom window
            mc.setBlocks(x, y + 1, z + midz, x, y + 2, z + length -1, window) # front bottom window
            # roof
            midwidth = width / 2
            top = height + height

            for i in range(length + 1):
                for j in range(4):
                    mc.setBlock(x - 1 + j, y + height + j, z + i, stairs)

            for i in range(4):
                mc.setBlock(x - 1 + i, y + height + i, z - 1, stairs)

            for i in range(4):
                mc.setBlock(x - 1 + i, y + height + i, z + length + 1, stairs)

            if width % 2 != 0:
                mc.setBlocks(x + 3, y + height + 1, z, x + 6, y + height + 3, z + length, roof_material)
                mc.setBlocks(x + 2, y + height + 1, z, x + 2, y + height + 2, z + length, roof_material)
                mc.setBlocks(x + 1, y + height + 1, z, x + 1, y + height + 1, z + length, roof_material)
                mc.setBlocks(x + 7, y + height + 1, z, x + 7, y + height + 2, z + length, roof_material)
                mc.setBlocks(x + 8, y + height + 1, z, x + 8, y + height + 1, z + length, roof_material)
                mc.setBlocks(x + 3, y + height + 3, z - 1, x + 6, y + height + 3, z - 1, roof_material)
                mc.setBlocks(x + 3, y + height + 3, z + length + 1, x + 6, y + height + 3, z + length + 1, roof_material)
            else:
                mc.setBlocks(x + 3, y + height + 1, z, x + 5, y + height + 3, z + length, roof_material)
                mc.setBlocks(x + 2, y + height + 1, z, x + 2, y + height + 2, z + length, roof_material)
                mc.setBlocks(x + 1, y + height + 1, z, x + 1, y + height + 1, z + length, roof_material)      
                mc.setBlocks(x + 6, y + height + 1, z, x + 6, y + height + 2, z + length, roof_material)
                mc.setBlocks(x + 6, y + height + 1, z, x + 7, y + height + 1, z + length, roof_material)
                mc.setBlocks(x + 3, y + height + 3, z - 1, x + 5, y + height + 3, z - 1, roof_material)
                mc.setBlocks(x + 3, y + height + 3, z + length + 1, x + 5, y + height + 3, z + length + 1, roof_material)
            for i in range(length + 1): 
                for j in range(4):
                    mc.setBlock(x + width + 1 - j, y + height + j, z + i, stair)

            for i in range(4):
                mc.setBlock(x + width + 1 - i, y + height + i, z - 1, stair)

            for i in range(4):
                mc.setBlock(x + width + 1 - i, y + height + i, z + length + 1, stair)

    def set_door(x, y, z):
        mc.setBlock(x, y + 2, z, block.DOOR_WOOD.withData(8))
        mc.setBlock(x, y + 1, z, block.DOOR_WOOD.withData(0))