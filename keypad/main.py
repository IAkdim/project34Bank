import serial
import time
from pynput.keyboard import Controller, Key

def process_serial_data(serial_port):
    ser = serial.Serial(serial_port, 9600)
    keyboard = Controller()

    while True:
        line = ser.readline().decode().strip()
        if line.startswith("<") and line.endswith(">"):
            key = line[1:-1]
            if key == 'A':
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif key == 'B':
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            elif key == 'D':
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            else:
                keyboard.press(key)
                keyboard.release(key)
        time.sleep(0.1)  # Adjust the delay if needed

if __name__ == '__main__':
    process_serial_data()