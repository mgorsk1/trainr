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
        font_size='0.5em'
    )


def heading() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading('🚴TRAINR 🚴', font_size='2em', padding_bottom='3%'),
            nav(),
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
            variant='solid',
            margin_bottom='5%',
        ),
    )
