import os
os.environ['KIVY_NO_ARGS'] = '1'
import kivy
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
Config.set('graphics', 'resizable', False)

class TimerWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(TimerWidget, self).__init__(**kwargs)
        Window.size = (360, 640)
        self.counter = 1
        self.user_input = TextInput(hint_text="Enter User Name", size_hint=(0.6, 0.04), pos_hint={'x': 0.08, 'top': 0.95},background_normal='',background_color=(184/255.0, 242/255.0, 1, 0.9))
        self.add_button = Button(text="Add Timer", size_hint=(0.24, 0.04), pos_hint={'x': 0.68, 'top': 0.95},background_normal='', background_color=(22/255.0, 87/255.0, 14/255.0, 1))
        self.add_button.bind(on_press=self.add_timer)
        self.add_widget(self.user_input)
        self.add_widget(self.add_button)
        self.timers_layout = FloatLayout(size_hint=(1, 0.8), pos_hint={'top': 0.75})
        self.add_widget(self.timers_layout)
        self.scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'top': 0.75})
        self.timers_layout = FloatLayout(size_hint_y=None)  
        self.scroll_view.add_widget(self.timers_layout)
        self.add_widget(self.scroll_view)
        self.timers = []
        self.scroll_y = 1.0

    def add_timer(self, instance):
        user_name = self.user_input.text
        if user_name:
            new_timer = Timer(user_name, self.counter, self.remove_timer)
            self.counter += 1
            self.timers.append(new_timer)
            self.timers_layout.add_widget(new_timer) 
            vertical_position = 1-(len(self.timers) * 0.35)
            new_timer.pos_hint = {'top': vertical_position}
            self.user_input.text = ""

    def start_timer1(self, instance):
        for timer in self.timers:
            timer.start_timer()

    def pause_timer1(self, instance):
        for timer in self.timers:
            timer.pause_timer()

    def update_timers(self, dt):
        for timer in self.timers:
            timer.update()

    def start(self):
        Clock.schedule_interval(self.update_timers, 1)

    def remove_timer(self, timer):
        if timer in self.timers:
            index = self.timers.index(timer)
            self.timers_layout.remove_widget(timer)
            self.timers.remove(timer)
            self.counter -= 1
            for i, timer in enumerate(self.timers[index:]):
                timer.serial_number = index + 1 + i
                timer.update_serial_number()
                vertical_position = 1-(index+i+1)*0.35
                timer.pos_hint = {'top': vertical_position}


class Timer(FloatLayout):
    def __init__(self, user_name, serial_number, remove_callback, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.user_name = user_name
        self.serial_number = serial_number
        self.remove_callback = remove_callback  
        # Name Label
        self.name_label = Label(text=f"{self.serial_number}. {user_name}", size_hint=(0.38, 0.1), pos_hint={'x': 0, 'top': 1})
        self.add_widget(self.name_label)        
        # Start Button
        self.start_button = Button(text="S", size_hint=(0.07, 0.1), pos_hint={'x': 0.42, 'top': 1}, background_normal='', background_color=(61/255.0, 206/255.0, 43/255.0, 1))
        self.start_button.bind(on_press=self.start_timer)
        self.add_widget(self.start_button)       
        # Pause Button
        self.pause_button = Button(text="P", size_hint=(0.07, 0.1), pos_hint={'x': 0.49, 'top': 1}, background_normal='', background_color=(1, 0, 0, 1))
        self.pause_button.bind(on_press=self.pause_timer)
        self.add_widget(self.pause_button)
        # Timer Label
        self.timer_label = Label(text="20:00", size_hint=(0.2, 0.1), pos_hint={'x': 0.6, 'top': 1})
        self.add_widget(self.timer_label)
        self.seconds_remaining = 1200
        self.clock_event = None
        self.paused = False
        # Delete Button
        self.delete_button = Button(text="D", size_hint=(0.1, 0.1), pos_hint={'x': 0.85, 'top': 1}, background_normal='', background_color=(1, 0, 0, 1))
        self.delete_button.bind(on_press=self.delete_timer)
        self.add_widget(self.delete_button)

    def update(self, dt): 
        if not self.paused:
            if self.seconds_remaining > 0:
                self.seconds_remaining -= 1
                minutes = self.seconds_remaining // 60
                seconds = self.seconds_remaining % 60
                self.timer_label.text = f"{minutes:02}:{seconds:02}"
            else:
                self.timer_label.text = "Time's up!"
                self.stop_timer()

    def start_timer(self, instance):
        if self.clock_event is None:
            self.paused = False
            self.clock_event = Clock.schedule_interval(self.update, 1)

    def pause_timer(self, instance):
        self.paused = True

    def stop_timer(self):
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None

    def delete_timer(self, instance):
        self.stop_timer()
        self.remove_callback(self)

    def update_serial_number(self):
        self.name_label.text = f"{self.serial_number}. {self.user_name}"

class MyApp(App):
    def build(self):
        timer_widget = TimerWidget()
        return timer_widget

if __name__ == '__main__':
    MyApp().run()
