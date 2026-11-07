from manim import *
import numpy as np
from bidi.algorithm import get_display

# --------------------------------------------------
# Helper for Hebrew text (David font + RTL handling)
# --------------------------------------------------



def hebrew_text(txt, font_size=30, color=WHITE):
    return Text(
        get_display(txt),
        font="David",
        font_size=font_size,
        color=color,
    )



class SphericalCoordinatesDefinition(ThreeDScene):
    def construct(self):
        # -----------------------------
        # Camera
        # -----------------------------
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.9,
        )

        # -----------------------------
        # Parameters of the point x
        # -----------------------------
        r_val = 2.8
        vartheta = 40 * DEGREES   # azimuth in xy-plane
        theta2 = 55 * DEGREES     # polar angle from positive z-axis

        x_val = r_val * np.sin(theta2) * np.cos(vartheta)
        y_val = r_val * np.sin(theta2) * np.sin(vartheta)
        z_val = r_val * np.cos(theta2)

        X_coords = np.array([x_val, y_val, z_val])
        P_coords = np.array([x_val, y_val, 0.0])
        O_coords = np.array([0.0, 0.0, 0.0])

        # -----------------------------
        # Axes and sphere
        # -----------------------------
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-1, 4, 1],
            x_length=7,
            y_length=7,
            z_length=5,
        )

        sphere = Surface(
            lambda u, v: np.array([
                r_val * np.cos(u) * np.cos(v),
                r_val * np.cos(u) * np.sin(v),
                r_val * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(20, 30),
            fill_opacity=0.20,
            checkerboard_colors=[BLUE_E, BLUE_D],
            stroke_color=BLUE_A,
            stroke_opacity=0.35,
        )

        # plane z = 0
        xy_plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-3.5, 3.5],
            v_range=[-3.5, 3.5],
            resolution=(2, 2),
            fill_opacity=0.12,
            checkerboard_colors=[GREY_BROWN, GREY_BROWN],
            stroke_opacity=0.0,
        )

        # -----------------------------
        # Points and lines
        # -----------------------------
        O = Dot3D(O_coords, color=WHITE, radius=0.06)
        X = Dot3D(X_coords, color=RED, radius=0.08)
        P = Dot3D(P_coords, color=YELLOW, radius=0.07)

        radius_line = Line3D(O_coords, X_coords, color=RED, thickness=0.03)
        proj_line = Line3D(O_coords, P_coords, color=YELLOW, thickness=0.025)
        vertical_line = DashedLine(P_coords, X_coords, color=GREY_B, dash_length=0.12)

        # z-axis direction line for angle illustration
        z_axis_segment = Line3D(O_coords, np.array([0, 0, 2.0]), color=GREY_A, thickness=0.02)

        # -----------------------------
        # Angle arcs
        # -----------------------------
        # Arc for vartheta in xy-plane
        arc_radius_xy = 0.9
        azimuth_arc = ParametricFunction(
            lambda t: np.array([
                arc_radius_xy * np.cos(t),
                arc_radius_xy * np.sin(t),
                0
            ]),
            t_range=[0, vartheta],
            color=GREEN,
            stroke_width=5,
        )

        # Arc for theta2 in plane spanned by z-axis and OP
        u_xy = P_coords / np.linalg.norm(P_coords)
        k_vec = np.array([0, 0, 1.0])
        arc_radius_polar = 1.1

        polar_arc = ParametricFunction(
            lambda t: arc_radius_polar * (np.sin(t) * u_xy + np.cos(t) * k_vec),
            t_range=[0, theta2],
            color=ORANGE,
            stroke_width=5,
        )

        # -----------------------------
        # Labels in 3D
        # -----------------------------
        label_O = MathTex("0").scale(0.7).move_to(O_coords + np.array([-0.25, -0.2, 0]))
        label_X = MathTex("x").scale(0.8).set_color(RED).move_to(X_coords + np.array([0.2, 0.15, 0.15]))
        label_P = MathTex(r"\mathrm{proj}_{xy}(x)").scale(0.65).set_color(YELLOW).move_to(P_coords + np.array([0.4, -0.1, -0.1]))
        label_r = MathTex("r").scale(0.8).set_color(RED).move_to((O_coords + X_coords) / 2 + np.array([0.25, 0.2, 0.1]))
        label_theta = MathTex(r"\theta_2").scale(0.8).set_color(ORANGE).move_to(
            arc_radius_polar * (np.sin(theta2 / 2) * u_xy + np.cos(theta2 / 2) * k_vec) + np.array([0.2, 0.0, 0.0])
        )
        label_vartheta = MathTex(r"\vartheta").scale(0.8).set_color(GREEN).move_to(
            np.array([
                1.15 * np.cos(vartheta / 2),
                1.15 * np.sin(vartheta / 2),
                0
            ]) + np.array([0.0, -0.1, 0.0])
        )

        self.add_fixed_orientation_mobjects(
            label_O, label_X, label_P, label_r, label_theta, label_vartheta
        )

        # -----------------------------
        # Fixed text panels
        # -----------------------------
        title = hebrew_text("הצגה כדורית — המחשה ב־ℝ³ והכללה ל־ℝᵏ", 34)
        title.to_edge(UP)

        step1 = hebrew_text("ניקח נקודה x במרחב ונרצה לתאר אותה באמצעות מרחק وزוויות", 26)
        step1.to_edge(DOWN)

        step2 = hebrew_text("r הוא המרחק של x מן הראשית", 28)
        step2.to_edge(DOWN)

        step3 = hebrew_text("ϑ היא הזווית של ההיטל של x על מישור xy", 28)
        step3.to_edge(DOWN)

        step4 = hebrew_text("θ₂ היא הזווית מן הציר z החיובי אל הווקטור x", 28)
        step4.to_edge(DOWN)

        step5 = hebrew_text("מכאן מתקבלות הקואורדינטות הקרטזיות של x", 28)
        step5.to_edge(DOWN)

        step6 = hebrew_text("ב־ℝᵏ חוזרים על אותו רעיון רקורסיבית", 28)
        step6.to_edge(DOWN)

        formula_3d = MathTex(
            r"""
            a_1=r\sin(\theta_2)\cos(\vartheta),\quad
            a_2=r\sin(\theta_2)\sin(\vartheta),\quad
            a_3=r\cos(\theta_2)
            """
        ).scale(0.75)
        formula_3d.to_corner(UL).shift(0.4 * DOWN)

        
        general_box = VGroup(
            hebrew_text("הדפוס הכללי במרחב מממד k", 28),

            MathTex(
                r"a_k=r\cos(\theta_{k-1})"
            ).scale(0.75),

            hebrew_text(
                "אורך ההיטל על תת המרחב הראשון",
                25
            ),

            MathTex(
                r"r_{k-1}=r\sin(\theta_{k-1})"
            ).scale(0.75),

            MathTex(
                r"a_{k-1}=r\sin(\theta_{k-1})\cos(\theta_{k-2})"
            ).scale(0.75),

            hebrew_text(
                "ממשיכים באופן דומה עד שני הרכיבים הראשונים",
                25
            ),

            MathTex(
                r"a_1=r\sin(\theta_{k-1})\cdots"
                r"\sin(\theta_2)\cos(\theta_1)"
            ).scale(0.75),

            MathTex(
                r"a_2=r\sin(\theta_{k-1})\cdots"
                r"\sin(\theta_2)\sin(\theta_1)"
            ).scale(0.75),

        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)


        general_panel = SurroundingRectangle(general_box, color=BLUE_B, buff=0.2, corner_radius=0.15)
        general_group = VGroup(general_panel, general_box)
        general_group.scale(0.85)
        general_group.to_corner(UL).shift(0.4 * DOWN)

        self.add_fixed_in_frame_mobjects(
            title, step1, step2, step3, step4, step5, step6, formula_3d, general_group
        )

        # Hide fixed texts initially
        for mob in [title, step1, step2, step3, step4, step5, step6, formula_3d, general_group]:
            mob.set_opacity(0)

        # -----------------------------
        # Animation
        # -----------------------------
        self.play(Create(axes), FadeIn(title), run_time=2)
        self.play(FadeIn(step1), run_time=1)
        self.play(FadeIn(xy_plane), run_time=1.5)
        self.play(Create(sphere), run_time=2)
        self.play(FadeIn(O), FadeIn(X), FadeIn(label_O), FadeIn(label_X), run_time=1.5)
        self.wait(1)

        # Show radius r
        self.play(FadeOut(step1), FadeIn(step2), run_time=0.7)
        self.play(Create(radius_line), FadeIn(label_r), run_time=2)
        self.wait(1.5)

        # Projection to xy-plane and azimuth
        self.play(FadeOut(step2), FadeIn(step3), run_time=0.7)
        self.play(FadeIn(P), FadeIn(label_P), Create(proj_line), Create(vertical_line), run_time=2)
        self.play(Create(azimuth_arc), FadeIn(label_vartheta), run_time=1.5)
        self.wait(2)

        # Polar angle
        self.play(FadeOut(step3), FadeIn(step4), run_time=0.7)
        self.play(Create(z_axis_segment), run_time=1)
        self.play(Create(polar_arc), FadeIn(label_theta), run_time=1.5)
        self.wait(2)

        # 3D formulas
        self.play(FadeOut(step4), FadeIn(step5), run_time=0.7)
        self.play(FadeIn(formula_3d), run_time=1.5)
        self.wait(3)

        # Generalization
        self.play(FadeOut(step5), FadeIn(step6), run_time=0.7)
        self.play(FadeOut(formula_3d), FadeIn(general_group), run_time=1.5)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        self.wait(2)