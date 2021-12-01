from bst import Node, BST
from manim import *
from collections import defaultdict
from math import inf

def get_bst(bst: BST, left=-7, width=14, top=4, height=8):
    if bst.root is None:
        return {}, {}, 0
    
    relative_positions = {}

    def naively_assign(current_node: Node, current_pos: int):
        """Assigns relative column positions to each node, with no regard for overlap"""
        if current_node is None:
            return
        
        relative_positions[current_node] = current_pos
        naively_assign(current_node.left, current_pos-1)
        naively_assign(current_node.right, current_pos+1)
    

    naively_assign(bst.root, 0)

    def eliminate_overlap(current_node: Node):
        """Recursively shifts the tree to eliminate overlaps and enforce a minimum horizontal distance between nodes from the bottom up"""
        if current_node is None:
            return
        
        eliminate_overlap(current_node.left)
        eliminate_overlap(current_node.right)

        def compute_rightmost_or_leftmost(current_node: Node, depth: int, depth_dict: dict, rightmost: bool):
            """Calculates and stores either the rightmost or leftmost position in a given subtree for every depth level"""
            if current_node is None:
                return
            
            operator = max if rightmost else min
            if depth in depth_dict.keys():
                depth_dict[depth] = operator(depth_dict[depth], relative_positions[current_node])
            else:
                depth_dict[depth] = relative_positions[current_node]

            compute_rightmost_or_leftmost(current_node.left, depth+1, depth_dict, rightmost)
            compute_rightmost_or_leftmost(current_node.right, depth+1, depth_dict, rightmost)

        
        rightmost_in_left, leftmost_in_right = {}, {}
        compute_rightmost_or_leftmost(current_node.left, 0, rightmost_in_left, True)
        compute_rightmost_or_leftmost(current_node.right, 0, leftmost_in_right, False)

        overlap_given_depth = {
            depth: rightmost_in_left[depth] - leftmost_in_right[depth] 
            for depth in set(rightmost_in_left.keys()).intersection(leftmost_in_right.keys())
        }

        if len(overlap_given_depth) == 0:
            return

        amount_to_shift = max(overlap_given_depth.values()) / 2 + 1
        
        def shift_subtree(current_node: Node, amount_to_shift: int):
            """Shifts the entire subtree rooted at the given node to the right by some given amount (could be negative)"""
            if current_node is None:
                return
            
            relative_positions[current_node] += amount_to_shift
            shift_subtree(current_node.left, amount_to_shift)
            shift_subtree(current_node.right, amount_to_shift)
        

        shift_subtree(current_node.left, -amount_to_shift)
        shift_subtree(current_node.right, amount_to_shift)
    

    eliminate_overlap(bst.root)

    def get_depth(current_node: Node):
        """Returns the depth of the current subtree"""
        if current_node is None:
            return 0
        return 1 + max(get_depth(current_node.left), get_depth(current_node.right))


    num_cols = max(relative_positions.values()) - min(relative_positions.values()) + 1
    horiz_increment = width / (num_cols+1)
    vert_increment = height / (get_depth(bst.root)+1)
    scale_factor = min(horiz_increment, vert_increment)
    radius = scale_factor * 0.375
    minimum_position = min(relative_positions.values())

    circles = {}

    def get_circles(current_node: Node, depth: int):
        """Converts the relative horizontal coordinates to circle objects in the canvas"""
        if current_node is None:
            return

        x_coord = left + (relative_positions[current_node] - minimum_position + 1)*horiz_increment
        y_coord = top - (depth+1)*vert_increment

        circles[current_node] = Group(
            Circle(radius=radius, color=BLUE, stroke_width=scale_factor*3).set_fill(BLACK, opacity=1),
            Text(str(current_node.key), font_size=scale_factor*20)
        ).move_to(RIGHT*x_coord + UP*y_coord)

        get_circles(current_node.left, depth+1)
        get_circles(current_node.right, depth+1)
    

    get_circles(bst.root, 0)

    arrows = {}

    def get_arrows(current_node: Node):
        """Creates arrow objects in the canvas mapping from circle center to circle center"""
        if current_node is None:
            return
        
        for child in [n for n in [current_node.left, current_node.right] if n is not None]:
            arrows[child] = Line(
                circles[current_node].get_center(), 
                circles[child].get_center(),
                buff=0,
                stroke_width=scale_factor*3,
                z_index=-10
            )
        
        get_arrows(current_node.left)
        get_arrows(current_node.right)
    

    get_arrows(bst.root)

    return arrows, circles, scale_factor
