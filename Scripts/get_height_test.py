from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
from terrain_analyzer import TerrainInfo
from grid_interface import Grid, Spot


mc = Minecraft.create()
playerTilePos = mc.player.getTilePos()
corner1 = (playerTilePos.x + 50, playerTilePos.z + 50)
corner2 = (playerTilePos.x - 50, playerTilePos.z - 50)
terrain = TerrainInfo(corner1, corner2, mc)
grid = Grid(terrain)
grid.test_given_tiles(Vec3(576, 62, -76), Vec3(547, 62, -71))



