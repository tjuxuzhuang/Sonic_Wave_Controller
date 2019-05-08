"""
pinout
,--------------------------------.
| oooooooooooooooooooo J8     +====
| 1ooooooooooooooooooo      P | USB
|  Wi                     ooo +====
|  Fi  Pi Model 3B+ V1.3  ooE    |
|        ,----.               +====
| |D|    |SoC |               | USB
| |S|    |    |               +====
| |I|    `----'                  |
|                   |C|     +======
|                   |S|     |   Net
| pwr        |HDMI| |I||A|  +======
`-| |--------|    |----|V|-------'


          3V3  (1) (2)  5V
wr      GPIO2  (3) (4)  5V
rd      GPIO3  (5) (6)  GND
cs      GPIO4  (7) (8)  GPIO14      data4
          GND  (9) (10) GPIO15      data5
data7   GPIO17 (11) (12) GPIO18
        GPIO27 (13) (14) GND
        GPIO22 (15) (16) GPIO23
           3V3 (17) (18) GPIO24
data0   GPIO10 (19) (20) GND
         GPIO9 (21) (22) GPIO25
data1   GPIO11 (23) (24) GPIO8      # temp_clk
           GND (25) (26) GPIO7      gate0
         GPIO0 (27) (28) GPIO1
a1       GPIO5 (29) (30) GND
a0       GPIO6 (31) (32) GPIO12     data2
data3   GPIO13 (33) (34) GND
        GPIO19 (35) (36) GPIO16     data6
        GPIO26 (37) (38) GPIO20
           GND (39) (40) GPIO21


"""

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
    # gate1 = LED(8)
    # gate2 = LED(9)
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
        if data_for_output[-index-1] == "0":
            data[index].off()
        elif data_for_output[-index-1] == "1":
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
    bin_num = ""

    for i in range(16):
        if i < len(bin_):
            bin_num = bin_[-i-1] + bin_num
        else:
            bin_num = "0" + bin_num

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

    clk_tem = LED(8)
    # main
    interval = 10
    for epotch in range(1000):
        set_num_registor(num=interval)
        start()
        for index in range(interval):
            time.sleep(0.01)
            clk_tem.on()
            time.sleep(0.01)
            clk_tem.off()
            if index % 100 == 0:
                print("100 term end ...")

        print("end .")
        time.sleep(1/interval)


    # end
    exit_GPIO()







