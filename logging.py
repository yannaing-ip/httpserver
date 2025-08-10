import time

def log(message):
    timestamp = time.strftime("[%d/%b/%Y:%H:%M:%S %z]", time.localtime())
    line = f"{timestamp} - {message}"
    print(line)