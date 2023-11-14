'''Welcome to Reflex! This file outlines the steps to create a basic app.'''
import reflex as rx

from trainr.ui.pages.admin import admin
from trainr.ui.pages.index import index

# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(admin)
app.compile()
