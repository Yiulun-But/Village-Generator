from typing import Self
from mcpi.minecraft import Minecraft
from mcpi import block
import random

mc = Minecraft.create()

class house_type1:
    def __init__(self, x, y, z, w, h, l):
    
    

    # Define a function to create a room
    def create_room(x, y, z, w, h, l):
        # Check if the room is big enough
            if w < 3 or h < 3 or l < 3:
                return

        # Set the material for the walls and roof
    wall_materials = [block.COBBLESTONE, block.BRICK_BLOCK, block.WOOD_PLANKS]
    wall_material = random.choice(wall_materials)
    roof_material = block.WOOD_PLANKS.id
    corner_material = block.WOOD.id  # Set the material for the corners

        # Build the walls
    for i in range(w):
        for j in range(h):
            for k in range(l):
                if (i == 0 and k == 0) or (i == w-1 and k == 0) or (i == 0 and k == l-1) or (i == w-1 and k == l-1):  # Check if the current block is a corner
                    mc.setBlock(x+i, y+j, z+k, corner_material)  # Set the material to corner_material
                elif i == 0 or i == w-1 or j == 0 or j == h-1 or k == 0 or k == l-1:
                    mc.setBlock(x+i, y+j, z+k, wall_material)

        # Build the roof
        for i in range(w):
            for j in range(h):
                for k in range(l):
                    if j == h-1 and (i != 0 and i != w-1 and k != 0 and k != l-1):
                        mc.setBlock(x+i, y+j, z+k, roof_material)

        # Recursively create more rooms
        if random.random() <= 0.5:
            create_room(x, y, z+random.randint(4, l-4), w, h, l//2)
            create_room(x, y, z, w, h, l//2)
        else:
            create_room(x+random.randint(4, w-4), y, z, w//2, h, l)
            create_room(x, y, z, w//2, h, l)

    # Get the player's current position
    playerTilePos = mc.player.getTilePos()

    # Define the size of the house
    width = random.randint(11, 15)
    length = random.randint(15, 19)
    height = random.randint(5, 6)

    # Calculate the starting position of the house based on the player's position
    x = playerTilePos.x - random.randint(-5, 5)
    z = playerTilePos.z - random.randint(-5, 5)

    # Create the first room
    create_room(x, playerTilePos.y, z, width, height, length)


    # Add some windows
    for i in range(2):
        window_pos = random.randint(1, width-2)
        if random.random() <= 0.5:  # Add a 2x2 window
            for j in range(2):
                for k in range(2):
                    mc.setBlock(x+window_pos+j, playerTilePos.y+2+k, z, block.GLASS_PANE.id)
        else:  # Add a 3x3 window
            for j in range(3):
                for k in range(3):
                    mc.setBlock(x+window_pos+j, playerTilePos.y+2+k, z, block.GLASS_PANE.id)

    # Add a door
    mc.setBlock(playerTilePos.x + 13, playerTilePos.y + 2, playerTilePos.z, block.DOOR_WOOD.withData(8))
    mc.setBlock(playerTilePos.x + 13, playerTilePos.y + 1, playerTilePos.z, block.DOOR_WOOD.withData(0))