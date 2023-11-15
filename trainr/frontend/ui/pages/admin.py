from trainr.frontend.ui.components import nav, heading
from trainr.frontend.ui.state import State

import reflex as rx

from trainr.utils import fan_speed_name_to_int_mapping, light_name_to_spec_mapping


@rx.page(on_load=State.get_data)
def admin() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float='right'),
        rx.vstack(
            heading(),
            nav(),
            rx.vstack(
                rx.vstack(
                    rx.heading('Reading Settings', size='md'),
                    rx.select(
                        ['HR', 'FTP'],
                        value=State.system_reading_type,
                        on_change=State.set_reading_type,
                    ),
                    rx.heading(
                        f'Threshold {State.system_reading_type.upper()}', size='md'),
                    rx.number_input(
                        value=State.reading_threshold,
                        on_change=State.set_threshold
                    ),
                    rx.button(
                        'Calculate Zones', on_click=State.calculate_zones, color_scheme='blue')
                ),
                rx.table(
                    headers=['Zone', 'From', 'To'],
                    rows=State.reading_zones,
                    variant='striped'
                ),
                rx.divider(),
                rx.slider(
                    value=State.system_last_seconds,
                    min_=5,
                    max_=60,
                    step=5,
                    on_change=State.set_last_seconds,
                    padding_top='5%'
                ),
                rx.heading(
                    f'Last Seconds: {State.system_last_seconds}', size='md'),
                border_radius='md',
                width='15%',
                font_size='0.5em'

            ),
            rx.divider(),
            rx.vstack(
                rx.switch(
                    is_checked=State.system_mode_auto,
                    on_change=State.toggle_system_mode
                ),
                rx.text(
                    f'SYSTEM MODE: {State.system_mode}', font_size='0.35em')
            ),
            rx.cond(
                State.system_mode_manual,
                rx.vstack(
                    rx.divider(),
                    rx.heading('Fan settings', size='md'),
                    rx.hstack(
                        rx.vstack(
                            rx.heading('Fan', size='sm'),
                            rx.switch(
                                is_checked=State.fan_on,
                                on_change=State.toggle_fan
                            ),
                        ),
                        rx.vstack(
                            rx.heading('Fan Speed', size='sm'),
                            rx.select(
                                list(fan_speed_name_to_int_mapping.keys()),
                                value=State.fan_speed_display_name,
                                on_change=State.set_fan_speed
                            ),
                        ),
                        spacing='1.5em'),
                    rx.divider(),
                    rx.heading('Light settings', size='md'),
                    rx.hstack(
                        rx.vstack(
                            rx.heading('Lights', size='sm'),
                            rx.switch(
                                is_checked=State.light_on,
                                on_change=State.toggle_light
                            )
                        ),
                        rx.vstack(
                            rx.heading('Light Color', size='sm'),
                            rx.select(
                                list(light_name_to_spec_mapping.keys()),
                                value=State.light_color_caption,
                                on_change=State.set_light_color
                            ),
                        ),
                        spacing='1.5em',
                        width='100%'),
                )
            ),
            spacing='1.5em',
            font_size='2em',
            padding_top='5%',
        ),
    )
