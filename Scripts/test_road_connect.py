from mcpi.minecraft import Minecraft, Vec3
from terrain_analyzer import TerrainInfo
from village import Village

mc = Minecraft.create()
playerTilePos = mc.player.getTilePos()
village = Village(mc, playerTilePos)
village.create_village()
