from mcpi.minecraft import Minecraft, Vec3
from mcpi import block

class TerrainInfo:
    def __init__(self, corner1, corner2, mc: Minecraft):
        #Corners are tuples with x and z values of a vector 3 variable
        self.corner1 = corner1
        self.corner2 = corner2
        self.mc = mc
        self.x_upper, self.x_lower, self.z_upper, self.z_lower = self.determine_bounds()
        self.y_lower, self.y_upper = self.determine_y_bound()
        self.surface_blocks = self.generate_surface_blocks()
        
    def _analyze_area(self):
        heights = self.mc.getHeights(self.corner1[0], self.corner1[1], self.corner2[0], self.corner2[1])
        return heights
    
    def determine_bounds(self):
        x1, z1 = self.corner1
        x2, z2 = self.corner2
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
            
        return x_upper, x_lower, z_upper, z_lower
    
    def generate_surface_blocks(self):
        heights = self._analyze_area()
        surface_blocks = {}
        x_upper, x_lower, z_upper, z_lower = self.x_upper, self.x_lower, self.z_upper, self.z_lower
        block_ids = self.set_block_ids()
        i = 0
        for col in range(x_lower, x_upper + 1):
            for row in range(z_lower, z_upper + 1):
                surface_blocks[(col, row)] = (heights[i], self.get_block_id(Vec3(col, heights[i], row), block_ids))
                i += 1
        return surface_blocks
    
    def determine_y_bound(self):
        heights = self._analyze_area()
        return min(heights), max(heights)
    
    def set_block_ids(self):
        x_upper, x_lower, z_upper, z_lower = self.determine_bounds()
        y_lower, y_upper = self.y_lower, self.y_upper
        blocks = self.mc.getBlocks(x_lower, y_lower, z_lower, x_upper, y_upper, z_upper)
        blocks = list(blocks)
        return blocks
            
    def get_block_id(self, pos: Vec3, blocks):
        x_upper, x_lower, z_upper, z_lower = self.x_upper, self.x_lower, self.z_upper, self.z_lower
        y_lower, y_upper = self.y_lower, self.y_upper
        return blocks[(pos.z - z_lower) + (pos.x - x_lower)*(z_upper - z_lower + 1) + (pos.y - y_lower)*(x_upper - x_lower + 1)*(z_upper - z_lower + 1)]
    
    def _show_surface(self):
        for axis, height in self.surface_blocks.items():
            x, z = axis
            self.mc.setBlock(x, height, z, 35)
            
            
    def _bulldoze_area(self, y, height):
        x_upper, x_lower, z_upper, z_lower = self.x_upper, self.x_lower, self.z_upper, self.z_lower
        self.mc.setBlocks(x_lower, y, z_lower, x_upper, y + height - 1, z_upper, 0)
        
    def _create_flat(self, y):
        x_upper, x_lower, z_upper, z_lower = self.x_upper, self.x_lower, self.z_upper, self.z_lower
        self.mc.setBlocks(x_lower, y, z_lower, x_upper, y, z_upper, 35)
        