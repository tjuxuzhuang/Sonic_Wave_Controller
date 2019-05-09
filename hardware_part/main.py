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
        GPIO22 (15) (16) GPIO23     choose3
           3V3 (17) (18) GPIO24     choose4
data0   GPIO10 (19) (20) GND
         GPIO9 (21) (22) GPIO25     choose5
data1   GPIO11 (23) (24) GPIO8      # temp_clk
           GND (25) (26) GPIO7      gate0
         GPIO0 (27) (28) GPIO1
a1       GPIO5 (29) (30) GND
a0       GPIO6 (31) (32) GPIO12     data2
data3   GPIO13 (33) (34) GND
        GPIO19 (35) (36) GPIO16     data6
        GPIO26 (37) (38) GPIO20     choose0
           GND (39) (40) GPIO21     choose1


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
    global choose
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
    choose = [LED(20),LED(21),LED(22),LED(23),LED(24),LED(25)]
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
def output_ram(target,data_for_output):
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
    time.sleep(0.000000100) # >=12ns 0.000000012, set 100 ns here
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
    for i in range(16): # change into 16 bits
        if i < len(bin_):
            bin_num = bin_[-i-1] + bin_num
        else:
            bin_num = "0" + bin_num

    # write into registor
    output_ram(control,"00110000") # write two binary number mode, function 0
    output_ram(t0,bin_num[8:]) # low 8 bit
    output_ram(t0,bin_num[:8]) # high 8 bit
def start_count():
    gate0.on() # start counting
    # output starts to be "high" when count to 0
    pass
def end_count():
    gate0.off() # end counting
    # output starts to be "high" when count to 0
    pass

# board operation level
def channel_select(channel_index):
    cs.on() # close chip-choosing at first
    # change into 8-bit binary num
    bin_ = bin(channel_index)[2:]
    bin_num = ""
    for i in range(8):  # change into 8 bits # add zero
        if i < len(bin_):
            bin_num = bin_[-i - 1] + bin_num
        else:
            bin_num = "0" + bin_num
    # set channel choosing pin according to bin_num
    for i in range(8):
        if bin_num[index] == "0":
            choose[index].off()
        elif bin_num[index] == "1":
            choose[index].on()
        else:
            assert False,"Channel choosing error."
def input_num_to_board(delay_list=[]):
    assert len(delay_list) == 64,"delay list length error, not 64."
    # time-to-number-ratio
    time_to_number_ratio = 1.0
    # output
    for channel_index in range(64):
        channel_select(channel_index)
        # add some exchange for time-to-number
        time_num = int(time_to_number_ratio * delay_list[channel_index])
        set_num_registor(num=time_num)


if __name__ == "__main__":
    # init
    init_GPIO()

    clk_tem = LED(8)
    # main
    interval = 10 # 0.01s one time
    for epotch in range(10000):
        # config registor
        set_num_registor(num=interval)
        start_count()

        # vitural clock ...
        for index in range(interval+5):
            time.sleep(0.005)
            clk_tem.on()
            time.sleep(0.005)
            clk_tem.off()
            if index % 100 == 0:
                print("100 term end ...")

        # end
        end_count()
        # delay
        time.sleep(interval*0.01)

    # end
    exit_GPIO()







