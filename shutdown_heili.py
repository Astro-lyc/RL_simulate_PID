import math

from quanser.hardware import HIL, MAX_STRING_LENGTH, EncoderQuadratureMode
from quanser.q_misc import Calculus

from array import array
# from numpy import array

import time
from torch.utils.tensorboard import SummaryWriter

# Build a tensorboard
writer = SummaryWriter(
    log_dir='tensorboard/quanser_sin')

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

_ao_channels2 = array('I', [1])

time.sleep(0.1)

# Set up a differentiator to get encoderSpeed from encoderCounts
diff_travel = Calculus().differentiator_variable(0.1)
diff_pitch = Calculus().differentiator_variable(0.1)
diff_elevation = Calculus().differentiator_variable(0.1)
next(diff_travel)
next(diff_pitch)
next(diff_elevation)

timestep = 0.1

_ao_buffer = array('d', [0])  # Voltage 1
card.write_analog(_ao_channels, len(_ao_channels), _ao_buffer)
_ao_buffer2 = array('d', [0])  # Voltage 2
card.write_analog(_ao_channels2, len(_ao_channels2), _ao_buffer2)

card.close()
