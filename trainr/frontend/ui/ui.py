'''Welcome to Reflex! This file outlines the steps to create a basic app.'''
import reflex as rx

from trainr.frontend.ui.pages.admin import admin
from trainr.frontend.ui.pages.index import index

# Add state and page to the app.
app = rx.App()
app.add_page(index, title='🚴TRAINR | Home')
app.add_page(admin, title='🚴TRAINR | Admin')
app.compile()
