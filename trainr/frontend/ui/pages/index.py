import reflex as rx

from trainr.frontend.ui.components import backend_health
from trainr.frontend.ui.components import heading
from trainr.frontend.ui.components import user_name_modal
from trainr.frontend.ui.state import State


@rx.page(on_load=[State.get_data, State.collect_readings])
def index() -> rx.Component:
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
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                rx.vstack(
                    backend_health(),
                    rx.stat_group(
                        rx.stat(
                            rx.stat_label(
                                State.reading_type_display_name, font_size='0.4em'),
                            rx.stat_number(rx.badge(State.reading_value, variant='solid', color_scheme='gray',
                                                    font_size='1em', border_radius='15px'), font_size='0.8em'),
                        ),
                        rx.stat(
                            rx.stat_label(
                                f'FAN {State.fan_speed_emoji}', font_size='0.4em'),
                            rx.stat_number(
                                State.fan_speed_caption, font_size='0.8em'),
                        ),
                        rx.stat(
                            rx.stat_label(
                                f'LIGHT {State.light_on_emoji}', font_size='0.4em'),
                            rx.stat_number(
                                State.light_color_caption, font_size='0.8em'),
                        ),
                        width='100%',
                        text_align='center',
                    ),
                    rx.progress(value=State.reading_percent,
                                width='100%',
                                color_scheme=State.reading_zone_color,
                                is_animated=True, has_stripe=True),
                    rx.text(State.reading_zone_display_name,
                            font_size='0.4em'),
                    rx.accordion(
                        rx.accordion_item(
                            rx.accordion_button(
                                rx.text('Reading History', color='Gray'),
                                rx.accordion_icon(),
                            ),
                            rx.accordion_panel(
                                rx.recharts.line_chart(
                                    rx.recharts.line(
                                        data_key='reading',
                                        fill='#000000',
                                        type='monotone',
                                        dot=True,
                                    ),
                                    rx.recharts.reference_line(
                                        stroke_width=2,
                                        fill='#8884d8',
                                        fill_opacity=0.3,
                                    ),
                                    rx.recharts.x_axis(data_key='time_label', type_='category',
                                                       name='Last 60 minutes.',
                                                       tick_line=False, axis_line=True),
                                    rx.recharts.y_axis(
                                        data_key='reading', type_='number'),
                                    rx.recharts.graphing_tooltip(),
                                    height=200,
                                    width='100%',
                                    margin={
                                        'left': 0,
                                        'right': 60,
                                        'top': 30
                                    },
                                    data=State.reading_history_sanitized,
                                ),
                            ),
                        ),
                        allow_toggle=True,
                        font_size='0.4em',
                        width='100%',
                        padding_top='2%'
                    ),
                ),
                row_span=8,
                col_span=3,
            ),
            rx.grid_item(
                row_span=8,
                col_span=7,
            ),
            rx.grid_item(
                row_span=8,
                col_span=1,
            ),
            template_columns='repeat(19, 1fr)',
            template_rows='repeat(10, 1fr)',
            width='100%',
            gap=1,
            font_size='2em'
        ),
    )
