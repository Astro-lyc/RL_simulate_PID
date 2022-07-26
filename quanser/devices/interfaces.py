import sys
import os

from cffi import FFI

from quanser.devices import RangingDistance, RangingMeasurementMode, RangingMeasurements, DeviceError


# region Setup


ffi = FFI()
ffi.cdef("""
    /* Type Definitions */
    
    typedef unsigned char   t_ubyte;    /* must always be 8 bits */
    typedef t_ubyte         t_uint8;
    typedef t_uint8         t_boolean;
    typedef unsigned short  t_uint16;   /* must always be 16 bits */
    typedef signed int      t_int;      /* must always be 32 bits */
    typedef unsigned int    t_uint;     /* must always be 32 bits */
    typedef t_uint          t_uint32;
    typedef t_int           t_error;
    typedef double          t_double;
    typedef float           t_single;
    typedef unsigned char   t_ubyte;

    typedef struct tag_game_controller * t_game_controller;
    typedef struct tag_ranging_sensor * t_ranging_sensor;
    typedef struct tag_st7032 * t_st7032;
    typedef struct tag_st7066u * t_st7066u;

    typedef enum tag_ranging_sensor_type
    {
        RANGING_SENSOR_TYPE_INVALID,        /* Invalid sensor type */
        RANGING_SENSOR_TYPE_VL53L0,         /* ST Microelectronics VL53L0 time-of-flight sensor */
        RANGING_SENSOR_TYPE_VL53L1,         /* ST Microelectronics VL53L1 time-of-flight sensor */
        RANGING_SENSOR_TYPE_RPLIDAR,        /* Slamtec RPLidar 2D LIDAR sensor */
        RANGING_SENSOR_TYPE_YDLIDAR,        /* YDLIDAR 2D LIDAR sensor */
        RANGING_SENSOR_TYPE_MS10,           /* Leishen MS10 LIDAR sensor */

        NUMBER_OF_RANGING_SENSOR_TYPES = RANGING_SENSOR_TYPE_MS10
    } t_ranging_sensor_type;

    typedef enum tag_ranging_distance
    {
        RANGING_DISTANCE_SHORT,
        RANGING_DISTANCE_MEDIUM,
        RANGING_DISTANCE_LONG,
    
        NUMBER_OF_RANGING_DISTANCES
    } t_ranging_distance;
    
    typedef enum tag_ranging_measurement_mode
    {
        RANGING_MEASUREMENT_MODE_NORMAL,        /* return actual measurement data. Number of measurements will vary and angles will not be consistent between scans. Angles will start close to zero. */
        RANGING_MEASUREMENT_MODE_INTERPOLATED,  /* returns the number of measurements, N, requested. Angles will start at zero and be 360/N apart. Raw measurements will be interpolated to estimate distance at each angle */
        
        NUMBER_OF_RANGING_MEASUREMENT_MODES
    } t_ranging_measurement_mode;
    
    typedef struct tag_ranging_measurement
    {
        t_double distance;          /* the distance in metres */
        t_double distance_sigma;    /* an estimate of the standard deviation in the current distance measurement */
        t_double heading;           /* the heading in radians (will be zero for 1D ranging sensors) */
        t_uint8 quality;            /* an indication of the quality of the measurement (0 to 100%) */
    } t_ranging_measurement;
    
    typedef struct tag_game_controller_states
    {
        t_single x;                 /* x-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single y;                 /* y-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single z;                 /* z-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single rx;                /* rx-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single ry;                /* ry-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single rz;                /* rz-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
        t_single sliders[2];        /* sliders as a percentage of the range. Spans 0.0 to 1.0 */
        t_single point_of_views[4]; /* point-of-view positions (in positive radians or -1 = centred). */
        t_uint32 buttons;           /* state of each of 32 buttons. If the bit corresponding to the button is 0 the button is released. If it is 1 then the button is pressed */
    } t_game_controller_states;

    /* LIDAR Methods */
    
    t_error rplidar_open(const char * uri, t_ranging_distance range, t_ranging_sensor * sensor);
    
    t_int rplidar_read(t_ranging_sensor sensor, t_ranging_measurement_mode mode, t_double maximum_interpolated_distance,
                       t_double maximum_interpolated_angle, t_ranging_measurement * measurements, t_uint num_measurements);

    t_error rplidar_close(t_ranging_sensor sensor);

    /* YDLIDAR 2D LIDAR Sensors */

    t_error ydlidar_open(const char* uri, t_uint samples_per_scan, t_ranging_sensor* sensor);

    t_int ydlidar_read(t_ranging_sensor sensor, t_ranging_measurement_mode mode, t_double maximum_interpolated_distance, t_double maximum_interpolated_angle,
        t_ranging_measurement* measurements, t_uint num_measurements);

    t_error ydlidar_close(t_ranging_sensor sensor);

    /* Leishen MS10 2D LIDAR Sensors */

    t_error leishen_ms10_open(const char* uri, t_uint samples_per_scan, t_ranging_sensor* sensor);

    t_int leishen_ms10_read(t_ranging_sensor sensor, t_ranging_measurement_mode mode, t_double maximum_interpolated_distance, t_double maximum_interpolated_angle,
        t_ranging_measurement* measurements, t_uint num_measurements);

    t_error leishen_ms10_close(t_ranging_sensor sensor);

    /* LCD ST7032Display Methods */
    
    t_error st7032_open(const char * uri, t_st7032 * display);

    t_error st7032_close(t_st7032 display);

    t_int st7032_print(t_st7032 display, t_uint line, t_uint column, const char * message, size_t length);

    t_error st7032_set_character(t_st7032 display, t_int code, const t_uint8 pattern[8]);

    /* LCD ST7066UDisplay Methods */
    
    t_error st7066u_open(const char * uri, t_st7066u * display);

    t_error st7066u_close(t_st7066u display);

    t_int st7066u_print(t_st7066u display, t_uint line, t_uint column, const char * message, size_t length);

    t_error st7066u_set_character(t_st7066u display, t_int code, const t_uint8 pattern[8]);
    
    /* Game Controller methods */

    /* If max_force_feedback_effects == 0 then not f/f. */
    t_error game_controller_open(t_uint8 controller_number, t_uint16 buffer_size, t_double deadzone[6], t_double saturation[6], t_boolean auto_center,
                                 t_uint16 max_force_feedback_effects, t_double force_feedback_gain, t_game_controller * game_controller);
    t_error game_controller_poll(t_game_controller controller, t_game_controller_states * state, t_boolean * is_new);
    t_error game_controller_close(t_game_controller controller); 
""")

