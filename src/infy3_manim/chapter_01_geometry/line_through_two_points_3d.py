
from manim import *
import numpy as np


class LineThroughTwoPoints3D(ThreeDScene):
    def construct(self):
        # ---------------------------------
        # Hebrew text helper
        # ---------------------------------
        def hebrew(text, size=30, color=WHITE):
            return Text(
                text,
                font="Arial",
                font_size=size,
                color=color,
            )

        # ---------------------------------
        # 3D camera and axes
        # ---------------------------------
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.85,
        )

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 5, 1],
            x_length=7,
            y_length=6,
            z_length=5,
        )

        # ---------------------------------
        # Points and direction vector
        # ---------------------------------
        a = np.array([-2.0, -1.0, 0.0])
        b = np.array([2.0, 1.0, 2.0])
        direction = b - a

        point_a = Dot3D(
            axes.c2p(*a),
            color=BLUE,
            radius=0.075,
        )

        point_b = Dot3D(
            axes.c2p(*b),
            color=GREEN,
            radius=0.075,
        )

        label_a = MathTex("A", color=BLUE).scale(0.8)
        label_b = MathTex("B", color=GREEN).scale(0.8)

        label_a.move_to(axes.c2p(*a) + LEFT * 0.35)
        label_b.move_to(axes.c2p(*b) + RIGHT * 0.35)

        self.add_fixed_orientation_mobjects(label_a, label_b)

        # ---------------------------------
        # Segment and entire line
        # ---------------------------------
        segment = Line3D(
            axes.c2p(*a),
            axes.c2p(*b),
            color=YELLOW,
            thickness=0.035,
        )

        full_line = Line3D(
            axes.c2p(*(a - 0.65 * direction)),
            axes.c2p(*(a + 1.65 * direction)),
            color=ORANGE,
            thickness=0.035,
        )

        # ---------------------------------
        # Moving point P(t)
        # ---------------------------------
        t = ValueTracker(0)

        moving_point = always_redraw(
            lambda: Dot3D(
                axes.c2p(*(a + t.get_value() * direction)),
                color=RED,
                radius=0.09,
            )
        )

        # ---------------------------------
        # Hebrew text and mathematical text
        # ---------------------------------
        title = hebrew(
            "הישר העובר דרך שתי נקודות במרחב",
            size=34,
        ).to_edge(UP)

        explanation_1 = hebrew(
            "שתי נקודות קובעות ישר יחיד",
            size=28,
        ).to_edge(DOWN)

        explanation_2 = hebrew(
            "בין שתי הנקודות מתקבל קטע",
            size=28,
        ).to_edge(DOWN)

        explanation_3 = hebrew(
            "ממשיכים מעבר לנקודות ומקבלים ישר שלם",
            size=28,
        ).to_edge(DOWN)

        explanation_4 = hebrew(
            "הפרמטר קובע את המיקום על הישר",
            size=28,
        ).to_edge(DOWN)

        formula_segment = MathTex(
            r"P(t)=A+t(B-A),\quad 0\le t\le 1",
            font_size=34,
        ).to_corner(UL).shift(DOWN * 0.65)

        formula_line = MathTex(
            r"\ell=\{A+t(B-A)\mid t\in\mathbb{R}\}",
            font_size=34,
        ).to_corner(UL).shift(DOWN * 0.65)

        vector_formula = MathTex(
            r"B-A",
            color=YELLOW,
            font_size=40,
        ).to_corner(UR).shift(DOWN * 0.65)

        # Keep all explanations fixed on the screen
        
        # Keep text fixed on the screen
        fixed_texts = [
            title,
            explanation_1,
            explanation_2,
            explanation_3,
            explanation_4,
            formula_segment,
            formula_line,
            vector_formula,
        ]

        self.add_fixed_in_frame_mobjects(*fixed_texts)

        # Hide initially without changing opacity.
        # FadeIn will reveal each object when needed.
        self.remove(*fixed_texts)


        # ---------------------------------
        # Scene 1: Points and axes
        # ---------------------------------
        self.play(Create(axes), run_time=2)

        self.play(
            FadeIn(title),
            FadeIn(point_a),
            FadeIn(point_b),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=2,
        )

        self.play(FadeIn(explanation_1))
        self.wait(1.5)

        # ---------------------------------
        # Scene 2: Segment AB
        # ---------------------------------
        self.play(
            Create(segment),
            FadeIn(vector_formula),
            run_time=2,
        )

        self.play(
            FadeOut(explanation_1),
            FadeIn(explanation_2),
            FadeIn(formula_segment),
        )

        self.add(moving_point)

        self.play(
            t.animate.set_value(1),
            run_time=4,
            rate_func=linear,
        )
        self.wait(1)

        self.play(
            t.animate.set_value(0),
            run_time=3,
            rate_func=linear,
        )
        self.wait(1)

        # ---------------------------------
        # Scene 3: Extend to the full line
        # ---------------------------------
        self.play(
            FadeOut(explanation_2),
            FadeIn(explanation_3),
            FadeOut(formula_segment),
            FadeIn(formula_line),
            FadeOut(vector_formula),
            run_time=1.5,
        )

        self.play(
            ReplacementTransform(segment, full_line),
            run_time=3,
        )

        # t < 0: before A
        self.play(
            t.animate.set_value(-0.5),
            run_time=3,
            rate_func=linear,
        )

        self.wait(0.5)

        # t > 1: beyond B
        self.play(
            t.animate.set_value(1.5),
            run_time=5,
            rate_func=linear,
        )

        # ---------------------------------
        # Scene 4: Rotate camera
        # ---------------------------------
        self.play(
            FadeOut(explanation_3),
            FadeIn(explanation_4),
        )

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        self.wait(1)
