import reflex as rx

from trainr.frontend.ui.state import State


def nav() -> rx.Component:
    return rx.breadcrumb(
        rx.breadcrumb_item(
            rx.breadcrumb_link('Home', href='/')
        ),
        rx.breadcrumb_item(
            rx.breadcrumb_link('Admin', href='/admin')
        ),
        font_size='0.5em',
        align='left'
    )


def heading() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.heading('TRAINR  🚴', float='left',
                                   size='md', width='100%', align='left'),
                        nav(),
                    ),
                    align_items='left',
                ),
                width='100%'
            ),
            rx.heading(f'Hi {State.system_user_name}! 👋',
                       font_size='2em', padding_bottom='1%', padding_top='3%'),
            width='100%'
        )
    )


def backend_health() -> rx.Component:
    return rx.cond(
        State.system_backend_healthy,
        rx.box(),
        rx.alert(
            rx.alert_icon(),
            rx.alert_title(
                'Backend not running.',
                font_size='0.5em'
            ),
            status='error',
            margin_bottom='5%',
        ),
    )


def user_name_input(**kwargs) -> rx.Component:
    return rx.input(
        value=State.system_user_name,
        on_change=State.set_user_name,
        id='user_name',
        **kwargs
    )


def threshold_input(**kwargs) -> rx.Component:
    return rx.number_input(
        value=State.reading_threshold,
        on_change=State.set_threshold,
        id='reading_threshold',
        **kwargs
    )


def reading_type_input(**kwargs) -> rx.Component:
    return rx.select(
        ['HR', 'FTP'],
        value=State.system_reading_type,
        on_change=State.set_reading_type,
        id='reading_type',
        **kwargs
    )


def user_name_modal() -> rx.Component:
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header('Hey, tell me something about you!'),
                rx.modal_body(
                    rx.form(
                        rx.vstack(
                            rx.hstack(
                                rx.box(rx.center(rx.text('My name is', as_='i')), width='11%'),
                                rx.box(user_name_input(), width='24%'),
                                rx.box(rx.center(rx.text('and my Threshold', as_='i')), width='20%'),
                                rx.box(reading_type_input(), width='15%'),
                                rx.box(rx.center(rx.text('is', as_='i')), width='5%'),
                                rx.box(threshold_input(), width='15%'),
                            ),
                            rx.button('Save', type_='submit'),
                        ),
                        on_submit=State.save_user_data,
                    ),
                ),
                rx.modal_footer(rx.text('💡You can change this configuration later in the admin menu.', as_='small'))
            ),
        ),
        is_open=State.system_not_initialized,
        size='4xl'
    )
