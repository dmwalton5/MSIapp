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


kivy.require('2.0.0')

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
    'Stiffness or restricted motion': {
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
        self.symptoms = [
            "Sharp stabbing pain",
            "General dull achiness",
            "Stiffness or restricted motion",
            "Weakness, clumsiness, or giving way",
            "Sensitivity to certain odors, lights, noises, or temperatures",
            "Numbness or pins and needles",
            "Fatigue",
            "Fogginess (difficulty concentrating or remembering things)",
            "Nausea or poor appetite",
            "Nervousness, anxiety, or sadness"
        ]
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
        return self.selected_symptoms
    def next_screen(self, *args):
        selected_symptoms = [symptom for symptom in self.symptoms if
                             App.get_running_app().selected_symptoms[symptom]["selected"]]
        self.manager.get_screen('frequency').populate_symptoms(selected_symptoms)
        self.manager.current = 'frequency'


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
                             App.get_running_app().selected_symptoms[symptom]["selected"]]
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
        self.manager.get_screen('interference').populate_symptoms(self.symptom_frequencies)
        self.manager.current = 'interference'


class InterferenceScreen(Screen):
    def __init__(self, **kwargs):
        super(InterferenceScreen, self).__init__(**kwargs)
        self.symptom_frequencies = {}
        next_button = Button(text="Next", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        next_button.bind(on_release=self.go_to_summary_screen)
        self.add_widget(next_button)

    def on_enter(self, *args):
        symptom_frequencies = self.manager.get_screen('frequency').get_symptom_frequencies()
        selected_symptoms = self.manager.get_screen('symptoms').get_selected_symptoms()
        self.symptom_frequencies = symptom_frequencies
        self.populate_symptoms(selected_symptoms)

    def on_interference_button_press(self, button):
        symptom = button.group
        interference = button.text
        self.symptom_frequencies[symptom] = {'interference': interference}

    #def pre_enter(self, *args):
    #    symptom_frequencies = self.manager.get_screen('frequency').get_symptom_frequencies()
    #    selected_symptoms = self.manager.get_screen('symptoms').get_selected_symptoms()
    #    self.symptom_frequencies = symptom_frequencies
    #    self.populate_symptoms(selected_symptoms)

    def populate_symptoms(self, selected_symptoms):
        self.ids.symptom_layout.clear_widgets()
        for symptom in selected_symptoms:
            symptom_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=170)
            symptom_label = Label(text=symptom, halign="left", valign="middle", size_hint_x=0.7, size_hint_y=None,
                                  height=170)
            symptom_label.bind(size=symptom_label.setter('text_size'))
            symptom_row.add_widget(symptom_label)

            for option in ['Barely noticeable, doesn\'t really bother me',
                           'Intense enough that I notice it but can usually carry on without too much effort',
                           'Quite intense requiring real effort to carry on',
                           'So intense I have to stop what I\'m doing and seek relief']:
                button = CustomToggleButton(text=option, group=symptom, size_hint_x=0.5, width=200, size_hint_y=None,
                                            height=150, font_size=28)
                button.bind(on_press=self.on_interference_button_press)
                symptom_row.add_widget(button)

            self.ids.symptom_layout.add_widget(symptom_row)

    def get_symptom_interference(self):
        return self.symptom_frequencies

    def go_to_summary_screen(self, *args):
        summary_screen = self.manager.get_screen('summary')
        summary_screen.symptom_frequencies = self.symptom_frequencies
        summary_screen.symptom_values = self.symptom_values  # Corrected line
        self.manager.current = 'summary'

    def on_leave(self, *args):
        self.ids.symptom_layout.clear_widgets()


class SummaryScreen(Screen):
    symptom_frequencies = ObjectProperty(None)
    symptom_values = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.populate_summary(self.symptom_frequencies, self.symptom_values)

    def populate_summary(self, symptom_frequencies, symptom_values):
        symptom_scores = self.calculate_symptom_scores(symptom_frequencies, symptom_values)

        # Convert the symptom_scores dictionary into two lists: labels and values
        labels = list(symptom_scores.keys())
        values = list(symptom_scores.values())

        self.plot_radar(labels, values)

    def calculate_symptom_scores(self, symptom_frequencies, symptom_values):
        symptom_scores = {}

        for symptom, freq_interference in symptom_frequencies.items():
            freq = freq_interference.get('frequency', 0)
            interference = freq_interference.get('interference', 0)
            value = symptom_values.get(symptom, {}).get(freq, {}).get(interference, 0)
            symptom_scores[symptom] = value

        return symptom_scores

    def plot_radar(self, labels, values):
        # Prepare the data for the radar plot
        data = list(values)

        # Convert data to a numpy array
        data = np.array(data)

        # Convert data to percentages
        data = data / data.sum() * 100

        num_vars = len(labels)

        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
        angles = angles.tolist()  # Explicitly convert angles to a list
        data = np.append(data, data[0]).tolist()  # Convert data back to a list
        angles.append(angles[0])  # Append the first angle value to the list

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, data, color='blue', alpha=0.25)
        ax.plot(angles, data, color='blue', linewidth=2, marker='o')

        ax.set_yticklabels([])
        ax.set_ylim(0, 100)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        plot_widget = self.ids.plot_widget
        plot_widget.clear_widgets()

        ax.margins(0.1)  # Add margins to the axes

        # Set the aspect ratio to 'auto'
        ax.set_aspect('auto')

        plot_widget.add_widget(FigureCanvasKivyAgg(figure=fig))


Builder.load_file('symptom.kv')


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.selected_symptoms = []

    def build(self):
        self.selected_symptoms = {
            symptom: {"selected": False} for symptom in [
                "Sharp stabbing pain",
                "General dull achiness",
                "Stiffness or restricted motion",
                "Weakness, clumsiness, or giving way",
                "Sensitivity to certain odors, lights, noises, or temperatures",
                "Numbness or pins and needles",
                "Fatigue",
                "Fogginess (difficulty concentrating or remembering things)",
                "Nausea or poor appetite",
                "Nervousness, anxiety, or sadness"
            ]
        }

        sm = ScreenManager()
        sm.add_widget(SymptomsScreen(name='symptoms'))
        sm.add_widget(FrequencyScreen(name='frequency'))
        sm.add_widget(InterferenceScreen(name="interference"))
        sm.add_widget(SummaryScreen(name="summary"))

        return sm


if __name__ == '__main__':
    MyApp().run()