devices_lib = ffi.dlopen("quanser_devices")

# endregion

# region Constants

_WOULD_BLOCK = 34

_CHAR_ARRAY = "char[]"

_RANGING_MEASUREMENT_ARRAY = "t_ranging_measurement[]"

# endregion

# region Device Classes


class RPLIDAR:
    """A Python wrapper for the Quanser Devices API interface to RPLIDAR ranging sensors.

    Example
    -------
    >>> from quanser.devices import RPLIDAR
    >>> lidar = RPLIDAR()

    """

    # region Life Cycle

    def __init__(self):
        self._lidar = None

    # endregion

    # region Implementation

    def close(self):
        """Closes the current open RPLIDAR device.

        Example
        -------

        >>> from quanser.devices import RPLIDAR, RangingDistance
        >>> lidar = RPLIDAR()
        >>> lidar.open("serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'",
        ...            RangingDistance.SHORT)
        ... # ...
        ...
        >>> lidar.close()

        """
        if self._lidar is None:
            return

        result = devices_lib.rplidar_close(self._lidar if self._lidar is not None else ffi.NULL)
        if result < 0:
            raise DeviceError(result)

        self._lidar = None

    def open(self, uri, ranging_distance):
        """Opens the specified RPLIDAR device with the given parameters.

        Parameters
        ----------
        uri : string
            A URI used for communicating with the device. Numerous URI parameters are available.
        ranging_distance : RangingDistance
            The type of ranging distance. Valid values are ``RangingDistance.SHORT``, ``RangingDistance.MEDIUM``, and
            ``RangingDistance.LONG``.

        Example
        -------

        >>> from quanser.devices import RPLIDAR, RangingDistance
        >>> lidar = RPLIDAR()
        >>> lidar.open("serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'",
        ...            RangingDistance.LONG)
        ... # ...
        ...
        >>> lidar.close()

        """
        if self._lidar is not None:
            self.close()

        lidar = ffi.new("t_ranging_sensor *")

        result = devices_lib.rplidar_open(uri.encode("UTF-8") if uri is not None else ffi.NULL,
                                          ranging_distance,
                                          lidar if lidar is not None else ffi.NULL)
        if result < 0:
            raise DeviceError(result)

        self._lidar = lidar[0]

    def read(self, mode, max_interpolated_distance, max_interpolated_angle, measurements):
        """Reads LIDAR data from the ranging sensor.

        Parameters
        ----------
        mode : RangingMeasurementMode
            The measurement mode, which determines how the scan data is returned.

            When the measurement mode is ``RangingMeasurementMode.NORMAL``, the "raw" sensor readings from the LIDAR are
            returned (but the values are scaled to the SI units expected). In this case, the number of measurements may
            vary and the angles may not be consistent between scans. Furthermore, while the angles will be in ascending
            order, the first angle may not be zero. It will, however, be close to zero. If the size of the
            `measurements` buffer provided is not large enough, then a ``-QERR_BUFFER_TOO_SMALL`` error will be raised.
            In this case, the function may be called again with a larger buffer.

            When the measurement mode is ``RangingMeasurementMode.INTERPOLATED``, the raw sensor readings from the LIDAR
            are not returned. Instead, the number of "measurements" requested will be returned, in which the angles are
            360/N degrees apart (in radians), where N is the number of measurements requested and the first angle is
            zero. The distances will be interpolated from the raw data, as will the standard deviation and quality.
            Interpolation is only performed between two consecutive valid readings. The advantage of this mode is that
            the angles are always consistent, as are the number of measurements, so the data is easier to process in
            Simulink.
        max_interpolated_distance : float
            In interpolation mode, this is the maximum difference between the distance measurement of contiguous samples
            for which interpolation will be used. Beyond this difference, the distance of the sample with the closest
            angle to the desired heading will be used.
        max_interpolated_angle : float
            In interpolation mode, this is the maximum difference between the angle measurement of contiguous samples
            for which interpolation will be used. Beyond this difference, the distance and quality will be set to zero.
        measurements : RangingMeasurements
            A buffer in which the actual measurement data is stored.

        Return Value
        ------------

        Returns the number of valid measurements. The result may be zero, indicating that no new measurements
        were available.

        Notes
        -----
        If the quality is zero, then it indicates an invalid measurement (no reflected laser pulse).
        
        To efficiently access an array using numpy, use the frombuffer function to wrap the array with
        a numpy array. For example:

        >>> buffer = array.array('i', [0]*7200))
        >>> numpy.frombuffer(buffer)

        Examples
        --------
        Continuously read 100 samples of 720 measurements in normal mode.

        >>> from quanser.devices import RPLIDAR, RangingMeasurements, RangingMeasurementMode
        >>> num_measurements = 720
        >>> measurements = RangingMeasurements(num_measurments)
        >>> lidar = RPLIDAR()
        >>> lidar.open("serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'",
        ...            RangingDistance.LONG)
        >>> for i in range(100):
        ...     lidar.read(RangingMeasurementMode.NORMAL, 0.0, 0.0, measurements)
        ...     # ...
        ...
        >>> lidar.close()

        Continuously read 100 samples, consisting of measurements every half degree, in interpolated mode.

        >>> from quanser.devices import RPLIDAR, RangingMeasurements, RangingMeasurementMode
        >>> num_measurements = 720
        >>> measurements = RangingMeasurements(num_measurements)
        >>> lidar = RPLIDAR()
        >>> lidar.open("serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'",
        ...            RangingDistance.LONG)
        >>> for i in range(100):
        ...     lidar.read(RangingMeasurementMode.INTERPOLATED, 0.05, 0.1, measurements)
        ...     # ...
        ...
        >>> lidar.close()

        """

        num_measurements = sys.maxsize
        if measurements.distance is not None:
            num_measurements = len(measurements.distance)
        if measurements.distance_sigma is not None:
            num_measurements = min(num_measurements, len(measurements.distance_sigma))
        if measurements.heading is not None:
            num_measurements = min(num_measurements, len(measurements.heading))
        if measurements.quality is not None:
            num_measurements = min(num_measurements, len(measurements.quality))
        if num_measurements == sys.maxsize:
            raise DeviceError(-4) # -QERR_INVALID_ARGUMENT

        measurement_buffer = ffi.new("t_ranging_measurement[%d]" % num_measurements)

        result = devices_lib.rplidar_read(self._lidar if self._lidar is not None else ffi.NULL,
                                          mode, max_interpolated_distance, max_interpolated_angle,
                                          measurement_buffer, num_measurements)
        if (result > 0):
            measurements.length = result;
            for i in range(0, result):
                if measurements.distance is not None:
                    measurements.distance[i] = measurement_buffer[i].distance
                if measurements.distance_sigma is not None:
                    measurements.distance_sigma[i] = measurement_buffer[i].distance_sigma
                if measurements.heading is not None:
                    measurements.heading[i] = measurement_buffer[i].heading
                if measurements.quality is not None:
                    measurements.quality[i] = measurement_buffer[i].quality

        if result == -34: # -QERR_WOULD_BLOCK
            result = 0 # indicate no data read
        elif result < 0:
            raise DeviceError(result)

        # Return number of measurements read. May be zero
        return result


