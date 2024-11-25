from mcpi.minecraft import Minecraft
from mcpi import block
import random

mc = Minecraft.create()

# get players position
x, y, z = mc.player.getTilePos()

# Define the size of the house
width = random.randint(9, 11)
length = random.randint(11, 15)
height = random.randint(5, 6)

# set material
materials = [block.COBBLESTONE, block.BRICK_BLOCK, block.WOOD_PLANKS]
material = random.choice(materials)
air = 0
roof_material = block.WOOD_PLANKS
window = block.GLASS_PANE
stairs = block.STAIRS_WOOD

# level 1 houses
mc.setBlocks(x, y, z, x + width, y + height, z + length, material)
mc.setBlocks(x + 1, y + 1, z + 1, x + width - 1, y + height - 1, z + length - 1, block.AIR)












# door
mc.setBlocks(x, y + 1, z + 2, x + 1, y + 3, z + 1, air)
mc.setBlock(x, y + 1, z + 2, x + 1, y + 3, z + 1, block.DOOR_WOOD.withData(8))

# 2nd floor
mc.setBlocks(x, y + 5, z, x + width, y + height + 5, z + length, material)

# Hollow out the top floor
mc.setBlocks(x + 1, y + 6, z + 1, x + width -1, y + height + 5 - 1, z + length -1, air)

# Windows
mc.setBlocks(x, y + 6, z + 1, x, y + 8, z + 2, window) # Front left window
mc.setBlocks(x, y + 6, z + 4, x, y + 8, z + 5, window) # Front right window
mc.setBlocks(x + 3, y + 7, z, x + 7, y + 8, z, window) # left side window
mc.setBlocks(x + 3, y + 7, z + length, x + 7, y + 8, z + length, window) # right side window

# Make a hole in first floor roof to allow for stair
mc.setBlocks(x + 5, y + 5, z + 5, x + 8, y + 5, z + 5,air)

# staris
for i in range(5):
    mc.setBlock(x + 4 + i, y + 1 + i, z + 5,stairs)
for i in range(5):
    mc.setBlock(x + 4 + i, y + 1 + i, z + 6,stairs)

