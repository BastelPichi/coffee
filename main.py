import time
import RPi.GPIO as GPIO
from flask import Flask, request, render_template


servo_pin = 11

pos1 = 2.9
pos2 = 2.4

status = "Turned Off"
made = 0

app = Flask(__name__)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)

def servomove():
    pwm.start(0)

    pwm.ChangeDutyCycle(pos2)
    time.sleep(0.35)

    pwm.ChangeDutyCycle(pos1)
    time.sleep(0.35)

@app.route("/")
def index():
    return render_template("index.html", status=status, made=made, date=time.time())


@app.route("/machine", methods=["POST"])
def machine():
    global status, made
    button = request.form.get("onoffbutton")

    if button == "onbutton":
        if status == "Turned Off":
            status = "Turned On"
            print("Coffemachine turned one!")
            servomove()
            return "Turned On! <a href=/>Go back</a>"
        else:
            return "You cant turn on a coffeemachine thats already on... <a href=/>Go back</a>"

    if button == "offbutton":
        if status == "Turned On":
            status = "Turned Off"
            made += 1
            servomove()
            return "Turned Off! <a href=/>Go back</a>"
        else:
            return "You cant turn off a coffemachine thats already off... <a href=/>Go back</a>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
