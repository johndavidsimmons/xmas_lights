import RPi.GPIO as GPIO
import time
import random

# Pins to use
# 5, 6, 13, 19, 26, 16

#################
#   GPIO SETUP  #
#################

# Turn off warnings
GPIO.setwarnings(False)

# Set pin mapping to board, use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)


class Pin(object):
    def __init__(self, pin_number, jumper_color, relay_number):
        self.pin_number = pin_number
        self.jumper_color = jumper_color
        self.relay_number = relay_number

pin1 = Pin(pin_number=5, jumper_color="green", relay_number=1)
pin2 = Pin(pin_number=6, jumper_color="orange", relay_number=2)
pin3 = Pin(pin_number=13, jumper_color="purple", relay_number=3)
pin4 = Pin(pin_number=19, jumper_color="blue", relay_number=4)
pin5 = Pin(pin_number=26, jumper_color="white", relay_number=5)
pin6 = Pin(pin_number=16, jumper_color="brown", relay_number=6)

pins = [
    pin1, pin2, pin3,
    pin4, pin5, pin6,
]

pin_numbers = [pin.pin_number for pin in pins]
relay_numbers = [pin.relay_number for pin in pins]
relay_pin_map = dict(zip(relay_numbers, pin_numbers))

# GPIO.LOW = relay on, GPIO.HIGH = relay off
on = lambda pin: GPIO.output(pin, GPIO.LOW)
off = lambda pin: GPIO.output(pin, GPIO.HIGH)

# "any" function executes the function on the iterator but doesn't return anything
# This is the same as "for pin in pins: GPIO.setup"
for pin in pin_numbers:
    GPIO.setup(pin, GPIO.OUT)

######################
#    GPIO FUNCTIONS  #
######################


def blink(*, pin_numbers: list, iterations=1, sleep=0.5) -> None:
    """Turn all pins on, sleep, turn all pins off"""
    while iterations > 0:
        any(on(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        any(off(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        iterations -= 1


def step(*, pin_numbers: list, iterations=1, sleep=0.5) -> None:
    """Turn a pin on then off then move onto the next pin"""
    while iterations > 0:
        for pin in pin_numbers:
            on(pin)
            time.sleep(sleep)
            off(pin)
        iterations -= 1


def climb(*, pin_numbers: list, iterations=1, sleep=0.5) -> None:
    """Turn the pins on in order then off in reverse"""
    climb_number = len(pin_numbers)
    reversed_pin_numbers = reversed(pin_numbers)

    while iterations > 0:
        for index, pin in enumerate(pin_numbers):
            if index <= climb_number:
                on(pin)
                time.sleep(sleep)
        for pin in reversed_pin_numbers:
            off(pin)
            time.sleep(sleep)
        iterations -= 1


def lightshow():
    """
    Choose a random light function
    Execute it for a random number of iterations between 1-5
    Sleep for a random time during function between .1 and .5 seconds
    """
    all_pins = pin_numbers
    even_pins = pin_numbers[0:][::2]
    odd_pins = pin_numbers[1:][::2]
    random_pin = [random.choice(pin_numbers)]
    first_half_pins = pin_numbers[:int(len(pin_numbers) / 2)]
    second_half_pins = pin_numbers[int(len(pin_numbers) / 2):]
    random_sleep = float(str(random.uniform(.1, .5))[:4])
    random_iterations = random.choice(list(range(5)))

    functions = [blink, step, climb]
    pin_configs = [
        all_pins, even_pins, odd_pins, 
        first_half_pins, second_half_pins, random_pin
    ]

    random.choice(functions)(
        pin_numbers=random.choice(pin_configs),
        iterations=random_iterations,
        sleep=random_sleep)


def blink_all():
    """Turn all pins on, sleep, turn all pins off"""
    any(on(pin) for pin in pin_numbers)
    time.sleep(0.5)
    any(off(pin) for pin in pin_numbers)
    time.sleep(0.5)

def cycle_all():
    """Turn all pins on in order, sleep, turn all pins off in reverse order"""
    climb(pin_numbers=pin_numbers)

def all_pins_off():
    """Turn off all pins"""
    any(off(pin) for pin in pin_numbers)
