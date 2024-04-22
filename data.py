# This code is modified from Analog Devices Inc. Python package for AD7124

import adi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set up AD7124 
ad7124 = adi.ad7124(uri="ip:localhost")

# Set ADC scale
# sc = ad7124.scale_available
# ad7124.channel[ad_channel].scale = sc[-1]  # get highest range

# Set sample rate for all channels
# ad7124.sample_rate = 1600

# Set the output type of the ADC
ad7124.rx_output_type = "SI"

# Enable channels for data acquisition
ad7124.rx_enabled_channels = [0, 1, 2, 3, 4, 5, 6, 7]

# Set the buffer size for data acquisition
ad7124.rx_buffer_size = 200

# Set the timeout for communication with the ADC
ad7124._ctx.set_timeout(100000)

# clock frequency at full power 
# WARNING: the Python packge may implicitly change power mode
fclk = 614400

# register configuration file recorded from Windows evaluation software
reg0 = pd.read_json('2-3 4-5 Register Map.json')['Registers']


# Returns: the sampling rate of each enabled channel
# WARNING: This function assumes number of enabled channels > 1, each channel has the same sampling rate,
#       and we have sinc4 or sinc3 filter. This function reads FS[10:0] from the last enabled channel register.
#       When no data has been collected, the registers may not have been initiated or updated.
# When multipled channels are enabled, ADC is automatically at zero latency mode.
# There is an extra dead time since we are continuously switching channels.
def real_sampling_rate():
    reg = ad7124._ctrl.reg_read(ad7124.rx_enabled_channels[2] + 33) 
    fs = reg % (2**11) # FS[10: 0]
    # Dead Time = 30 when the old channel and the new channel both have 
    # an FS[10:0] > 1 or both have an FS[10:0] = 1
    dt = 30
    if reg // (2**21) == 0: # sinc4 filter
        settle = (4 * 32 * fs + dt) / fclk # settle time
    elif reg // (2**21) == 2: # sinc3 filter
        settle = (3 * 32 * fs + dt) / fclk # settle time
    else:
        raise NotImplementedError('filter for real_sampling_rate function must be sinc4 or sinc3!')
    print(bin(reg), reg, fs, settle)
    return 1 / (settle * len(ad7124.rx_enabled_channels))


# set filter of ADC. Only sinc4 or sinc3 filter (without averaging block) are implemented.
def set_filter(ft : str):
    if ft != 'sinc4' and ft != 'sinc3':
        raise NotImplementedError('Choose sinc4 or sinc3 filter! Other filters not implemented')
    # s = '000001100000000000000001' # sps 19200
    # s = '000001100000000000001100' # sps 1600
    # s = '000001100000000110000000' # sps 50
    for addr in range(33, 41):
        reg = ad7124._ctrl.reg_read(addr) # read it back
#         print('Register {0:d}: {1:s} has value {2:24b}'.format(addr, reg0[addr]['Name'], reg))
        if ft == 'sinc4':
            reg = reg % (2**21) + 2 ** 21 * 0
        elif ft == 'sinc3':
            reg = reg % (2**21) + 2 ** 21 * 2
        ad7124._ctrl.reg_write(addr, reg)
#         print('Register {0:d}: {1:s} has value {2:24b}'.format(addr, reg0[addr]['Name'], ad7124._ctrl.reg_read(addr)))


# Function to check the register values stored from Windows evaluation software against the actual values read from the ADC
# WARNING: ADC registers do not need to match the values stored in the Windows software to work properly
def check_register(check_all=False):
    for addr in range(57):
        val0 = int(reg0[addr]['Value'], 16)
        reg = ad7124._ctrl.reg_read(addr) # read it back
        if val0 - reg != 0:
            print('Stored value from Windows is {0:24b}\n while ADC is {1:39b} for address {2:d}: {3:s}'
                .format(val0, reg, addr, reg0[addr]['Name']))
        elif check_all:
            print('Stored value from Windows is {0:24b}\n while ADC is {1:39b} for address {2:d}: {3:s}'
                .format(val0, reg, addr, reg0[addr]['Name']))


if __name__ == '__main__':
    # filter type is 'sinc4' or 'sinc3'
    ft = 'sinc3'
    
    ad7124.sample_rate = 1600 if ft == 'sinc4' else 1200
    set_filter(ft)

    data = np.array(ad7124.rx())
    
    # fig, (ax0, ax1) = plt.subplots(2, 1)
    #     plt.plot(data)
    plt.plot(data[0], label='0')
    plt.plot(data[1], label='1')
    plt.plot(data[2], label='2')
    plt.plot(data[3], label='3')
    plt.plot(data[4], label='4')
    plt.plot(data[5], label='5')
    plt.plot(data[6], label='6')
    plt.plot(data[7], label='7')
    plt.grid()
    plt.xlabel('sample')
    plt.ylabel('mV')
    plt.legend(bbox_to_anchor=(1., 1.))

    # plt.psd(data[3], ad7124.rx_buffer_size, real_sampling_rate)
    check_register(check_all=True)
    print(real_sampling_rate())
    plt.tight_layout()
    # plt.savefig('fig/60Hz'+s+'.png')
    plt.show()
