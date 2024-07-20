import subprocess

def ping(server='example.com', count=1, wait_sec=1):
    cmd = "ping -n {} -w {} {}".format(count, wait_sec * 1000, server).split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\r\n")
        total = lines[-3].split(',')[2].split('=')[1].strip()
        loss = lines[-3].split(',')[2].split('=')[1].strip()
        timing = lines[-1].split('=')[1].split('/')

        return {
            'type': 'rtt',
            'min': timing[0].split('ms')[0].strip(),
            'avg': timing[1].split('ms')[0].strip(),
            'max': timing[2].split('ms')[0].strip(),
            'total': total,
            'loss': loss,
        }
    except Exception as e:
        print(e)
        return False


retult = ping(server="8.8.8.8")
print(retult)