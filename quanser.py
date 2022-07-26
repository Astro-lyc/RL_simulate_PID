from quanser.hardware import HIL, MAX_STRING_LENGTH, EncoderQuadratureMode
from quanser.q_misc import Calculus

from array import array

import time

# Define card type as NI PCIe-6351

card = HIL()

card.open("ni_pcie_6351", "0")

card.set_card_specific_options("terminal_board=mx_series;", MAX_STRING_LENGTH)

print("DAQ Initialized")

# Sets the quadrature mode of the encoder inputs on the card

channels = array('I', [0, 1, 2])
num_channels = len(channels)
modes = array('i', [EncoderQuadratureMode.X4, EncoderQuadratureMode.X4, EncoderQuadratureMode.X4])
card.set_encoder_quadrature_mode(channels, num_channels, modes)

# Write Voltage to analog output channel 0 and 1
_ao_channels = array('I', [0])  #
_ao_buffer = array('d', [0])    # Voltage 1
card.write_analog(_ao_channels, len(_ao_channels), _ao_buffer)

_ao_channels2 = array('I', [1])
_ao_buffer2 = array('d', [0])   # Voltage 2
card.write_analog(_ao_channels2, len(_ao_channels2), _ao_buffer2)

time.sleep(0.1)

# Set up a differentiator to get encoderSpeed from encoderCounts
diff_travel = Calculus().differentiator_variable(0.1)
diff_pitch = Calculus().differentiator_variable(0.1)
diff_elevation = Calculus().differentiator_variable(0.1)
next(diff_travel)
next(diff_pitch)
next(diff_elevation)

timestep = 0.1

# Read Encoders channel 0,1,2
for i in range(1000):
    channels = array('I', [0, 1, 2])
    num_channels = len(channels)
    buffer = array('i', [0] * num_channels)
    card.read_encoder(channels, num_channels, buffer)
    travel = float(buffer[0]) / 8192 * 360
    pitch = float(buffer[1]) / 4096 * 360
    elevation = float(buffer[2]) / 4096 * 360

    # Differentiate encoder counts and then estimate linear speed in m/s
    delta_travel = diff_travel.send((buffer[0], timestep))
    delta_pitch = diff_pitch.send((buffer[1], timestep))
    delta_elevation = diff_elevation.send((buffer[2], timestep))
    w_travel = delta_travel / 8192 * 360   # Travel Speed
    w_pitch = delta_pitch / 4096 * 360   # Pitch Speed
    w_elevation = delta_elevation / 4096 * 360   # Elevation Speed

    state = [travel, pitch, elevation, w_travel, w_pitch, w_elevation]
    print(state)
    time.sleep(0.1)


card.close()
