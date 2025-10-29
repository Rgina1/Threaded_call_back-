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


def web_page(led1_brightness='0', led2_brightness='0', led3_brightness='0'):
    # Define html code, with user text passed from the browser via POST request.
    # Note we cannot use an f-string here since there are HTML style definitions
    # that use the {} syntax!
    html ="""
    <html>
    <head>
        <title>LED Brightness Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600&display=swap" rel="stylesheet">
        <style>
            /* === Minimal Animated Dark Theme === */
            body {
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #1c1c1e;
                color: #f2f2f7;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                overflow-x: hidden;
            }

            .container {
                background-color: #2c2c2e;
                border-radius: 18px;
                padding: 40px;
                width: 90%;
                max-width: 480px;
                box-sizing: border-box;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
                transition: transform 0.6s ease;
            }

            h1 {
                text-align: center;
                font-weight: 600;
                font-size: 2em;
                color: #ffffff;
                margin: 0 0 10px;
            }

            p {
                text-align: center;
                color: #a1a1a6;
                font-size: 1em;
                margin: 0 0 35px;
            }

            .slider-row {
                display: flex;
                align-items: center;
                margin-bottom: 28px;
                transition: transform 0.2s ease, box-shadow 0.3s ease;
                transform-origin: center;
            }

            .slider-row:last-child {
                margin-bottom: 0;
            }

            label {
                width: 60px;
                font-size: 1em;
                color: #ffffff;
            }

            input[type="range"] {
                -webkit-appearance: none;
                width: 100%;
                height: 6px;
                background: linear-gradient(to right, #0a84ff 50%, #3a3a3c 50%);
                border-radius: 3px;
                outline: none;
                transition: background 0.3s ease;
                margin: 0 16px;
            }

            input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 22px;
                height: 22px;
                background: #0a84ff;
                border-radius: 50%;
                cursor: pointer;
                border: 2px solid #2c2c2e;
                transition: background 0.2s ease, transform 0.2s ease;
            }

            input[type="range"]:active::-webkit-slider-thumb {
                background: #38c2ff;
                transform: scale(1.1);
            }

            input[type="range"]::-moz-range-thumb {
                width: 22px;
                height: 22px;
                background: #0a84ff;
                border-radius: 50%;
                border: 2px solid #2c2c2e;
                cursor: pointer;
            }

            .brightness-value {
                width: 38px;
                text-align: right;
                font-size: 1em;
                font-weight: 600;
                color: #0a84ff;
                transition: color 0.15s ease, transform 0.15s ease;
            }

            .brightness-value.active {
                color: #38c2ff;
                transform: scale(1.1);
            }

            /* === Hover/proximity visual feedback === */
            .slider-row.near {
                transform: translateY(-8px) scale(1.03);
                box-shadow: 0 6px 20px rgba(10, 132, 255, 0.15);
            }

            .slider-row.active {
                transform: translateY(-12px) scale(1.05);
                box-shadow: 0 8px 30px rgba(10, 132, 255, 0.25);
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>LED Brightness</h1>
            <p>Adjust each slider to set LED intensity.</p>

            <div class="slider-row">
                <label for="led1_slider">LED 1</label>
                <input type="range" id="led1_slider" min="0" max="100" value="""+ led1_brightness +""">
                <span id="led1_val" class="brightness-value">"""+ led1_brightness +"""</span>
            </div>

            <div class="slider-row">
                <label for="led2_slider">LED 2</label>
                <input type="range" id="led2_slider" min="0" max="100" value="""+ led2_brightness +""">
                <span id="led2_val" class="brightness-value">"""+ led2_brightness +"""</span>
            </div>

            <div class="slider-row">
                <label for="led3_slider">LED 3</label>
                <input type="range" id="led3_slider" min="0" max="100" value="""+ led3_brightness +""">
                <span id="led3_val" class="brightness-value">"""+ led3_brightness +"""</span>
            </div>
        </div>

        <script>
        document.addEventListener('DOMContentLoaded', () => {
            const sliders = document.querySelectorAll('input[type="range"]');
            const rows = document.querySelectorAll('.slider-row');

            
            sliders.forEach(slider => {
                const ledNum = slider.id.split('_')[0].replace('led', '');
                const valueSpan = document.getElementById('led' + ledNum + '_val');

                const updateSliderVisuals = () => {
                    const value = (slider.value - slider.min) / (slider.max - slider.min) * 100;
                    slider.style.background = `linear-gradient(to right, #0a84ff ${value}%, #3a3a3c ${value}%)`;
                    valueSpan.textContent = slider.value;
                };

                updateSliderVisuals();

                slider.addEventListener('input', () => {
                    updateSliderVisuals();
                    valueSpan.classList.add('active');
                    sendDataToServer(ledNum, slider.value);
                });

                slider.addEventListener('change', () => {
                    valueSpan.classList.remove('active');
                });
            });

           
            document.addEventListener('mousemove', (e) => {
                rows.forEach(row => {
                    const rect = row.getBoundingClientRect();
                    const rowCenterY = rect.top + rect.height / 2;
                    const distance = Math.abs(e.clientY - rowCenterY);

                    if (distance < 30) {
                        row.classList.add('near');
                    } else {
                        row.classList.remove('near');
                    }
                });
            });

            function sendDataToServer(ledNum, brightness) {
                fetch('/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `led=${ledNum}&brightness=${brightness}`
                })
                .then(response => {
                    if (!response.ok) console.error('Server responded with error:', response.status);
                })
                .catch(error => console.error('Fetch error:', error));
            }
        });
        </script>
    </body>
    </html>

    """

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

    led_brightness_history ={'led1': '0' ,'led2': '0' , 'led3': '0' }
    led = '0'
    brightness = '0'
    while not off.is_set():
        try:
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
        except socket.timeout:
            pass




           
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pass IP addr & socket type
s.bind(('', 80))     # bind to given port
s.listen(3)    
s.settimeout(1.0)      
off = threading.Event()
webpageTread = threading.Thread(target=serve_web_page, args=(off,))
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