class ST7032Display:
    """A Python wrapper for the Quanser Devices API interface to Sitronix ST7032 displays.

    Example
    -------
    >>> from quanser.devices import ST7032Display
    >>> display = ST7032Display()

    """
    # region Life Cycle

    def __init__(self):        
        self._display = None

    # endregion

    # region Implementation

    def open(self, uri):
        """Opens the ST7032 (or NewHaven NHD-C0216C0Z) display.

        Example
        -------

        >>> from quanser.devices import ST7032Display
        >>> display = ST7032Display()
        >>> display.open("i2c-cpu://localhost:8?address=0x3E,baud=400000")
        >>> # ...
        ...
        >>> display.close()

        """
        display = ffi.new("t_st7032 *")
        result = devices_lib.st7032_open(uri.encode("UTF-8") if uri is not None else ffi.NULL, display)

        if result < 0:
            raise DeviceError(result)
            
        self._display = display[0]

    def close(self):
        """Close the display.

        Example
        -------

        >>> from quanser.devices import ST7032Display
        >>> display = ST7032Display()
        >>> display.open("i2c-cpu://localhost:8?address=0x3E,baud=400000")
        >>> # ...
        ...        
        >>> display.close()

        """
        result = devices_lib.st7032_close(self._display if self._display is not None else ffi.NULL)

        if result < 0:
            raise DeviceError(result)

        self._display = None

    def printText(self, line, column, message, length):
        """Print to the display. 

        Parameters
        ----------
        line : int
            The line where the message will be displayed. Line 0 is the first line.
            
        column : int
            The column where the message will be displayed. Column 0 is the first column.
        
        message : string
            The message to display. Unrecognized characters are skipped. If more than 16 characters would be printed on 
            a line then the line is truncated. A newline will cause the characters to be displayed on the next line. 
            As there are only two lines on the display there should only be one newline in the format string. 
            Printing starts at the given line and column. Line 0 is the first line and column 0 is the first column. 

            The format string is UTF-8 and does support Unicode (particularly, Katakana characters).
                        
        length : int
            The length of the `message`.

        Example
        -------
        Print 'Hello, World!' to the top, left corner of the display.

        >>> from quanser.devices import ST7032Display
        >>> display = ST7032Display()
        >>> display.open("i2c-cpu://localhost:8?address=0x3E,baud=400000")
        >>> message = "Hello, world!"
        >>> display.printText(0, 0, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        """

        result = devices_lib.st7032_print(self._display if self._display is not None else ffi.NULL,
                                          line, column,
                                          message.encode("UTF-8") if message is not None else ffi.NULL,
                                          length)

        if result < 0:
            raise DeviceError(result)

    def set_character(self, code, pattern):
        """Defines the character associated with the given character code. 

        Parameters
        ----------
        code : int
            Defines the character associated with the given character code. 
            Valid character codes are 0x10 to 0x17 i.e., '\020' to '\027'. Using these characters will produce the bitmap 
            defined in the pattern for that character.
            
        pattern : bytes
            The pattern defines each line of the character being defined, with the five bits in each byte defining the pixels of that line.
            For example to define the letter T, the pattern would be:

            pattern = b'\x1F\x40\x40\x40\x40\x40\x40\x00'

            0b00011111 (\x1F)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000000 (\x00) <= should generally be zero to allow for cursor
            Note that only bits 0-4 are used. Bit 0 is the rightmost pixel and bit 4 is the leftmost pixel. 
        
        Examples
        --------
        Print a custom character with three lines along the top, middle and bottom. 

        >>> from quanser.devices import ST7032Display
        >>> display = ST7032Display()
        >>> display.open("i2c-cpu://localhost:8?address=0x3E,baud=400000")
        >>> character_code = 0o20
        >>> pattern = b'\x1F\x00\x00\x1F\x00\x00\x1F\x00'
        >>> display.set_character(character_code, pattern)
        >>> message = str(chr(character_code))
        >>> display.printText(0, 0, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        Print a pair of custom characters that give the appearance of a wifi signal strength indicator.

        >>> from quanser.devices import ST7032Display
        >>> display = ST7032Display()
        >>> display.open("i2c-cpu://localhost:8?address=0x3E,baud=400000")
        >>> character_code_left = 0o20
        >>> pattern_left = b'\x00\x00\x00\x01\x05\x15\x15\x15'
        >>> character_code_right = 0o21        
        >>> pattern_right = b'\x01\x05\x15\x15\x15\x15\x15\x15'
        >>> display.set_character(character_code_left, pattern_left)
        >>> display.set_character(character_code_right, pattern_right)
        >>> message = str(chr(character_code_left)) + str(chr(character_code_right))
        >>> display.printText(1, 1, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        """       
        result = devices_lib.st7032_set_character(self._display if self._display is not None else ffi.NULL,
                                                  code, pattern)
    
        if result < 0:
            raise DeviceError(result)

