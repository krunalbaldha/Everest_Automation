import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
from time import sleep

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to female voice (can change to 0 for male)
engine.setProperty('rate', 150)  # Speech speed

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

# Task and Reminder Storage
tasks = []
reminders = {}

# Function to Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Listen to Voice Input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return None

# Function to Greet User
def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning Krunal! How can I assist you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon Krunal! How can I help you?")
    else:
        speak("Good evening Krunal! What can I do for you?")

# Function to Add Task
def add_task(command):
    task = command.replace("add task", "").strip()
    tasks.append(task)
    speak(f"Task added: {task}")
    print(f"Current tasks: {tasks}")

# Function to Show Tasks
def show_tasks():
    if tasks:
        speak("Here are your tasks:")
        for i, task in enumerate(tasks, 1):
            speak(f"{i}. {task}")
    else:
        speak("You have no tasks yet.")

# Function to Set Reminder
def set_reminder(command):
    try:
        reminder_text = command.split("in")[0].replace("set reminder", "").strip()
        time_part = command.split("in")[1].strip()
        time_value = int(time_part.split()[0])
        time_unit = time_part.split()[1]

        if "minute" in time_unit:
            delay = time_value * 60
        elif "hour" in time_unit:
            delay = time_value * 3600
        else:
            speak("Please specify time in minutes or hours.")
            return

        reminders[reminder_text] = delay
        speak(f"Reminder set for '{reminder_text}' in {time_value} {time_unit}.")
        sleep(delay)
        speak(f"Reminder: {reminder_text}")
    except Exception as e:
        speak("Sorry, I couldn't set the reminder. Please try again.")
        print(e)

# Function to Open Website
def open_website(command):
    site = command.replace("open", "").strip()
    url = f"https://{site}.com"
    webbrowser.open(url)
    speak(f"Opening {site}")

# Main Assistant Loop
def run_assistant():
    greet_user()
    while True:
        command = listen()
        if command:
            # Exit Command
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break

            # Task Management
            elif "add task" in command:
                add_task(command)
            elif "show tasks" in command:
                show_tasks()

            # Reminder Management
            elif "set reminder" in command:
                set_reminder(command)

            # Web Browsing
            elif "open" in command:
                open_website(command)

            # Daily Briefing
            elif "briefing" in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The current time is {current_time}. Anything else I can help with?")

            # Default Response
            else:
                speak("I'm not sure how to help with that. Try something like 'add task', 'set reminder', or 'open google'.")

if __name__ == "__main__":
    # Ensure required libraries are installed
    try:
        speak("Initializing your AI assistant.")
        run_assistant()
    except Exception as e:
        print(f"Error: {e}")
        speak("There was an error starting the assistant.")