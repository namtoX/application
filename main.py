from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens import MainScreen, ConfigScreen

class POSApp(App):
    def build(self):
        sm = ScreenManager()
        
        main_screen = Screen(name='main')
        main_screen.add_widget(MainScreen())
        sm.add_widget(main_screen)
        
        config_screen = Screen(name='config')
        config_screen.add_widget(ConfigScreen())
        sm.add_widget(config_screen)
        
        return sm

if __name__ == '__main__':
    POSApp().run()
