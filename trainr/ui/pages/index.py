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
                        rx.stat_label('FAN'),
                        rx.stat_number(State.fan_speed_caption),
                    ),
                    rx.stat(
                        rx.stat_label('LIGHT'),
                        rx.stat_number(State.light_color_caption),
                    ),
                    spacing="2em"),
                rx.progress(value=State.reading_percent, width="100%", color_scheme=State.active_zone_color),
            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="5%",
        ),
    )
