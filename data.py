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

# Convert sampling frequency to FS[10:0] value
# Arguments:
#       freq: sampling frequency specified in ad7124.sample_rate
# Returns: FS[10:0] value
def freq2fs(freq):
    return int(fclk / (32 * freq))


# Calculate the real sampling rate of the ADC, which is the sampling rate of each enabled channel
# ad7124.sample_rate is (in general) different from the real sampling rate of each enabled channel as
# ad7124.sample_rate does not take into account of filter type and filter operation mode.
# Instead, ad7124.sample_rate is iio's parameter to specify FS[10:0] value.
# See freq2fs function for more details.
# WARNING: This function assumes number of enabled channels > 1, each channel has the same sampling rate,
#       and we have sinc4 or sinc3 filter. This function reads FS[10:0] from the last enabled channel register.
#       When no data has been collected, the registers may not have been initiated or updated.
# When multipled channels are enabled, ADC is automatically at zero latency mode.
# There is an extra dead time since we are continuously switching channels.
# 
# Arguments: 
#       from_reg: if True, return the real sampling rate of channel 'chan'
#           if False, return the real sampling rate corresponding to ad7124.sample_rate
#       chan: channel number for which to determine filter type (and calculate the sampling rate) (default 0)
# Returns: the sampling rate of each enabled channel
def real_sampling_rate(from_reg: bool, chan=0):
    reg = ad7124._ctrl.reg_read(ad7124.rx_enabled_channels[chan] + 33) 
    if from_reg == True:
        fs = reg % (2**11) # FS[10: 0]
    elif from_reg == False:
        fs = freq2fs(ad7124.sample_rate)
    else: raise ValueError('fr must be True or False!')

    # Dead Time = 30 when the old channel and the new channel both have 
    # an FS[10:0] > 1 or both have an FS[10:0] = 1
    dt = 30
    if reg // (2**21) == 0: # sinc4 filter
        settle = (4 * 32 * fs + dt) / fclk # settle time
    elif reg // (2**21) == 2: # sinc3 filter
        settle = (3 * 32 * fs + dt) / fclk # settle time
    else:
        raise NotImplementedError('filter for real_sampling_rate function must be sinc4 or sinc3!')
#     print(bin(reg), fs, settle)
    return 1 / (settle * len(ad7124.rx_enabled_channels))


# set filter of ADC. Only sinc4 or sinc3 filter (without averaging block) are implemented.
# Arguments:
#       ft: filter type, 'sinc4' or 'sinc3'
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
# Arguments:
#       check_all: if True, print all register values, if False, print only the registers that do not match
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


# Given an array of data, this function will return the position and values of elements lower than the threshold in pairs
# Arguments:
#       data: array of data
#       threshold: threshold value
# Returns: list of tuples containing the position and value of elements lower than the threshold
def find_threshold(data, threshold):
    positions = np.where(data < threshold)[0]
    values = data[positions]
    return list(zip(positions, values))

if __name__ == '__main__':
    # filter type is 'sinc4' or 'sinc3'
    ft = 'sinc3'
    
    ad7124.sample_rate = 1600 if ft == 'sinc4' else 1200
    set_filter(ft)

    data = np.array(ad7124.rx())
#     print(find_threshold(data[3], -990))
    
    # plt.plot(data)
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

#     check_register(check_all=True)
#     print(real_sampling_rate(True, chan=3))
    print(real_sampling_rate(False))
    # pxx, freqs = plt.psd(data[3], ad7124.rx_buffer_size, real_sampling_rate(False))
    # find the frequency where pxx is maximum
    # print(freqs[np.argmax(pxx)])

    plt.tight_layout()
    # plt.savefig('fig/60Hz'+s+'.png')
    plt.show()
