from manim import *
import numpy as np


def make_axes_centered(x_range=(-4, 4), y_range=(-2, 10)):
    """Create axes without LaTeX numbers."""
    return Axes(
        x_range=[x_range[0], x_range[1], 1],
        y_range=[y_range[0], y_range[1], 2],
        x_length=8,
        y_length=5,
        axis_config={"include_numbers": False},
    ).scale(0.9)


class ParabolasLesson(Scene):
    """A comprehensive lesson on parabolas with animations and vector flow."""

    def construct(self):
        # ========== SECTION 1: DEFINITION ==========
        title = Text("Parabolas", font_size=56, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        definition = Text(
            "1. Definition",
            font_size=40,
            weight=BOLD,
        ).to_edge(UP).shift(DOWN * 0.5)
        self.play(ReplacementTransform(title, definition))
        self.wait(0.5)

        def_text = Text(
            "A parabola is the graph of a quadratic function.",
            font_size=32,
        ).next_to(definition, DOWN, buff=0.4)
        self.play(Write(def_text))
        self.wait(1)

        quad_form = Text(
            "y = ax² + bx + c    (where a ≠ 0)",
            font_size=36,
            color=YELLOW,
        ).next_to(def_text, DOWN, buff=0.5)
        self.play(Write(quad_form))
        self.wait(2)

        self.play(FadeOut(definition), FadeOut(def_text), FadeOut(quad_form))
        self.wait(0.5)

        # ========== SECTION 2: STANDARD FORM ==========
        section2 = Text("2. Standard Form", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(section2))
        self.wait(0.5)

        simple_form = Text(
            "The simplest quadratic: y = x²",
            font_size=32,
        ).next_to(section2, DOWN, buff=0.4)
        self.play(Write(simple_form))
        self.wait(1)

        axes = make_axes_centered((-3, 3), (0, 10))
        axes.to_edge(DOWN, buff=0.3)
        labels = axes.get_axis_labels(
            x_label=Text("x", font_size=24),
            y_label=Text("y", font_size=24),
        )

        curve = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2.5, 2.5])
        curve_label = Text("y = x²", font_size=28).next_to(curve, UP, buff=0.3).set_color(BLUE)

        self.play(Create(axes), Create(labels), run_time=1)
        self.play(Create(curve), Write(curve_label), run_time=1.5)
        self.wait(1)

        # U-shape and vertex
        u_arrow = Arrow(
            axes.coords_to_point(-1.5, 2.25),
            axes.coords_to_point(1.5, 2.25),
            color=GREEN,
            buff=0.1,
        )
        u_label = Text("U-shape, opens upward", font_size=24).next_to(u_arrow, UP).set_color(GREEN)
        self.play(GrowArrow(u_arrow), Write(u_label))
        self.wait(1)

        vertex_dot = Dot(axes.coords_to_point(0, 0), color=RED, radius=0.12)
        vertex_label = Text("Vertex at (0, 0)", font_size=24).next_to(vertex_dot, DOWN).set_color(RED)
        self.play(Create(vertex_dot), Write(vertex_label))
        self.wait(1)

        # Axis of symmetry
        axis_line = DashedLine(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(0, 9),
            color=YELLOW,
            stroke_width=3,
        )
        sym_label = Text("Axis of symmetry: x = 0", font_size=24).to_edge(RIGHT).set_color(YELLOW)
        self.play(Create(axis_line), Write(sym_label))
        self.wait(2)

        self.play(
            FadeOut(section2),
            FadeOut(simple_form),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(curve),
            FadeOut(curve_label),
            FadeOut(u_arrow),
            FadeOut(u_label),
            FadeOut(vertex_dot),
            FadeOut(vertex_label),
            FadeOut(axis_line),
            FadeOut(sym_label),
        )
        self.wait(0.5)

        # ========== SECTION 3: KEY FEATURES ==========
        section3 = Text("3. Key Features of a Parabola", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(section3))
        self.wait(1)

        axes = make_axes_centered((-3, 3), (-1, 10))
        axes.to_edge(DOWN, buff=0.2).scale(0.85)
        curve = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2.5, 2.5])
        self.add(axes, curve)

        # (i) Vertex
        vertex_title = Text("(i) Vertex", font_size=32, weight=BOLD, color=RED).to_edge(UP).shift(DOWN * 0.8)
        vertex_desc = Text(
            "The turning point. Min if opens up, Max if opens down.",
            font_size=24,
        ).next_to(vertex_title, DOWN)
        vertex_dot = Dot(axes.coords_to_point(0, 0), color=RED, radius=0.15)
        self.play(Write(vertex_title), Write(vertex_desc), Create(vertex_dot))
        self.wait(2)

        self.play(FadeOut(vertex_title), FadeOut(vertex_desc), FadeOut(vertex_dot))

        # (ii) Axis of symmetry
        axis_title = Text("(ii) Axis of Symmetry", font_size=32, weight=BOLD, color=YELLOW).to_edge(UP).shift(DOWN * 0.8)
        axis_desc = Text(
            "Vertical line through vertex. Divides parabola into two equal halves.",
            font_size=24,
        ).next_to(axis_title, DOWN)
        axis_line = DashedLine(
            axes.coords_to_point(0, -0.5),
            axes.coords_to_point(0, 9),
            color=YELLOW,
            stroke_width=4,
        )
        self.play(Write(axis_title), Write(axis_desc), Create(axis_line))
        self.wait(2)

        self.play(FadeOut(axis_title), FadeOut(axis_desc), FadeOut(axis_line))

        # (iii) Direction of opening - show a>0 and a<0
        dir_title = Text("(iii) Direction of Opening", font_size=32, weight=BOLD, color=GREEN).to_edge(UP).shift(DOWN * 0.8)
        dir_desc = Text("a > 0: opens upward    |    a < 0: opens downward", font_size=24).next_to(dir_title, DOWN)

        curve_up = axes.plot(lambda x: x**2, color=GREEN, x_range=[-2.5, 2.5])
        curve_down = axes.plot(lambda x: -x**2 + 4, color=RED, x_range=[-2.5, 2.5])

        self.play(Write(dir_title), Write(dir_desc))
        self.play(Transform(curve, curve_up), run_time=0.5)
        self.wait(1)
        self.play(Transform(curve, curve_down), run_time=0.5)
        self.wait(1)
        self.play(Transform(curve, curve_up), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(dir_title), FadeOut(dir_desc))

        # (iv) Width - show different |a| values
        width_title = Text("(iv) Width of the Parabola", font_size=32, weight=BOLD, color=PURPLE).to_edge(UP).shift(DOWN * 0.8)
        width_desc = Text("Larger |a| = narrower    |    Smaller |a| = wider", font_size=24).next_to(width_title, DOWN)

        curve_narrow = axes.plot(lambda x: 2 * x**2, color=PURPLE, x_range=[-2, 2])
        curve_wide = axes.plot(lambda x: 0.3 * x**2, color=TEAL, x_range=[-2.5, 2.5])

        self.play(Write(width_title), Write(width_desc))
        self.play(Transform(curve, curve_narrow), run_time=1)
        self.wait(1)
        self.play(Transform(curve, curve_wide), run_time=1)
        self.wait(1)
        self.play(Transform(curve, curve_up), run_time=1)
        self.wait(1)

        self.play(
            FadeOut(section3),
            FadeOut(width_title),
            FadeOut(width_desc),
            FadeOut(axes),
            FadeOut(curve),
        )
        self.wait(0.5)

        # ========== SECTION 4: VERTEX FORM ==========
        section4 = Text("4. Vertex Form", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(section4))
        self.wait(0.5)

        vertex_form = Text(
            "y = a(x - h)² + k",
            font_size=44,
            color=YELLOW,
        ).next_to(section4, DOWN, buff=0.5)
        vertex_point = Text("Vertex is at the point (h, k)", font_size=32).next_to(vertex_form, DOWN)
        self.play(Write(vertex_form), Write(vertex_point))
        self.wait(2)

        self.play(FadeOut(section4), FadeOut(vertex_form), FadeOut(vertex_point))

        # ========== SECTION 5: EXAMPLE ==========
        section5 = Text("5. Example", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(section5))
        self.wait(0.5)

        example_eq = Text(
            "y = (x - 2)² + 3",
            font_size=40,
            color=BLUE,
        ).next_to(section5, DOWN, buff=0.4)
        self.play(Write(example_eq))
        self.wait(1)

        axes = make_axes_centered((-1, 5), (-1, 10))
        axes.to_edge(DOWN, buff=0.2).scale(0.9)
        labels = axes.get_axis_labels(
            x_label=Text("x", font_size=24),
            y_label=Text("y", font_size=24),
        )

        def example_func(x):
            return (x - 2) ** 2 + 3

        curve = axes.plot(example_func, color=BLUE, x_range=[-0.5, 4.5])
        self.play(Create(axes), Create(labels), Create(curve))
        self.wait(1)

        # Vertex at (2, 3)
        vertex = axes.coords_to_point(2, 3)
        vertex_dot = Dot(vertex, color=RED, radius=0.15)
        vertex_label = Text("Vertex (2, 3)", font_size=28).next_to(vertex_dot, UR).set_color(RED)
        self.play(Create(vertex_dot), Write(vertex_label))
        self.wait(1)

        # Axis of symmetry x = 2
        axis_line = DashedLine(
            axes.coords_to_point(2, 0),
            axes.coords_to_point(2, 9),
            color=YELLOW,
            stroke_width=3,
        )
        axis_label = Text("Axis: x = 2", font_size=24).next_to(axis_line, RIGHT).set_color(YELLOW)
        self.play(Create(axis_line), Write(axis_label))
        self.wait(1)

        # Vector flow - arrows showing upward direction
        flow_arrow1 = Arrow(
            axes.coords_to_point(2, 3),
            axes.coords_to_point(2, 6),
            color=GREEN,
            buff=0.1,
        )
        flow_arrow2 = Arrow(
            axes.coords_to_point(2, 3),
            axes.coords_to_point(2, 7.5),
            color=GREEN,
            buff=0.1,
        )
        a_positive = Text("a = 1 > 0 → opens upward", font_size=24).to_edge(DOWN).set_color(GREEN)
        self.play(GrowArrow(flow_arrow1), GrowArrow(flow_arrow2), Write(a_positive))
        self.wait(2)

        self.play(
            FadeOut(flow_arrow1),
            FadeOut(flow_arrow2),
            FadeOut(a_positive),
        )
        self.wait(0.5)

        # ========== SUMMARY ==========
        self.play(
            FadeOut(section5),
            FadeOut(example_eq),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(curve),
            FadeOut(vertex_dot),
            FadeOut(vertex_label),
            FadeOut(axis_line),
            FadeOut(axis_label),
        )

        summary_title = Text("Summary", font_size=48, weight=BOLD).to_edge(UP)
        self.play(Write(summary_title))
        self.wait(0.5)

        bullets = VGroup(
            Text("• A parabola is the graph of a quadratic function.", font_size=28),
            Text("• It has a vertex (turning point) and axis of symmetry.", font_size=28),
            Text("• Shape and direction depend on the coefficient of x².", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(summary_title, DOWN, buff=0.6)

        for bullet in bullets:
            self.play(Write(bullet), run_time=0.8)
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)


class ExponentialLesson(Scene):
    """Lesson on exponential growth and decay."""

    def construct(self):
        # ========== SECTION 1: WHAT IS EXPONENTIAL CHANGE? ==========
        title = Text("Exponential Change", font_size=56, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        def_text = Text(
            "Exponential change: quantity increases/decreases by a constant PERCENTAGE,",
            font_size=28,
        ).next_to(title, DOWN, buff=0.5)
        def_text2 = Text(
            "not a constant amount. Different from linear change.",
            font_size=28,
        ).next_to(def_text, DOWN)
        self.play(Write(def_text), Write(def_text2))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(def_text), FadeOut(def_text2))

        # ========== SECTION 2: EXPONENTIAL GROWTH ==========
        growth_title = Text("2. Exponential Growth", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(growth_title))
        self.wait(0.5)

        formula = Text(
            "y = a(1 + r)^t",
            font_size=40,
            color=GREEN,
        ).next_to(growth_title, DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait(0.5)

        vars_text = VGroup(
            Text("a = starting amount", font_size=24),
            Text("r = growth rate", font_size=24),
            Text("t = time", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=0.5)
        self.play(Write(vars_text))
        self.wait(1)

        examples = Text(
            "Examples: Population, Bacteria, Compound Interest",
            font_size=24,
        ).next_to(vars_text, DOWN, buff=0.4)
        self.play(Write(examples))
        self.wait(1)

        # Growth graph
        axes = make_axes_centered((0, 6), (0, 8))
        axes.to_edge(DOWN, buff=0.3)
        growth_curve = axes.plot(
            lambda x: 0.5 * (1.5) ** x,
            color=GREEN,
            x_range=[0, 5.5],
        )
        curve_label = Text("Starts slowly, then rises faster", font_size=24).next_to(growth_curve, UR).set_color(GREEN)
        self.play(Create(axes), Create(growth_curve), Write(curve_label))
        self.wait(2)

        self.play(
            FadeOut(growth_title),
            FadeOut(formula),
            FadeOut(vars_text),
            FadeOut(examples),
            FadeOut(axes),
            FadeOut(growth_curve),
            FadeOut(curve_label),
        )

        # ========== SECTION 3: EXPONENTIAL DECAY ==========
        decay_title = Text("3. Exponential Decay", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(decay_title))
        self.wait(0.5)

        decay_formula = Text(
            "y = a(1 - r)^t",
            font_size=40,
            color=RED,
        ).next_to(decay_title, DOWN, buff=0.4)
        self.play(Write(decay_formula))
        self.wait(0.5)

        decay_examples = Text(
            "Examples: Radioactive decay, Cooling, Depreciation",
            font_size=24,
        ).next_to(decay_formula, DOWN)
        self.play(Write(decay_examples))
        self.wait(1)

        # Decay graph
        axes = make_axes_centered((0, 6), (0, 5))
        axes.to_edge(DOWN, buff=0.3)
        decay_curve = axes.plot(
            lambda x: 4 * (0.5) ** x,
            color=RED,
            x_range=[0, 5.5],
        )
        decay_label = Text("Drops quickly, then levels off", font_size=24).next_to(decay_curve, UR).set_color(RED)
        self.play(Create(axes), Create(decay_curve), Write(decay_label))
        self.wait(2)

        self.play(
            FadeOut(decay_title),
            FadeOut(decay_formula),
            FadeOut(decay_examples),
            FadeOut(axes),
            FadeOut(decay_curve),
            FadeOut(decay_label),
        )

        # ========== SECTION 4: KEY IDEA ==========
        key_title = Text("4. Key Idea", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(key_title))
        self.wait(0.5)

        key_bullets = VGroup(
            Text("• Growth curves bend UPWARDS", font_size=28, color=GREEN),
            Text("• Decay curves bend DOWNWARDS", font_size=28, color=RED),
            Text("• The change becomes more dramatic over time", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(key_title, DOWN, buff=0.6)

        for bullet in key_bullets:
            self.play(Write(bullet), run_time=0.8)
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)


class DerivativeExplanation(Scene):
    """Original derivative explanation scene (kept for reference)."""

    def construct(self):
        def func(x):
            return x**2

        axes = make_axes_centered((-3, 3), (0, 10))
        axes.to_edge(UP + LEFT, buff=0.5)
        labels = axes.get_axis_labels(
            x_label=Text("x", font_size=28),
            y_label=Text("f(x)", font_size=28),
        )
        curve = axes.plot(func, color=BLUE)
        function_label = Text("f(x) = x²", font_size=36).next_to(curve, UP, buff=0.5).set_color(BLUE)

        self.play(Create(axes), Create(labels), Create(curve), Write(function_label))
        self.wait(1)

        x1, x2 = 1.0, 1.7
        p1 = axes.coords_to_point(x1, func(x1))
        p2 = axes.coords_to_point(x2, func(x2))
        dot1 = Dot(p1, color=RED).scale(0.7)
        dot2 = Dot(p2, color=GREEN).scale(0.7)
        secant_line = Line(p1, p2, color=YELLOW)

        self.play(Create(dot1), Create(dot2), Create(secant_line))
        self.wait(0.5)

        delta_x_val = x2 - x1
        dx_text = Text("Δx", font_size=28).next_to(secant_line, DOWN, buff=0.1).set_color(RED_C)
        dy_text = Text("Δy", font_size=28).next_to(secant_line, RIGHT, buff=0.1).set_color(GREEN_C)
        self.play(Write(dx_text), Write(dy_text))
        self.wait(1)
        self.play(FadeOut(dx_text), FadeOut(dy_text))

        title = Text("The Derivative: Limit of the Slope").to_edge(UP).set_color(WHITE)
        self.play(ReplacementTransform(function_label, title))
        self.wait(1)

        slope_formula = Text("Slope = m = Δy/Δx = (f(x+h) - f(x))/h", font_size=28).to_edge(DOWN)
        self.play(Write(slope_formula))
        self.wait(1.5)

        num_steps = 15
        for i in range(num_steps):
            new_x2 = x1 + delta_x_val * (1 - (i + 1) / num_steps)
            new_p2 = axes.coords_to_point(new_x2, func(new_x2))
            dot2.target = Dot(new_p2, color=GREEN).scale(0.7)
            new_secant_line = Line(p1, new_p2, color=YELLOW)
            self.play(
                Transform(secant_line, new_secant_line),
                MoveToTarget(dot2),
                run_time=0.2,
            )

        self.wait(1)
        self.play(FadeOut(dot2), FadeOut(dot1), FadeOut(secant_line))

        tangent_slope = 2 * x1
        p2_tangent = axes.coords_to_point(x1 + 1, func(x1) + tangent_slope)
        direction = p2_tangent - p1
        direction = direction / np.linalg.norm(direction)
        tangent_line = Line(
            p1 - 3 * direction,
            p1 + 3 * direction,
            color=YELLOW_A,
            stroke_width=5,
        )
        tangent_label = Text("f'(x) = lim[Δx→0] Δy/Δx", font_size=28).next_to(slope_formula, UP, buff=0.5).set_color(YELLOW_A)
        self.play(Create(tangent_line), Transform(slope_formula, tangent_label))

        final_derivative_val = Text(
            "At x=1, the derivative is f'(1) = 2",
            font_size=28,
        ).next_to(tangent_line, DOWN, buff=1).set_color(YELLOW_A)
        self.play(Write(final_derivative_val))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
