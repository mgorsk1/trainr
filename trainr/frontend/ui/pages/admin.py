import reflex as rx

from trainr.frontend.ui.components import heading
from trainr.frontend.ui.components import nav
from trainr.frontend.ui.state import State
from trainr.utils import fan_speed_name_to_int_mapping
from trainr.utils import light_name_to_spec_mapping


@rx.page(on_load=State.get_data)
def admin() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float='right'),
        rx.vstack(
            heading(),
            nav(),
            rx.grid(
                rx.grid_item(
                    rx.responsive_grid(
                        rx.box(rx.card(
                            rx.card_body(
                                rx.select(
                                    ['HR', 'FTP'],
                                    value=State.system_reading_type,
                                    on_change=State.set_reading_type,
                                ),
                            ),
                            header=rx.heading(f'Reading Source {State.reading_type_emoji}', size='md'),
                            footer=rx.text(
                                'Choose which metric should drive you!',
                                as_='i',
                                font_size='0.4em',
                                padding_top='18px'
                            )
                        ),
                            width='10em',
                        ), rx.box(
                            rx.card(
                                rx.card_body(
                                    rx.number_input(
                                        value=State.reading_threshold,
                                        on_change=State.set_threshold,
                                        padding_top='10px',
                                    )
                                ),
                                header=rx.heading(
                                    f'Threshold {State.system_reading_type.upper()}',
                                    size='md'
                                ),
                                footer=rx.text(
                                    'Zones will be calculated based on this value.',
                                    as_='i',
                                    font_size='0.4em',
                                    padding_top='10px'
                                )
                            ),
                            width='10em',
                        ),
                        rx.box(
                            rx.card(
                                rx.table(
                                    headers=['Zone', 'From', 'To'],
                                    rows=State.reading_zones,
                                    variant='striped',
                                    font_size='0.5em',
                                    size='sm'
                                ),
                            ),
                            width='10em',
                        ),
                        rx.box(
                            rx.card(
                                rx.vstack(
                                    rx.slider(
                                        value=State.system_last_seconds,
                                        min_=5,
                                        max_=60,
                                        step=5,
                                        on_change=State.set_last_seconds,
                                        margin_top='20px'
                                    ),
                                    rx.badge(
                                        State.system_last_seconds,
                                        variant='solid',
                                        color_scheme='blue',
                                    )
                                ),
                                header=rx.heading('Last Seconds', size='md'),
                                footer=rx.text(
                                    'Time period for which readings are collected.',
                                    as_='i',
                                    font_size='0.4em',
                                    padding_top='10px'
                                )
                            ),
                            width='10em',
                            height='10em'
                        ),
                        columns=[3],
                        spacing='4'
                    ),
                    col_span=4,
                    row_span=1
                ),
                rx.grid_item(
                    rx.vstack(
                        rx.switch(
                            is_checked=State.system_mode_auto,
                            on_change=State.toggle_system_mode
                        ),
                        rx.text(
                            f'SYSTEM MODE: {State.system_mode}', font_size='0.35em'
                        ),
                    ),
                    col_span=1,
                    row_span=1
                ),
                rx.grid_item(
                    rx.responsive_grid(
                        rx.box(
                            rx.card(
                                rx.select(
                                    list(fan_speed_name_to_int_mapping.keys()),
                                    value=State.fan_speed_display_name,
                                    on_change=State.set_fan_speed,
                                    is_disabled=State.system_mode_auto
                                ),
                                header=rx.heading(
                                    'Fan Settings',
                                    size='md',
                                    color=State.system_mode_header_color
                                ),
                                footer=rx.switch(
                                    is_checked=State.fan_on,
                                    on_change=State.toggle_fan,
                                    padding_top='17px',
                                    is_disabled=State.system_mode_auto
                                ),
                            ),
                            width='10em'
                        ),
                        rx.box(
                            rx.card(
                                rx.select(
                                    list(light_name_to_spec_mapping.keys()),
                                    value=State.light_color_caption,
                                    on_change=State.set_light_color,
                                    is_disabled=State.system_mode_auto
                                ),
                                header=rx.heading(
                                    'Light Settings',
                                    size='md',
                                    color=State.system_mode_header_color
                                ),
                                footer=rx.switch(
                                    is_checked=State.light_on,
                                    on_change=State.toggle_light,
                                    padding_top='17px',
                                    is_disabled=State.system_mode_auto,
                                    color_scheme=State.light_color.lower()
                                )
                            ),
                        ),
                        columns=[3],
                        spacing='4'
                    ),
                    col_span=4,
                    row_span=1
                ),
                template_columns="repeat(9, 1fr)",
            ),
            spacing='1.5em',
            font_size='2em',
            padding_top='5%',
        ),
    )
