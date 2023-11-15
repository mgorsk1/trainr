import reflex as rx


def heading() -> rx.Component:
    return rx.heading('🚴TRAINR 🚴', font_size='2em')


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
