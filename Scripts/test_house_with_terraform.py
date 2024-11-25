from mcpi.minecraft import Minecraft, Vec3
from terrain_analyzer import TerrainInfo
from village import Village
from terraformer import Terraformer
from house import House

mc = Minecraft.create()
playerTilePos = mc.player.getTilePos()
pos = Vec3(playerTilePos.x + 15, playerTilePos.y, playerTilePos.z)
terraformer = Terraformer(pos, mc)
house = House(pos, mc)
terraformer.terraform(house.w, house.l)
house._test_create_room()