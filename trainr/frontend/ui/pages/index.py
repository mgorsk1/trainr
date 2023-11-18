import reflex as rx

from trainr.frontend.ui.components import heading, backend_health
from trainr.frontend.ui.state import State


@rx.page(on_load=[State.get_data, State.collect_readings])
def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float='right'),
        rx.grid(
            rx.grid_item(
                heading(),
                row_span=2,
                col_span=20,
                padding_top='4%',
                padding_bottom='1%'
            ),
            rx.grid_item(
                row_span=8,
                col_span=1,
            ),
            rx.grid_item(
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                rx.vstack(
                    backend_health(),
                    rx.stat_group(
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
                        width='100%',
                        text_align='center',
                    ),
                    rx.progress(value=State.reading_percent,
                                width='100%',
                                color_scheme=State.reading_zone_color,
                                is_animated=True, has_stripe=True),
                    rx.text(State.reading_zone_display_name, font_size='0.35em')
                ),
                row_span=8,
                col_span=4,
            ),
            rx.grid_item(
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                row_span=8,
                col_span=1,
            ),
            template_columns='repeat(20, 1fr)',
            template_rows='repeat(10, 1fr)',
            width='100%',
            gap=1,
            font_size='2em'
        ),
        # rx.vstack(
        #
        #     rx.grid(
        #
        #     ),
        #     # rx.grid(
        #     #     rx.grid_item(
        #     #         rx.box(),
        #     #         col_span=4,
        #     #         row_span=1,
        #     #         maring_left='10%'
        #     #     ),
        #     #     rx.grid_item(
        #     #         rx.responsive_grid(
        #     #
        #     #         col_span=2,
        #     #         row_span=1
        #     #     ),
        #     #     rx.grid_item(
        #     #         rx.box(),
        #     #         col_span=4,
        #     #         row_span=1
        #     #     ),
        #     #     template_columns="repeat(10, 1fr)",
        #     # ),
        #     spacing='1.5em',
        #     font_size='2em',
        #     padding_top='5%',
        #     width='100%'
        # )
    )
