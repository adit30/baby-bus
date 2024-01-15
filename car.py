import wiringpi as wp
from wiringpi import GPIO
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Define GPIO pins for the four motors   #1 bot left 2 front left 3 bot right 4 front right
Motor1A = 12 #front left
Motor1B = 11
Motor2A = 16 #bot right
Motor2B = 15
Motor3A = 9  #front right
Motor3B = 10
Motor4A = 4  #bot left 
Motor4B = 3

PIN_TO_PWM1 = 8  #front two
PIN_TO_PWM2 = 14  #bot two
#PIN_TO_PWM3 = 13  #bot left
#PIN_TO_PWM4 = 16  #front left




# Initialize WiringPi
wp.wiringPiSetup()

for pin in (PIN_TO_PWM1, PIN_TO_PWM2):
    wp.pinMode(pin, wp.GPIO.OUTPUT)
    wp.softPwmCreate(pin, 0, 100)
    wp.softPwmWrite(pin,80) # Change PWM duty cycle



# Set the GPIO pins as outputs, OFF for now (DEBUG MODE)
for pin in (Motor1A, Motor1B, Motor2A, Motor2B, Motor3A, Motor3B, Motor4A, Motor4B):
     wp.pinMode(pin, GPIO.OUTPUT)  # OUTPUT

# Define functions to control the mecanum wheels

def front_left_forward():
    wp.digitalWrite(Motor1A, GPIO.HIGH)
    wp.digitalWrite(Motor1B, GPIO.LOW)

def front_left_backward():
    wp.digitalWrite(Motor1A, GPIO.LOW)
    wp.digitalWrite(Motor1B, GPIO.HIGH)
     
def front_left_stop():
    wp.digitalWrite(Motor1A, GPIO.LOW)
    wp.digitalWrite(Motor1B, GPIO.LOW)
    
def bot_right_forward():
    wp.digitalWrite(Motor2A, GPIO.HIGH)
    wp.digitalWrite(Motor2B, GPIO.LOW)
    
def bot_right_backward():
    wp.digitalWrite(Motor2A, GPIO.LOW)
    wp.digitalWrite(Motor2B, GPIO.HIGH)
    
def bot_right_stop():
    wp.digitalWrite(Motor2A, GPIO.LOW)
    wp.digitalWrite(Motor2B, GPIO.LOW)
    
def front_right_forward():
    wp.digitalWrite(Motor3A, GPIO.HIGH)
    wp.digitalWrite(Motor3B, GPIO.LOW)
    
def front_right_backward():
    wp.digitalWrite(Motor3A, GPIO.LOW)
    wp.digitalWrite(Motor3B, GPIO.HIGH)

def front_right_stop():
    wp.digitalWrite(Motor3A, GPIO.LOW)
    wp.digitalWrite(Motor3B, GPIO.LOW)
     
def bot_left_forward():
    wp.digitalWrite(Motor4A, GPIO.HIGH)
    wp.digitalWrite(Motor4B, GPIO.LOW)
    
def bot_left_backward():
    wp.digitalWrite(Motor4A, GPIO.LOW)
    wp.digitalWrite(Motor4B, GPIO.HIGH)

def bot_left_stop():
    wp.digitalWrite(Motor4A, GPIO.LOW)
    wp.digitalWrite(Motor4B, GPIO.LOW)
    
    
def move_back():   #all backward
    bot_left_backward()
    front_left_backward()
    bot_right_backward()
    front_right_backward()

def move_up():   #all forward
    bot_left_forward()
    front_left_forward()
    bot_right_forward()
    front_right_forward()

def move_left():   #strafe left
    bot_left_backward()
    front_left_forward()
    bot_right_forward()
    front_right_backward()

def move_right():    #strafe right
    bot_left_forward()
    front_left_backward()
    bot_right_backward()
    front_right_forward()

def rotate_right():
    front_left_backward()
    front_right_forward()
    bot_right_stop()
    bot_left_stop()

def rotate_left():
    front_left_forward()
    front_right_backward()
    bot_right_stop()
    bot_left_stop()
    
def spin_left():
    front_left_forward()
    front_right_backward()
    bot_right_backward()
    bot_left_forward()

def spin_right():
    front_left_backward()
    front_right_forward()
    bot_right_forward()
    bot_left_backward()

def stop():
    for pin in (Motor1A, Motor1B, Motor2A, Motor2B, Motor3A, Motor3B, Motor4A, Motor4B):
        wp.digitalWrite(pin, GPIO.LOW)


@app.route("/", methods=["GET", "POST"])
def control_robot():
    if request.method == "POST":
        try:
            data = request.get_json()  # Parse JSON data from request body
            movement = data.get("movement")
            # pwm_value = data.get("pwm_value")  # Get PWM value from JSON data
            
            # pwm_value = 100

            if movement == "forward":
                move_up()
            elif movement == "backward":
                move_back()
            elif movement == "left":
                move_left()
            elif movement == "right":
                move_right()
            elif movement == "rotate_left":
                rotate_left()
            elif movement == "rotate_right":
                rotate_right()
            elif movement == "spin_left":
                spin_left()
            elif movement == "spin_right":
                spin_right()
            elif movement == "stop":
                stop()  # Call the stop function
                
            # wp.softPwmWrite(PIN_TO_PWM1,pwm_value) # Change PWM duty cycle
            # wp.softPwmWrite(PIN_TO_PWM2,pwm_value) # Change PWM duty cycle
            # wp.softPwmWrite(PIN_TO_PWM3,pwm_value) # Change PWM duty cycle
            # wp.softPwmWrite(PIN_TO_PWM4,pwm_value) # Change PWM duty cycle
                

            return jsonify({"message": "Success"})  # Return a JSON response
        except Exception as e:
            return jsonify({"error": str(e)}), 400  # Return an error response if JSON parsing fails

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
