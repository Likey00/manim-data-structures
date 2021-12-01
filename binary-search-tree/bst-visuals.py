from manim import *
from bst import BST
from get_bst import get_bst
from random import sample

class DrawOneBST(Scene):
    def construct(self):
        arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
        self.add(*arrows.values(), *circles.values())

