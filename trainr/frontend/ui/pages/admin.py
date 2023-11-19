import reflex as rx

from trainr.frontend.ui.components import backend_health
from trainr.frontend.ui.components import heading
from trainr.frontend.ui.components import user_name_modal
from trainr.frontend.ui.state import State
from trainr.utils import fan_speed_name_to_int_mapping
from trainr.utils import light_name_to_spec_mapping


@rx.page(on_load=State.get_data)
def admin() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float='right'),
        user_name_modal(),
        rx.grid(
            rx.grid_item(
                heading(),
                row_span=2,
                col_span=17,
                col_start=2,
                padding_bottom='1%'
            ),
            rx.grid_item(
                row_span=8,
                col_span=1,
                col_start=1,
            ),
            rx.grid_item(
                rx.responsive_grid(
                    rx.card(
                        rx.card_body(
                            rx.select(
                                ['HR', 'FTP'],
                                value=State.system_reading_type,
                                on_change=State.set_reading_type,
                            ),
                        ),
                        header=rx.heading(
                            f'Reading Source {State.reading_type_emoji}', size='md'),
                        footer=rx.text(
                            'Choose which metric should drive you!',
                            as_='i',
                            font_size='0.4em',
                            padding_top='18px'
                        ),
                    ),
                    rx.card(
                        rx.card_body(
                            rx.form(
                                rx.hstack(
                                    rx.number_input(
                                        value=State.reading_threshold,
                                        on_change=State.set_threshold,
                                        padding_top='10px',
                                        id='reading_threshold',
                                    ),
                                    rx.button('Save', type_='submit')
                                ),
                                on_submit=State.save_threshold,
                                reset_on_submit=False
                            )
                        ),
                        header=rx.heading(
                            f'Threshold {State.system_reading_type.upper()}',
                            size='md'
                        ),
                        footer=rx.text(
                            'Used to calculated zones.',
                            as_='i',
                            font_size='0.4em',
                            padding_top='10px'
                        ),
                    ),
                    rx.card(
                        rx.table(
                            headers=['Zone', 'From', 'To'],
                            rows=State.reading_zones,
                            variant='striped',
                            font_size='0.5em',
                            size='sm'
                        ),
                    ),
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
                                border_radius='10px'
                            )
                        ),
                        header=rx.heading('Last Seconds', size='md'),
                        footer=rx.text(
                            'Time period for which readings are collected.',
                            as_='i',
                            font_size='0.4em',
                            padding_top='10px'
                        ),
                    ),
                    rx.card(
                        rx.card_body(
                            rx.form(
                                rx.hstack(
                                    rx.input(
                                        value=State.system_user_name,
                                        on_change=State.set_user_name,
                                        id='user_name',
                                    ),
                                    rx.button('Save', type_='submit')
                                ),
                                on_submit=State.save_user_name,
                                reset_on_submit=False
                            )
                        ),
                        header=rx.heading(
                            f'User Name',
                            size='md'
                        ),
                        footer=rx.text(
                            'How do you want to be called?',
                            as_='i',
                            font_size='0.4em',
                            padding_top='10px'
                        ),
                    ),
                    columns=[3],
                    spacing='3',
                    min_child_width='250px'
                ),
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                rx.vstack(
                    backend_health(),
                    rx.switch(
                        is_checked=State.system_mode_auto,
                        on_change=State.toggle_system_mode
                    ),
                    rx.center(
                        rx.text(
                            f'SYSTEM MODE: {State.system_mode}', font_size='0.35em'
                        ),
                    )
                ),
                row_span=8,
                col_span=3,
            ),
            rx.grid_item(
                rx.responsive_grid(
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
                            color_scheme=State.light_color_class,
                        )
                    ),
                    rx.box(),
                    columns=[3],
                    spacing='3',
                    min_child_width='250px'
                ),
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                row_span=8,
                col_span=1
            ),
            template_columns='repeat(19, 1fr)',
            template_rows='repeat(10, 1fr)',
            width='100%',
            gap=1,
            font_size='2em'
        ),
    )
