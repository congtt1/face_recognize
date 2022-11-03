import subprocess
import os
import time

in_gpio_door1 = 488 # pin16 PY.04
in_gpio_door2 = 462 # pin12 PT.05  
in_gpio_door3 = 447 # pin11 PR.04
in_gpio_door4 = 453 # pin7  PS.04

out_gpio_door1 = 499 # pin26  PZ.07 
out_gpio_door2 = 498 # pin24  PZ.06
out_gpio_door3 = 485 # pin22  PY.01
out_gpio_door4 = 487 # pin18  PY.03

def execute_command(cmd):
	try:
		#print(cmd)
		cmd_lits = cmd.split(' ')
		process = subprocess.Popen(cmd_lits, stdout=subprocess.PIPE,
									stderr=subprocess.PIPE)
		out, err = process.communicate()
		get_log = out.decode('UTF-8')
		return get_log
	except Exception as err:
		#print("Execute cmd " + str(err))
		return str(err)

def init_gpio():
	os.system("devmem2 0x0243D050 w 0x0a") 
	os.system("devmem2 0x0243D010 w 0x0a")
	os.system("devmem2 0x0243D008 w 0x0a")
	os.system("devmem2 0x0243D018 w 0x0a")

	os.system("echo 499 > /sys/class/gpio/export")
	os.system("echo out > /sys/class/gpio/PZ.07/direction") 

	os.system("echo 498 > /sys/class/gpio/export")
	os.system("echo out > /sys/class/gpio/PZ.06/direction") 

	os.system("echo 485 > /sys/class/gpio/export")
	os.system("echo out > /sys/class/gpio/PY.01/direction")

	os.system("echo 487 > /sys/class/gpio/export")
	os.system("echo out > /sys/class/gpio/PY.03/direction")


	os.system("echo 488 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/PY.04/direction") 
	
	os.system("echo 462 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/PT.05/direction")

	os.system("echo 447 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/PR.04/direction")

	os.system("echo 453 > /sys/class/gpio/export")
	os.system("echo in > /sys/class/gpio/PS.04/direction")

def read_gpio(pin):
	value = 0
	if pin == in_gpio_door1:
		cmd = f"cat /sys/class/gpio/PY.04/value"
		value = int(execute_command(cmd))
	elif pin == in_gpio_door2:
		cmd = f"cat /sys/class/gpio/PT.05/value"
		value = int(execute_command(cmd))
	elif pin == in_gpio_door3:
		cmd = f"cat /sys/class/gpio/PR.04/value"
		value = int(execute_command(cmd))
	else:
		cmd = f"cat /sys/class/gpio/PS.04/value"
		value = int(execute_command(cmd))
	return value

def write_gpio(pin, value):
	if pin == out_gpio_door1:
		os.system("echo %d > /sys/class/gpio/PZ.07/value" % (value))
	elif pin == out_gpio_door2:
		os.system("echo %d > /sys/class/gpio/PZ.06/value" % (value))
	elif pin == out_gpio_door3:
		os.system("echo %d > /sys/class/gpio/PY.01/value" % (value))
	else:
		os.system("echo %d > /sys/class/gpio/PY.03/value" % (value))


def open_door1():
	write_gpio(out_gpio_door1, 1)
	time.sleep(2)
	write_gpio(out_gpio_door1, 0)

def open_door2():
	write_gpio(out_gpio_door2, 1)
	time.sleep(2)
	write_gpio(out_gpio_door2, 0)

def open_door3():
	write_gpio(out_gpio_door3, 1)
	time.sleep(2)
	write_gpio(out_gpio_door3, 0)

def open_door4():
	write_gpio(out_gpio_door4, 1)
	time.sleep(2)
	write_gpio(out_gpio_door4, 0)

def read_door1():
	return int(read_gpio(in_gpio_door1))

def read_door2():
	return int(read_gpio(in_gpio_door2))

def read_door3():
	return int(read_gpio(in_gpio_door3))

def read_door4():
	return int(read_gpio(in_gpio_door4))

a = time.time()
init_gpio()
print(time.time() - a)
