
# import RPi.GPIO as gpio
import time
from gpiozero import LED




#===============#
# Pre-processing
#===============#
def init_GPIO():
    global wr
    global rd
    global cs
    global a1
    global a0
    global gate0
    global gate1
    global gate2
    global data
    global t0
    global t1
    global t2
    global control
    t0 = "t0"
    t1 = "t1"
    t2 = "t2"
    control = "control"
    wr = LED(2)
    rd = LED(3)
    cs = LED(4)
    a1 = LED(5)
    a0 = LED(6)
    gate0 = LED(7)
    gate1 = LED(8)
    gate2 = LED(9)
    data = [LED(10),LED(11),LED(12),LED(13),LED(14),LED(15),LED(16),LED(17)]
    pass

def exit_GPIO():
    pass




#===============#
# API
#===============#
# single pin level
# do not need to write code for single pin level control
# xxx.on() and xxx.off() is efficient enough.

# adress io level
def output_ram(target="",data_for_output="00000000"):
    # note that off sometimes means ON

    # address
    if target == "t0":
        a1.off()
        a0.off()
    if target == "t1":
        a1.off()
        a0.on()
    if target == "t2":
        a1.on()
        a0.off()
    if target == "control":
        a1.on()
        a0.on()

    # Data
    for index in range(8):
        if data_for_output[index] == "0":
            data[index].off()
        elif data_for_output[index] == "1":
            data[index].on()
        else:
            assert False,"data output to ram error, not '0' or '1'."

    # CS
    cs.off()

    # WR
    wr.off() # pull to low
    time.sleep(0.000000100) # >=12ns 0.000000012
    wr.on() # rising-edge triggle

    # exit
    cs.on() # dis-connect
    wr.on() # double high, high-Z
    rd.on() # double high, high-Z

    time.sleep(0.000000100) # may be useless



    pass
def input_ram(target=""):
    pass

# chip operation level
def set_num_registor(num = 100):
    # counter choosing (00 for counter0                        : 00
    # Read/Writer way (01 for low, 10 for high 11 low then high: 11
    # function (001 for funciton 1)                            : 000
    # binary mode( 1 for BCD mode)                             : 0

    # change into binary
    if num>65535:
        assert False,"too big number for registor"
    bin_ = bin(num)[2:]
    bin_num = "0000000000000000"
    for i in range(16):
        if i < len(bin_):
            bin_num[-i-1] = bin_[-i-1]

    # write into registor
    output_ram(control,"00110000") # write two binary number mode, function 0
    output_ram(t0,bin_num[8:]) # low 8 bit
    output_ram(t0,bin_num[:8]) # high 8 bit

def start():
    gate0.on() # start counting
    # output starts to be "high" when count to 0
    pass

if __name__ == "__main__":
    # init
    init_GPIO()

    # main
    set_num_registor(num=200)
    start()



    # end
    exit_GPIO()