class ST7066UDisplay:
    """A Python wrapper for the Quanser Devices API interface to Sitronix ST7066U displays.

    Example
    -------
    >>> from quanser.devices import ST7066UDisplay
    >>> display = ST7066UDisplay()

    """
    # region Life Cycle

    def __init__(self):        
        self._display = None

    # endregion

    # region Implementation

    def open(self, uri):
        """Opens the ST7066U (or NewHaven NHD-C0216C0Z) display.

        Example
        -------

        >>> from quanser.devices import ST7066UDisplay
        >>> display = ST7066UDisplay()
        >>> display.open("serial://qbot3:0?baud=115200,device='/dev/qbot3_lcd'")
        >>> # ...
        ...
        >>> display.close()

        """
        display = ffi.new("t_st7066u *")
        result = devices_lib.st7066u_open(uri.encode("UTF-8") if uri is not None else ffi.NULL, display)

        if result < 0:
            raise DeviceError(result)
            
        self._display = display[0]

    def close(self):
        """Close the display.

        Example
        -------

        >>> from quanser.devices import ST7066UDisplay
        >>> display = ST7066UDisplay()
        >>> display.open("serial://qbot3:0?baud=115200,device='/dev/qbot3_lcd'")
        >>> # ...
        ...        
        >>> display.close()

        """
        result = devices_lib.st7066u_close(self._display if self._display is not None else ffi.NULL)

        if result < 0:
            raise DeviceError(result)

        self._display = None

    def printText(self, line, column, message, length):
        """Print to the display. 

        Parameters
        ----------
        line : int
            The line where the message will be displayed. Line 0 is the first line.
            
        column : int
            The column where the message will be displayed. Column 0 is the first column.
        
        message : string
            The message to display. Unrecognized characters are skipped. If more than 16 characters would be printed on 
            a line then the line is truncated. A newline will cause the characters to be displayed on the next line. 
            As there are only two lines on the display there should only be one newline in the format string. 
            Printing starts at the given line and column. Line 0 is the first line and column 0 is the first column. 

            The format string is UTF-8 and does support Unicode (particularly, Katakana characters).
                        
        length : int
            The length of the `message`.

        Example
        -------
        Print 'Hello, World!' to the top, left corner of the display.

        >>> from quanser.devices import ST7066UDisplay
        >>> display = ST7066UDisplay()
        >>> display.open("serial://qbot3:0?baud=115200,device='/dev/qbot3_lcd'")
        >>> message = "Hello, world!"
        >>> display.printText(0, 0, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        """

        result = devices_lib.st7066u_print(self._display if self._display is not None else ffi.NULL,
                                          line, column,
                                          message.encode("UTF-8") if message is not None else ffi.NULL,
                                          length)

        if result < 0:
            raise DeviceError(result)

    def set_character(self, code, pattern):
        """Defines the character associated with the given character code. 

        Parameters
        ----------
        code : int
            Defines the character associated with the given character code. 
            Valid character codes are 0x10 to 0x17 i.e., '\020' to '\027'. Using these characters will produce the bitmap 
            defined in the pattern for that character.
            
        pattern : bytes
            The pattern defines each line of the character being defined, with the five bits in each byte defining the pixels of that line.
            For example to define the letter T, the pattern would be:

            pattern = b'\x1F\x40\x40\x40\x40\x40\x40\x00'

            0b00011111 (\x1F)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000100 (\x40)
            0b00000000 (\x00) <= should generally be zero to allow for cursor
            Note that only bits 0-4 are used. Bit 0 is the rightmost pixel and bit 4 is the leftmost pixel. 
        
        Examples
        --------
        Print a custom character with three lines along the top, middle and bottom. 

        >>> from quanser.devices import ST7066UDisplay
        >>> display = ST7066UDisplay()
        >>> display.open("serial://qbot3:0?baud=115200,device='/dev/qbot3_lcd'")
        >>> character_code = 0o20
        >>> pattern = b'\x1F\x00\x00\x1F\x00\x00\x1F\x00'
        >>> display.set_character(character_code, pattern)
        >>> message = str(chr(character_code))
        >>> display.printText(0, 0, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        Print a pair of custom characters that give the appearance of a wifi signal strength indicator.

        >>> from quanser.devices import ST7066UDisplay
        >>> display = ST7066UDisplay()
        >>> display.open("serial://qbot3:0?baud=115200,device='/dev/qbot3_lcd'")
        >>> character_code_left = 0o20
        >>> pattern_left = b'\x00\x00\x00\x01\x05\x15\x15\x15'
        >>> character_code_right = 0o21        
        >>> pattern_right = b'\x01\x05\x15\x15\x15\x15\x15\x15'
        >>> display.set_character(character_code_left, pattern_left)
        >>> display.set_character(character_code_right, pattern_right)
        >>> message = str(chr(character_code_left)) + str(chr(character_code_right))
        >>> display.printText(1, 1, message, len(message))
        >>> # ...
        ...
        >>> display.close()

        """       
        result = devices_lib.st7066u_set_character(self._display if self._display is not None else ffi.NULL,
                                                  code, pattern)
    
        if result < 0:
            raise DeviceError(result)

    # endregion

