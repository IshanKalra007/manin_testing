"""
manim-Astronomy Plugin Example
=============================
Uses the manim-Astronomy plugin for astronomical visualizations.
Requires OpenGL renderer for 3D scenes.

Run with:
    manim render AstronomyExample.py SimpleOrbit -ql --renderer opengl
    manim render AstronomyExample.py KeplersSecondLaw -ql --renderer opengl
"""

from manim import *
import numpy as np
from manim_Astronomy.stellar_objects import Planet, Star

# OpenGL renderer is required for 3D celestial objects (Star, Planet, SpaceTimeFabric)
config.renderer = "opengl"


class SimpleOrbit(ThreeDScene):
    """Simple planet orbiting a star - quick demo of the plugin."""

    def construct(self):
        star = Star(radius=0.8, size_of_particle=0.001, colors=[YELLOW])
        self.add(star)

        planet = Planet(center=[2, 0, 0], radius=0.08)
        self.add(planet)

        # Elliptical orbit path
        orbit = ParametricFunction(
            lambda t: np.array([2.5 * np.cos(t), 1.5 * np.sin(t), 0]),
            t_range=[0, TAU],
            color=BLUE,
        )
        self.add(orbit)

        self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES)

        # Animate planet along orbit
        time_tracker = ValueTracker(0)
        planet.add_updater(
            lambda mob: mob.move_to(
                orbit.point_from_proportion(time_tracker.get_value() % 1)
            )
        )
        self.play(
            time_tracker.animate.set_value(1),
            run_time=4,
            rate_func=linear,
        )
        self.wait(2)


class KeplersSecondLaw(ThreeDScene):
    """Kepler's Second Law: equal areas in equal times (from plugin README)."""

    def construct(self):
        star = Star(radius=1, size_of_particle=0.001, colors=[YELLOW])
        self.add(star)

        planet = Planet(center=[1, 0, 0], radius=0.05)
        self.add(planet)

        a, b = 4, 6
        orbit = ParametricFunction(
            lambda t: np.array([a * np.cos(t), b * np.sin(t), 0]),
            t_range=[0, TAU],
            color=BLUE,
        )
        self.add(orbit)

        last_pos = [orbit.point_from_proportion(1)]

        def trace(mob):
            curr_pos = mob.get_center()
            self.add(Line3D(last_pos[0], curr_pos, color=BLUE))
            last_pos[0] = curr_pos

        time_tracker = ValueTracker(0)
        planet.add_updater(
            lambda mob: mob.move_to(
                orbit.point_from_proportion(time_tracker.get_value())
            )
        )

        def get_swept_sector(start, end, close_factor=0.1):
            num_points = 50
            start = np.clip(start, 0, 1)
            end = np.clip(end, 0, 1)
            points = [orbit.point_from_proportion(start)]
            for alpha in np.linspace(start, end, num_points):
                points.append(orbit.point_from_proportion(alpha))
            last_point = orbit.point_from_proportion(end)
            closing_point = last_point * close_factor
            points.append(closing_point)
            return Polygon(*points, fill_opacity=0.3, color=YELLOW)

        sweep_intervals = [(0.1, 0.2), (0.4, 0.5), (0.7, 0.8)]
        cumulative_sweep = VGroup()

        def update_swept_area():
            current_time = time_tracker.get_value()
            for start, end in sweep_intervals:
                if start <= current_time <= end:
                    new_swept_area = get_swept_sector(start, current_time)
                    cumulative_sweep.add(new_swept_area)
            return cumulative_sweep

        sweep_area = always_redraw(lambda: update_swept_area())
        self.add(sweep_area)
        self.move_camera(phi=70 * DEGREES, theta=-90 * DEGREES)
        planet.add_updater(trace)
        self.play(
            time_tracker.animate.set_value(1),
            run_time=5,
            rate_func=linear,
        )
        self.wait(5)
