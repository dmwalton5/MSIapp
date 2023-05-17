import kivy
import matplotlib.pyplot as plt
import mpltern
import numpy as np
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from math import pi
from kivy.graphics import Color, Rectangle

kivy.require('2.0.0')

symptoms = [
    "Sharp stabbing pain",
    "General dull achiness",
    "Stiffness or restricted movement",
    "Weakness, clumsiness, or giving way",
    "Sensitivity to certain odors, lights, noises, or temperatures",
    "Numbness or pins and needles",
    "Fatigue",
    "Fogginess (difficulty concentrating or remembering things)",
    "Nausea or poor appetite",
    "Nervousness, anxiety, or sadness"
]

symptom_values = {
    'Sharp stabbing pain': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 3,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 10,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 4,
            'Intense enough that I notice it but can usually carry on without too much effort': 7,
            'Quite intense requiring real effort to carry on': 11,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'General dull achiness': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 7,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 6,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Stiffness or restricted movement': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 7,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 10,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 6,
            'Quite intense requiring real effort to carry on': 11,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Weakness, clumsiness, or giving way': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 7,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 10,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 6,
            'Quite intense requiring real effort to carry on': 11,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Sensitivity to certain odors, lights, noises, or temperatures': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 7,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Numbness or pins and needles': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 7,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
     'Fatigue': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 7,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Fogginess (difficulty concentrating or remembering things)': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 7,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 8,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Nausea or poor appetite': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 4,
            'Quite intense requiring real effort to carry on': 6,
            'So intense I have to stop what I\'m doing and seek relief': 7,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 10,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 3,
            'Intense enough that I notice it but can usually carry on without too much effort': 8,
            'Quite intense requiring real effort to carry on': 11,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
    'Nervousness, anxiety, or sadness': {
        'Rarely': {
            'Barely noticeable, doesn\'t really bother me': 1,
            'Intense enough that I notice it but can usually carry on without too much effort': 3,
            'Quite intense requiring real effort to carry on': 7,
            'So intense I have to stop what I\'m doing and seek relief': 8,
        },
        'Often': {
            'Barely noticeable, doesn\'t really bother me': 2,
            'Intense enough that I notice it but can usually carry on without too much effort': 5,
            'Quite intense requiring real effort to carry on': 9,
            'So intense I have to stop what I\'m doing and seek relief': 11,
        },
        'All the time': {
            'Barely noticeable, doesn\'t really bother me': 4,
            'Intense enough that I notice it but can usually carry on without too much effort': 6,
            'Quite intense requiring real effort to carry on': 10,
            'So intense I have to stop what I\'m doing and seek relief': 12,
        },
    },
}

