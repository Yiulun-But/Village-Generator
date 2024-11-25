import math, random
from terrain_analyzer import TerrainInfo
from grid_interface import Grid
from terraformer_new import Terraformer
from house3 import House
# terraformer, house

class Village:
    def __init__(self, mc, pos):
        self.mc = mc
        self.pos = pos
        self.setup()
        
    def setup(self):
        self.terrain = self.generate_terrain_info(self.pos, self.mc)
        print('terrain valid')
        self.grid = Grid(self.terrain)
        print('grid valid')
        
    def generate_terrain_info(self, pos, mc):
        corner1 = (pos.x + 100, pos.z + 100)
        corner2 = (pos.x - 100, pos.z - 100)
        terrain = TerrainInfo(corner1, corner2, mc)
        return terrain
    
    def create_village(self):
        locations = self.generate_random_houses()
        houses = []  
        path_nodes = []          
        for location in locations:
            axis = location.pos #Vec3
            house = House(axis, self.mc)
            house_scale = house.scale
            terraformer = Terraformer(axis, house_scale, self.mc)
            terraformer.perform_terraforming()
            house.construct()
            houses.append(house)
            path_nodes.append(house.door_front)
        print([house.pos for house in houses])
        self.setup()
        for house in houses:
            self.grid.update_obstacles(house.scale[0], house.scale[1])
        self.grid.update_houses(path_nodes)
        self.grid.connect_road()
        
    def generate_random_houses(self):
        num = random.randint(5, 7)
        spots = self.grid.generate_random_locations(num)
        return spots