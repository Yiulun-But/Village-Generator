from mcpi.minecraft import Minecraft, Vec3
from mcpi import block
import numpy as np

import math


class Terraformer:
    def __init__(self, pos: Vec3, scale, mc: Minecraft):
        self.player_pos_x = pos.x
        self.player_pos_y = pos.y
        self.player_pos_z = pos.z
        self.scale = scale
        self.scale_conversion()
        self.mc = mc
        self.upper_left_corner_height = None
        self.upper_right_corner_height = None
        self.lower_left_corner_height = None
        self.lower_right_corner_height = None

        self.upper_right_corner_loopcount = None
        self.upper_left_corner_loopcount = None
        self.lower_left_corner_loopcount = None
        self.lower_right_corner_loopcount = None

        self.upper_left_corner_cordinate = [None, None]
        self.upper_right_corner_cordinate = [None, None]
        self.lower_left_corner_cordinate = [None, None]
        self.lower_right_corner_cordinate = [None, None]
        
    def scale_conversion(self):
        x_lower = self.scale[0].x
        x_upper = self.scale[1].x
        z_lower = self.scale[0].z
        z_upper = self.scale[1].z
        self.width = x_upper - x_lower + 3
        self.length = z_upper - z_lower + 3
        
    def perform_terraforming(self):
        self.terraform(self.width, self.length)  

    def column_each_terraces(self, x, z, target_height, default_height, loops_smooth_count, loop_each_terraces, current_height, block_id):
        # Get current height
        # current_height = self.mc.getHeight(x, z)
        # Check if target height is higher or lower than current height
        if target_height > current_height:
            # Add blocks to reach target height
            for i in range(target_height - current_height):
                self.mc.setBlock(x, current_height + i+1, z, block_id)
            if loop_each_terraces == 1:
                return True
        elif default_height >= current_height and current_height >= target_height:
            self.mc.setBlock(x, current_height, z, block_id)

        else:
            # Find the best target_height when smooth up (futher=weaker, closer= stronger)
            smooth_up_target_height = 0
            # check 2 blocks arround the center
            if loops_smooth_count == 0:
                if current_height - default_height <= 2:
                    smooth_up_target_height = round(
                        (current_height-default_height)/3)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = round(
                        (current_height-default_height)/4)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = round(
                        (current_height-default_height)/5)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = round(
                        (current_height-default_height)/6)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = round(
                        (current_height-default_height)/7)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/8)
                elif current_height - default_height > 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/9)
            if loops_smooth_count == 1:
                if current_height - default_height <= 2:
                    smooth_up_target_height = round(
                        (current_height-default_height)/2)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = round(
                        (current_height-default_height)/3)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = round(
                        (current_height-default_height)/3.5)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = round(
                        (current_height-default_height)/4)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = round(
                        (current_height-default_height)/4.5)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/5.0)
                elif current_height - default_height > 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/6)
            # 2 continue blocks (index 2-3)
            elif loops_smooth_count == 2:
                if current_height - default_height <= 2:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1.5)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1.75)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = round(
                        (current_height-default_height)/2)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = round(
                        (current_height-default_height)/3)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/4)
                elif current_height - default_height > 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/5)
            elif loops_smooth_count == 3:
                if current_height - default_height <= 2:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1.25)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1.35)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = round(
                        (current_height-default_height)/1.5)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = round(
                        (current_height-default_height)/2)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/2.5)
                elif current_height - default_height > 15:
                    smooth_up_target_height = round(
                        (current_height-default_height)/3)
            #  2 continue blocks (index 4)
            elif loops_smooth_count == 4:
                if current_height - default_height <= 2:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.2)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.3)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.4)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.5)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/2)
                elif current_height - default_height > 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/2.5)

            elif loops_smooth_count == 5:
                if current_height - default_height <= 2:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.1)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.2)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.3)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.4)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.5)
                elif current_height - default_height > 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.75)

            elif loops_smooth_count >= 6:
                if current_height - default_height <= 2:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1)
                elif current_height - default_height > 2 and current_height - default_height <= 3:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1)
                elif current_height - default_height > 3 and current_height - default_height <= 6:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.1)
                elif current_height - default_height > 6 and current_height - default_height <= 9:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.1)
                elif current_height - default_height > 9 and current_height - default_height <= 12:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.2)
                elif current_height - default_height > 12 and current_height - default_height <= 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.2)
                elif current_height - default_height > 15:
                    smooth_up_target_height = math.ceil(
                        (current_height-default_height)/1.3)
            # Remove blocks to reach default height
            for i in range(current_height - (default_height + smooth_up_target_height)):
                self.mc.setBlock(x, current_height - i, z, block.AIR.id)
            self.mc.setBlock(x, default_height +
                             smooth_up_target_height, z, block_id)

    def bulldoze_area(self, x, z, target_height, current_height, block_id):
        # Get current height
        # Check if target height is higher or lower than current height
        if target_height > current_height:
            # Add blocks to reach target height
            for i in range(target_height - current_height):
                self.mc.setBlock(x, current_height + i+1, z, block_id)
        elif target_height < current_height:
            # Remove blocks to reach target height
            for i in range(current_height - target_height):
                self.mc.setBlock(x, current_height - i, z, block.AIR.id)
            self.mc.setBlock(x, target_height, z, block_id)

    def rounded_area(self, x, z, target_height, block_id):
        # Get current height
        current_height = self.mc.getHeight(x, z)

        if target_height > current_height:
            # Add blocks to reach target height
            for i in range(target_height - current_height + 1):
                self.mc.setBlock(x, current_height + i, z, block_id)
        elif target_height < current_height:
            # Remove blocks to reach target height
            for i in range(current_height - target_height):
                self.mc.setBlock(x, current_height - i, z, block.AIR.id)
            self.mc.setBlock(x, target_height, z, block_id)
        else:
            self.mc.setBlock(x, target_height, z, block_id)

    def create_terraces(self, cur_x, cur_z, cur_len_x, cur_len_z, target_height, default_height, loops_smooth_count, block_id):

        rounded_lower_right_corners = False
        rounded_lower_left_corners = False
        rounded_upper_left_corners = False
        rounded_upper_right_corners = False

        lower_heights = self.mc.getHeights(
            cur_x, cur_z, cur_x + cur_len_x-1, cur_z)
        left_heights = self.mc.getHeights(
            cur_x + cur_len_x - 1, cur_z+1, cur_x + cur_len_x - 1,  cur_z + cur_len_z-1-1)
        upper_heights = self.mc.getHeights(
            cur_x + cur_len_x-1, cur_z + cur_len_z - 1, cur_x-1-1, cur_z + cur_len_z - 1)
        right_heights = self.mc.getHeights(
            cur_x, cur_z + cur_len_z - 2, cur_x, cur_z)

        upper_heights.reverse()
        right_heights.reverse()

        # block_id_lower = self.mc.getBlockWithData(
        #     cur_x, lower_heights[0], cur_z)
        # block_id_left = self.mc.getBlockWithData(
        #     cur_x + cur_len_x - 1, left_heights[0], cur_z+1)
        # block_id_upper = self.mc.getBlockWithData(
        #     cur_x-1-1, cur_z + cur_len_z - 1, upper_heights[len(upper_heights)-1], cur_z+1)
        # block_id_right = self.mc.getBlockWithData(
        #     cur_x+1, right_heights[len(right_heights)-1], cur_z+1)

        # red_|blue
        # _ under <-
        count_loop_under_edge = 0
        under = 0
        for i in range(cur_x, cur_x + cur_len_x):
            # current_height = heights[][]
            temp = self.column_each_terraces(i,  cur_z, target_height,
                                             default_height, loops_smooth_count, count_loop_under_edge, lower_heights[under], block_id)
            if temp == True:
                rounded_lower_right_corners = temp
            count_loop_under_edge += 1
            under += 1

        # | left ^
        left = 0
        count_loop_left_edge = 0
        for i in range(cur_z+1, cur_z + cur_len_z-1):
            temp = self.column_each_terraces(cur_x + cur_len_x - 1, i, target_height,
                                             default_height, loops_smooth_count, count_loop_left_edge, left_heights[left], block_id)
            if temp == True:
                rounded_lower_left_corners = temp
            count_loop_left_edge += 1
            left += 1

        # # # - top ->
        top = 0
        count_loop_top_edge = 0
        for i in range(cur_x + cur_len_x-1, cur_x-1, -1):
            temp = self.column_each_terraces(i, cur_z + cur_len_z - 1, target_height,
                                             default_height, loops_smooth_count, count_loop_top_edge, upper_heights[top], block_id)
            if temp == True:
                rounded_upper_left_corners = temp
            count_loop_top_edge += 1
            top += 1

        # # # # | right v
        right = 0
        count_loop_right_edge = 0
        for i in range(cur_z + cur_len_z - 2, cur_z, -1):
            temp = self.column_each_terraces(cur_x,  i, target_height,
                                             default_height, loops_smooth_count, count_loop_right_edge, right_heights[right], block_id)
            if temp == True:
                rounded_upper_right_corners = temp
            count_loop_right_edge += 1
            right += 1

        if rounded_lower_left_corners == True:
            self.terracorner(cur_x, cur_z, cur_len_x, cur_len_z,
                             loops_smooth_count, target_height, 2, block_id)
        if rounded_lower_right_corners == True:
            self.terracorner(cur_x, cur_z, cur_len_x, cur_len_z,
                             loops_smooth_count, target_height, 1, block_id)
        if rounded_upper_left_corners == True:
            self.terracorner(cur_x, cur_z, cur_len_x, cur_len_z,
                             loops_smooth_count, target_height, 4, block_id)
        if rounded_upper_right_corners == True:
            self.terracorner(cur_x, cur_z, cur_len_x, cur_len_z,
                             loops_smooth_count, target_height, 3, block_id)

    def terracorner(self, cur_x, cur_z, cur_len_x, cur_len_z, loops, target_height, corner_number, block_id):
        if corner_number == 1:
            corner1x = cur_x
            corner1z = cur_z + loops
            for j in range(loops+1):
                self.rounded_area(corner1x + j, corner1z - j,
                                  target_height, block_id)

                self.lower_right_corner_cordinate = [
                    corner1x + j, corner1z - j+1]
            self.lower_right_corner_height = target_height
            self.lower_right_corner_loopcount = loops+1

        elif corner_number == 2:
            corner2x = cur_x + cur_len_x - 1 - loops
            corner2z = cur_z
            for j in range(loops+1):
                self.rounded_area(corner2x + j, corner2z + j,
                                  target_height, block_id)
                self.lower_left_corner_height = target_height
                self.lower_left_corner_cordinate = [corner2x + j, corner2z + j]
            self.lower_left_corner_loopcount = loops+1

        elif corner_number == 3:
            corner3x = cur_x
            corner3z = cur_z + cur_len_z - 1 - loops
            for j in range(loops+1):
                self.rounded_area(corner3x + j,  corner3z + j,
                                  target_height, block_id)
                self.upper_right_corner_height = target_height
                self.upper_right_corner_cordinate = [
                    corner3x + j,  corner3z + j]
            self.upper_right_corner_loopcount = loops+1

        elif corner_number == 4:
            corner4x = cur_x + cur_len_x - 1 - loops
            corner4z = cur_z + cur_len_z - 1
            for j in range(loops+1):
                self.rounded_area(corner4x + j,  corner4z - j,
                                  target_height, block_id)
                self.upper_left_corner_height = target_height
                self.upper_left_corner_cordinate = [
                    corner4x + j,  corner4z - j]
            self.upper_left_corner_loopcount = loops+1

    def check_remain_corner(self, cordinate_x, cordinate_z, target_height, loops, corner_numb):
        if corner_numb == 1:
            corner1x = cordinate_x
            corner1z = cordinate_z
            for j in range(loops-1):
                # print(
                #     f"{target_height} {corner1x - j}, {corner1z + j}")
                self.remove_remain_corner(corner1x - j-1, corner1z + j,
                                          target_height)

        elif corner_numb == 2:
            corner2x = cordinate_x
            corner2z = cordinate_z
            for j in range(loops-1):
                # print(
                #     f"{target_height} {corner2x - j}, {corner2z - j-1}")
                self.remove_remain_corner(corner2x - j, corner2z - j-1,
                                          target_height)
        elif corner_numb == 3:
            corner3x = cordinate_x
            corner3z = cordinate_z
            for j in range(loops-1):
                # print(
                #     f"{target_height} {corner3x + j}, {corner3z + j}")
                self.remove_remain_corner(corner3x - j-1,  corner3z - j,
                                          target_height)
        elif corner_numb == 4:
            corner4x = cordinate_x
            corner4z = cordinate_z
            for j in range(loops-1):
                # print(
                #     f"{target_height} {corner4x - j-1}, {corner4z + j+1}")
                self.remove_remain_corner(corner4x - j-1,  corner4z + j+1,
                                          target_height)

    def remove_remain_corner(self, x, z, target_height):
        current_height = self.mc.getHeight(x, z)
        if current_height >= target_height:
            for i in range(current_height - target_height):
                self.mc.setBlock(x, current_height - i, z, block.AIR.id)

    def terraform(self, xx, zz):
        # Get heights array
        N = xx + 16
        M = zz + 16

        start_cordinate_x = self.player_pos_x-N//2
        start_cordinate_z = self.player_pos_z-M//2

        heights = self.mc.getHeights(
            start_cordinate_x, start_cordinate_z, start_cordinate_x + N-1, start_cordinate_z + M-1)
        min_height = min(heights)

        # Convert 1D array to 2D array
        heights_2d = np.reshape(heights, (N, M))

        # Calculate small rectangle coordinates
        center_x = N // 2
        center_z = M // 2
        x_start = center_x - xx // 2
        z_start = center_z - zz // 2

        target_block_height = heights_2d[center_x][center_z]
        # print(target_block_height)

        block_id = self.mc.getBlockWithData(
            self.player_pos_x, target_block_height, self.player_pos_z)
        print(block_id)
        self.mc.setBlocks(x_start, self.player_pos_y, x_start + xx,
                     x_start, 100, x_start + xx, block.AIR)
        for i in range(x_start, x_start + xx):
            for j in range(z_start, z_start + zz):
                current_height = heights_2d[i][j]

                self.bulldoze_area(start_cordinate_x + i, start_cordinate_z + j,
                                   target_block_height, current_height, block_id)

        default_height = target_block_height
        cur_len_x = xx + 2
        cur_len_z = zz + 2
        cur_x = start_cordinate_x + x_start - 1
        cur_z = start_cordinate_z + z_start - 1

        division = (target_block_height-min_height)//6
        if (target_block_height-min_height)//6 == 0:
            division = 1

        for i in range(8):
            if i == 0 or target_block_height-min_height == 2:
                target_block_height -= 1
            else:
                target_block_height -= division
            self.create_terraces(cur_x, cur_z, cur_len_x, cur_len_z,
                                 target_block_height, default_height, i, block_id)
            cur_x -= 1
            cur_z -= 1
            cur_len_z += 2
            cur_len_x += 2

        if self.lower_left_corner_loopcount != None:
            for i in range(self.lower_left_corner_loopcount+1):
                self.lower_left_corner_loopcount -= 1
                self.check_remain_corner(self.lower_left_corner_cordinate[0], self.lower_left_corner_cordinate[1]-i,
                                         self.lower_left_corner_height, self.lower_left_corner_loopcount, 2)

        if self.lower_right_corner_loopcount != None:
            for i in range(self.lower_right_corner_loopcount+1):
                self.lower_right_corner_loopcount -= 1
                self.check_remain_corner(self.lower_right_corner_cordinate[0]-i, self.lower_right_corner_cordinate[1],
                                         self.lower_right_corner_height, self.lower_right_corner_loopcount, 1)

        if self.upper_right_corner_loopcount != None:
            for i in range(self.upper_right_corner_loopcount+1):
                self.upper_right_corner_loopcount -= 1
                self.check_remain_corner(self.upper_right_corner_cordinate[0]-i, self.upper_right_corner_cordinate[1],
                                         self.upper_right_corner_height, self.upper_right_corner_loopcount, 3)

        if self.upper_left_corner_loopcount != None:
            for i in range(self.upper_left_corner_loopcount+1):
                self.upper_left_corner_loopcount -= 1
                self.check_remain_corner(self.upper_left_corner_cordinate[0], self.upper_left_corner_cordinate[1]+i,
                                         self.upper_left_corner_height, self.upper_left_corner_loopcount, 4)


if __name__ == "__main__":
    mc = Minecraft.create()
    playerPos = mc.player.getTilePos()

    terra = Terraformer(playerPos, mc)
    terra.terraform(10, 15)
