import subprocess
from utils.bcolors import Bcolors


# print colored text
def print_c(text, style, newLine=False):
    if newLine:
        print(style + text + Bcolors.ENDC, end='')
    else:
        print(style + text + Bcolors.ENDC)


def send_message(text):
    subprocess.Popen(['notify-send', text])


# get ping of server
def ping(server='example.com', count=1, wait_sec=1):
    cmd = "ping -n {} -w {} {}".format(count, wait_sec, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-3].split(',')[2].split('=')[1].strip()
        loss = lines[-3].split(',')[2].split('=')[1].strip()
        timing = lines[-1].split(',')
        return {
            'type': 'rtt',
            'min': timing[0].split('=')[1].split('ms')[0].strip(),
            'avg': timing[1].split('=')[1].split('ms')[0].strip(),
            'max': timing[2].split('=')[1].split('ms')[0].strip(),
            'total': total,
            'loss': loss,
        }
    except Exception as e:
        # print(e)
        return False
    

# Get ping ipv6
def ping6(server='example.com', count=1, wait_sec=1):
    cmd = "ping -n {} -w {} -6 {}".format(count, wait_sec, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        total = lines[-3].split(',')[2].split('=')[1].strip()
        loss = lines[-3].split(',')[2].split('=')[1].strip()
        timing = lines[-1].split(',')
        return {
            'type': 'rtt',
            'min': timing[0].split('=')[1].split('ms')[0].strip(),
            'avg': timing[1].split('=')[1].split('ms')[0].strip(),
            'max': timing[2].split('=')[1].split('ms')[0].strip(),
            'total': total,
            'loss': loss,
        }
    except Exception as e:
        # print(e)
        return False
