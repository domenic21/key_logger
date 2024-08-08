from pynput import keyboard
from datetime import datetime

# Initialize the key logger with the current timestamp
start_time = datetime.now()
with open("keylog.txt", "a") as log_file:
    log_file.write(f"Script initialized at: {start_time}\n")
print(f"Script initialized at: {start_time}")

# Initialize lists to hold the logged numbers and letters
logged_numbers = []
logged_letters = []

def on_press(key):
    global logged_numbers, logged_letters
    try:
        if hasattr(key, 'char'):
            # Handle alphanumeric keys
            if key.char.isdigit():
                logged_numbers.append(key.char)
                print(f"Number key pressed: {key.char}")
            elif key.char.isalpha():
                if len(logged_letters) < 7:
                    logged_letters.append(key.char)
                    print(f"Letter key pressed: {key.char}")
        elif key.vk in {96, 97, 98, 99, 100, 101, 102, 103, 104, 105}:  # Numpad keys
            numpad_keys = {
                96: '0', 97: '1', 98: '2', 99: '3', 100: '4',
                101: '5', 102: '6', 103: '7', 104: '8', 105: '9'
            }
            numpad_value = numpad_keys.get(key.vk, '')
            if numpad_value:
                logged_numbers.append(numpad_value)
                print(f"Num pad key pressed: {numpad_value}")
            if len(logged_numbers) == 7:
                logged_numbers.append("*")
                print(f"Added asterisk after 7 numbers: {' '.join(logged_numbers)}")
    except AttributeError:
        # Special keys handling (if needed)
        print(f"Special key pressed: {key}")

def write_log():
    global logged_numbers, logged_letters
    with open("keylog.txt", "a") as log_file:
        log_file.write("Numbers: " + " ".join(logged_numbers) + "\n")
        log_file.write("Letters: " + " ".join(logged_letters) + "\n")
    print(f"Logged numbers: {' '.join(logged_numbers)}")
    print(f"Logged letters: {' '.join(logged_letters)}")

def on_release(key):
    if key == keyboard.Key.esc:
        # Log the finalization timestamp and content
        end_time = datetime.now()
        with open("keylog.txt", "a") as log_file:
            log_file.write(f"Script finalized at: {end_time}\n")
            write_log()
        print(f"Script finalized at: {end_time}")
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
