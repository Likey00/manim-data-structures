from manim import *
from bst import BST
from get_bst import get_bst
from insert_bst import insert_bst
from random import sample

class DrawOneBST(Scene):
    """Draws one binary search tree of 30 random numbers"""
    def construct(self):
        arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
        self.add(*arrows.values(), *circles.values())


class DrawManyBSTs(Scene):
    """Draws many binary search trees, transitioning between them"""
    def construct(self):
        arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
        full_bst = Group(*arrows.values(), *circles.values())
        self.add(full_bst)
        self.wait()

        for i in range(30):
            arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
            new_bst = Group(*arrows.values(), *circles.values())
            self.play(Transform(full_bst, new_bst))
            self.wait()


class InsertOneElement(Scene):
    """Inserts a random element to a random BST of size 30"""
    def construct(self):
        random_list = sample(range(100), 31)
        insert_bst(self, BST(random_list[:-1]), random_list[-1])


class InsertAllElements(Scene):
    """Builds a BST with a random list of elements"""
    def construct(self):
        random_list = sample(range(100), 30)
        bst = BST([random_list[0]])

        for num in random_list[1:]:
            to_remove = insert_bst(self, bst, num)
            self.remove(*to_remove)
