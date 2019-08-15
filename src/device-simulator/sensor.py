from random import random

class SensorSimulator():

    def __init__(self):
        self._temperature = 20

    def read(self):
        self._temperature += 3 * (random() - 0.5)
        return {
            "temperature": self._temperature
        }
