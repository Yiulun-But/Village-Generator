from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
from queue import PriorityQueue
from terrain_analyzer import TerrainInfo
import math, random

class Spot:
    status = {'none':0, 'start':1, 'end':2, 'open':4, 'closed':5}
    def __init__(self, row, col, pos: Vec3, max_row, max_col, block_id=0):
        self.pos = pos
        self.status = 0
        self.is_path = False
        self.max_row = max_row
        self.max_col = max_col
        self.row = row
        self.col = col
        self.block_id = block_id
        self.barrier = False
        self.neighbours = []
        
    def set_start(self):
        self.status = 1
        
    def set_end(self):
        self.status = 2
    
    def set_barrier(self):
        self.barrier = True
        
    def set_open(self):
        self.status = 4
    
    def set_closed(self):
        self.status = 5
    
    def is_start(self):
        if self.status == 1:
            return True
        return False
    
    def is_end(self):
        if self.status == 2:
            return True
        return False
    
    def is_barrier(self):
        if self.barrier == True:
            return True
        return False
    
    def is_open(self):
        if self.status == 4:
            return True
        return False
    
    def is_closed(self):
        if self.status == 5:
            return True
        return False
    
    def reset(self):
        self.status = 0
        
    def get_pos(self):
        return self.pos
    
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.max_row and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append((grid[self.row + 1][self.col], spot_distance(self, grid[self.row + 1][self.col])))
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append((grid[self.row - 1][self.col], spot_distance(self, grid[self.row - 1][self.col])))
            
        if self.col < self.max_col and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append((grid[self.row][self.col + 1], spot_distance(self, grid[self.row][self.col + 1])))
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append((grid[self.row][self.col - 1], spot_distance(self, grid[self.row][self.col - 1])))
        
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # TOP LEFT
            self.neighbours.append((grid[self.row - 1][self.col - 1], spot_distance(self, grid[self.row - 1][self.col - 1])))
            
        if self.col < self.max_col and self.row < self.max_row and not grid[self.row + 1][self.col + 1].is_barrier(): # LOWER RIGHT
            self.neighbours.append((grid[self.row + 1][self.col + 1], spot_distance(self, grid[self.row + 1][self.col + 1])))
        
        if self.row > 0 and self.col < self.max_col and not grid[self.row - 1][self.col + 1].is_barrier(): # TOP RIGHT
            self.neighbours.append((grid[self.row - 1][self.col + 1], spot_distance(self, grid[self.row - 1][self.col + 1])))
            
        if self.col > 0 and self.row < self.max_row and not grid[self.row + 1][self.col - 1].is_barrier(): # LOWER LEFT
            self.neighbours.append((grid[self.row + 1][self.col - 1], spot_distance(self, grid[self.row + 1][self.col - 1])))
            
        # if self.col < self.max_col and self.row < self.max_row - 1 and not grid[self.row + 2][self.col + 1].is_barrier(): # L
        #     self.neighbours.append((grid[self.row + 2][self.col + 1], math.sqrt(5)))
            
        # if self.col > 0 and self.row < self.max_row - 1 and not grid[self.row + 2][self.col - 1].is_barrier(): # REVERSED L
        #     self.neighbours.append((grid[self.row + 2][self.col - 1], math.sqrt(5)))
        
        # if self.row < self.max_row and self.col > 1 and not grid[self.row + 1][self.col - 2].is_barrier(): # 90D L
        #     self.neighbours.append((grid[self.row + 1][self.col - 2], math.sqrt(5)))
            
        # if self.row > 0 and self.col > 1 and not grid[self.row - 1][self.col - 2].is_barrier(): # 90D REVERSED L
        #     self.neighbours.append((grid[self.row - 1][self.col - 2], math.sqrt(5)))
            
        # if self.row > 1 and self.col > 0 and not grid[self.row - 2][self.col - 1].is_barrier(): # 180D L
        #     self.neighbours.append((grid[self.row - 2][self.col - 1], math.sqrt(5)))
            
        # if self.row > 1 and self.col < self.max_col and not grid[self.row - 2][self.col + 1].is_barrier(): # 180D REVERSED L
        #     self.neighbours.append((grid[self.row - 2][self.col + 1], math.sqrt(5)))
            
        # if self.row > 0 and self.col < self.max_col - 1 and not grid[self.row - 1][self.col + 2].is_barrier(): # -90D L
        #     self.neighbours.append((grid[self.row - 1][self.col + 2], math.sqrt(5)))
            
        # if self.col < self.max_col - 1 and self.row < self.max_row and not grid[self.row + 1][self.col + 2].is_barrier(): # -90D REVERSED L
        #     self.neighbours.append((grid[self.row + 1][self.col + 2], math.sqrt(5)))
            
    def __str__(self):
        return str(self.pos)
    
    
