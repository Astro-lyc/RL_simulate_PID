class Clock:
    """The clocks used to time operations."""
    __slots__ = ()

    SYSTEM_CLOCK_4 = -4
    """System clock 4"""

    SYSTEM_CLOCK_3 = -3
    """System clock 3"""

    SYSTEM_CLOCK_2 = -2
    """System clock 2"""

    SYSTEM_CLOCK_1 = -1
    """System clock 1"""

    HARDWARE_CLOCK_0 = 0
    """Hardware clock 0"""

    HARDWARE_CLOCK_1 = 1
    """Hardware clock 1"""

    HARDWARE_CLOCK_2 = 2
    """Hardware clock 2"""

    HARDWARE_CLOCK_3 = 3
    """Hardware clock 3"""

    HARDWARE_CLOCK_4 = 4
    """Hardware clock 4"""

    HARDWARE_CLOCK_5 = 5
    """Hardware clock 5"""

    HARDWARE_CLOCK_6 = 6
    """Hardware clock 6"""

    HARDWARE_CLOCK_7 = 7
    """Hardware clock 7"""

    HARDWARE_CLOCK_8 = 8
    """Hardware clock 8"""

    HARDWARE_CLOCK_9 = 9
    """Hardware clock 9"""

    HARDWARE_CLOCK_10 = 10
    """Hardware clock 10"""

    HARDWARE_CLOCK_11 = 11
    """Hardware clock 11"""

    HARDWARE_CLOCK_12 = 12
    """Hardware clock 12"""

    HARDWARE_CLOCK_13 = 13
    """Hardware clock 13"""

    HARDWARE_CLOCK_14 = 14
    """Hardware clock 14"""

    HARDWARE_CLOCK_15 = 15
    """Hardware clock 15"""

    HARDWARE_CLOCK_16 = 16
    """Hardware clock 16"""

    HARDWARE_CLOCK_17 = 17
    """Hardware clock 17"""

    HARDWARE_CLOCK_18 = 18
    """Hardware clock 18"""

    HARDWARE_CLOCK_19 = 19
    """Hardware clock 19"""


class ClockMode:
    """The mode for the hardware clocks."""
    __slots__ = ()

    TIMEBASE = 0
    """Allow the clock to be used as a hardware timebase."""

    PWM = 1
    """Use the hardware clock as a PWM output."""

    ENCODER = 2
    """Use the hardware clock as an encoder input."""


class AnalogInputConfiguration:
    """The configuration of the analog inputs."""
    __slots__ = ()

    RSE = 0
    """The input is referenced single-ended."""

    NRSE = 1
    """The input is non-referenced single-ended."""

    DIFF = 2
    """The input is differential."""

    PDIFF = 3
    """The input is pseudo-differential."""


class PWMMode:
    """The mode of a PWM output."""
    __slots__ = ()

    DUTY_CYCLE = 0
    """Values written to a PWM output are interpreted as duty cycles. Duty cycle values must be fractions between 0.0
    and 1.0, where 0.0 indicates 0% and 1.0 denotes 100%. The value may be signed for those boards which support
    bidirectional PWM outputs. The PWM frequency is fixed. The PWM frequency is set using `set_pwm_frequency`."""

    FREQUENCY = 1
    """Values written to a PWM output are interpreted as frequencies. Frequencies must be positive. The PWM duty cycle
    is fixed. The PWM duty cycle is set using `set_pwm_duty_cycle`."""

    PERIOD = 2
    """Values written to a PWM output are interpreted as periods. Periods must be positive. The PWM duty cycle is fixed.
    The PWM duty cycle is set using `set_pwm_duty_cycle`."""

    ONE_SHOT = 3
    """PWM outputs vary in duty cycle. Only a single pulse generated per write."""

    TIME = 4
    """PWM outputs vary in duty cycle by specifying the active pulse time."""

    ENCODER_EMULATION = 5
    """PWM outputs vary in frequency by specifying counts/sec. Paired/complementary signals are 90 degrees out of
    phase."""

    RAW = 6
    """PWM outputs vary in duty cycle by raw board-specific values (used for DSHOT, for example, to allow throttle,
    telemetry, and checksum to be encoded in a PWM output)."""


class PWMConfiguration:
    """The configuration of a PWM output."""
    __slots__ = ()

    UNIPOLAR = 0
    """The PWM output is unipolar."""

    BIPOLAR = 1
    """The PWM output is bipolar. in this case, an analog output is typically used for the PWM signal."""

    PAIRED = 2
    """The PWM output is paired with another output to produce coordinated outputs separated by a programmable deadband."""

    COMPLEMENTARY= 3
    """The PWM output is paired with another output of opposite polarity to produce coordinated outputs separated by a programmable deadband."""


