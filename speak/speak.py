import pyttsx3

engine = pyttsx3.init()
msg = input("Ingresa que queres que diga: ")
speed = int(input("Speed(100-300)"))

engine.setProperty("rate", speed)
engine.say(msg)
engine.runAndWait()