class Grid:
    def __init__(self, terrain: TerrainInfo):
        self.terrain = terrain
        self.grid = self.make_grid()
        self.set_obstacles()
        self.houses = []
        self.generate_neighbours()
        
    def update_houses(self, houses):
        for house in houses:
            spot = self.retreive_spot(house)
            self.houses.append(spot)
        
        
    def make_grid(self):
        surface = self.terrain.generate_surface_blocks()
        x_upper, x_lower, z_upper, z_lower = self.terrain.determine_bounds()
        max_col = x_upper - x_lower
        max_row = z_upper - z_lower
        grid = []
        for row in range(z_upper - z_lower + 1):
            grid.append([])
            for col in range(x_upper - x_lower + 1):
                spot = Spot(row, col, Vec3(col + x_lower, surface[(col + x_lower, row + z_lower)][0], row + z_lower), max_row, max_col, surface[(col + x_lower, row + z_lower)][1])
                grid[row].append(spot)
        return grid
    
    def generate_neighbours(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbours(self.grid)
    
    def retreive_spot(self, vec3: Vec3):
        x_upper, x_lower, z_upper, z_lower = self.terrain.determine_bounds()
        row = vec3.z - z_lower
        col = vec3.x - x_lower
        return self.grid[row][col]
    
    def search_route(self, start: Spot, end: Spot):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot:float('inf') for row in self.grid for spot in row}
        g_score[start] = 0
        f_score = {spot:float('inf') for row in self.grid for spot in row}
        f_score[start] = self.dist(start.pos, end.pos)
        
        open_set_hash = {start}
        
        while not open_set.empty():      
            current = open_set.get()[2]
            open_set_hash.remove(current)
            
            if current == end:
                route = self.deter_route(came_from, end) # make path
                return route
            
            for neighbour, distance in current.neighbours:
                temp_g_score = g_score[current] + float(distance)
                
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + self.dist(neighbour.pos, end.pos)
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.set_open()
            
            if current != start:
                current.set_closed()
        
        return []
    
    def dist(self, a: Vec3, b: Vec3):
        return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)
    
    def deter_route(self, came_from, end):
        route = []
        curr = end
        while (curr in came_from.keys()):
            route.append(curr)
            curr = came_from[curr]
        return route
    
    def generate_road(self, route):
        if route != False:
            for spot in route:
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y, spot.pos.z, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y, spot.pos.z+1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y, spot.pos.z-1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y, spot.pos.z-1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y, spot.pos.z+1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y, spot.pos.z, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y, spot.pos.z+1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y, spot.pos.z, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y, spot.pos.z-1, 35, 12)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 1, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 1, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 1, spot.pos.z-1, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 1, spot.pos.z-1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 1, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 1, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 1, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 1, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 1, spot.pos.z-1, 0)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 2, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 2, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 2, spot.pos.z-1, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 2, spot.pos.z-1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 2, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x+1, spot.pos.y + 2, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 2, spot.pos.z+1, 0)
                self.terrain.mc.setBlock(spot.pos.x-1, spot.pos.y + 2, spot.pos.z, 0)
                self.terrain.mc.setBlock(spot.pos.x, spot.pos.y + 2, spot.pos.z-1, 0)
                # for neighbour in spot.neighbours:
                #     if neighbour[1] <= 3:
                #         self.terrain.mc.setBlock(neighbour[0].pos.x, neighbour[0].pos.y, neighbour[0].pos.z, 35, 12)
            return True
        return False
    
    def set_obstacles(self):
        x_upper, x_lower, z_upper, z_lower = self.terrain.determine_bounds()
        for row in range(z_upper - z_lower + 1):
            for col in range(x_upper - x_lower + 1):
                if self.grid[row][col].block_id in [17, 18]:
                    self.grid[row][col].barrier = True
                    
    def update_obstacles(self, edge1: Vec3, edge2: Vec3):
        spot1 = self.retreive_spot(edge1)
        spot2 = self.retreive_spot(edge2)
        x1, z1 = spot1.pos.x, spot1.pos.z
        x2, z2 = spot2.pos.x, spot2.pos.z
        
        if x1 > x2:
            x_upper = x1
            x_lower = x2
        else:
            x_upper = x2
            x_lower = x1
        if z1 > z2:
            z_upper = z1
            z_lower = z2
        else:
            z_upper = z2
            z_lower = z1
        
        for row in range(z_lower - 2, z_upper + 3):
            for col in range(x_lower - 2, x_upper + 3):
                spot = self.retreive_spot(Vec3(col, 0, row))
                spot.set_barrier()
        
    def generate_random_locations(self, num: int):
        max_scale = 15
        x_upper, x_lower, z_upper, z_lower = self.terrain.determine_bounds()
        max_col = x_upper - x_lower
        max_row = z_upper - z_lower
        locations = []
        while len(locations) < num:
            valid = True
            center_row = random.randint(max_scale, max_row - max_scale)
            center_col = random.randint(max_scale, max_col - max_scale)
            center_spot =  self.grid[center_row][center_col]
            
            for row in range(center_row - max_scale, center_row + max_scale + 1):
                for col in range(center_col - max_scale, center_col + max_scale + 1):
                    spot = self.grid[row][col]
                    if spot.block_id in [8, 9, 10, 11] or spot.is_barrier():
                        valid = False
                        break
                if valid == False:
                    break
            
            for location in locations:
                distance = abs_distance(center_spot, location)
                if distance < 45:
                    print(distance)
                    valid = False
            
            if valid == True:
                locations.append(center_spot)
                small_spot = self.grid[center_row - max_scale][center_col - max_scale]
                large_spot = self.grid[center_row + max_scale][center_col + max_scale]
                self.update_obstacles(Vec3(small_spot.pos.x - 1, 0, small_spot.pos.z - 1), Vec3(large_spot.pos.x + 1, 0, large_spot.pos.z + 1))
        return locations
                
    def connect_road(self):
        self.generate_neighbours()
        unlinked_houses = self.houses
        linked_houses = []
        routes = []
        if len(unlinked_houses) < 2:
            print('Not enough houses')
            return
        route = []
        while len(route) == 0:
            i, j = random.sample(range(len(unlinked_houses)), 2)
            a = unlinked_houses[i]
            b = unlinked_houses[j]
            route = self.search_route(a, b)
            print(a.pos, b.pos)
            
        unlinked_houses.remove(a)
        unlinked_houses.remove(b)
        self.generate_road(route)
        routes.extend(route)
        while len(unlinked_houses) > 0:
            k = random.sample(range(len(unlinked_houses)), 1)[0]
            c = unlinked_houses.pop(k)
            print(c.pos)
            path_distance = {}
            for node in routes:
                distance = abs_distance(node, c)
                path_distance[node] = distance
            min_node = min(path_distance.items(), key=lambda x: x[1])[0]
            route = self.search_route(min_node, c)
            self.generate_road(route)
            routes.extend(route)
        
                
    def _show_locations(self, locations):
        for location in locations:
            print(location.block_id)
            self.terrain.mc.setBlock(location.pos.x, location.pos.y, location.pos.z, 35, 13)
    
    def _create_rand_start_end(self):
        x_upper, x_lower, z_upper, z_lower = self.terrain.determine_bounds()
        max_col = x_upper - x_lower
        max_row = z_upper - z_lower
        rows = random.sample(range(0, max_row + 1), 2)
        cols = random.sample(range(0, max_col + 1), 2)
        return self.grid[rows[0]][cols[0]], self.grid[rows[1]][cols[1]]
        
    def _test_rand_route(self):
        self.start, self.end = self._create_rand_start_end()
        self.generate_neighbours()
        route = self.search_route(self.start, self.end)
        success = self.generate_road(route)
        return success
    
    def test_given_tiles(self, pos1: Vec3, pos2: Vec3):
        start = self.retreive_spot(pos1)
        end = self.retreive_spot(pos2)
        self.generate_neighbours()
        route = self.search_route(start, end)
        success = self.generate_road(route)
        return success
    
        
    
def draw(mc:Minecraft, vec3: Vec3):
    mc.setBlock(vec3.x, vec3.y, vec3.z)
    
def spot_distance(spot1: Spot, spot2: Spot):
    x1, y1, z1 = spot1.pos.x, spot1.pos.y, spot1.pos.z
    x2, y2, z2 = spot2.pos.x, spot2.pos.y, spot2.pos.z
    y_weight = abs(y1 - y2)
    if abs(y1 - y2) > 1:
        y_weight = float('inf')
    return abs(x1 - x2) + y_weight + abs(z1 - z2)

def abs_distance(spot1: Spot, spot2: Spot):
    x1, y1, z1 = spot1.pos.x, spot1.pos.y, spot1.pos.z
    x2, y2, z2 = spot2.pos.x, spot2.pos.y, spot2.pos.z
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)