class PWMAlignment:
    """The alignment of a PWM output."""
    __slots__ = ()

    LEADING_EDGE_ALIGNED = 0
    """The PWM output is aligned to the leading edge of the PWM period."""

    TRAILING_EDGE_ALIGNED = 1
    """The PWM output is aligned to the trailing edge of the PWM period."""

    CENTER_ALIGNED = 2
    """The PWM output is aligned to the center of the PWM period."""


class PWMPolarity:
    """The alignment of a PWM output."""
    __slots__ = ()

    ACTIVE_LOW = 0
    """The PWM output is active low."""

    ACTIVE_HIGH = 1
    """The PWM output is active high."""


class DigitalState:
    """The state that the digital outputs will be set to if the watchdog expires."""

    LOW = 0
    """Set the digital output low (ground)."""

    HIGH = 1
    """Set the digital output high (Vcc)."""

    TRISTATE = 2
    """Set the digital output tristate."""

    NO_CHANGE = 3
    """Do not change the expiration state of this digital output."""


class DigitalConfiguration:
    """The configuration of a digital output."""

    OPEN_COLLECTOR = 0
    """Set the digital output to be open-collector (only driven low)."""

    TOTEM_POLE = 1
    """Set the digital output to be a totem pole output (driven high and low)."""


class EncoderQuadratureMode:
    """The quadrature mode of the encoder inputs on the card."""
    __slots__ = ()

    NONE = 0
    """No quadrature. Inputs are count and direction."""

    X1 = 1
    """1X. Inputs are A and B channels."""

    X2 = 2
    """2X. Inputs are A and B channels."""

    X4 = 4
    """4X. Inputs are A and B channels."""



class IntegerProperty:
    """The common or board-specific integer property."""
    __slots__ = ()

    # Product identification
    VENDOR_ID = 0
    """The identifier of the vendor associated with the board."""

    PRODUCT_ID = 1
    """The product identifier of the board."""

    SUBVENDOR_ID = 2
    """The identifier of the subvendor associated with the board."""

    SUBPRODUCT_ID = 3
    """The subproduct identifier of the board."""

    # Product version information
    MAJOR_VERSION = 4
    """The major version number of the board. For example, if the version is 2.7.1.9 then the major version is 2."""

    MINOR_VERSION = 5
    """The minor version number of the board. For example, if the version is 2.7.1.9 then the minor version is 7."""

    BUILD = 6
    """The build number of the board. For example, if the version is 2.7.1.9 then the build number is 1."""

    REVISION = 7
    """The revision number of the board. For example, if the version is 2.7.1.9 then the revision number is 9."""

    DATE = 8
    """The date the board was designed or manufactured, in days, since January 1, 2000."""

    TIME = 9
    """The time the board was designed or manufactured in milliseconds."""

    # Firmware version information
    FIRMWARE_MAJOR_VERSION = 10
    """The major version number of the board's firmware."""

    FIRMWARE_MINOR_VERSION = 11
    """The minor version number of the board's firmware."""

    FIRMWARE_BUILD = 12
    """The build version number of the board's firmware."""

    FIRMWARE_REVISION = 13
    """The revision version number of the board's firmware."""

    FIRMWARE_DATE = 14
    """The date the board's firmware was designed or created, in days, since January 1, 2000."""

    FIRMWARE_TIME = 15
    """The date the board's firmware was designed or created in milliseconds."""

    # Channel information
    NUMBER_OF_ANALOG_INPUTS = 16
    """The number of analog input channels the board supports."""

    NUMBER_OF_ENCODER_INPUTS = 17
    """The number of encoder input channels the board supports."""

    NUMBER_OF_DIGITAL_INPUTS = 18
    """The number of digital input channels the board supports."""

    NUMBER_OF_OTHER_INPUTS = 19
    """The number of other input channels the board supports."""

    NUMBER_OF_ANALOG_OUTPUTS = 20
    """The number of analog output channels the board supports."""

    NUMBER_OF_PWM_OUTPUTS = 21
    """The number of PWM output channels the board supports."""

    NUMBER_OF_DIGITAL_OUTPUTS = 22
    """The number of digital output channels the board supports."""

    NUMBER_OF_OTHER_OUTPUTS = 23
    """The number of other output channels the board supports."""

    NUMBER_OF_CLOCKS = 24
    """The number of hardware clocks the board supports."""

    NUMBER_OF_INTERRUPTS = 25
    """The number of interrupts the board supports."""

    PRODUCT_SPECIFIC = 128

    # HiQ-specific integer properties
    HIQ_GYRO_RANGE = PRODUCT_SPECIFIC
    """The range of the gyro for the HIQ board."""

    HIQ_MAGNETOMETER_MODE = PRODUCT_SPECIFIC + 1
    """The magnetometer mode of the HIQ board."""

    HIQ_BLDC_MAX_PWM_TICKS = PRODUCT_SPECIFIC + 2
    """The BLDC max PWM ticks of the HIQ board."""

    HIQ_BLDC_RAMPUP_DELAY = PRODUCT_SPECIFIC + 3
    """The BLDC ramp up delay of the HIQ board."""

    HIQ_BLDC_MAX_DUTY_CYCLE = PRODUCT_SPECIFIC + 4
    """The BLDC max duty cycle of the HIQ board."""

    HIQ_BLDC_MIN_DUTY_CYCLE = PRODUCT_SPECIFIC + 5
    """The BLDC min duty cycle of the HIQ board."""

    HIQ_BLDC_POLE_PAIRS = PRODUCT_SPECIFIC + 6
    """The BLDC pole pairs of the HIQ board."""

    HIQ_PWM_MODE = PRODUCT_SPECIFIC + 7
    """The PWM mode of the HIQ board."""

    # QBus-specific integer properties
    QBUS_NUM_MODULES = PRODUCT_SPECIFIC
    """The number of modules for the QBUS board."""

    # Kobuki-specific integer properties
    KOBUKI_UDID0 = PRODUCT_SPECIFIC
    """UDID0 for the KOBUKI board."""

    KOBUKI_UDID1 = PRODUCT_SPECIFIC + 1
    """UDID1 for the KOBUKI board."""

    KOBUKI_UDID2 = PRODUCT_SPECIFIC + 2
    """UDID2 for the KOBUKI board."""