class ToggleButtonGroup(BoxLayout):
    def __init__(self, options, symptom_index, **kwargs):
        super(ToggleButtonGroup, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.options = options
        self.buttons = []
        for option in options:
            button = ToggleButton(text=option, group=f"frequency_{symptom_index}", size_hint_x=None, width=200)
            self.buttons.append(button)
            self.add_widget(button)

    def get_selected_option(self):
        selected_button = next((button for button in self.buttons if button.state == "down"), None)
        return selected_button.text if selected_button else None


class SymptomsScreen(Screen):
    def __init__(self, **kwargs):
        super(SymptomsScreen, self).__init__(**kwargs)
        self.selected_symptoms = []  # Initialize selected_symptoms here
        self.symptoms = symptoms
        next_button = Button(text="Next", on_release=self.next_screen, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        self.add_widget(next_button)

    def on_pre_enter(self, *args):
        self.ids.symptoms_grid.clear_widgets()
        for symptom in self.symptoms:
            btn = ToggleButton(text=symptom, allow_no_selection=False, size_hint_y=None, height=60)
            btn.bind(state=self.update_symptom_selection)
            self.ids.symptoms_grid.add_widget(btn)

    def update_symptom_selection(self, instance, value):
        app_instance = App.get_running_app()
        if value == "down":
            app_instance.selected_symptoms[instance.text] = {"selected": True}
        else:
            app_instance.selected_symptoms[instance.text] = {"selected": False}

    def get_selected_symptoms(self):
        selected_symptoms = [symptom for symptom in self.symptoms if
                             App.get_running_app().selected_symptoms[symptom]["selected"]]
        print(f'selected_symptoms from SymptomsScreen: {selected_symptoms}')
        return selected_symptoms

    def next_screen(self, *args):
        selected_symptoms = self.get_selected_symptoms()
        app = App.get_running_app()
        app.selected_symptoms = selected_symptoms
        # app.symptom_frequencies = {symptom: app.symptom_frequencies[symptom] for symptom in selected_symptoms}
        self.manager.current = 'frequency'
        print(f'symptom_frequencies from SymptomsScreen: {app.symptom_frequencies}')


class CustomToggleButton(ToggleButton):
    pass


class FrequencyScreen(Screen):
    def __init__(self, **kwargs):
        super(FrequencyScreen, self).__init__(**kwargs)
        self.symptom_frequencies = {}  # dynamically updating dictionary of symptom + frequency combos
        next_button = Button(text="Next", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        next_button.bind(on_release=self.go_to_interference_screen)
        self.add_widget(next_button)

    def on_frequency_button_press(self, button):
        symptom = button.group
        frequency = button.text
        self.symptom_frequencies[symptom] = {'frequency': frequency}

    def on_enter(self, *args):
        selected_symptoms = [symptom for symptom in self.manager.get_screen('symptoms').symptoms if
                             symptom in App.get_running_app().selected_symptoms]
        self.populate_symptoms(selected_symptoms)

    def populate_symptoms(self, selected_symptoms):
        self.ids.symptom_layout.clear_widgets()
        for symptom in selected_symptoms:
            symptom_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
            symptom_label = Label(text=symptom, size_hint_x=0.7, halign="left", valign="middle")
            symptom_label.bind(size=symptom_label.setter('text_size'))
            symptom_row.add_widget(symptom_label)

            for option in ['Rarely', 'Often', 'All the time']:
                button = ToggleButton(text=option, group=symptom, size_hint_x=0.5, width=200)
                button.bind(on_press=self.on_frequency_button_press)  # Bind the on_press event
                symptom_row.add_widget(button)

            self.ids.symptom_layout.add_widget(symptom_row)

    def get_symptom_frequencies(self):
        return self.symptom_frequencies

    def go_to_interference_screen(self, *args):
        app = App.get_running_app()
        for symptom in app.selected_symptoms:
            app.symptom_frequencies[symptom]['frequency'] = self.symptom_frequencies[symptom]['frequency']
        self.manager.current = 'interference'
        print(f'selected_symptoms after FrequencyScreen: {app.selected_symptoms}')
        print(f'symptom_frequencies after FrequencyScreen: {app.symptom_frequencies}')


class InterferenceScreen(Screen):
    def __init__(self, **kwargs):
        super(InterferenceScreen, self).__init__(**kwargs)
        self.symptom_frequencies = {}
        next_button = Button(text="Next", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        next_button.bind(on_release=self.go_to_summary_screen)
        self.add_widget(next_button)

    def on_enter(self, *args):
        selected_symptoms = [symptom for symptom in App.get_running_app().selected_symptoms]
        # print(f"Selected symptoms in InterferenceScreen.on_enter: {selected_symptoms}")
        self.populate_symptoms(selected_symptoms)

    def on_interference_button_press(self, button):
        symptom = button.group
        interference = button.text
        self.symptom_frequencies[symptom] = {'interference': interference}

    def populate_symptoms(self, selected_symptoms):
        # print(f"Selected symptoms in InterferenceScreen.populate_symptoms: {selected_symptoms}")
        self.ids.symptom_layout.clear_widgets()
        for symptom in selected_symptoms:
            # print(f"Adding symptom: {symptom}")
            symptom_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=170)
            symptom_label = Label(text=symptom, halign="left", valign="middle", size_hint_x=0.7, size_hint_y=None,
                                  height=170)
            symptom_label.bind(size=symptom_label.setter('text_size'))
            symptom_row.add_widget(symptom_label)

            for option in ['Barely noticeable, doesn\'t really bother me',
                           'Intense enough that I notice it but can usually carry on without too much effort',
                           'Quite intense requiring real effort to carry on',
                           'So intense I have to stop what I\'m doing and seek relief']:
                # print(f"Adding option: {option}")
                button = CustomToggleButton(text=option, group=symptom, size_hint_x=0.5, width=200, size_hint_y=None,
                                            height=150, font_size=28)
                button.bind(on_press=self.on_interference_button_press)
                symptom_row.add_widget(button)

            self.ids.symptom_layout.add_widget(symptom_row)

    def get_symptom_interference(self):
        return self.symptom_frequencies

    def go_to_summary_screen(self, *args):
        app = App.get_running_app()
        for symptom in app.selected_symptoms:
            app.symptom_frequencies[symptom]['interference'] = self.symptom_frequencies[symptom]['interference']
        self.manager.current = 'summary'
        print(f'selected_symptoms after InterferenceScreen: {app.selected_symptoms}')
        print(f'symptom_frequencies after InterferenceScreen: {app.symptom_frequencies}')


class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super(SummaryScreen, self).__init__(**kwargs)
        restart_button = Button(text="Restart", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        restart_button.bind(on_release=self.restart_app)
        self.add_widget(restart_button)

    def on_enter(self, *args):
        self.ids.plot_area.clear_widgets()  # clear any existing plots
        app = App.get_running_app()
        symptom_frequencies = app.symptom_frequencies
        scores = self.calculate_scores(symptom_frequencies)
        self.plot_radar(scores)

    def calculate_scores(self, symptom_frequencies):
        scores = {symptom: 0 for symptom in symptoms}
        for symptom, values in symptom_frequencies.items():
            frequency = values['frequency']
            interference = values['interference']
            if frequency != 'None' and interference != 'None':  # only if frequency and interference are not 'None'
                scores[symptom] = symptom_values[symptom][frequency][interference]
        print(f'symptom scores: {scores}')
        return scores


    def plot_radar(self, scores):
        # Number of variables (symptoms)
        num_vars = 10

        # Compute angle of each axis in the plot
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Complete the loop by appending the first angle
        angles += angles[:1]

        # Initialize the plot
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))

        # set y limit
        ax.set_ylim(0, 12)

        # Arrange the data
        values = list(scores.values())
        values += values[:1]

        # Plot the data
        ax.plot(angles, values, linewidth=1, linestyle='solid')

        # Fill the area
        ax.fill(angles, values, 'b', alpha=0.25)

        # Set the labels for each axis
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(list(scores.keys()))

        # Display the plot in the SummaryScreen
        plot = FigureCanvasKivyAgg(plt.gcf())
        self.ids.plot_area.add_widget(plot)

    def restart_app(self, *args):
        app = App.get_running_app()
        app.selected_symptoms = {symptom: {"selected": False} for symptom in symptoms}
        app.symptom_frequencies = {symptom: {"frequency": "None", "interference": "None"} for symptom in symptoms}
        self.manager.current = 'symptoms'


Builder.load_file('symptom.kv')


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.selected_symptoms = []
        self.symptom_frequencies = {symptom: {'frequency': 'None', 'interference': 'None'} for symptom in symptoms}

    def build(self):
        self.selected_symptoms = {
            symptom: {"selected": False} for symptom in symptoms
            }

        sm = ScreenManager()
        sm.add_widget(SymptomsScreen(name='symptoms'))
        sm.add_widget(FrequencyScreen(name='frequency'))
        sm.add_widget(InterferenceScreen(name="interference"))
        sm.add_widget(SummaryScreen(name="summary"))

        return sm


if __name__ == '__main__':
    MyApp().run()
