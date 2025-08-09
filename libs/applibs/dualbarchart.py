from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, ColorProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from libs.applibs.utils import *


class AKDualBarChart(FloatLayout):
    x_values = ListProperty([])
    y_values = ListProperty([])  # List of [current, previous] y-values
    current_bar_color = ColorProperty([0.2, 0.6, 1, 1])  # Blue
    previous_bar_color = ColorProperty([1, 0.5, 0.2, 1])  # Orange
    background_color = ColorProperty([1, 1, 1, 1])  # White

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._init_ui)

    def _init_ui(self, *_):
        self.bind(pos=self._draw_chart, size=self._draw_chart,
                  x_values=self._draw_chart, y_values=self._draw_chart)

    def _draw_chart(self, *args):
        self.canvas.clear()
        self.clear_widgets()

        if not self.x_values or not self.y_values:
            return

        # Drawing area
        chart_x = self.x
        chart_y = self.y

        chart_padding = dp(40)
        chart_width = self.width - 2 * chart_padding
        chart_height = self.height - 2 * chart_padding
        num_bars = len(self.x_values)

        # Flatten y-values and find max
        all_y_vals = [val for pair in self.y_values for val in pair]
        max_y = max(all_y_vals) if all_y_vals else 1

        bar_width = chart_width / (num_bars * 3)
        spacing = bar_width

        with self.canvas:
            # Background
            Color(*self.background_color)
            Rectangle(pos=(chart_x, chart_y), size=(self.width, self.height))

            # Horizontal axis line
            Color(0.7, 0.7, 0.7)
            Line(points=[
                chart_x + chart_padding,
                chart_y + chart_padding,
                chart_x + chart_padding + chart_width,
                chart_y + chart_padding
            ], width=1.2)

        for i, label in enumerate(self.x_values):
            # Base X position of bar group
            base_x = chart_x + chart_padding + i * (2 * bar_width + spacing) + spacing / 2
            base_y = chart_y + chart_padding

            # Current bar
            current_y = self.y_values[i][0]
            current_height = (current_y / max_y) * chart_height
            current_bar_x = base_x
            self._animate_bar(current_bar_x, base_y, bar_width, current_height, self.current_bar_color)

            # Current bar label
            self._add_value_label(current_y, current_bar_x + bar_width / 2, base_y + current_height)

            # Previous bar
            previous_y = self.y_values[i][1]
            previous_height = (previous_y / max_y) * chart_height
            previous_bar_x = base_x + bar_width
            self._animate_bar(previous_bar_x, base_y, bar_width, previous_height, self.previous_bar_color)

            # Previous bar label
            self._add_value_label(previous_y, previous_bar_x + bar_width / 2, base_y + previous_height)

            # X-axis label
            x_label = MDLabel(
                text=label,
                halign="center",
                font_size=dp(12),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(dp(60), dp(20)),
                pos=(base_x + bar_width / 2 - dp(30), chart_y)
            )
            self.add_widget(x_label)

        # Legend
        self._add_legend(chart_x + chart_padding, chart_y + chart_height + chart_padding + dp(10))

    def _animate_bar(self, x, y, width, target_height, bar_color):
        with self.canvas:
            Color(*bar_color)
            bar = Rectangle(pos=(x, y), size=(width, 0))
        Animation(size=(width, target_height), d=0.5).start(bar)

    def _add_value_label(self, value, center_x, y_top):
        label = MDLabel(
            text=str(format_number(float(value))),
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_size=dp(8),
            size_hint=(None, None),
            size=(dp(57), dp(20)),
            pos=(center_x - dp(25), y_top + dp(5))
        )
        self.add_widget(label)

    def _add_legend(self, start_x, top_y):
        legend_height = dp(20)
        legend_spacing = dp(100)
        color_size = dp(14)

        def add_legend_item(x, color, text):
            with self.canvas:
                Color(*color)
                Rectangle(pos=(x, top_y), size=(color_size, color_size))
            label = MDLabel(
                text=text,
                pos=(x + color_size + dp(5), top_y - dp(4)),
                font_size=dp(12),
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(dp(80), dp(20)),
            )
            self.add_widget(label)

        # add_legend_item(start_x, self.current_bar_color, "Current")
        # add_legend_item(start_x + legend_spacing, self.previous_bar_color, "Previous")


