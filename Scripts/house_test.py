from house import House
from mcpi.minecraft import Minecraft, Vec3

mc = Minecraft.create()
playerTilePos = mc.player.getTilePos()
house = House(playerTilePos, mc)
house._test_create_room()
mc.setBlock(house.door_front.x, house.door_front.y, house.door_front.z, 18)