class DoubleProperty:
    """The common or board-specific double property."""
    __slots__ = ()

    PRODUCT_SPECIFIC = 128

    # HiQ-specific double properties
    HIQ_SERVO_FINAL_VALUE_CH_0 = PRODUCT_SPECIFIC
    """The servo final value for channel 0 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_1 = PRODUCT_SPECIFIC + 1
    """The servo final value for channel 1 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_2 = PRODUCT_SPECIFIC + 2
    """The servo final value for channel 2 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_3 = PRODUCT_SPECIFIC + 3
    """The servo final value for channel 3 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_4 = PRODUCT_SPECIFIC + 4
    """The servo final value for channel 4 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_5 = PRODUCT_SPECIFIC + 5
    """The servo final value for channel 5 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_6 = PRODUCT_SPECIFIC + 6
    """The servo final value for channel 6 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_7 = PRODUCT_SPECIFIC + 7
    """The servo final value for channel 7 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_8 = PRODUCT_SPECIFIC + 8
    """The servo final value for channel 8 on the HIQ board."""

    HIQ_SERVO_FINAL_VALUE_CH_9 = PRODUCT_SPECIFIC + 9
    """The servo final value for channel 9 on the HIQ board."""

    # Kobuki-specific double properties
    KOBUKI_P_GAIN = PRODUCT_SPECIFIC
    """The `P` gain for the KOBUKI board."""

    KOBUKI_I_GAIN = PRODUCT_SPECIFIC + 1
    """The `I` gain for the KOBUKI board."""

    KOBUKI_D_GAIN = PRODUCT_SPECIFIC + 2
    """The `D` gain for the KOBUKI board."""


class StringProperty:
    """The common or board-specific string property."""
    __slots__ = ()

    MANUFACTURER = 0
    """The name of the manufacturer of the board."""

    PRODUCT_NAME = 1
    """The product name for the board."""

    MODEL_NAME = 2
    """The model name for the board."""

    SERIAL_NUMBER = 3
    """The serial number of the board."""

    FIRMWARE_VERSION = 4
    """The firmware version of the board. This value may not match the integer properties, as some firmware versions
    are better expressed as a string."""

    PRODUCT_SPECIFIC = 128

        
class BufferOverflowMode:
    """The buffer overflow mode for HIL tasks."""
    __slots__ = ()

    ERROR_ON_OVERFLOW = 0
    """Return an error on buffer overflow."""

    OVERWRITE_ON_OVERFLOW = 1
    """Overwrite old samples on buffer overflow."""

    DISCARD_ON_OVERFLOW = 2
    """Discard new samples on buffer overflow."""

    WAIT_ON_OVERFLOW = 3
    """Waits on buffer overflow for space to become available (not supported by hardware cards. Only for use by simulated cards)."""

    SYNCHRONIZED = 4
    """Provides complete buffer synchronization (not supported by hardware cards. Only for use by simulated cards)."""
