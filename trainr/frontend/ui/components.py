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
                        rx.heading('TRAINR  🚴', float='left', size='md', width='100%', align='left'),
                        nav(),
                    ),
                    align_items='left',
                ),
                width='100%'
            ),
            rx.heading(f'Hi {State.system_user_name}! 👋', font_size='2em', padding_bottom='1%', padding_top='3%'),
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
