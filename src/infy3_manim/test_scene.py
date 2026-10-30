
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle(radius=1.5, color=BLUE)
        dot = Dot(color=YELLOW)

        self.play(Create(circle))
        self.play(FadeIn(dot))
        self.play(dot.animate.shift(RIGHT * 2))
        self.wait(1)
