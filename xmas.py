import RPi.GPIO as GPIO
import time
import pygame
import random
from light_functions import Pin, pins, pin_numbers, relay_numbers, relay_pin_map, on, off


def russian_xmas():

	# GPIO
	# Turn off warnings
	GPIO.setwarnings(False)

	# # Set pin mapping to board, use GPIO numbers not pin numbers
	GPIO.setmode(GPIO.BCM)

	# # Prepare the pins for output
	# "any" function executes the function on the iterator but doesn't return anything
	# This is the same as "for pin in pins: GPIO.setup"
	any(GPIO.setup(pin, GPIO.OUT) for pin in pin_numbers)

	# Open the input sequnce file and read/parse it
	with open("sequence_file.txt",'r') as f:
		seq_data = f.readlines()
		for i in range(len(seq_data)):
			seq_data[i] = seq_data[i].rstrip()

	# Load and play the music
	pygame.mixer.init()
	pygame.mixer.music.load("xmas.mp3")
	pygame.mixer.music.play()

	# Loop through the sequence and turn pins on/off 
	start_time = int(round(time.time()*1000))
	step       = 0 
	while True :
		next_step = seq_data[step].split(",");
		timestamp, pin, state = [int(num.rstrip()) for num in next_step]
		current_time = int(round(time.time()*1000)) - start_time

	  # time to run the command
		if timestamp <= current_time:
		# if the command is Relay 1-6 
			if 1 <= pin <= 6:  

		  # turn the pin on or off depending on the state
				if state:
					on(relay_pin_map[pin])
				else:
					off(relay_pin_map[pin])
				step += 1

		# If last step in sequence
		if step == len(seq_data):
		# if time == 279800:
			GPIO.output(pin_map[logical_map[i]],False)
			break
		

if __name__ == '__main__':
	russian_xmas()