import reflex as rx

from trainr.ui.components import nav, heading
from trainr.ui.state import State


@rx.page(on_load=State.get_data)
def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            heading(),
            nav(),
            rx.vstack(
                rx.hstack(
                    rx.stat(
                        rx.stat_label(State.reading_type_display_name),
                        rx.stat_number(State.reading_value),
                    ),
                    rx.stat(
                        rx.stat_label(f'FAN {State.fan_speed_emoji}'),
                        rx.stat_number(State.fan_speed_caption),
                    ),
                    rx.stat(
                        rx.stat_label(f'LIGHT {State.light_on_emoji}'),
                        rx.stat_number(State.light_color_caption),
                    ),
                    width="125%",
                    spacing="2em"),
                rx.progress(value=State.reading_percent, width="125%", color_scheme=State.reading_zone_color),
                rx.text(State.reading_zone_display_name, font_size="0.35em")
            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="5%",
        ),
    )
