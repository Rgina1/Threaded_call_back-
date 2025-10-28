# Web interface for GPIO control using POST request
#
# Display a user-defined binary value on an LED bar


import RPi.GPIO as GPIO
import threading
from time import sleep
import socket

#from shifter import Shifter    # Use our custom Shifter class
GPIO.setmode(GPIO.BCM)

Led_1, Led_2, Led_3 = 23, 24, 25

GPIO.setup(Led_1, GPIO.OUT)
GPIO.setup(Led_2, GPIO.OUT)
GPIO.setup(Led_3, GPIO.OUT)

pwm_1 = GPIO.PWM(Led_1,100)
pwm_2 = GPIO.PWM(Led_2,100)
pwm_3 = GPIO.PWM(Led_3,100)

pwm_1.start(0)
pwm_2.start(0)
pwm_3.start(0)


def web_page(led1_brightness=0, led2_brightness=0, led3_brightness=0):
    # Define html code, with user text passed from the browser via POST request.
    # Note we cannot use an f-string here since there are HTML style definitions
    # that use the {} syntax!
    html ="""
    <html>
    <head><title>LED Brightness Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html {font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1 {color: #0F3376; padding: 2vh;}
        p {font-size: 1.2rem;}
        .button {
            display: inline-block; background-color: #0F3376; border: none; border-radius: 4px;
            color: white; padding: 12px 30px; text-decoration: none; font-size: 20px;
            margin: 10px; cursor: pointer;
        }
        .slider {width: 60%; margin: 20px;}
        .led-state {font-weight: bold; color: #e7bd3b;}
    </style>
    </head>

    <body>
        <h1>LED Brightness Controller</h1> 
        <p>Select an LED and set its brightness:</p>

        <form action="/" method="POST">
            <p>
                <label><input type="radio" name="led" value="1" required> LED 1</label>
                <label><input type="radio" name="led" value="2"> LED 2</label>
                <label><input type="radio" name="led" value="3"> LED 3</label>
            </p>

            <p>
                <input type="range" name="brightness" min="0" max="100" value="50" class="slider">
            </p>

            <p>
                <button type="submit" class="button">Set Brightness</button>
            </p>
        </form>

        <h2>Current LED Brightness Levels</h2>
        <p>LED 1: <span class="led-state">{led1}%</span></p>
        <p>LED 2: <span class="led-state">{led2}%</span></p>
        <p>LED 3: <span class="led-state">{led3}%</span></p>
    </body>
    </html>
    """.format(led1=led1_brightness, led2=led2_brightness, led3=led3_brightness)

    return bytes(html, 'utf-8')

# Helper function to extract key,value pairs of POST data
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict


def serve_web_page(off = False):

    led_brightness_history ={'led1': 0 ,'led2': 0 , 'led3':0  }

    while not off.is_set():
        print('Waiting for connection...')
        conn, (client_ip, client_port) = s.accept()     # blocking call
        print(f'Connection from {client_ip} on client port {client_port}')
        client_message = conn.recv(2048).decode('utf-8')
        print(f'Message from client:\n{client_message}')
        data_dict = parsePOSTdata(client_message)
        if 'led' in data_dict.keys() and 'brightness' in data_dict.keys():   # make sure data was posted
            led = data_dict["led"]
            brightness = data_dict["brightness"]
                 
        conn.send(b'HTTP/1.1 200 OK\r\n')                  # status line
        conn.send(b'Content-Type: text/html\r\n')          # headers
        conn.send(b'Connection: close\r\n\r\n')

        if int (led) == 1:
            pwm_1.ChangeDutyCycle(int(brightness))
            led_brightness_history['led1'] = brightness
        elif int (led) == 2:
            pwm_2.ChangeDutyCycle(int(brightness))
            led_brightness_history['led2'] = brightness
        elif int (led) == 3:
            pwm_3.ChangeDutyCycle(int(brightness))
            led_brightness_history['led3'] = brightness

        try:
            conn.sendall(web_page(led_brightness_history['led1'],led_brightness_history['led2'],led_brightness_history['led3']))                       # body
        finally:
            conn.close()


           
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pass IP addr & socket type
s.bind(('', 80))     # bind to given port
s.listen(3)          # up to 3 queued connections
off = threading.Event()
webpageTread = threading.Thread(target=serve_web_page, args=(off))
webpageTread.daemon = True
webpageTread.start()

# Do whatever we want while the web server runs in a separate thread:
try:
    while True:
        pass
finally:
    print('Joining webpageTread')
    print('Closing socket')
    off.set()
    webpageTread.join()
    s.close()
    GPIO.cleanup()