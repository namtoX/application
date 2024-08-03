import os
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from kivy.app import App  # Import App class
from database import get_db_path

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Top buttons
        top_buttons = BoxLayout(size_hint_y=None, height=50)

        config_button = Button(text='Config')
        exit_button = Button(text='Exit')
        status_button = Button(text='Status')
        top_buttons.add_widget(config_button)
        top_buttons.add_widget(status_button)
        top_buttons.add_widget(exit_button)

        # Bind the exit button to the stop method
        exit_button.bind(on_press=self.stop_app)
        config_button.bind(on_press=self.go_to_config)

        self.add_widget(top_buttons)

        # Main layout below top buttons
        main_layout = BoxLayout()

        # Left layout (30% of width)
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)

        # Ticket display
        ticket_display = Label(text='Ticket Display', size_hint_y=None, height=200)
        left_layout.add_widget(ticket_display)

        # Numeric keypad
        keypad_layout = GridLayout(cols=3, size_hint_y=None, height=200)
        for i in range(1, 10):
            keypad_layout.add_widget(Button(text=str(i)))
        left_layout.add_widget(keypad_layout)

        main_layout.add_widget(left_layout)

        # Right layout (70% of width)
        right_layout = BoxLayout(orientation='vertical')
        right_layout.add_widget(Label(text='Pending Items'))

        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def stop_app(self, instance):
        App.get_running_app().stop()

    def go_to_config(self, instance):
        App.get_running_app().root.current = 'config'

class ConfigScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Top buttons
        top_buttons = BoxLayout(size_hint_y=None, height=50)

        back_button = Button(text='Back to Main')
        top_buttons.add_widget(back_button)

        back_button.bind(on_press=self.go_back)
        
        self.add_widget(top_buttons)

        # Config options and data display
        config_and_data_layout = BoxLayout()

        # Left layout with buttons
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, size_hint_y=1)
        self.company_button = Button(text='Company', size_hint_y=None, height=50)
        self.cashiers_button = Button(text='Cashiers', size_hint_y=None, height=50)
        self.vatrates_button = Button(text='VAT Rates', size_hint_y=None, height=50)

        left_layout.add_widget(self.company_button)
        left_layout.add_widget(self.cashiers_button)
        left_layout.add_widget(self.vatrates_button)

        self.company_button.bind(on_press=self.show_company)
        self.cashiers_button.bind(on_press=self.show_cashiers)
        self.vatrates_button.bind(on_press=self.show_vatrates)

        config_and_data_layout.add_widget(left_layout)

        # Right layout for data display
        self.data_display = BoxLayout(orientation='vertical', size_hint_x=0.7, size_hint_y=1)
        config_and_data_layout.add_widget(self.data_display)

        self.add_widget(config_and_data_layout)

        # Status bar at the bottom
        self.status_bar = Label(size_hint_y=None, height=50)
        self.add_widget(self.status_bar)
        self.update_status()

    def go_back(self, instance):
        App.get_running_app().root.current = 'main'

    def show_company(self, instance):
        self.display_data('company')

    def show_cashiers(self, instance):
        self.display_cashiers_table()

    def show_vatrates(self, instance):
        self.display_data('vatrates')

    def display_data(self, table_name):
        self.data_display.clear_widgets()
        scrollview = ScrollView()
        data_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        data_layout.bind(minimum_height=data_layout.setter('height'))

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                data_layout.add_widget(Label(text=str(row), size_hint_y=None, height=40))
            scrollview.add_widget(data_layout)
            self.data_display.add_widget(scrollview)
            conn.close()
        except sqlite3.Error as e:
            Logger.error(f"SQL Error: {e}")
            self.status_bar.text = f"Error accessing table {table_name}: {e}"

    def display_company_info(self):
        self.data_display.clear_widgets()
        grid = GridLayout(cols=2, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM company LIMIT 1")  # Fetch the single row
            row = cursor.fetchone()

            if row:
                Logger.info(f"Fetched company info: {row}")  # Log fetched row

                # Assuming the company table has columns: name, address, etc.
                field_names = ['Name', 'Address', 'Phone', 'Email']  # Example column names

                for i, field_name in enumerate(field_names):
                    Logger.info(f"Field {field_name}: {row[i]}")  # Log each field's data

                    # Add label and field
                    label = Label(text=field_name, size_hint_y=None, height=40)
                    field = TextInput(text=row[i] if row[i] is not None else "", size_hint_y=None, height=40)

                    grid.add_widget(label)
                    grid.add_widget(field)

            else:
                Logger.warning("No data found in company table")
                self.status_bar.text = "No data found in company table"

            scrollview = ScrollView()
            scrollview.add_widget(grid)
            self.data_display.add_widget(scrollview)

            conn.close()
        except sqlite3.Error as e:
            Logger.error(f"SQL Error: {e}")
            self.status_bar.text = f"Error accessing table company: {e}"


    def display_cashiers_table(self):
        self.data_display.clear_widgets()
        grid = GridLayout(cols=3, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cashiers")
            rows = cursor.fetchall()

            Logger.info(f"Fetched rows: {rows}")  # Log fetched rows

            # Add headers
            grid.add_widget(Label(text='ID', size_hint_y=None, height=40, color=(0.5, 0.5, 0.5, 1)))  # Grayed out header
            grid.add_widget(Label(text='Name', size_hint_y=None, height=40))
            grid.add_widget(Label(text='NISS', size_hint_y=None, height=40))

            for row in rows:
                Logger.info(f"Row data: {row}")  # Log each row's data

                id_field = TextInput(text=str(row[0]), readonly=True, size_hint_y=None, height=40, background_color=(0.9, 0.9, 0.9, 1))  # Grayed out field
                name_field = TextInput(text=row[1] if row[1] is not None else "", size_hint_y=None, height=40)
                niss_field = TextInput(text=row[2] if row[2] is not None else "", size_hint_y=None, height=40)

                grid.add_widget(id_field)
                grid.add_widget(name_field)
                grid.add_widget(niss_field)

            scrollview = ScrollView()
            scrollview.add_widget(grid)
            self.data_display.add_widget(scrollview)

            conn.close()
        except sqlite3.Error as e:
            Logger.error(f"SQL Error: {e}")
            self.status_bar.text = f"Error accessing table cashiers: {e}"

    def update_status(self):
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            tables_list = ", ".join([table[0] for table in tables])
            self.status_bar.text = f'Connected to db.db. Tables: {tables_list}'
            conn.close()
        except sqlite3.Error as e:
            Logger.error(f"SQL Error: {e}")
            self.status_bar.text = 'Failed to connect to db.db'
