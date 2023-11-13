from trainr.ui.components import nav, heading
from trainr.ui.state import State

import reflex as rx

from trainr.utils import fan_speed_mapping, light_spec_mapping


@rx.page(on_load=State.get_data)
def admin() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            heading(),
            nav(),
            rx.hstack(
                rx.vstack(
                    rx.heading("Fan", size="sm"),
                    rx.switch(
                        is_checked=State.fan_on,
                        on_change=State.toggle_fan
                    ),
                ),
                rx.vstack(
                    rx.heading('Fan Speed', size='sm'),
                    rx.select(
                        list(fan_speed_mapping.keys()),
                        value=State.fan_speed_name,
                        on_change=State.set_fan_speed
                    ),
                ),
                spacing="1.5em"),
            rx.hstack(
                rx.vstack(
                    rx.heading("Lights", size="sm"),
                    rx.switch(
                        is_checked=State.light_on,
                        on_change=State.toggle_light
                    )
                ),
                rx.vstack(
                    rx.heading('Light Color', size='sm'),
                    rx.select(
                        list(light_spec_mapping.keys()),
                        default_value=str(State.light_color_caption),
                        on_change=State.set_light_color
                    ),
                ),
                spacing="1.5em"),
            rx.vstack(
                rx.heading("Threshold HR", size="md"),
                rx.number_input(
                    value=State.hr_threshold,
                    on_change=State.set_hr_threshold
                ),
                rx.button("Calculate Zones", on_click=State.calculate_hr_zones, color_scheme="blue")
            ),
            rx.box(
                rx.data_table(
                    columns=["Zone", "From", "To"],
                    data=State.hr_zones
                ),
                border_radius="md",
                width="15%",
                font_size="0.5em"

            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="5%",
        ),
    )