class GameController:
    """A Python wrapper for the Quanser Devices API interface to game controllers.

    Example
    -------
    >>> from quanser.devices import GameController
    >>> joystick = GameController()

    """
    # region Life Cycle

    def __init__(self):        
        self._controller = None

    # endregion

    # region Implementation

    def open(self, controller_number):
        """Opens a game controller.

        Example
        -------

        >>> from quanser.devices import GameController
        >>> joystick = GameController()
        >>> joystick.open(1)
        >>> # ...
        ...
        >>> joystick.close()

        """
        controller = ffi.new("t_game_controller *")
        result = devices_lib.game_controller_open(controller_number, 64, ffi.NULL, ffi.NULL, 1, 0, 1.0, controller)

        if result < 0:
            raise DeviceError(result)
            
        self._controller = controller[0]

    def close(self):
        """Close the game controller.

        Example
        -------

        >>> from quanser.devices import GameController
        >>> joystick = GameController()
        >>> joystick.open(1)
        >>> # ...
        ...
        >>> joystick.close()

        """
        result = devices_lib.game_controller_close(self._controller if self._controller is not None else ffi.NULL)

        if result < 0:
            raise DeviceError(result)

        self._controller = None

    def poll(self):
        """Poll the game controller state.

        Return Values
        -------------
        The first return value contains the state of the game controller axes, sliders and buttons as an object. The properties of the object are:
                x : float
                    The x-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                y : float
                    The y-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                z : float
                    The z-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                rx : float
                    The rx-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                ry : float
                    The ry-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                rz : float
                    The rz-coordinate as a percentage of the range. Spans -1.0 to +1.0.
                sliders : float[2]
                    The slider positions as a percentage of the range. Spans 0.0 to 1.0.
                point_of_views : float[4]
                    The point-of-view positions in positive radians or -1 (centred).
                buttons : uint32
                    The state of each of 32 buttons as a bitmask. A bit value of 0 indicates the button is released, while a value of 1 indicates the button is pressed.

        The second return value is a boolean indicating whether the state is new since the last time it was polled.

        Example
        -------
        Poll the state of the joystick.

        >>> from quanser.devices import GameController
        >>> joystick = GameController()
        >>> joystick.open(1)
        >>> state, is_new = joystick.poll()
        >>> print("new=%d x=%f y=%f z=%f", is_new, state.x, state.y, state.z)
        ...
        >>> joystick.close()

        """

        c_states = ffi.new("t_game_controller_states *")
        c_is_new = ffi.new("t_boolean *")

        result = devices_lib.game_controller_poll(self._controller if self._controller is not None else ffi.NULL, c_states, c_is_new)

        is_new = bool(c_is_new[0])
        if result == -34:
            is_new = False
        elif result < 0:
            raise DeviceError(result)

        return c_states[0], is_new

    # endregion

# endregion


