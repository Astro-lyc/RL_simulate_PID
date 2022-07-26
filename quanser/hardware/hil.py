import os
import sys

from cffi import FFI

from quanser.hardware import (AnalogInputConfiguration, Clock, ClockMode, DigitalState, EncoderQuadratureMode, PWMMode,
                              IntegerProperty, DoubleProperty, StringProperty, HILError, Version, MAX_STRING_LENGTH)

# region Variables

_is_legacy_python = sys.version_info < (3, 0)

# endregion

# region Setup


ffi = FFI()
ffi.cdef("""
    /* Type Definitions */

    typedef char            t_boolean;
    typedef unsigned int    t_uint;
    typedef unsigned short  t_ushort;
    typedef t_ushort        t_uint16;
    typedef t_uint          t_uint32;
    typedef signed int      t_int;
    typedef t_int           t_int32;
    typedef t_int           t_error;
    typedef double          t_double;
            
    typedef struct tag_card*    t_card;
    typedef struct tag_task*    t_task;
    
    typedef struct tag_version
    {
        t_uint32 size;
        t_uint16 major;
        t_uint16 minor;
        t_uint16 release;
        t_uint16 build;
    } t_version;
    
    typedef enum tag_clock
    {
        SYSTEM_CLOCK_4    = -4,
        SYSTEM_CLOCK_3    = -3,
        SYSTEM_CLOCK_2    = -2,
        SYSTEM_CLOCK_1    = -1,
    
        HARDWARE_CLOCK_0  = 0,
        HARDWARE_CLOCK_1  = 1,
        HARDWARE_CLOCK_2  = 2,
        HARDWARE_CLOCK_3  = 3,
        HARDWARE_CLOCK_4  = 4,
        HARDWARE_CLOCK_5  = 5,
        HARDWARE_CLOCK_6  = 6,
        HARDWARE_CLOCK_7  = 7,
        HARDWARE_CLOCK_8  = 8,
        HARDWARE_CLOCK_9  = 9,
        HARDWARE_CLOCK_10 = 10,
        HARDWARE_CLOCK_11 = 11,
        HARDWARE_CLOCK_12 = 12,
        HARDWARE_CLOCK_13 = 13,
        HARDWARE_CLOCK_14 = 14,
        HARDWARE_CLOCK_15 = 15,
        HARDWARE_CLOCK_16 = 16,
        HARDWARE_CLOCK_17 = 17,
        HARDWARE_CLOCK_18 = 18,
        HARDWARE_CLOCK_19 = 19
    } t_clock;
    
    typedef enum tag_clock_mode
    {
        CLOCK_TIMEBASE_MODE,
        CLOCK_PWM_MODE,
        CLOCK_ENCODER_MODE,

        NUMBER_OF_CLOCK_MODES
    } t_clock_mode;
    
    typedef enum tag_analog_input_configuration
    {
        ANALOG_INPUT_RSE_CONFIGURATION,
        ANALOG_INPUT_NRSE_CONFIGURATION,
        ANALOG_INPUT_DIFF_CONFIGURATION,
        ANALOG_INPUT_PDIFF_CONFIGURATION,

        NUMBER_OF_ANALOG_INPUT_CONFIGURATIONS
    } t_analog_input_configuration;

    typedef enum tag_pwm_mode
    {
        PWM_DUTY_CYCLE_MODE,
        PWM_FREQUENCY_MODE,
        PWM_PERIOD_MODE,
        PWM_ONE_SHOT_MODE,
        PWM_TIME_MODE,
        PWM_ENCODER_EMULATION_MODE,
        PWM_RAW_MODE
    } t_pwm_mode;

    typedef enum tag_pwm_configuration
    {
        PWM_UNIPOLAR_CONFIGURATION,
        PWM_BIPOLAR_CONFIGURATION,
        PWM_PAIRED_CONFIGURATION,
        PWM_COMPLEMENTARY_CONFIGURATION,

        NUMBER_OF_PWM_CONFIGURATIONS
    } t_pwm_configuration;

    typedef enum tag_pwm_alignment
    {
        PWM_LEADING_EDGE_ALIGNED,
        PWM_TRAILING_EDGE_ALIGNED,
        PWM_CENTER_ALIGNED,

        NUMBER_OF_PWM_ALIGNMENTS
    } t_pwm_alignment;

    typedef enum tag_pwm_polarity
    {
        PWM_ACTIVE_LOW_POLARITY,
        PWM_ACTIVE_HIGH_POLARITY,

        NUMBER_OF_PWM_POLARITIES
    } t_pwm_polarity;

    typedef enum tag_encoder_quadrature_mode
    {
        ENCODER_QUADRATURE_NONE = 0,
        ENCODER_QUADRATURE_1X   = 1,
        ENCODER_QUADRATURE_2X   = 2,
        ENCODER_QUADRATURE_4X   = 4
    } t_encoder_quadrature_mode;
    
    typedef enum tag_digital_configuration
    {
        DIGITAL_OPEN_COLLECTOR_CONFIGURATION,   /* 0 = open collector */
        DIGITAL_TOTEM_POLE_CONFIGURATION,       /* 1 = totem-pole */

        NUMBER_OF_DIGITAL_CONFIGURATIONS
    } t_digital_configuration;

    typedef enum tag_digital_state
    {
        DIGITAL_STATE_LOW,
        DIGITAL_STATE_HIGH,
        DIGITAL_STATE_TRISTATE,
        DIGITAL_STATE_NO_CHANGE,

        NUM_DIGITAL_STATES
    } t_digital_state;

    typedef enum tag_hil_integer_property
    {
        /* Product identification */
        PROPERTY_INTEGER_VENDOR_ID,
        PROPERTY_INTEGER_PRODUCT_ID,
        PROPERTY_INTEGER_SUBVENDOR_ID,
        PROPERTY_INTEGER_SUBPRODUCT_ID,

        /* Product version information */
        PROPERTY_INTEGER_MAJOR_VERSION,
        PROPERTY_INTEGER_MINOR_VERSION,
        PROPERTY_INTEGER_BUILD,
        PROPERTY_INTEGER_REVISION,
        PROPERTY_INTEGER_DATE,
        PROPERTY_INTEGER_TIME,

        /* Firmware version information */
        PROPERTY_INTEGER_FIRMWARE_MAJOR_VERSION,
        PROPERTY_INTEGER_FIRMWARE_MINOR_VERSION,
        PROPERTY_INTEGER_FIRMWARE_BUILD,
        PROPERTY_INTEGER_FIRMWARE_REVISION,
        PROPERTY_INTEGER_FIRMWARE_DATE,
        PROPERTY_INTEGER_FIRMWARE_TIME,

        /* Channel information */
        PROPERTY_INTEGER_NUMBER_OF_ANALOG_INPUTS,
        PROPERTY_INTEGER_NUMBER_OF_ENCODER_INPUTS,
        PROPERTY_INTEGER_NUMBER_OF_DIGITAL_INPUTS,
        PROPERTY_INTEGER_NUMBER_OF_OTHER_INPUTS,

        PROPERTY_INTEGER_NUMBER_OF_ANALOG_OUTPUTS,
        PROPERTY_INTEGER_NUMBER_OF_PWM_OUTPUTS,
        PROPERTY_INTEGER_NUMBER_OF_DIGITAL_OUTPUTS,
        PROPERTY_INTEGER_NUMBER_OF_OTHER_OUTPUTS,

        PROPERTY_INTEGER_NUMBER_OF_CLOCKS,
        PROPERTY_INTEGER_NUMBER_OF_INTERRUPTS,

        PROPERTY_INTEGER_PRODUCT_SPECIFIC = 128,

        /* HiQ specific integer properties */
        PROPERTY_INTEGER_HIQ_GYRO_RANGE = PROPERTY_INTEGER_PRODUCT_SPECIFIC,
        PROPERTY_INTEGER_HIQ_MAGNETOMETER_MODE,
        PROPERTY_INTEGER_HIQ_BLDC_MAX_PWM_TICKS,
        PROPERTY_INTEGER_HIQ_BLDC_RAMPUP_DELAY,
        PROPERTY_INTEGER_HIQ_BLDC_MAX_DUTY_CYCLE,
        PROPERTY_INTEGER_HIQ_BLDC_MIN_DUTY_CYCLE,
        PROPERTY_INTEGER_HIQ_BLDC_POLE_PAIRS,
        PROPERTY_INTEGER_HIQ_PWM_MODE,

        /* QBus specific integer properties */
        PROPERTY_INTEGER_QBUS_NUM_MODULES = PROPERTY_INTEGER_PRODUCT_SPECIFIC,

        /* Kobuki specific integer properties */
        PROPERTY_INTEGER_KOBUKI_UDID0 = PROPERTY_INTEGER_PRODUCT_SPECIFIC,
        PROPERTY_INTEGER_KOBUKI_UDID1,
        PROPERTY_INTEGER_KOBUKI_UDID2
    } t_hil_integer_property;

    typedef enum tag_hil_double_property
    {
        PROPERTY_DOUBLE_PRODUCT_SPECIFIC = 128,

        /* HiQ specific double properties */
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_0 = PROPERTY_DOUBLE_PRODUCT_SPECIFIC,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_1,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_2,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_3,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_4,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_5,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_6,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_7,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_8,
        PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_9,

        /* Kobuki-specific double properties */
        PROPERTY_DOUBLE_KOBUKI_P_GAIN = PROPERTY_DOUBLE_PRODUCT_SPECIFIC,
        PROPERTY_DOUBLE_KOBUKI_I_GAIN,
        PROPERTY_DOUBLE_KOBUKI_D_GAIN

    } t_hil_double_property;

    typedef enum tag_hil_string_property
    {
        PROPERTY_STRING_MANUFACTURER,
        PROPERTY_STRING_PRODUCT_NAME,
        PROPERTY_STRING_MODEL_NAME,
        PROPERTY_STRING_SERIAL_NUMBER,
        PROPERTY_STRING_FIRMWARE_VERSION,

        PROPERTY_STRING_PRODUCT_SPECIFIC = 128

    } t_hil_string_property;

    typedef enum tag_buffer_overflow_mode
    {
        BUFFER_MODE_ERROR_ON_OVERFLOW,      /* return an error on buffer overflow (default). */
        BUFFER_MODE_OVERWRITE_ON_OVERFLOW,  /* overwrite old samples on buffer overflow. */
        BUFFER_MODE_DISCARD_ON_OVERFLOW,    /* discard new samples on buffer overflow. */
        BUFFER_MODE_WAIT_ON_OVERFLOW,       /* waits on buffer overflow for space to become available (not supported by hardware cards, only for use by simulated cards) */
        BUFFER_MODE_SYNCHRONIZE,            /* provides complete buffer synchronization (not supported by hardware cards, only for use by simulated cards) */

        NUMBER_OF_BUFFER_OVERFLOW_MODES
    } t_buffer_overflow_mode;

    /* Configuration Functions */
    
    t_error hil_close(t_card card);
    
    t_error hil_close_all(void);
    
    t_error hil_open(const char* card_type, const char* card_identifier, t_card* card);

    t_error hil_set_analog_input_configuration(t_card card,
                                               const t_uint32 analog_channels[], t_uint32 num_channels, 
                                               const t_analog_input_configuration config[]);
    
    t_error hil_set_analog_input_ranges(t_card card,
                                        const t_uint32 analog_channels[], t_uint32 num_channels, 
                                        const t_double minimums[], const t_double maximums[]);
                                        
    t_error hil_set_analog_output_ranges(t_card card,
                                         const t_uint32 analog_channels[], t_uint32 num_channels, 
                                         const t_double minimums[], const t_double maximums[]);

    t_error hil_set_clock_mode(t_card card,
                               const t_clock clocks[], t_uint32 num_clocks,
                               const t_clock_mode modes[]);
    
    t_error hil_set_digital_directions(t_card card,
                                       const t_uint32 digital_inputs[], t_uint32 num_digital_inputs,
                                       const t_uint32 digital_outputs[], t_uint32 num_digital_outputs);
                         
    t_error hil_set_digital_output_configuration(t_card card, const t_uint32 channels[], t_uint32 num_channels, const t_digital_configuration configurations[]);

    t_error hil_set_encoder_counts(t_card card,
                                   const t_uint32 encoder_channels[], t_uint32 num_channels,
                                   const t_int32 buffer[]);

    t_error hil_set_encoder_filter_frequency(t_card card,
                                             const t_uint32 encoder_channels[], t_uint32 num_channels,
                                             const t_double frequency[]);
                                             
    t_error hil_set_encoder_quadrature_mode(t_card card,
                                            const t_uint32 encoder_channels[], t_uint32 num_channels,
                                            const t_encoder_quadrature_mode mode[]);
                                            
    t_error hil_set_pwm_mode(t_card card,
                             const t_uint32 pwm_channels[], t_uint32 num_channels,
                             const t_pwm_mode mode[]);
                             
    t_error hil_set_pwm_configuration(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_pwm_configuration configurations[],
                                      const t_pwm_alignment alignments[], const t_pwm_polarity polarities[]);

    t_error hil_set_pwm_deadband(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double leading_edge_deadband[], const t_double trailing_edge_deadband[]);

    t_error hil_set_pwm_frequency(t_card card,
                                  const t_uint32 pwm_channels[], t_uint32 num_channels,
                                  const t_double frequency[]);
                                  
    t_error hil_set_pwm_duty_cycle(t_card card,
                                   const t_uint32 pwm_channels[], t_uint32 num_channels,
                                   const t_double duty_cycle[]);

    t_error hil_set_card_specific_options(t_card card,
                                          const char* options, size_t options_size);

    /* Information Functions */
    
    t_error hil_get_version(t_version* version);
    
    t_boolean hil_is_valid(t_card card);
    
    /* Property Functions */

    t_error hil_get_integer_property(t_card card, 
                                    const t_hil_integer_property properties[], t_uint32 num_properties, 
                                    t_int buffer[]);

    t_error hil_get_double_property(t_card card, 
                                    const t_hil_double_property properties[], t_uint32 num_properties, 
                                    t_double buffer[]);

    t_error hil_get_string_property(t_card card, 
                                    t_hil_string_property property_code, char * buffer, 
                                    size_t buffer_size);

    t_error hil_set_integer_property(t_card card, 
                                    const t_hil_integer_property properties[], t_uint32 num_properties, 
                                    const t_int buffer[]);
                                        
    t_error hil_set_double_property(t_card card, 
                                    const t_hil_double_property properties[], t_uint32 num_properties, 
                                    const t_double buffer[]);

    t_error hil_set_string_property(t_card card, 
                                    const t_hil_string_property property_code, const char * buffer, 
                                    size_t buffer_size);
    
    /* Immediate I/O Functions */
    
    t_error hil_read_analog(t_card card,
                            const t_uint32 analog_channels[], t_uint32 num_channels,
                            t_double buffer[]);
                            
    t_error hil_read_analog_codes(t_card card,
                                  const t_uint32 analog_channels[], t_uint32 num_channels,
                                  t_int32 buffer[]);
    
    t_error hil_read_encoder(t_card card,
                             const t_uint32 encoder_channels[], t_uint32 num_channels,
                             t_int32 buffer[]);
    
    t_error hil_read_digital(t_card card,
                             const t_uint32 digital_lines[], t_uint32 num_lines,
                             t_boolean buffer[]);
    
    t_error hil_read_other(t_card card,
                           const t_uint32 other_channels[], t_uint32 num_channels,
                           t_double buffer[]);
                           
    t_error hil_read(t_card card, 
                     const t_uint32 analog_channels[], t_uint32 num_analog_channels, 
                     const t_uint32 encoder_channels[], t_uint32 num_encoder_channels, 
                     const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                     const t_uint32 other_channels[], t_uint32 num_other_channels, 
                     t_double analog_buffer[],
                     t_int32 encoder_buffer[],
                     t_boolean digital_buffer[],
                     t_double other_buffer[]);
                     
    t_error hil_write_analog(t_card card,
                             const t_uint32 analog_channels[], t_uint32 num_channels,
                             const t_double buffer[]);
                             
    t_error hil_write_analog_codes(t_card card,
                                   const t_uint32 analog_channels[], t_uint32 num_channels,
                                   const t_int32 buffer[]);

    t_error hil_write_pwm(t_card card,
                          const t_uint32 pwm_channels[], t_uint32 num_channels,
                          const t_double buffer[]);

    t_error hil_write_digital(t_card card,
                              const t_uint32 digital_lines[], t_uint32 num_lines,
                              const t_boolean buffer[]);

    t_error hil_write_other(t_card card,
                            const t_uint32 other_channels[], t_uint32 num_channels,
                            const t_double  buffer[]);
                            
    t_error hil_write(t_card card, 
                      const t_uint32 analog_channels[], t_uint32 num_analog_channels, 
                      const t_uint32 pwm_channels[], t_uint32 num_pwm_channels, 
                      const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                      const t_uint32 other_channels[], t_uint32 num_other_channels, 
                      const t_double analog_buffer[],
                      const t_double pwm_buffer[],
                      const t_boolean digital_buffer[],
                      const t_double other_buffer[]);
    
    t_error hil_read_analog_write_analog(t_card card, 
                                         const t_uint32 analog_input_channels[], t_uint32 num_analog_input_channels, 
                                         const t_uint32 analog_output_channels[], t_uint32 num_analog_output_channels, 
                                         t_double analog_input_buffer[],
                                         const t_double analog_output_buffer[]);

    t_error hil_read_encoder_write_pwm(t_card card, 
                                       const t_uint32 encoder_input_channels[], t_uint32 num_encoder_input_channels, 
                                       const t_uint32 pwm_output_channels[], t_uint32 num_pwm_output_channels, 
                                       t_int32 encoder_input_buffer[],
                                       const t_double pwm_output_buffer[]);

    t_error hil_read_digital_write_digital(t_card card, 
                                           const t_uint32 digital_input_lines[], t_uint32 num_digital_input_lines, 
                                           const t_uint32 digital_output_lines[], t_uint32 num_digital_output_lines, 
                                           t_boolean digital_input_buffer[],
                                           const t_boolean digital_output_buffer[]);

    t_error hil_read_other_write_other(t_card card, 
                                      const t_uint32 other_input_channels[], t_uint32 num_other_input_channels, 
                                      const t_uint32 other_output_channels[], t_uint32 num_other_output_channels, 
                                      t_double other_input_buffer[],
                                      const t_double other_output_buffer[]);
    
    t_error hil_read_write(t_card card,
                           const t_uint32 analog_input_channels[], t_uint32 num_analog_input_channels, 
                           const t_uint32 encoder_input_channels[], t_uint32 num_encoder_input_channels, 
                           const t_uint32 digital_input_lines[], t_uint32 num_digital_input_lines, 
                           const t_uint32 other_input_channels[], t_uint32 num_other_input_channels, 
                    
                           const t_uint32 analog_output_channels[], t_uint32 num_analog_output_channels, 
                           const t_uint32 pwm_output_channels[], t_uint32 num_pwm_output_channels, 
                           const t_uint32 digital_output_lines[], t_uint32 num_digital_output_lines, 
                           const t_uint32 other_output_channels[], t_uint32 num_other_output_channels, 
                    
                           t_double analog_input_buffer[],
                           t_int32 encoder_input_buffer[],
                           t_boolean digital_input_buffer[],
                           t_double other_input_buffer[],
                    
                           const t_double analog_output_buffer[],
                           const t_double pwm_output_buffer[],
                           const t_boolean digital_output_buffer[],
                           const t_double other_output_buffer[]);
    
    /* Buffered I/O Functions */
    
    /* Task Functions */
    
    t_error hil_task_create_analog_reader(t_card card, t_uint32 samples_in_buffer, 
                                          const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                                          t_task *task);

    t_error hil_task_create_encoder_reader(t_card card, t_uint32 samples_in_buffer,
                                           const t_uint32 encoder_channels[], t_uint32 num_encoder_channels,
                                           t_task *task);

    t_error hil_task_create_digital_reader(t_card card, t_uint32 samples_in_buffer,
                                           const t_uint32 digital_lines[], t_uint32 num_digital_lines,
                                           t_task *task);

    t_error hil_task_create_other_reader(t_card card, t_uint32 samples_in_buffer, 
                                         const t_uint32 other_channels[], t_uint32 num_other_channels,
                                         t_task *task);

    t_error hil_task_create_reader(t_card card, t_uint32 samples_in_buffer, 
                                   const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                                   const t_uint32 encoder_channels[], t_uint32 num_encoder_channels,
                                   const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                                   const t_uint32 other_channels[], t_uint32 num_other_channels,
                                   t_task *task);
                                           
    t_error hil_task_create_analog_writer(t_card card, t_uint32 samples_in_buffer, 
                                          const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                                          t_task *task);

    t_error hil_task_create_pwm_writer(t_card card, t_uint32 samples_in_buffer, 
                                       const t_uint32 pwm_channels[], t_uint32 num_pwm_channels, 
                                       t_task *task);
    
    t_error hil_task_create_digital_writer(t_card card, t_uint32 samples_in_buffer, 
                                           const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                                           t_task *task);
    
    t_error hil_task_create_other_writer(t_card card, t_uint32 samples_in_buffer, 
                                         const t_uint32 other_channels[], t_uint32 num_other_channels,
                                         t_task *task);
    
    t_error hil_task_create_writer(t_card card, t_uint32 samples_in_buffer, 
                                   const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                                   const t_uint32 pwm_channels[], t_uint32 num_pwm_channels,
                                   const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                                   const t_uint32 other_channels[], t_uint32 num_other_channels,
                                   t_task *task);
    
    t_error hil_task_set_buffer_overflow_mode(t_task task, t_buffer_overflow_mode mode);

    t_int hil_task_get_buffer_overflows(t_task task);

    t_error hil_task_start(t_task task, t_clock clock, t_double frequency, t_uint32 num_samples);
    
    t_error hil_task_flush(t_task task);
    
    t_error hil_task_stop(t_task task);

    t_error hil_task_stop_all(t_card card);

    t_error hil_task_delete(t_task task);

    t_error hil_task_delete_all(t_card card);
    
    t_error hil_task_read_analog(t_task task, t_uint32 num_samples, t_double analog_buffer[]);

    t_error hil_task_read_encoder(t_task task, t_uint32 num_samples, t_int32 encoder_buffer[]);

    t_error hil_task_read_digital(t_task task, t_uint32 num_samples, t_boolean digital_buffer[]);
    
    t_error hil_task_read_other(t_task task, t_uint32 num_samples, t_double other_buffer[]);
    
    t_error hil_task_read(t_task task, t_uint32 num_samples,
                          t_double analog_buffer[],
                          t_int32 encoder_buffer[],
                          t_boolean digital_buffer[],
                          t_double other_buffer[]);
    
    t_error hil_task_write_analog(t_task task, t_uint32 num_samples, const t_double analog_buffer[]);
    
    t_error hil_task_write_pwm(t_task task, t_uint32 num_samples, const t_double pwm_buffer[]);
    
    t_error hil_task_write_digital(t_task task, t_uint32 num_samples, const t_boolean digital_buffer[]);
    
    t_error hil_task_write_other(t_task task, t_uint32 num_samples, const t_double other_buffer[]);
    
    t_error hil_task_write(t_task task, t_uint32 num_samples,
                           const t_double  analog_buffer[],
                           const t_double  pwm_buffer[],
                           const t_boolean digital_buffer[],
                           const t_double  other_buffer[]);
    
    /* Watchdog Functions */
    
    t_error hil_watchdog_set_analog_expiration_state(t_card card, 
                                                     const t_uint channels[], t_uint num_channels, 
                                                     const t_double voltages[]);

    t_error hil_watchdog_set_pwm_expiration_state(t_card card, 
                                                  const t_uint channels[], t_uint num_channels, 
                                                  const t_double duty_cycles[]);

    t_error hil_watchdog_set_digital_expiration_state(t_card card, 
                                                      const t_uint channels[], t_uint num_channels, 
                                                      const t_digital_state states[]);         

    t_error hil_watchdog_set_other_expiration_state(t_card card, 
                                                    const t_uint channels[], t_uint num_channels, 
                                                    const t_double values[]);

    t_error hil_watchdog_start(t_card card, t_double timeout);
    
    t_error hil_watchdog_reload(t_card card);

    t_error hil_watchdog_is_expired(t_card card);

    t_error hil_watchdog_clear(t_card card);

    t_error hil_watchdog_stop(t_card card);
""")

hil_lib = ffi.dlopen("hil")

# endregion

# region Constants

_BOOLEAN_ARRAY = "t_boolean[]"
_CHAR_ARRAY = "char[]"
_UINT_ARRAY = "t_uint[]"
_UINT32_ARRAY = "t_uint32[]"
_INT_ARRAY = "t_int[]"
_INT32_ARRAY = "t_int32[]"
_DOUBLE_ARRAY = "t_double[]"

_ANALOG_INPUT_CONFIGURATION_ARRAY = "t_analog_input_configuration[]"
_CLOCK_ARRAY = "t_clock[]"
_CLOCK_MODE_ARRAY = "t_clock_mode[]"
_ENCODER_QUADRATURE_MODE_ARRAY = "t_encoder_quadrature_mode[]"
_PWM_MODE_ARRAY = "t_pwm_mode[]"
_PWM_CONFIGURATION_ARRAY = "t_pwm_configuration[]"
_PWM_ALIGNMENT_ARRAY = "t_pwm_alignment[]"
_PWM_POLARITY_ARRAY = "t_pwm_polarity[]"
_DIGITAL_CONFIGURATION_ARRAY = "t_digital_configuration[]"
_DIGITAL_STATE_ARRAY = "t_digital_state[]"

_INTEGER_PROPERTY_ARRAY = "t_hil_integer_property[]"
_DOUBLE_PROPERTY_ARRAY = "t_hil_double_property[]"

# endregion

# region HIL Classes


class HIL:
    """A Python wrapper for the Quanser HIL API.

    Parameters
    ----------
    card_type : string
        A string indicating the type of HIL board being configured. For example, for the Q8 board the board type is
        "q8". Some other valid board types are "q4" and "qpid_e".
    card_identifier : string
        A string identifying the particular board among all the boards of the same type. This parameter is only
        used when there is more than one board of the given type in the computer. Typically, this parameter is "0",
        indicating the first board of the given type. Subsequent boards are typically numbered sequentially. Hence,
        the second board in the system is board "1".

    Raises
    ------
    HILError
        On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

    Examples
    --------
    Constructs a new HIL object without opening a connection to a board.

    >>> from quanser.hardware import HIL
    >>> card = HIL()

    Constructs a new HIL object and immediately connects to the specified board.
    
    >>> from quanser.hardware import HIL
    >>> card = HIL("q8_usb", "0")

    """
    # region Life Cycle

    def __init__(self, card_type=None, card_identifier=None):
        self._card = None

        # If non-default arguments are passed, attempt to open the card.
        if card_type is not None or card_identifier is not None:
            self.open(card_type, card_identifier)

    # endregion

    # region Configuration

    def close(self):
        """Closes the HIL board.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("q8_usb", "0")
        >>> card.close()

        """
        if self._card is None:
            return

        result = hil_lib.hil_close(self._card)
        if result < 0:
            raise HILError(result)

        self._card = None

    @staticmethod
    def close_all():
        """Closes all HIL boards opened by the current process.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        >>> from quanser.hardware import HIL
        >>> card1 = HIL()
        >>> card2 = HIL()
        >>> card1.open("q8_usb", "0")
        >>> card2.open("qube_servo2_usb", "0")
        >>> HIL.close_all()

        """
        result = hil_lib.hil_close_all()
        if result < 0:
            raise HILError(result)

    def open(self, card_type, card_identifier):
        """Opens a particular HIL board.

        Parameters
        ----------
        card_type : string
            A string indicating the type of HIL board being configured. For example, for the Q8 board the board type is
            "q8". Some other valid board types are "q4" and "qpid_e".
        card_identifier : string
            A string identifying the particular board among all the boards of the same type. This parameter is only
            used when there is more than one board of the given type in the computer. Typically, this parameter is "0",
            indicating the first board of the given type. Subsequent boards are typically numbered sequentially. Hence,
            the second board in the system is board "1".

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Notes
        -----
        This function is called automatically if the ``HIL`` object is constructed with parameters.

        Example
        -------
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("q8_usb", "0")
        >>> # ...
        ...
        >>> card.close()

        """
        # Close any existing, open board.
        self.close()

        card = ffi.new("t_card *")

        if _is_legacy_python:
            result = hil_lib.hil_open(str(card_type), str(card_identifier), card)
        else:
            result = hil_lib.hil_open(card_type.encode('UTF-8'), card_identifier.encode('UTF-8'), card)

        if result < 0:
            raise HILError(result)

        self._card = card[0]

    def set_analog_input_configuration(self, channels, num_channels, configs):
        """Sets the configuration of the specified analog input channels. Only configurations supported by the board may
        be specified. Invalid configurations will generate an error. Refer to the documentation for your card for
        details on the features supported by the card.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the analog input channels whose configurations will be changed. Channel
            numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in `channels` array.
        configs : array_like
            An array containing the configuration of the analog inputs. The array must contain `num_channels` elements.
            Each element in the `configs` array corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the analog input configuration of channel 0 to ``DIFF`` and channel 3 to ``PDIFF``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, AnalogInputConfiguration
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 3])
        >>> num_channels = len(channels)
        >>> configs = array('i', [AnalogInputConfiguration.DIFF, AnalogInputConfiguration.PDIFF])
        >>> card.set_analog_input_configuration(channels, num_channels, configs)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, AnalogInputConfiguration
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> configs = np.array([AnalogInputConfiguration.DIFF, AnalogInputConfiguration.PDIFF], dtype=np.int32)
        >>> card.set_analog_input_configuration(channels, num_channels, configs)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_analog_input_configuration(self._card if self._card is not None else ffi.NULL,
                                                            ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                            num_channels,
                                                            ffi.from_buffer(_ANALOG_INPUT_CONFIGURATION_ARRAY, configs) if configs is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_analog_input_ranges(self, channels, num_channels, minima, maxima):
        """Sets the ranges of the analog inputs. Not all cards support programmable input ranges. Some cards only allow
        the ranges of all inputs to be set to the same value, rather than allowing each analog input to have a separate
        input range. Refer to the documentation for your card for details on the features supported by the card.

        The units for the minimum and maximum values are typically Volts, but may be Amps or a unit appropriate to the
        specific card.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the analog input channels whose ranges will be configured. Channel
            numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the `channels`, `minima, and `maxima` arrays.
        minima : array_like
            An array of doubles containing the minimum value of the input range for the corresponding channel in the
            `channels` array. This array must be the same size as the `channels` array.
        maxima : array_like
            An array of doubles containing the maximum value of the input range for the corresponding channel in the
            `channels` array. This array must be the same size as the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the range of analog input #0 to +/-10V, the range of analog input #3 to 0..5V and the range of input #5 to
        +/-5V.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 3, 5])
        >>> num_channels = len(channels)
        >>> minima = array('i', [-10, 0, -5])
        >>> maxima = array('i', [+10, 5, +5])
        >>> card.set_analog_input_ranges(channels, num_channels, minima, maxima)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 3, 5], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> minima = np.array([-10, 0, -5], dtype=np.int32)
        >>> maxima = np.array([+10, 5, +5], dtype=np.int32)
        >>> card.set_analog_input_ranges(channels, num_channels, minima, maxima)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_analog_input_ranges(self._card if self._card is not None else ffi.NULL,
                                                     ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                     num_channels,
                                                     ffi.from_buffer(_DOUBLE_ARRAY, minima) if minima is not None else ffi.NULL,
                                                     ffi.from_buffer(_DOUBLE_ARRAY, maxima) if maxima is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_analog_output_ranges(self, channels, num_channels, minima, maxima):
        """Sets the ranges of the analog outputs. Not all cards support programmable output ranges. Some cards only
        allow the ranges of all outputs to be set to the same value, rather than allowing each analog output to have a
        separate output range. Refer to the documentation for your card for details on the features supported by the
        card.

        The units for the minimum and maximum values are typically Volts, but may be Amps or a unit appropriate to the
        specific card.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the analog output channels whose ranges will be configured. Channel
            numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the `channels`, `minima, and `maxima` arrays.
        minima : array_like
            An array of doubles containing the minimum value of the output range for the corresponding channel in the
            `channels` array. This array must be the same size as the `channels` array.
        maxima : array_like
            An array of doubles containing the maximum value of the output range for the corresponding channel in the
            `channels` array. This array must be the same size as the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the range of analog output #0 to +/-10V, the range of analog output #3 to 0..5V and the range of output #5 to
        +/-5V.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 3, 5])
        >>> num_channels = len(channels)
        >>> minima = array('i', [-10, 0, -5])
        >>> maxima = array('i', [+10, 5, +5])
        >>> card.set_analog_output_ranges(channels, num_channels, minima, maxima)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 3, 5], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> minima = np.array([-10, 0, -5], dtype=np.int32)
        >>> maxima = np.array([+10, 5, +5], dtype=np.int32)
        >>> card.set_analog_output_ranges(channels, num_channels, minima, maxima)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_analog_output_ranges(self._card if self._card is not None else ffi.NULL,
                                                      ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                      num_channels,
                                                      ffi.from_buffer(_DOUBLE_ARRAY, minima) if minima is not None else ffi.NULL,
                                                      ffi.from_buffer(_DOUBLE_ARRAY, maxima) if maxima is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_clock_mode(self, clocks, num_clocks, clock_modes):
        """Sets the mode of the hardware clocks. This function is used with hardware clocks that are multipurpose. Some
        boards, like the Q8, allow the hardware clocks to be configured as timebases (the default) or as PWM outputs.
        This function allows the appropriate mode to be selected.

        Parameters
        ----------
        clocks : array_like
            An array containing the clocks whose mode will be changed. System clocks do not support different modes, so
            only hardware clocks, such as ``HARDWARE_CLOCK_0``, should be specified.
        num_clocks : int
            The number of clocks specified in the `clocks` and `clock_modes` arrays.
        clock_modes : array_like
            An array of clock modes to which to set the clocks. Each element in the `clock_modes` array corresponds to
            the same element in the `clocks` array. Hence, there must be as many elements in the `clock_modes` array as
            there are clocks.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure HARDWARE_CLOCK_0 as a PWM output.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock, ClockMode
        >>> card = HIL("q8_usb", "0")
        >>> clocks = array('i', [Clock.HARDWARE_CLOCK_0])
        >>> num_clocks = len(clocks)
        >>> modes = array('i', [ClockMode.PWM])
        >>> card.set_clock_mode(clocks, num_clocks, modes)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock, ClockMode
        >>> card = HIL("q8_usb", "0")
        >>> clocks = np.array([Clock.HARDWARE_CLOCK_0], dtype=np.uint32)
        >>> num_clocks = len(clocks)
        >>> modes = np.array([ClockMode.PWM], dtype=np.int32)
        >>> card.set_clock_mode(clocks, num_clocks, modes)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_clock_mode(self._card if self._card is not None else ffi.NULL,
                                            ffi.from_buffer(_CLOCK_ARRAY, clocks) if clocks is not None else ffi.NULL,
                                            num_clocks,
                                            ffi.from_buffer(_CLOCK_MODE_ARRAY, clock_modes) if clock_modes is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_digital_directions(self, input_channels, num_input_channels, output_channels, num_output_channels):
        """Configures digital I/O channels as either inputs or outputs. In general, a digital I/O line cannot be
        configured as an input and an output at the same time.

        Parameters
        ----------
        input_channels : array_like
            An array containing the numbers of the digital I/O channels which will be configured as inputs.
        num_input_channels : int
            The number of channels specified in the `input_channels` array. This parameter may be zero.
        output_channels : array_like
            An array containing the numbers of the digital I/O channels which will be configured as outputs.
        num_output_channels : int
            The number of channels specified in the `output_channels` array. This parameter may be zero.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the directions for the first two digital channels. Channel 1 is configured as an output while channel 0 is
        configured as an input.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("q2_usb", "0")
        >>> input_channels = array('I', [1])
        >>> output_channels = array('I', [0])
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> card.set_digital_directions(input_channels, num_input_channels, output_channels, num_output_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("q2_usb", "0")
        >>> input_channels = np.array([1], dtype=np.uint32)
        >>> output_channels = np.array([0], dtype=np.uint32)
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> card.set_digital_directions(input_channels, num_input_channels, output_channels, num_output_channels)
        >>> card.close()
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_digital_directions(self._card if self._card is not None else ffi.NULL,
                                                    ffi.from_buffer(_UINT32_ARRAY, input_channels) if input_channels is not None else ffi.NULL,
                                                    num_input_channels,
                                                    ffi.from_buffer(_UINT32_ARRAY, output_channels) if output_channels is not None else ffi.NULL,
                                                    num_output_channels)
        if result < 0:
            raise HILError(result)

    def set_digital_output_configuration(self, channels, num_channels, configurations):
        """Sets the configuration of digital output lines.

        Two output configurations are possible:
            `DigitalConfiguration.TOTEM_POLE`     = use a totem-pole output (active high and active low)
            `DigitalConfiguration.OPEN_COLLECTOR` = use an open-collector output (passive high, active low)

        Cards which have totem-pole outputs normally drive the output high or low actively. However,
        these outputs can simulate open-collector outputs by making the output tristate for a "high" output
        and active low for a "low" output. This function allows this emulation to be configured. Some
        cards allow the configuration to be programmed on a per-channel basis.

        Parameters
        ----------
        channels : array_like
            An array containing the digital output channels which will be configured.
        num_channels : int
            The number of channels specified in the `channels` array. This parameter may be zero.
        configurations : array_like
            An array containing the configuration of each digital output channel. Each element in the `configurations` array
            corresponds to the same element in the `channels` array. Hence, there must be as many elements in the
            `configurations` array as there are channels.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the configurations for the first two digital output channels. Channel 0 is configured as a totem-pole output 
        while channel 1 is configured as an open-collector output.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("qpid_e", "0")
        >>> channels = array('I', [1])
        >>> num_channels = len(channels)
        >>> configurations = array('i', [DigitalConfiguration.TOTEM_POLE, DigitalConfiguration.OPEN_COLLECTOR])
        >>> card.set_digital_output_configuration(channels, num_channels, configurations)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL()
        >>> card.open("qpid_e", "0")
        >>> channels = np.array([1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> configurations = np.array([DigitalConfiguration.TOTEM_POLE, DigitalConfiguration.OPEN_COLLECTOR], dtype=np.int32)
        >>> card.set_digital_output_configuration(channels, num_channels, configurations)
        >>> card.close()
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_digital_output_configuration(self._card if self._card is not None else ffi.NULL,
                                                              ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                              num_channels,
                                                              ffi.from_buffer(_DIGITAL_CONFIGURATION_ARRAY, configurations) if configurations is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_encoder_counts(self, channels, num_channels, counts):
        """Sets the count values for the encoder counters. This function is typically used to initialize the encoder
        counters to zero when the board is first opened.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the encoder inputs whose counters will be set.
        num_channels : int
            The number of channels specified in the `channels` array.
        counts : array_like
            An array of count values to which to set the encoder counters. Each element in the `counts` array
            corresponds to the same element in the `channels` array. Hence, there must be as many elements in the
            `counts` array as there are channels.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the encoder counts for the first three encoder channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2])
        >>> num_channels = len(channels)
        >>> counts = array('i', [1000, -1000, 0])
        >>> card.set_encoder_counts(channels, num_channels, counts)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> counts = np.array([1000, -1000, 0], dtype=np.int32)
        >>> card.set_encoder_counts(channels, num_channels, counts)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_encoder_counts(self._card if self._card is not None else ffi.NULL,
                                                ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                num_channels,
                                                ffi.from_buffer(_INT32_ARRAY, counts) if counts is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_encoder_filter_frequency(self, channels, num_channels, frequencies):
        """Some cards support filtering of their encoder inputs. This function sets the filter frequency of the encoder
        inputs on the card. Note that many cards do not support encoders. Cards which do provide encoders may not
        support filtering or different filter frequencies, or may not support different filter frequencies for each
        channel.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the encoder inputs whose filter frequencies will be set. Channel
            numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the `channels` array.
        frequencies : array_like
            An array of doubles containing the new encoder filter frequency for each channel in Hertz. There must be
            one element for each encoder channel specified in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the filter frequencies of channels 0 and 4 to 8.33 MHz and set channel 2 to 4.17 MHz.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 2, 4])
        >>> num_channels = len(channels)
        >>> frequencies = array('d', [1 / (120e-9 * 1), 1 / (120e-9 * 2), 1 / (120e-9 * 1)])
        >>> card.set_encoder_filter_frequency(channels, num_channels, frequencies)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 2, 4], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequencies = np.array([1 / (120e-9 * 1), 1 / (120e-9 * 2), 1 / (120e-9 * 1)], dtype=np.float64)
        >>> card.set_encoder_filter_frequency(channels, num_channels, frequencies)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_encoder_filter_frequency(self._card if self._card is not None else ffi.NULL,
                                                          ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                          num_channels,
                                                          ffi.from_buffer(_DOUBLE_ARRAY, frequencies) if frequencies is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_encoder_quadrature_mode(self, channels, num_channels, modes):
        """Sets the quadrature mode of the encoder inputs on the card. Many cards do not support encoders. Cards which
        do provide encoders may not support different quadrature modes, or may not support different quadrature modes
        for each channel.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the encoder inputs whose quadrature modes will be set. Channel
            numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the `channels` array.
        modes : array_like
            An array of ``EncoderQuadritureMode`` constants containing the new encoder quadrature mode for each
            channel. There must be one element for each encoder channel specified in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the quadrature mode of channels 0 and 2 to 4X quadrature and set channel 1 to non-quadrature mode.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, EncoderQuadratureMode
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2])
        >>> num_channels = len(channels)
        >>> modes = array('i', [EncoderQuadratureMode.X4, EncoderQuadratureMode.NONE, EncoderQuadratureMode.X4])
        >>> card.set_encoder_quadrature_mode(channels, num_channels, modes)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, EncoderQuadratureMode
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 2, 4], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> modes = np.array([EncoderQuadratureMode.X4, EncoderQuadratureMode.NONE, EncoderQuadratureMode.X4], dtype=np.int32)
        >>> card.set_encoder_quadrature_mode(channels, num_channels, modes)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_encoder_quadrature_mode(self._card if self._card is not None else ffi.NULL,
                                                         ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                         num_channels,
                                                         ffi.from_buffer(_ENCODER_QUADRATURE_MODE_ARRAY, modes) if modes is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_pwm_mode(self, channels, num_channels, modes):
        """Sets the mode that will be used for a PWM output. The mode determines how the values written to a PWM output
        are interpreted.
        The actual PWM output mode is not changed until the PWM output is used in one of the following functions:
        `write_pwm`, `write`, `read_encoder_write_pwm`, `read_write`,
        `write_pwm_buffer`, `write_buffer`, `read_encoder_write_pwm_buffer`, `read_write_buffer`,
        `task_start`.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs whose modes are being set.
        num_channels : int
            The number of channels specified in the `channels` array.
        modes : array_like
            An array containing the modes of the PWM outputs. The array must contain `num_channels` elements. Each
            element in the `modes` array corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the PWM mode to ``DutyCycle`` for PWM output channel 0 and ``FREQUENCY`` for PWM output channel 1.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, PWMMode
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> modes = array('i', [PWMMode.DUTY_CYCLE, PWMMode.FREQUENCY])
        >>> card.set_pwm_mode(channels, num_channels, modes)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, PWMMode
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> modes = np.array([PWMMode.DUTY_CYCLE, PWMMode.FREQUENCY], dtype=np.int32)
        >>> card.set_pwm_mode(channels, num_channels, modes)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_pwm_mode(self._card if self._card is not None else ffi.NULL,
                                          ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                          num_channels,
                                          ffi.from_buffer(_PWM_MODE_ARRAY, modes) if modes is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_pwm_configuration(self, channels, num_channels, configurations, alignments, polarities):
        """Sets the configuration of the PWM output channels.
        
        Most cards do not support different configurations for their PWM channels but the Quanser QPID does. A PWM
        output configuration determines whether each PWM channel is an independent unipolar output, a bipolar output,
        or whether the outputs are paired to make complementary outputs. It also determines whether the PWM signals
        aligned to either the leading or trailing edge of the PWM period, or aligned to the center of the PWM period.
        Finally, the configuration also determines the polarity of the output (whether the duty cycle refers to the
        high pulse or low pulse width).

        The actual PWM output mode is not changed until the PWM output is used in one of the following functions:
        `write_pwm`, `write`, `read_encoder_write_pwm`, `read_write`,
        `write_pwm_buffer`, `write_buffer`, `read_encoder_write_pwm_buffer`, `read_write_buffer`,
        `task_start`.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs which are being configured.
        num_channels : int
            The number of channels specified in the `channels` array.
        configurations : array_like
            An array containing the configurations of the PWM outputs, as `PWMConfiguration` values. 
            The array must contain `num_channels` elements. Each element in the `configurations` array 
            corresponds to the same element in the `channels` array.
        alignments : array_like
            An array containing the alignments of the PWM outputs, as `PWMAlignment` values. 
            The array must contain `num_channels` elements. Each element in the `alignments` array 
            corresponds to the same element in the `channels` array.
        polarities : array_like
            An array containing the polarities of the PWM outputs, as `PWMPolarity` values.
            The array must contain `num_channels` elements. Each element in the `polarities` array
            corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure PWM output 0 to be ``UNIPOLAR`` and output 2 to be ``COMPLEMENTARY``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, PWMconfiguration, PWMAlignment, PWMPolarity
        >>> card = HIL("qpid_e", "0")
        >>> channels = array('I', [0, 2])
        >>> num_channels = len(channels)
        >>> configurations = array('i', [PWMConfiguration.UNIPOLAR, PWMConfiguration.COMPLEMENTARY])
        >>> alignments = array('i', [PWMAlignment.LEADING_EDGE_ALIGNED, PWMAlignment.LEADING_EDGE_ALIGNED])
        >>> polarities = array('i', [PWMPolarity.ACTIVE_HIGH, PWMPolarity.ACTIVE_HIGH])
        >>> card.set_pwm_configuration(channels, num_channels, configurations, alignments, polarities)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, PWMMode
        >>> card = HIL("qpid_e", "0")
        >>> channels = np.array([0, 2], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> configurations = np.array([PWMConfiguration.UNIPOLAR, PWMConfiguration.COMPLEMENTARY], dtype=np.int32)
        >>> alignments = np.array([PWMAlignment.LEADING_EDGE_ALIGNED, PWMAlignment.LEADING_EDGE_ALIGNED], dtype=np.int32)
        >>> polarities = np.array([PWMPolarity.ACTIVE_HIGH, PWMPolarity.ACTIVE_HIGH], dtype=np.int32)
        >>> card.set_pwm_configuration(channels, num_channels, configurations, alignments, polarities)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_pwm_configuration(self._card if self._card is not None else ffi.NULL,
                                                   ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                   num_channels,
                                                   ffi.from_buffer(_PWM_CONFIGURATION_ARRAY, configurations) if configurations is not None else ffi.NULL,
                                                   ffi.from_buffer(_PWM_ALIGNMENT_ARRAY, alignments) if alignments is not None else ffi.NULL,
                                                   ffi.from_buffer(_PWM_POLARITY_ARRAY, polarities) if polarities is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_pwm_deadband(self, channels, num_channels, leading_edge_deadband, trailing_edge_deadband):
        """Sets the deadband of paired or complementary PWM output channels.
                
        When two PWM outputs are configured as complementary by the `set_pwm_configuration` function, the secondary 
        channel outputs the inverse of the primary channel. Hence, when the primary channel is high, the secondary
        channel is low, and vice versa. However, a "deadband" may be introduced in the transition from high-to-low 
        or low-to-high, such that the secondary output does not change immediately, as soon as the primary channel 
        changes state. Such "deadband" is necessary when the PWM outputs are being used to drive an H-bridge or other
        transistor configurations to avoid two transistors in an H-bridge from being turned on at the same time, albeit
        briefly, and causing a current surge (since power would essentially be shorted to ground for a brief instant).

        This function allows the deadband to be specified. In fact, a different deadband may be specified for when
        the primary channel transitions from high-to-low or low-to-high, since transistor switching times may not be
        symmetric.

        The deadband may be set for any channels that are configured as bipolar, paired or complementary. Channels
        which are configured as unipolar are ignored (i.e., hil_set_pwm_deadband may be called for those channels
        but the deadband value is ignored and success is returned). Only the primary channel should have its deadband
        set. The secondary channel is ignored since its behaviour is governed entirely by the primary channel.

        The actual PWM output mode is not changed until the PWM output is used in one of the following functions:
        `write_pwm`, `write`, `read_encoder_write_pwm`, `read_write`,
        `write_pwm_buffer`, `write_buffer`, `read_encoder_write_pwm_buffer`, `read_write_buffer`,
        `task_start`.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs which are being configured.
        num_channels : int
            The number of channels specified in the `channels` array.
        leading_edge_deadband : array_like
            An array containing the leading-edge deadband for the PWM outputs, as real values. 
            The array must contain `num_channels` elements. Each element in the `leading_edge_deadband` array
            corresponds to the same element in the `channels` array.
        trailing_edge_deadband : array_like
            An array containing the trailing-edge deadband for the PWM outputs, as real values.
            The array must contain `num_channels` elements. Each element in the `trailing_edge_deadband` array
            corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the deadbands of PWM outputs 0, 1 and 2.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("qpid_e", "0")
        >>> channels = array('I', [0, 2])
        >>> num_channels = len(channels)
        >>> leading_edge = array('d', [50e-9, 0, 100e-9])
        >>> trailing_edge = array('d', [100e-9, 0, 200e-9])
        >>> card.set_pwm_deadband(channels, num_channels, leading_edge, trailing_edge)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, PWMMode
        >>> card = HIL("qpid_e", "0")
        >>> channels = np.array([0, 2], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> leading_edge = np.array([50e-9, 0, 100e-9], dtype=np.double)
        >>> trailing_edge = np.array([100e-9, 0, 200e-9], dtype=np.double)
        >>> card.set_pwm_deadband(channels, num_channels, leading_edge, trailing_edge)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_pwm_deadband(self._card if self._card is not None else ffi.NULL,
                                              ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                              num_channels,
                                              ffi.from_buffer(_DOUBLE_ARRAY, leading_edge_deadband) if leading_edge_deadband is not None else ffi.NULL,
                                              ffi.from_buffer(_DOUBLE_ARRAY, trailing_edge_deadband) if trailing_edge_deadband is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_pwm_frequency(self, channels, num_channels, frequencies):
        """Sets the frequency that will be used for a PWM output. This function is typically used only in
        ``PWMMode.DutyCycle`` (the default). The actual PWM output frequency is not changed until the PWM output is
        used in one of the following functions:
        `write_pwm`, `write`, `read_encoder_write_pwm`, `read_write`,
        `write_pwm_buffer`, `write_buffer`, `read_encoder_write_pwm_buffer`, `read_write_buffer`,
        `task_start`.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs whose frequencies are being set.
        num_channels : int
            The number of channels specified in the `channels` array.
        frequencies : array_like
            An array containing the frequencies in Hertz of the PWM outputs. The array must contain `num_channels`
            elements. Each element in the `frequencies` array corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the PWM frequency to 10 kHz for PWM output channel 0 and 20 kHz for PWM output channel 1.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> frequencies = array('d', [10000.0, 20000.0])
        >>> card.set_pwm_frequency(channels, num_channels, frequencies)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequencies = np.array([10000.0, 20000.0], dtype=np.float64)
        >>> card.set_pwm_frequency(channels, num_channels, frequencies)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_pwm_frequency(self._card if self._card is not None else ffi.NULL,
                                               ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                               num_channels,
                                               ffi.from_buffer(_DOUBLE_ARRAY, frequencies) if frequencies is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_pwm_duty_cycle(self, channels, num_channels, duty_cycles):
        """Sets the duty cycle that will be used for a PWM output. This function is typically used only in
        ``PWM_FREQUENCY_MODE`` or ``PWM_PERIOD_MODE``. The actual PWM output duty cycle is not changed until the PWM
        output is used in one of the following functions:
        `write_pwm`, `write`, `read_encoder_write_pwm`, `read_write`,
        `write_pwm_buffer`, `write_buffer`, `read_encoder_write_pwm_buffer`, `read_write_buffer`,
        `task_start`.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs whose duty cycles are being set.
        num_channels : int
            The number of channels specified in the `channels` array.
        duty_cycles : array_like
            An array containing the duty cycle values for the PWM outputs. Duty cycle values must be fractions between
            0.0 and 1.0, where 0.0 indicates 0% and 1.0 denotes 100%. The value may be signed for those boards which
            support bidirectional PWM outputs. The array must contain `num_channels` elements. Each element in the
            `duty_cycles` array corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the PWM duty cycle to 50% for PWM output channel 0 and 75% for PWM output channel 1.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> duty_cycles = array('d', [0.5, 0.75])
        >>> card.set_pwm_duty_cycle(channels, num_channels, duty_cycles)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> duty_cycles = np.array([10000.0, 20000.0], dtype=np.float64)
        >>> card.set_pwm_duty_cycle(channels, num_channels, duty_cycles)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_pwm_duty_cycle(self._card if self._card is not None else ffi.NULL,
                                                ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                num_channels,
                                                ffi.from_buffer(_DOUBLE_ARRAY, duty_cycles) if duty_cycles is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def set_card_specific_options(self, options, size):
        """Sets options specific to a particular card. The `options` parameter is a string containing the card-specific
        options. The string typically takes the form:

            <name>=<value>,<name>=<value>,...

        where <name> is the name of an option and <value> is the option's value. In general, spaces should be avoided.
        Spaces may be contained in values if the value is enclosed in double quotes. For example, in the hypothetical
        options string below, the value of the vendor option contains a space, so it is enclosed in quotes:

        options = "vendor=\"National Instruments\",terminal_board=e_series"

        Refer to the card's documentation for details on the options supported by the card. Many cards do not support
        any options, since the standard HIL API functions cover most, if not all, of their functionality.

        Parameters
        ----------
        options : string
            A string containing the options. See the standard format of this argument in the discussion above. The
            string should be null terminated, although the `options_size` argument may be used to circumvent this
            requirement by providing the actual length of the string.
        size : int
            The maximum number of characters that will be used from the options string. If the options string is
            null-terminated, then this argument may be set to ``MAX_STRING_LENGTH``.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        --------
        Configure a National Instruments PCI-6259 card for use with a Quanser E-Series terminal board.

        >>> from quanser.hardware import HIL, MAX_STRING_LENGTH
        >>> card = HIL()
        >>> card.open("ni_pci_6259", "0")
        >>> card.set_card_specific_options("terminal_board=e_series", MAX_STRING_LENGTH)
        >>> # ...
        ...
        >>> card.close()

        """
        if _is_legacy_python:
            result = hil_lib.hil_set_card_specific_options(self._card if self._card is not None else ffi.NULL,
                                                           options, size)
        else:
            result = hil_lib.hil_set_card_specific_options(self._card if self._card is not None else ffi.NULL,
                                                           options.encode('UTF-8'), size)

        if result < 0:
            raise HILError(result)

    # endregion

    # region Information

    @staticmethod
    def get_version():
        """Returns the version of the Quanser HIL API that is installed.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Returns
        -------
        Version
            A version structure.

        Example
        -------
        >>> from quanser.hardware import HIL
        >>> version = HIL.get_version()

        """
        version = ffi.new("t_version *")
        version.size = ffi.sizeof("t_version")

        result = hil_lib.hil_get_version(version)
        if result < 0:
            raise HILError(result)

        return Version(version.size, version.major, version.minor, version.release, version.build)

    def is_valid(self):
        """Determines if the given board handle is valid. A board handle is valid if it was opened successfully and has
        not been closed.

        Returns
        -------
        bool
            ``True`` if the given board handle is valid; ``False`` otherwise.

        Example
        -------
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> is_valid = card.is_valid()
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_is_valid(self._card if self._card is not None else ffi.NULL)
        return result == b'\x01'

    # endregion

    # region Properties

    def get_integer_property(self, properties, num_properties, buffer):
        """Gets the value of integer properties of the board. This function can retrieve the value of more than one
        integer property at the same time. Standard integer properties are listed in the table below. The board may also
        support product-specific integer properties.

        Parameters
        ----------
        properties : array_like
            An array containing the property numbers of the properties to be retrieved. 
        num_properties : int
            The number of properties specified in the properties array.
        buffer : array_like
            An array for receiving the property values retrieved from the board. The array must contain `num_properties`
            elements. Each element in the returned `buffer` array will correspond to the same element in the
            `properties` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Fetch the major and minor version numbers of the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, IntegerProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = array('i', [IntegerProperty.MAJOR_VERSION, IntegerProperty.MINOR_VERSION])
        >>> num_properties = len(properties)
        >>> buffer = array('i', [0] * num_properties)
        >>> card.get_integer_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, IntegerProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = np.array([IntegerProperty.MAJOR_VERSION, IntegerProperty.MINOR_VERSION], dtype=np.int32)
        >>> num_properties = len(properties)
        >>> buffer = np.zeros(num_properties, dtype=np.int32)
        >>> card.get_integer_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_get_integer_property(self._card if self._card is not None else ffi.NULL,
                                                  ffi.from_buffer(_INTEGER_PROPERTY_ARRAY, properties) if properties is not None else ffi.NULL,
                                                  num_properties,
                                                  ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)
       
        if result < 0:
            raise HILError(result)

    def get_double_property(self, properties, num_properties, buffer):
        """Gets the value of double properties of the board. There are currently no standard double properties defined,
        but the board may support product-specific double properties. This function can retrieve the value of more than
        one double property at the same time.

        Parameters
        ----------
        properties : array_like
            An array containing the property numbers of the properties to be retrieved. There are no standard double
            properties currently defined.
 
        num_properties : int
            The number of properties specified in the properties array.
        buffer : array_like
            An array for receiving the property values retrieved from the board. The array must contain `num_properties`
            elements. Each element in the returned `buffer` array will correspond to the same element in the
            `properties` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Fetch the second product-specific double property of the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, DoubleProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = array('i', [DoubleProperty.PRODUCT_SPECIFIC + 1])
        >>> num_properties = len(properties)
        >>> buffer = array('i', [0] * num_properties)
        >>> card.get_double_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, DoubleProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = np.array([DoubleProperty.PRODUCT_SPECIFIC + 1], dtype=np.int32)
        >>> num_properties = len(properties)
        >>> buffer = np.zeros(num_properties, dtype=np.float64)
        >>> card.get_double_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_get_double_property(self._card if self._card is not None else ffi.NULL,
                                                 ffi.from_buffer(_DOUBLE_PROPERTY_ARRAY, properties) if properties is not None else ffi.NULL,
                                                 num_properties,
                                                 ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        
        if result < 0:
            raise HILError(result)

    def get_string_property(self, property_code, buffer, buffer_size):
        """Gets the value of a string property of the board. This function can only retrieve the value of one string
        property at a time. Standard string properties are listed in the table below. The board may also support
        product-specific string properties.

        Parameters
        ----------
        property_code : int
            The number of the property to be retrieved.
                     
        buffer : array_like
            A character array for receiving the property value retrieved from the board. The array must contain
            `buffer_size` elements.

        buffer_size : int
            The size of the buffer in code units (bytes).

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Fetch the manufacturer of the board.

        >>> from quanser.hardware import HIL, StringProperty
        >>> card = HIL("q8_usb", "0")
        >>> buffer = []
        >>> buffer_size = 64
        >>> card.get_string_property(StringProperty.MANUFACTURER, buffer, buffer_size)
        >>> # ...
        ...
        >>> card.close()

        """
        _buffer = ffi.new("char *")
        result = hil_lib.hil_get_string_property(self._card if self._card is not None else ffi.NULL,
                                                 property_code, _buffer, buffer_size)
        buffer[:] = ffi.string(_buffer).decode("UTF-8")

        if result < 0:
            raise HILError(result)

    def set_integer_property(self, properties, num_properties, buffer):
        """Sets the value of integer properties of the board. There are currently no standard integer properties
        defined. Typically, only board-specific properties may actually be reconfigured. This function can set the value
        of more than one integer property at the same time.

        Parameters
        ----------
        properties : array_like
            An array containing the property numbers of the properties to be set. There are currently no standard
            integer properties defined.
        num_properties : int
            The number of properties specified in the properties array.
        buffer : array_like
            An array of the property values to be set for the board. The array must contain `num_properties` elements.
            Each element in the `buffer` array corresponds to the same element in the `properties` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the second product-specific integer property of the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, IntegerProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = array('i', [IntegerProperty.PRODUCT_SPECIFIC + 1])
        >>> num_properties = len(properties)
        >>> buffer = array('i', [0] * num_properties)
        >>> card.set_integer_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, IntegerProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = np.array([IntegerProperty.PRODUCT_SPECIFIC + 1], dtype=np.int32)
        >>> num_properties = len(properties)
        >>> buffer = np.zeros(num_properties, dtype=np.int32)
        >>> card.set_integer_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_integer_property(self._card if self._card is not None else ffi.NULL,
                                                  ffi.from_buffer(_INTEGER_PROPERTY_ARRAY, properties) if properties is not None else ffi.NULL,
                                                  num_properties,
                                                  ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

    def set_double_property(self, properties, num_properties, buffer):
        """Sets the value of double properties of the board. There are currently no standard double properties defined.
        Typically, only board-specific properties may actually be reconfigured. This function can set the value of more
        than one double property at the same time.

        Parameters
        ----------
        properties : array_like
            An array containing the property numbers of the properties to be set. There are currently no standard double
            properties defined.
        num_properties : int
            The number of properties specified in the properties array.
        buffer : array_like
            An array of the property values to be set for the board. The array must contain num_properties elements.
            Each element in the `buffer` array corresponds to the same element in the `properties` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Set the second product-specific double property of the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, DoubleProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = array('i', [DoubleProperty.PRODUCT_SPECIFIC + 1])
        >>> num_properties = len(properties)
        >>> buffer = array('i', [0] * num_properties)
        >>> card.set_double_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, DoubleProperty
        >>> card = HIL("q8_usb", "0")
        >>> properties = np.array([DoubleProperty.PRODUCT_SPECIFIC + 1], dtype=np.int32)
        >>> num_properties = len(properties)
        >>> buffer = np.zeros(num_properties, dtype=np.float64)
        >>> card.set_double_property(properties, num_properties, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_set_double_property(self._card if self._card is not None else ffi.NULL,
                                                 ffi.from_buffer(_DOUBLE_PROPERTY_ARRAY, properties) if properties is not None else ffi.NULL,
                                                 num_properties,
                                                 ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

    def set_string_property(self, property_code, buffer, buffer_size):
        """Sets the value of a string property of the board. There are currently no standard string properties defined
        that can be set. Typically only board-specific properties may actually be reconfigured.

        Parameters
        ----------
        property_code : int
            The number of the property to be set. There are currently no standard string properties defined that may be
            set.
        buffer : string
            A string containing the property value to be set for the board. The function will not copy more than
            `buffer_size` code units (bytes) from the buffer.
        buffer_size : int
            The maximum number of code units (bytes) to copy from `buffer`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Set the second product-specific string property of the board.

        >>> from quanser.hardware import HIL, StringProperty
        >>> card = HIL("q8_usb", "0")
        >>> buffer = "My String Value"
        >>> buffer_size = len(buffer)
        >>> card.set_string_property(StringProperty.PRODUCT_SPECIFIC + 1, buffer, buffer_size)
        >>> # ...
        ...
        >>> card.close()

        """  
        _buffer = ffi.new(_CHAR_ARRAY, buffer.encode('UTF-8'))
        result = hil_lib.hil_set_string_property(self._card if self._card is not None else ffi.NULL,
                                                 property_code, _buffer, buffer_size)

        if result < 0:
            raise HILError(result)    

    # endregion

    # region Immediate I/O

    # region Immediate Read

    def read_analog(self, channels, num_channels, buffer):
        """Reads from analog inputs immediately. The function does not return until the data has been read.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the analog inputs to be read.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array for receiving the voltage values read from the analog inputs. The array must contain
            `num_channels` elements. Each element in the returned `buffer` array will correspond to the same element in
            the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four analog input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0] * num_channels)
        >>> card.read_analog(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> card.read_analog(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_analog(self._card if self._card is not None else ffi.NULL,
                                         ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                         num_channels,
                                         ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_analog_codes(self, channels, num_channels, buffer):
        """Reads from the specified analog input channels immediately. The function does not return until the data has
        been read. The data returned is the raw integer A/D converter values, not voltages.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the analog inputs to be read.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array for receiving the raw A/D converter values read from the analog inputs. The array must contain
            `num_channels` elements. Each element in the returned `buffer` array will correspond to the same element in
            the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four analog input channels as raw A/D converter values.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('i', [0] * num_channels)
        >>> card.read_analog_codes(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.int32)
        >>> card.read_analog_codes(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_analog_codes(self._card if self._card is not None else ffi.NULL,
                                               ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                               num_channels,
                                               ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_encoder(self, channels, num_channels, buffer):
        """Reads from encoder inputs immediately. The function does not return until the data has been read.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the encoder inputs to be read.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array for receiving the count values read from the encoder inputs. The array must contain
            `num_channels` elements. Each element in the returned buffer array will correspond to the same element in
            the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four encoder input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('i', [0] * num_channels)
        >>> card.read_encoder(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.int32)
        >>> card.read_encoder(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_encoder(self._card if self._card is not None else ffi.NULL,
                                          ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                          num_channels,
                                          ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_digital(self, channels, num_channels, buffer):
        """Reads from digital inputs immediately. The function does not return until the data has been read.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the digital inputs to be read.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array for receiving the binary values read from the digital inputs. The array must contain
            `num_channels` elements. Each element in the returned buffer array will correspond to the same element in
            the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four digital input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('b', [0] * num_channels)
        >>> card.read_digital(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.int8)
        >>> card.read_digital(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_digital(self._card if self._card is not None else ffi.NULL,
                                          ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                          num_channels,
                                          ffi.from_buffer(_BOOLEAN_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_other(self, channels, num_channels, buffer):
        """Reads from the specified other input channels immediately. The function does not return until the data has
        been read.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the other inputs to be read.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array for receiving the values read from the other inputs. The array must contain `num_channels`
            elements. Each element in the returned buffer array will correspond to the same element in the `channels`
            array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four encoder input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0] * num_channels)
        >>> card.read_other(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> card.read_other(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_other(self._card if self._card is not None else ffi.NULL,
                                        ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                        num_channels,
                                        ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read(self,
             analog_channels, num_analog_channels,
             encoder_channels, num_encoder_channels,
             digital_channels, num_digital_channels,
             other_channels, num_other_channels,
             analog_buffer,
             encoder_buffer,
             digital_buffer,
             other_buffer):
        """Reads from the specified input channels immediately. The function does not return until the data has been
        read.

        Parameters
        ----------
        analog_channels : array_like or None
            An array containing the channel numbers of the analog outputs to be read. If no analog channels are
            required, then this parameter may be ``None``. In this case, `num_analog_channels` must be zero.
        num_analog_channels : int
            The number of channels specified in the `analog_channels` array. This parameter may be zero.
        encoder_channels : array_like or None
            An array containing the channel numbers of the encoder inputs to be read. If no encoder channels are
            required, then this parameter may be ``None``. In this case, `num_pwm_channels` must be zero.
        num_encoder_channels : int
            The number of channels specified in the `pwm_channels` array. This parameter may be zero.
        digital_channels : array_like or None
            An array containing the channel numbers of the digital outputs to be read. If no digital channels are
            required, then this parameter may be ``None``. In this case, `num_digital_channels` must be zero.
        num_digital_channels : int
            The number of channels specified in the `digital_channels` array. This parameter may be zero.
        other_channels : array_like or None
            An array containing the channel numbers of the other outputs to be read. If no other channels are
            required, then this parameter may be ``None``. In this case, `num_other_channels` must be zero.
        num_other_channels : int
            The number of channels specified in the `other_channels` array. This parameter may be zero.
        analog_buffer : array_like or None
            An array for receiving the voltage values read from the analog inputs. The array must contain
            `num_analog_channels` elements. Each element in the returned `analog_buffer` array will correspond to the
            same element in the `analog_channels` array. If no analog channels were specified, then this parameter may
            be ``None``.
        encoder_buffer : array_like or None
            An array for receiving the count values read from the encoder inputs. The array must contain
            `num_encoder_channels` elements. Each element in the returned `encoder_buffer` array will correspond to the
            same element in the `encoder_channels` array. If no digital channels were specified, then this parameter may
            be ``None``.
        digital_buffer : array_like or None
            An array for receiving the binary values read from the digital inputs. The array must contain
            `num_digital_channels` elements. Each element in the returned `digital_buffer` array will correspond to the
            same element in the `digital_channels` array. If no digital channels were specified, then this parameter may
            be ``None``.
        other_buffer : array_like or None
            An array for receiving the values read from the other inputs. The array must contain `num_other_channels`
            elements. Each element in the returned `other_buffer` array will correspond to the same element in the
            `other_channels` array. If no other channels were specified, then this parameter may be ``None``.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `read` function failing to write those outputs.

        Examples
        --------
        Read two analog input channels, two encoder input channels, and four digital input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1])
        >>> encoder_channels = array('I', [0, 1])
        >>> digital_channels = array('I', [0, 1, 2, 3])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> num_digital_channels = len(digital_channels)
        >>> analog_buffer = array('d', [0.0] * num_analog_channels)
        >>> encoder_buffer = array('i', [0] * num_encoder_channels)
        >>> digital_buffer = array('b', [0] * num_digital_channels)
        >>> card.read(analog_channels, num_analog_channels,
        ...           encoder_channels, num_encoder_channels,
        ...           digital_channels, num_digital_channels,
        ...           None, 0,
        ...           analog_buffer,
        ...           encoder_buffer,
        ...           digital_buffer,
        ...           None)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.uint32)
        >>> digital_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> num_digital_channels = len(digital_channels)
        >>> analog_buffer = np.zeros(num_analog_channels, dtype=np.float64)
        >>> encoder_buffer = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> digital_buffer = np.zeros(num_digital_channels, dtype=np.int8)
        >>> card.read(analog_channels, num_analog_channels,
        ...           encoder_channels, num_encoder_channels,
        ...           digital_channels, num_digital_channels,
        ...           None, 0,
        ...           analog_buffer,
        ...           encoder_buffer,
        ...           digital_buffer,
        ...           None)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read(self._card if self._card is not None else ffi.NULL,
                                  ffi.from_buffer(_UINT32_ARRAY, analog_channels) if analog_channels is not None else ffi.NULL,
                                  num_analog_channels,
                                  ffi.from_buffer(_UINT32_ARRAY, encoder_channels) if encoder_channels is not None else ffi.NULL,
                                  num_encoder_channels,
                                  ffi.from_buffer(_UINT32_ARRAY, digital_channels) if digital_channels is not None else ffi.NULL,
                                  num_digital_channels,
                                  ffi.from_buffer(_UINT32_ARRAY, other_channels) if other_channels is not None else ffi.NULL,
                                  num_other_channels,
                                  ffi.from_buffer(_DOUBLE_ARRAY, analog_buffer) if analog_buffer is not None else ffi.NULL,
                                  ffi.from_buffer(_INT32_ARRAY, encoder_buffer) if encoder_buffer is not None else ffi.NULL,
                                  ffi.from_buffer(_BOOLEAN_ARRAY, digital_buffer) if digital_buffer is not None else ffi.NULL,
                                  ffi.from_buffer(_DOUBLE_ARRAY, other_buffer) if other_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    # endregion

    # region Immediate Write

    def write_analog(self, channels, num_channels, buffer):
        """Writes to analog outputs immediately. The function does not return until the data has been written.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the analog outputs to be written.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array containing the voltage values to write to the analog outputs. The array must contain
            `num_channels` elements. Each element in the buffer array corresponds to the same element in the
            `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to the first four analog output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.5, 1.5, 2.5, 3.5])
        >>> card.write_analog(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.array([0.5, 1.5, 2.5, 3.5], dtype=np.float64)
        >>> card.write_analog(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write_analog(self._card if self._card is not None else ffi.NULL,
                                          ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                          num_channels,
                                          ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def write_analog_codes(self, channels, num_channels, buffer):
        """Writes to the specified analog output channels immediately using raw D/A converter values. The function does
        not return until the data has been written.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the analog outputs to be written.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array containing the raw D/A converter values to write to the analog outputs. The array must contain
            `num_channels` elements. Each element in the `buffer` array corresponds to the same element in the
            `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to the first four analog output channels using raw D/A converter values.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('i', [0x000, 0x3ff, 0x5ff, 0x7ff])
        >>> card.write_analog_codes(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.array([0x000, 0x3ff, 0x5ff, 0x7ff], dtype=np.int32)
        >>> card.write_analog_codes(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write_analog_codes(self._card if self._card is not None else ffi.NULL,
                                                ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                num_channels,
                                                ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def write_pwm(self, channels, num_channels, buffer):
        """Writes to specified PWM output channels immediately. The function does not return until the data has been
        written.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the PWM outputs to be written.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `hil_set_pwm_mode` function. The array must contain
            `num_channels` elements. Each element in the `buffer` array corresponds to the same element in the
            `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to the first four PWM output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0, 0.3, 0.7, 1.0])
        >>> card.write_pwm(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.array([0.0, 0.3, 0.7, 1.0], dtype=np.float64)
        >>> card.write_pwm(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write_pwm(self._card if self._card is not None else ffi.NULL,
                                       ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                       num_channels,
                                       ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def write_digital(self, channels, num_channels, buffer):
        """Writes to digital outputs immediately. The function does not return until the data has been written.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the digital outputs to be written.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array containing the binary values to write to the digital outputs. The array must contain
            `num_channels` elements. Each element in the `buffer` array corresponds to the same element in the
            `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to the first four PWM output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('b', [0, 1, 1, 0])
        >>> card.write_digital(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.array([0, 1, 1, 0], dtype=np.int8)
        >>> card.write_digital(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write_digital(self._card if self._card is not None else ffi.NULL,
                                           ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                           num_channels,
                                           ffi.from_buffer(_BOOLEAN_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def write_other(self, channels, num_channels, buffer):
        """Writes to the specified other output channels immediately. The function does not return until the data has
        been written.

        Parameters
        ----------
        channels : array_like
            An array containing the channel numbers of the other outputs to be written.
        num_channels : int
            The number of channels specified in the `channels` array.
        buffer : array_like
            An array containing the values to write to the other outputs. The array must contain `num_channels`
            elements. Each element in the `buffer` array corresponds to the same element in the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to the first two other output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [1.0, 0.0])
        >>> card.write_other(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.array([1.0, 0.0], dtype=np.float64)
        >>> card.write_other(channels, num_channels, buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write_other(self._card if self._card is not None else ffi.NULL,
                                         ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                         num_channels,
                                         ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def write(self,
              analog_channels, num_analog_channels,
              pwm_channels, num_pwm_channels,
              digital_channels, num_digital_channels,
              other_channels, num_other_channels,
              analog_buffer,
              pwm_buffer,
              digital_buffer,
              other_buffer):
        """Writes to the specified output channels immediately. The function does not return until the data has been
        written.

        The interpretation of the PWM samples to be written depends upon the PWM mode. Typically, the data is
        interpreted as a duty cycle, in which a magnitude of 0.0 denotes a 0% duty cycle and magnitude of 1.0 indicates
        a 100% duty cycle. The sign determines the polarity of the output for those boards supporting bidirectional PWM
        outputs. However, other PWM modes are possible with some boards. Refer to the `set_pwm_mode` function for
        details.

        Parameters
        ----------
        analog_channels : array_like or None
            An array containing the channel numbers of the analog outputs to be written. If no analog channels are
            required, then this parameter may be ``None``. In this case, `num_analog_channels` must be zero.
        num_analog_channels : int
            The number of channels specified in the `analog_channels` array. This parameter may be zero.
        pwm_channels : array_like or None
            An array containing the channel numbers of the PWM outputs to be written. If no PWM channels are required,
            then this parameter may be ``None``. In this case, `num_pwm_channels` must be zero.
        num_pwm_channels : int
            The number of channels specified in the `pwm_channels` array. This parameter may be zero.
        digital_channels : array_like or None
            An array containing the channel numbers of the digital outputs to be written. If no digital channels are
            required, then this parameter may be ``None``. In this case, `num_digital_channels` must be zero.
        num_digital_channels : int
            The number of channels specified in the `digital_channels` array. This parameter may be zero.
        other_channels : array_like or None
            An array containing the channel numbers of the other outputs to be written. If no other channels are
            required, then this parameter may be ``None``. In this case, `num_other_channels` must be zero.
        num_other_channels : int
            The number of channels specified in the `other_channels` array. This parameter may be zero.
        analog_buffer : array_like
            An array containing the voltage values to write to the analog outputs. The array must contain
            `num_analog_channels` elements. Each element in the `analog_buffer` array corresponds to the same element in
            the `analog_channels` array. If no analog channels were specified, then this parameter may be ``None``.
        pwm_buffer : array_like or None
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `set_pwm_mode` function. The array must contain
            `num_pwm_channels` elements. Each element in the `pwm_buffer` array corresponds to the same element in the
            `pwm_channels` array. If no PWM channels were specified, then this parameter may be ``None``.
        digital_buffer : array_like or None
            An array containing the binary values to write to the digital outputs. The array must contain
            `num_digital_channels` elements. Each element in the `digital_buffer` array corresponds to the same element
            in the `digital_channels` array. If no digital channels were specified, then this parameter may be ``None``.
        other_buffer : array_like or None
            An array containing the values to write to the other outputs. The array must contain `num_other_channels`
            elements. Each element in the `other_buffer` array corresponds to the same element in the
            `other_channels` array. If no other channels were specified, then this parameter may be ``None``.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `write` function failing to write those outputs.

        Examples
        --------
        Write to two analog output channels, two PWM output channels, and four digital output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1])
        >>> pwm_channels = array('I', [0, 1])
        >>> digital_channels = array('I', [0, 1, 2, 3])
        >>> num_analog_channels = len(analog_channels)
        >>> num_pwm_channels = len(pwm_channels)
        >>> num_digital_channels = len(digital_channels)
        >>> analog_buffer = array('d', [0.5, -0.5])
        >>> pwm_buffer = array('d', [-1000.0, 1000.0])
        >>> digital_buffer = array('b', [0, 1, 0, 1])
        >>> card.write(analog_channels, num_analog_channels,
        ...            pwm_channels, num_pwm_channels,
        ...            digital_channels, num_digital_channels,
        ...            None, 0,
        ...            analog_buffer,
        ...            pwm_buffer,
        ...            digital_buffer,
        ...            None)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1], dtype=np.uint32)
        >>> pwm_channels = np.array([0, 1], dtype=np.uint32)
        >>> digital_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_pwm_channels = len(pwm_channels)
        >>> num_digital_channels = len(digital_channels)
        >>> analog_buffer = np.array([0.5, -0.5], dtype=np.float64)
        >>> pwm_buffer = np.array([-1000.0, 1000.0], dtype=np.int32)
        >>> digital_buffer = np.array([0, 1, 0, 1], dtype=np.int8)
        >>> card.write(analog_channels, num_analog_channels,
        ...            pwm_channels, num_pwm_channels,
        ...            digital_channels, num_digital_channels,
        ...            None, 0,
        ...            analog_buffer,
        ...            pwm_buffer,
        ...            digital_buffer,
        ...            None)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_write(self._card if self._card is not None else ffi.NULL,
                                   ffi.from_buffer(_UINT32_ARRAY, analog_channels) if analog_channels is not None else ffi.NULL,
                                   num_analog_channels,
                                   ffi.from_buffer(_UINT32_ARRAY, pwm_channels) if pwm_channels is not None else ffi.NULL,
                                   num_pwm_channels,
                                   ffi.from_buffer(_UINT32_ARRAY, digital_channels) if digital_channels is not None else ffi.NULL,
                                   num_digital_channels,
                                   ffi.from_buffer(_UINT32_ARRAY, other_channels) if other_channels is not None else ffi.NULL,
                                   num_other_channels,
                                   ffi.from_buffer(_DOUBLE_ARRAY, analog_buffer) if analog_buffer is not None else ffi.NULL,
                                   ffi.from_buffer(_DOUBLE_ARRAY, pwm_buffer) if pwm_buffer is not None else ffi.NULL,
                                   ffi.from_buffer(_BOOLEAN_ARRAY, digital_buffer) if digital_buffer is not None else ffi.NULL,
                                   ffi.from_buffer(_DOUBLE_ARRAY, other_buffer) if other_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    # endregion

    # region Immediate Read/Write

    def read_analog_write_analog(self,
                                 input_channels, num_input_channels,
                                 output_channels, num_output_channels,
                                 input_buffer,
                                 output_buffer):
        """Reads from the specified analog input channels and writes to the specified analog output channels in a
        single function call. The write operation occurs immediately following the read operation. Since the read-write
        operation occurs at the lowest level, the read and write occur virtually concurrently. The function does not
        return until the data has been read and written.

        Parameters
        ----------
        input_channels : array_like
            An array containing the channel numbers of the analog inputs to be read.
        num_input_channels : int
            The number of channels specified in the `input_channels` array.
        output_channels : array_like
            An array containing the channel numbers of the analog outputs to be written.
        num_output_channels : int
            The number of channels specified in the `output_channels` array.
        input_buffer : array_like
            An array for receiving the voltage values read from the analog inputs.
            The array must contain `num_input_channels` elements. Each element in the returned `input_buffer` array
            will correspond to the same element in the `input_channels` array.
        output_buffer : array_like
            An array of voltage values to write to the analog outputs.
            The array must contain `num_output_channels` elements. Each element in the `output_buffer` array
            corresponds to the same element in the `output_channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four analog input channels and writes to the first two analog output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = array('I', [0, 1, 2, 3])
        >>> output_channels = array('I', [0, 1])
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = array('d', [0.0] * num_input_channels])
        >>> output_buffer = array('d', [0.5, 1.5])
        >>> card.read_analog_write_analog(input_channels, num_input_channels,
        ...                               output_channels, num_output_channels,
        ...                               input_buffer,
        ...                               output_buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> output_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = np.zeros(num_input_channels, dtype=np.float64)
        >>> output_buffer = np.array([0.5, 1.5], dtype=np.float64)
        >>> card.read_analog_write_analog(input_channels, num_input_channels,
        ...                               output_channels, num_output_channels,
        ...                               input_buffer,
        ...                               output_buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_analog_write_analog(self._card if self._card is not None else ffi.NULL,
                                                      ffi.from_buffer(_UINT32_ARRAY, input_channels) if input_channels is not None else ffi.NULL,
                                                      num_input_channels,
                                                      ffi.from_buffer(_UINT32_ARRAY, output_channels) if output_channels is not None else ffi.NULL,
                                                      num_output_channels,
                                                      ffi.from_buffer(_DOUBLE_ARRAY, input_buffer) if input_buffer is not None else ffi.NULL,
                                                      ffi.from_buffer(_DOUBLE_ARRAY, output_buffer) if output_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_encoder_write_pwm(self,
                               input_channels, num_input_channels,
                               output_channels, num_output_channels,
                               input_buffer,
                               output_buffer):
        """Reads from the specified encoder input channels and writes to the specified PWM output channels in a single
        function call. The write operation occurs immediately following the read operation. Since the read-write
        operation occurs at the lowest level, the read and write occur virtually concurrently. The function does not
        return until the data has been read and written.

        The interpretation of the PWM data to be written depends upon the PWM mode. Typically, the data is interpreted
        as a duty cycle, in which a magnitude of 0.0 denotes a 0% duty cycle and magnitude of 1.0 indicates a 100% duty
        cycle. The sign determines the polarity of the output for those boards supporting bidirectional PWM outputs.
        However, other PWM modes are possible with some boards. Refer to the `set_pwm_mode` function for details.

        Parameters
        ----------
        input_channels : array_like
            An array containing the channel numbers of the encoder inputs to be read.
        num_input_channels : int
            The number of channels specified in the `input_channels` array.
        output_channels : array_like
            An array containing the channel numbers of the PWM outputs to be written.
        num_output_channels : int
            The number of channels specified in the `output_channels` array.
        input_buffer : array_like
            An array for receiving the counter values read from the encoder inputs.
            The array must contain `num_input_channels` elements. Each element in the returned `input_buffer` array
            will correspond to the same element in the `input_channels` array.
        output_buffer : array_like
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `set_pwm_mode` function.
            The array must contain `num_output_channels` elements. Each element in the `output_buffer` array
            corresponds to the same element in the `output_channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four encoder input channels and writes to the first two PWM output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = array('I', [0, 1, 2, 3])
        >>> output_channels = array('I', [0, 1])
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = array('i', [0] * num_input_channels])
        >>> output_buffer = array('d', [0.7, 0.3])
        >>> card.read_encoder_write_pwm(input_channels, num_input_channels,
        ...                             output_channels, num_output_channels,
        ...                             input_buffer,
        ...                             output_buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> output_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = np.zeros(num_input_channels, dtype=np.int32)
        >>> output_buffer = np.array([0.7, 0.3], dtype=np.float64)
        >>> card.read_encoder_write_pwm(input_channels, num_input_channels,
        ...                             output_channels, num_output_channels,
        ...                             input_buffer,
        ...                             output_buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_encoder_write_pwm(self._card if self._card is not None else ffi.NULL,
                                                    ffi.from_buffer(_UINT32_ARRAY, input_channels) if input_channels is not None else ffi.NULL,
                                                    num_input_channels,
                                                    ffi.from_buffer(_UINT32_ARRAY, output_channels) if output_channels is not None else ffi.NULL,
                                                    num_output_channels,
                                                    ffi.from_buffer(_INT32_ARRAY, input_buffer) if input_buffer is not None else ffi.NULL,
                                                    ffi.from_buffer(_DOUBLE_ARRAY, output_buffer) if output_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_digital_write_digital(self,
                                   input_channels, num_input_channels,
                                   output_channels, num_output_channels,
                                   input_buffer,
                                   output_buffer):
        """Reads from digital inputs and writes to digital outputs immediately.

        Reads from the specified digital input channels and writes to the specified digital output channels in a single
        function call. The write operation occurs immediately following the read operation. Since the read-write
        operation occurs at the lowest level the read and write occur virtually concurrently. The function does not
        return until the data has been read and written.

        Parameters
        ----------
        input_channels : array_like
            An array containing the channel numbers of the digital inputs to be read.
        num_input_channels : int
            The number of channels specified in the `input_channels` array.
        output_channels : array_like
            An array containing the channel numbers of the digital outputs to be written.
        num_output_channels : int
            The number of channels specified in the `output_channels` array.
        input_buffer : array_like
            An array for receiving the voltage values read from the digital inputs.
            The array must contain `num_input_channels` elements. Each element in the returned `input_buffer` array
            will correspond to the same element in the `input_channels` array.
        output_buffer : array_like
            An array of voltage values to write to the digital outputs. The array must contain `num_output_channels`
            elements. Each element in the `output_buffer` array corresponds to the same element in the
            `output_channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four digital input channels and writes to digital output channels 5 and 7.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = array('I', [0, 1, 2, 3])
        >>> output_channels = array('I', [5, 7])
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = array('b', [0] * num_input_channels])
        >>> output_buffer = array('b', [1, 0])
        >>> card.read_digital_write_digital(input_channels, num_input_channels,
        ...                                 output_channels, num_output_channels,
        ...                                 input_buffer,
        ...                                 output_buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> output_channels = np.array([5, 7], dtype=np.uint32)
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = np.zeros(num_input_channels, dtype=np.int8)
        >>> output_buffer = np.array([1, 0], dtype=np.int8)
        >>> card.read_digital_write_digital(input_channels, num_input_channels,
        ...                                 output_channels, num_output_channels,
        ...                                 input_buffer,
        ...                                 output_buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_digital_write_digital(self._card if self._card is not None else ffi.NULL,
                                                        ffi.from_buffer(_UINT32_ARRAY, input_channels) if input_channels is not None else ffi.NULL,
                                                        num_input_channels,
                                                        ffi.from_buffer(_UINT32_ARRAY, output_channels) if output_channels is not None else ffi.NULL,
                                                        num_output_channels,
                                                        ffi.from_buffer(_BOOLEAN_ARRAY, input_buffer) if input_buffer is not None else ffi.NULL,
                                                        ffi.from_buffer(_BOOLEAN_ARRAY, output_buffer) if output_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_other_write_other(self,
                               input_channels, num_input_channels,
                               output_channels, num_output_channels,
                               input_buffer,
                               output_buffer):
        """Reads from digital inputs and writes to digital outputs immediately.

        Reads from the specified digital input channels and writes to the specified digital output channels in a single
        function call. The write operation occurs immediately following the read operation. Since the read-write
        operation occurs at the lowest level the read and write occur virtually concurrently. The function does not
        return until the data has been read and written.

        Parameters
        ----------
        input_channels : array_like
            An array containing the channel numbers of the digital inputs to be read.
        num_input_channels : int
            The number of channels specified in the `input_channels` array.
        output_channels : array_like
            An array containing the channel numbers of the digital outputs to be written.
        num_output_channels : int
            The number of channels specified in the `output_channels` array.
        input_buffer : array_like
            An array for receiving the voltage values read from the digital inputs.
            The array must contain `num_input_channels` elements. Each element in the returned `input_buffer` array
            will correspond to the same element in the `input_channels` array.
        output_buffer : array_like
            An array of voltage values to write to the digital outputs. The array must contain `num_output_channels`
            elements. Each element in the `output_buffer` array corresponds to the same element in the
            `output_channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Read the first four other input channels and writes to the first two other output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = array('I', [0, 1, 2, 3])
        >>> output_channels = array('I', [0, 1])
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = array('d', [0] * num_input_channels])
        >>> output_buffer = array('d', [0.5, 1.5])
        >>> card.read_other_write_other(input_channels, num_input_channels,
        ...                             output_channels, num_output_channels,
        ...                             input_buffer,
        ...                             output_buffer)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> input_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> output_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_input_channels = len(input_channels)
        >>> num_output_channels = len(output_channels)
        >>> input_buffer = np.zeros(num_input_channels, dtype=np.float64)
        >>> output_buffer = np.array([0.5, 1.5], dtype=np.float64)
        >>> card.read_other_write_other(input_channels, num_input_channels,
        ...                             output_channels, num_output_channels,
        ...                             input_buffer,
        ...                             output_buffer)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_other_write_other(self._card if self._card is not None else ffi.NULL,
                                                    ffi.from_buffer(_UINT32_ARRAY, input_channels) if input_channels is not None else ffi.NULL,
                                                    num_input_channels,
                                                    ffi.from_buffer(_UINT32_ARRAY, output_channels) if output_channels is not None else ffi.NULL,
                                                    num_output_channels,
                                                    ffi.from_buffer(_DOUBLE_ARRAY, input_buffer) if input_buffer is not None else ffi.NULL,
                                                    ffi.from_buffer(_DOUBLE_ARRAY, output_buffer) if output_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def read_write(self,
                   analog_input_channels, num_analog_input_channels,
                   encoder_input_channels, num_encoder_input_channels,
                   digital_input_channels, num_digital_input_channels,
                   other_input_channels, num_other_input_channels,

                   analog_output_channels, num_analog_output_channels,
                   pwm_output_channels, num_pwm_output_channels,
                   digital_output_channels, num_digital_output_channels,
                   other_output_channels, num_other_output_channels,

                   analog_input_buffer,
                   encoder_input_buffer,
                   digital_input_buffer,
                   other_input_buffer,

                   analog_output_buffer,
                   pwm_output_buffer,
                   digital_output_buffer,
                   other_output_buffer):
        """Reads from inputs and writes to outputs immediately.

        Reads from the specified analog, encoder, digital and/or other input channels and writes to the specified
        analog, PWM, digital and/or other output channels in a single function call. The write operation occurs
        immediately following the read operation. Since the read-write operation occurs at the lowest level the read
        and write occur virtually concurrently. The function does not return until the data has been read and written.

        Parameters
        ----------
        analog_input_channels : array_like or None
            An array containing the channel numbers of the analog inputs to be read. If no analog input channels are
            required, then this parameter may be ``None``. In this case, `num_analog_input_channels` must be zero.
        num_analog_input_channels : int
            The number of channels specified in the `analog_input_channels` array. This parameter may be zero.
        encoder_input_channels : array_like or None
            An array containing the channel numbers of the encoder inputs to be read. If no encoder input channels are
            required, then this parameter may be ``None``. In this case, `num_encoder_input_channels` must be zero.
        num_encoder_input_channels : int
            The number of channels specified in the `encoder_input_channels` array. This parameter may be zero.
        digital_input_channels : array_like or None
            An array containing the channel numbers of the digital inputs to be read. If no digital input channels are
            required, then this parameter may be ``None``. In this case, num_digital_input_channels must be zero.
        num_digital_input_channels : int
            The number of channels specified in the `digital_input_channels` array. This parameter may be zero.
        other_input_channels : array_like or None
            An array containing the channel numbers of the other inputs to be read. If no other input channels are
            required, then this parameter may be ``None``. In this case, `num_other_input_channels` must be zero.
        num_other_input_channels : int
            The number of channels specified in the `other_input_channels` array. This parameter may be zero.

        analog_output_channels : array_like or None
            An array containing the channel numbers of the analog outputs to be written. If no analog output channels
            are required, then this parameter may be ``None``. In this case, `num_analog_output_channels` must be zero.
        num_analog_output_channels : int
            The number of channels specified in the `analog_output_channels` array. This parameter may be zero.
        pwm_output_channels : array_like or None
            An array containing the channel numbers of the PWM outputs to be written. If no PWM output channels are
            required, then this parameter may be ``None``. In this case, `num_pwm_output_channels` must be zero.
        num_pwm_output_channels : int
            The number of channels specified in the `pwm_output_channels` array. This parameter may be zero.
        digital_output_channels : array_like or None
            An array containing the channel numbers of the digital outputs to be written. If no digital output channels
            are required, then this parameter may be ``None``. In this case, `num_digital_output_channels` must be zero.
        num_digital_output_channels : int
            The number of channels specified in the `digital_output_channels` array. This parameter may be zero.
        other_output_channels : array_like or None
            An array containing the channel numbers of the other outputs to be written. If no other output channels are
            required, then this parameter may be ``None``. In this case, `num_other_output_channels` must be zero.
        num_other_output_channels : int
            The number of channels specified in the `other_output_channels` array. This parameter may be zero.

        analog_input_buffer : array_like or None
            An array for receiving the voltage values read from the analog inputs. The array must contain
            `num_analog_input_channels` elements. Each element in the returned `analog_input_buffer` array will
            correspond to the same element in the `analog_input_channels` array.
            If no analog input channels were specified, then this parameter may be ``None``.
        encoder_input_buffer : array_like or None
            An array for receiving the counter values read from the encoder inputs. The array must contain
            `num_encoder_input_channels` elements. Each element in the returned `encoder_input_buffer` array will
            correspond to the same element in the encoder_input_channels array.
            If no encoder input channels were specified, then this parameter may be ``None``.
        digital_input_buffer : array_like or None
            An array for receiving the voltage values read from the digital inputs. The array must contain
            `num_digital_input_channels` elements. Each element in the returned `digital_input_buffer` array will
            correspond to the same element in the `digital_input_channels` array.
            If no digital input channels were specified, then this parameter may be ``None``.
        other_input_buffer : array_like or None
            An array for receiving the values read from the other inputs. The array must contain
            `num_other_input_channels elements`. Each element in the returned `other_input_buffer` array will
            correspond to the same element in the other_input_channels array.
            If no other input channels were specified, then this parameter may be ``None``.

        analog_output_buffer : array_like or None
            An array of voltage values to write to the analog outputs. The array must contain
            `num_analog_output_channels` elements. Each element in the `analog_output_buffer` array corresponds to the
            same element in the analog_output_channels array.
            If no analog output channels were specified, then this parameter may be ``None``.
        pwm_output_buffer : array_like or None
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `hil_set_pwm_mode` function. The array must contain
            `num_pwm_output_channels` elements. Each element in the `pwm_output_buffer` array corresponds to the same
            element in the `pwm_output_channels` array.
            If no PWM output channels were specified, then this parameter may be ``None``.
        digital_output_buffer : array_like or None
            An array of voltage values to write to the digital outputs. The array must contain
            `num_digital_output_channels` elements. Each element in the `digital_output_buffer` array corresponds to
            the same element in the `digital_output_channels` array.
            If no digital output channels were specified, then this parameter may be ``None``.
        other_output_buffer : array_like or None
            An array of values to write to the other outputs. The array must contain `num_other_output_channels`
            elements. Each element in the `other_output_buffer` array corresponds to the same element in the
            `other_output_channels` array.
            If no other output channels were specified, then this parameter may be ``None``.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Write to two analog output channels, two PWM output channels, and four digital output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_input_channels = array('I', [0, 1])
        >>> encoder_input_channels = array('I', [0, 1])
        >>> digital_input_channels = array('I', [0, 1])
        >>> analog_output_channels = array('I', [0, 1])
        >>> digital_output_channels = array('I', [5, 6, 7])
        >>> num_analog_input_channels = len(analog_input_channels)
        >>> num_encoder_input_channels = len(encoder_input_channels)
        >>> num_digital_input_channels = len(digital_input_channels)
        >>> num_analog_output_channels = len(analog_output_channels)
        >>> num_digital_output_channels = len(digital_output_channels)
        >>> analog_input_buffer = array('d', [0.0] * num_analog_input_channels)
        >>> encoder_input_buffer = array('i', [0] * num_encoder_input_channels)
        >>> digital_input_buffer = array('b', [0] * num_digital_input_channels)
        >>> analog_output_buffer = array('d', [0.5, 1.5])
        >>> digital_output_buffer = array('b', [1, 0, 1])
        >>> card.read_write(analog_input_channels, num_analog_input_channels,
        ...                 encoder_input_channels, num_encoder_input_channels,
        ...                 digital_input_channels, num_digital_input_channels,
        ...                 None, 0,
        ...                 analog_output_channels, num_analog_output_channels,
        ...                 None, 0,
        ...                 digital_output_channels, num_digital_output_channels,
        ...                 None, 0,
        ...                 analog_input_buffer,
        ...                 encoder_input_buffer,
        ...                 digital_input_buffer,
        ...                 None,
        ...                 analog_output_buffer,
        ...                 None,
        ...                 digital_output_buffer,
        ...                 None)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> analog_input_channels = np.array([0, 1], dtype=np.uint32)
        >>> encoder_input_channels = np.array([0, 1], dtype=np.uint32)
        >>> digital_input_channels = np.array([0, 1], dtype=np.uint32)
        >>> analog_output_channels = np.array([0, 1], dtype=np.uint32)
        >>> digital_output_channels = np.array([5, 6, 7], dtype=np.uint32)
        >>> num_analog_input_channels = len(analog_input_channels)
        >>> num_encoder_input_channels = len(encoder_input_channels)
        >>> num_digital_input_channels = len(digital_input_channels)
        >>> num_analog_output_channels = len(analog_output_channels)
        >>> num_digital_output_channels = len(digital_output_channels)
        >>> analog_input_buffer = np.zeros(num_analog_input_channels, dtype=np.float64)
        >>> encoder_input_buffer = np.zeros(num_encoder_input_channels, dtype=np.int32)
        >>> digital_input_buffer = np.zeros(num_digital_input_channels, dtype=np.int8)
        >>> analog_output_buffer = np.array([0.5, 1.5], dtype=np.float64)
        >>> digital_output_buffer = np.array([1, 0, 1], dtype=np.int8)
        >>> card.read_write(analog_input_channels, num_analog_input_channels,
        ...                 encoder_input_channels, num_encoder_input_channels,
        ...                 digital_input_channels, num_digital_input_channels,
        ...                 None, 0,
        ...                 analog_output_channels, num_analog_output_channels,
        ...                 None, 0,
        ...                 digital_output_channels, num_digital_output_channels,
        ...                 None, 0,
        ...                 analog_input_buffer,
        ...                 encoder_input_buffer,
        ...                 digital_input_buffer,
        ...                 None,
        ...                 analog_output_buffer,
        ...                 None,
        ...                 digital_output_buffer,
        ...                 None)
        ...
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_read_write(self._card if self._card is not None else ffi.NULL,
                                        ffi.from_buffer(_UINT32_ARRAY, analog_input_channels) if analog_input_channels is not None else ffi.NULL,
                                        num_analog_input_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, encoder_input_channels) if encoder_input_channels is not None else ffi.NULL,
                                        num_encoder_input_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, digital_input_channels) if digital_input_channels is not None else ffi.NULL,
                                        num_digital_input_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, other_input_channels) if other_input_channels is not None else ffi.NULL,
                                        num_other_input_channels,

                                        ffi.from_buffer(_UINT32_ARRAY, analog_output_channels) if analog_output_channels is not None else ffi.NULL,
                                        num_analog_output_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, pwm_output_channels) if pwm_output_channels is not None else ffi.NULL,
                                        num_pwm_output_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, digital_output_channels) if digital_output_channels is not None else ffi.NULL,
                                        num_digital_output_channels,
                                        ffi.from_buffer(_UINT32_ARRAY, other_output_channels) if other_output_channels is not None else ffi.NULL,
                                        num_other_output_channels,

                                        ffi.from_buffer(_DOUBLE_ARRAY, analog_input_buffer) if analog_input_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_INT32_ARRAY, encoder_input_buffer) if encoder_input_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_BOOLEAN_ARRAY, digital_input_buffer) if digital_input_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_DOUBLE_ARRAY, other_input_buffer) if other_input_buffer is not None else ffi.NULL,

                                        ffi.from_buffer(_DOUBLE_ARRAY, analog_output_buffer) if analog_output_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_DOUBLE_ARRAY, pwm_output_buffer) if pwm_output_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_BOOLEAN_ARRAY, digital_output_buffer) if digital_output_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_DOUBLE_ARRAY, other_output_buffer) if other_output_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    # endregion

    # endregion

    # region Buffered I/O

    # endregion

    # region Task I/O

    def task_create_analog_reader(self, samples_in_buffer, channels, num_channels):
        """Creates a task for reading from the specified analog input channels. The task allows other operations to be
        performed while the analog inputs are being read "in the background". The data is read into an internal circular
        "task buffer" from which it can be read at any time using the `task_read_analog` function. The size of this task
        buffer is determined by the `samples_in_buffer` parameter.

        The task does not actually start reading from the analog inputs until the `task_start` function is called. The
        task must be deleted when it is no longer in use using the `task_delete` function, in order to free the system
        and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_read_analog` function cannot read more samples than this
            in a single call. If the task buffer overflows because `task_read_analog` has not been called in time to
            remove the data from the task buffer, then the next call to `task_read_analog` will return a
            `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the analog inputs to be read by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to read from the first four analog input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_analog_reader(self._card if self._card is not None else ffi.NULL,
                                                       samples_in_buffer,
                                                       ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                       num_channels,
                                                       task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_encoder_reader(self, samples_in_buffer, channels, num_channels):
        """Creates a task for reading from the specified encoder input channels. The task allows other operations to be
        performed while the encoder inputs are being read "in the background". The data is read into an internal
        circular "task buffer" from which it can be read at any time using the `task_read_encoder` function. The size of
        this task buffer is determined by the `samples_in_buffer` parameter.

        The task does not actually start reading from the encoder inputs until the `task_start` function is called. The
        task must be deleted when it is no longer in use using the `task_delete` function, in order to free the system
        and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_read_encoder` function cannot read more samples than
            this in a single call. If the task buffer overflows because `task_read_encoder` has not been called in time
            to remove the data from the task buffer, then the next call to `task_read_encoder` will return a
            `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the encoder inputs to be read by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to read from the first four encoder input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_encoder_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_encoder_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_encoder_reader(self._card if self._card is not None else ffi.NULL,
                                                        samples_in_buffer,
                                                        ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                        num_channels,
                                                        task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_digital_reader(self, samples_in_buffer, channels, num_channels):
        """Creates a task for reading from the specified digital input channels. The task allows other operations to be
        performed while the digital inputs are being read "in the background". The data is read into an internal
        circular "task buffer" from which it can be read at any time using the hil_task_read_digital function. The size
        of this task buffer is determined by the `samples_in_buffer` parameter.

        The task does not actually start reading from the digital inputs until the `task_start` function is called.
        Before starting the task, the directions of the digital I/O lines should be set using the
        `set_digital_directions` function. The task must be deleted when it is no longer in use using the `task_delete`
        function, in order to free the system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_read_digital` function cannot read more samples than
            this in a single call. If the task buffer overflows because `task_read_digital` has not been called in time
            to remove the data from the task buffer, then the next call to `task_read_digital` will return a
            `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the digital inputs to be read by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital inputs or outputs must be configured accordingly using this function. Failure to configure the
        digital I/O may result in the `task_read_digital` function failing to read or write the digital I/O as expected.

        Examples
        --------
        Create a task to read from the first four digital input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_digital_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_digital_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_digital_reader(self._card if self._card is not None else ffi.NULL,
                                                        samples_in_buffer,
                                                        ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                        num_channels,
                                                        task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_other_reader(self, samples_in_buffer, channels, num_channels):
        """Creates a task for reading from the specified other input channels. The task allows other operations to be
        performed while the other inputs are being read "in the background". The data is read into an internal circular
        "task buffer" from which it can be read at any time using the `task_read_other` function. The size of this
        task buffer is determined by the `samples_in_buffer` parameter.

        The task does not actually start reading from the other inputs until the `task_start` function is called. The
        task must be deleted when it is no longer in use using the `task_delete` function, in order to free the system
        and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_read_other` function cannot read more samples than this
            in a single call. If the task buffer overflows because `task_read_other` has not been called in time to
            remove the data from the task buffer, then the next call to `task_read_other` will return a
            `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the other inputs to be read by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to read from the first two other input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> card.task_create_other_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_other_reader(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_other_reader(self._card if self._card is not None else ffi.NULL,
                                                      samples_in_buffer,
                                                      ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                      num_channels,
                                                      task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_reader(self,
                           samples_in_buffer,
                           analog_channels, num_analog_channels,
                           encoder_channels, num_encoder_channels,
                           digital_channels, num_digital_channels,
                           other_channels, num_other_channels):
        """Creates a task for reading from the specified input channels. The task allows other operations to be
        performed while the inputs are being read "in the background". The data is read into an internal circular
        "task buffer" from which it can be read at any time using the `task_read` function. The size of this task buffer
        is determined by the `samples_in_buffer` parameter.

        The task does not actually start reading from the inputs until the `task_start` function is called. Before
        starting the task, the directions of the digital I/O lines should be set using the `set_digital_directions`
        function. The task must be deleted when it is no longer in use using the `task_delete` function, in order to
        free the system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_read` function cannot read more samples than this in a
            single call. If the task buffer overflows because `task_read` has not been called in time to remove the data
            from the task buffer, then the next call to `task_read` will return a `HIL_BUFFER_OVERFLOW` error.
        analog_channels : array_like or None
            An array containing the channel numbers of the analog inputs to be read by the task. If no analog channels
            are required, then this parameter may be ``None``. In this case, `num_analog_channels` must be zero.
        num_analog_channels : int
            The number of channels specified in the `analog_channels` array.
        encoder_channels : array_like or None
            An array containing the channel numbers of the encoder inputs to be read by the task. If no encoder channels
            are required, then this parameter may be ``None``. In this case, `num_encoder_channels` must be zero.
        num_encoder_channels : int
            The number of channels specified in the `encoder_channels` array.
        digital_channels : array_like or None
            An array containing the channel numbers of the digital inputs to be read by the task. If no digital channels
            are required, then this parameter may be ``None``. In this case, `num_digital_channels` must be zero.
        num_digital_channels : int
            The number of channels specified in the `digital_channels` array.
        other_channels : array_like or None
            An array containing the channel numbers of the other inputs to be read by the task. If no other channels
            are required, then this parameter may be ``None``. In this case, `num_other_channels` must be zero.
        num_other_channels : int
            The number of channels specified in the `other_channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital inputs or outputs must be configured accordingly using this function. Failure to configure the
        digital I/O may result in the `task_read` function failing to read or write the digital I/O as expected.

        Examples
        --------
        Create a task to read from the first four analog input channels and the first two encoder input channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> card.task_create_reader(samples_in_buffer,
        ...                         analog_channels, num_analog_channels
        ...                         encoder_channels, num_encoder_channels,
        ...                         None, 0,
        ...                         None, 0)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> card.task_create_reader(samples_in_buffer,
        ...                         analog_channels, num_analog_channels
        ...                         encoder_channels, num_encoder_channels,
        ...                         None, 0,
        ...                         None, 0)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_reader(self._card if self._card is not None else ffi.NULL,
                                                samples_in_buffer,
                                                ffi.from_buffer(_UINT32_ARRAY, analog_channels) if analog_channels is not None else ffi.NULL,
                                                num_analog_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, encoder_channels) if encoder_channels is not None else ffi.NULL,
                                                num_encoder_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, digital_channels) if digital_channels is not None else ffi.NULL,
                                                num_digital_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, other_channels) if other_channels is not None else ffi.NULL,
                                                num_other_channels,
                                                task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_analog_writer(self, samples_in_buffer, channels, num_channels):
        """Creates a task for writing to the specified analog output channels. The task allows other operations to be
        performed while the analog outputs are being written "in the background". The data written to the analog outputs
        is read from an internal circular "task buffer". This data may be written into the task buffer at any time using
        the `task_write_analog` function. The size of this task buffer is determined by the `samples_in_buffer`
        parameter.

        The task does not actually start reading the data from the task buffer and writing it to the analog outputs
        until the `task_start` function is called. In order for data to be available in the task buffer as soon as the
        task starts, store data in the buffer using `task_write_analog` prior to starting the task. Since the task
        writes to the analog outputs at the sampling rate specified when the task is started, it will be reading data
        from the task buffer at that rate. Thus, `task_write_analog` must be called to add more data to the task buffer
        before all the data in the buffer is depleted. Otherwise, the task will have no data to write to the analog
        outputs and will return with a `QERR_BUFFER_OVERFLOW` error the next time `task_write_analog` is called.

        The task must be deleted when it is no longer in use using the `task_delete` function, in order to free the
        system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_write_analog` function cannot write more samples than
            this in a single call. If the task buffer underflows because `task_write_analog` has not been called in time
            to add data to the task buffer, then the next call to `task_write_analog` will return a`HIL_BUFFER_OVERFLOW`
            error.
        channels : array_like
            An array containing the channel numbers of the analog outputs to be written to by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to write to the first four analog output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_analog_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_analog_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_analog_writer(self._card if self._card is not None else ffi.NULL,
                                                       samples_in_buffer,
                                                       ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                       num_channels,
                                                       task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_pwm_writer(self, samples_in_buffer, channels, num_channels):
        """Creates a task for writing to the specified PWM output channels. The task allows other operations to be
        performed while the PWM outputs are being written "in the background". The data written to the PWM outputs is
        read from an internal circular "task buffer". This data may be written into the task buffer at any time using
        the `task_write_pwm` function. The size of this task buffer is determined by the samples_in_buffer parameter.

        The task does not actually start reading the data from the task buffer and writing it to the PWM outputs until
        the `task_start` function is called. In order for data to be available in the task buffer as soon as the task
        starts, store data in the buffer using `task_write_pwm` prior to starting the task. Since the task writes to the
        PWM outputs at the sampling rate specified when the task is started, it will be reading data from the task
        buffer at that rate. Thus, `task_write_pwm` must be called to add more data to the task buffer before all the
        data in the buffer is depleted. Otherwise, the task will have no data to write to the PWM outputs and will
        return with a `QERR_BUFFER_OVERFLOW` error the next time `task_write_pwm` is called.

        The task must be deleted when it is no longer in use using the `task_delete` function, in order to free the
        system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_write_pwm` function cannot write more samples than this
            in a single call. If the task buffer underflows because `task_write_pwm` has not been called in time to add
            data to the task buffer, then the next call to `task_write_pwm` will return a `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the PWM outputs to be written to by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to write to the first two PWM output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> card.task_create_pwm_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_pwm_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_pwm_writer(self._card if self._card is not None else ffi.NULL,
                                                    samples_in_buffer,
                                                    ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                    num_channels,
                                                    task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_digital_writer(self, samples_in_buffer, channels, num_channels):
        """Creates a task for writing to the specified digital output channels. The task allows other operations to be
        performed while the digital outputs are being written "in the background". The data written to the digital
        outputs is read from an internal circular "task buffer". This data may be written into the task buffer at any
        time using the hil_task_write_digital function. The size of this task buffer is determined by the
        `samples_in_buffer` parameter.

        The task does not actually start reading the data from the task buffer and writing it to the digital outputs
        until the `task_start` function is called. Before starting the task, the directions of the digital I/O lines
        should be set using the `set_digital_directions` function. Also, in order for data to be available in the task
        buffer as soon as the task starts, store data in the buffer using `task_write_digital` prior to starting the
        task. Since the task writes to the digital outputs at the sampling rate specified when the task is started, it
        will be reading data from the task buffer at that rate. Thus, `task_write_digital` must be called to add more
        data to the task buffer before all the data in the buffer is depleted. Otherwise the task will have no data to
        write to the digital outputs and will return with a `QERR_BUFFER_OVERFLOW` error the next time
        `task_write_digital` is called.

        The task must be deleted when it is no longer in use using the `task_delete` function, in order to free the
        system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_write_digital` function cannot write more samples than
            this in a single call. If the task buffer underflows because `task_write_digital` has not been called in
            time to add data to the task buffer then the next call to `task_write_digital` will return an
            `HIL_BUFFER_OVERFLOW` error.
        channels : array_like
            An array containing the channel numbers of the digital outputs to be written to by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `task_write_digital` function failing to write those outputs.

        Examples
        --------
        Create a task to write to the first four digital output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_digital_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_digital_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_digital_writer(self._card if self._card is not None else ffi.NULL,
                                                        samples_in_buffer,
                                                        ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                        num_channels,
                                                        task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_other_writer(self, samples_in_buffer, channels, num_channels):
        """Creates a task for writing to the specified other output channels. The task allows other operations to be
        performed while the other outputs are being written "in the background". The data written to the other outputs
        is read from an internal circular "task buffer". This data may be written into the task buffer at any time using
        the `task_write_other` function. The size of this task buffer is determined by the `samples_in_buffer`
        parameter.

        The task does not actually start reading the data from the task buffer and writing it to the other outputs
        until the `task_start` function is called. In order for data to be available in the task buffer as soon as the
        task starts, store data in the buffer using `task_write_other` prior to starting the task. Since the task
        writes to the other outputs at the sampling rate specified when the task is started, it will be reading data
        from the task buffer at that rate. Thus, `task_write_other` must be called to add more data to the task buffer
        before all the data in the buffer is depleted. Otherwise, the task will have no data to write to the other
        outputs and will return with a `QERR_BUFFER_OVERFLOW` error the next time `task_write_other` is called.

        The task must be deleted when it is no longer in use using the `task_delete` function, in order to free the
        system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_write_other` function cannot write more samples than
            this in a single call. If the task buffer underflows because `task_write_other` has not been called in time
            to add data to the task buffer, then the next call to `task_write_other` will return a`HIL_BUFFER_OVERFLOW`
            error.
        channels : array_like
            An array containing the channel numbers of the other outputs to be written to by the task.
        num_channels : int
            The number of channels specified in the `channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Create a task to write to the first four other output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> card.task_create_other_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> card.task_create_other_writer(samples_in_buffer, channels, num_channels)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_other_writer(self._card if self._card is not None else ffi.NULL,
                                                      samples_in_buffer,
                                                      ffi.from_buffer(_UINT32_ARRAY, channels) if channels is not None else ffi.NULL,
                                                      num_channels,
                                                      task)
        if result < 0:
            raise HILError(result)
        return task

    def task_create_writer(self,
                           samples_in_buffer,
                           analog_channels, num_analog_channels,
                           pwm_channels, num_pwm_channels,
                           digital_channels, num_digital_channels,
                           other_channels, num_other_channels):
        """Creates a task for writing to the specified output channels. The task allows other operations to be performed
        while the outputs are being written "in the background". The data written to the outputs is read from an
        internal circular "task buffer". This data may be written into the task buffer at any time using the
        `task_write` function. The size of this task buffer is determined by the `samples_in_buffer parameter`. Before
        starting the task, the directions of the digital I/O lines should be set using the `set_digital_directions`
        function.

        The task does not actually start reading the data from the task buffer and writing it to the outputs until the
        `task_start` function is called. In order for data to be available in the task buffer as soon as the task
        starts, store data in the buffer using `task_write` prior to starting the task. Since the task writes to the
        outputs at the sampling rate specified when the task is started, it will be reading data from the task buffer at
        that rate. Thus, `task_write` must be called to add more data to the task buffer before all the data in the
        buffer is depleted. Otherwise, the task will have no data to write to the outputs and will return with a
        `QERR_BUFFER_OVERFLOW` error the next time `task_write` is called.

        The task must be deleted when it is no longer in use using the `task_delete` function, in order to free the
        system and hardware resources used by the task.

        Parameters
        ----------
        samples_in_buffer : int
            The number of samples in the task buffer. The `task_write` function cannot write more samples than this in a
            single call. If the task buffer overflows because `task_write` has not been called in time to remove the data
            from the task buffer, then the next call to `task_write` will return a `HIL_BUFFER_OVERFLOW` error.
        analog_channels : array_like or None
            An array containing the channel numbers of the analog outputs to be written by the task. If no analog
            channels are required, then this parameter may be ``None``. In this case, `num_analog_channels` must be
            zero.
        num_analog_channels : int
            The number of channels specified in the `analog_channels` array.
        pwm_channels : array_like or None
            An array containing the channel numbers of the PWM outputs to be write by the task. If no encoder channels
            are required, then this parameter may be ``None``. In this case, `num_encoder_channels` must be zero.
        num_pwm_channels : int
            The number of channels specified in the `encoder_channels` array.
        digital_channels : array_like or None
            An array containing the channel numbers of the digital outputs to be write by the task. If no digital
            channels are required, then this parameter may be ``None``. In this case, `num_digital_channels` must be
            zero.
        num_digital_channels : int
            The number of channels specified in the `digital_channels` array.
        other_channels : array_like or None
            An array containing the channel numbers of the other outputs to be write by the task. If no other channels
            are required, then this parameter may be ``None``. In this case, `num_other_channels` must be zero.
        num_other_channels : int
            The number of channels specified in the `other_channels` array.

        Returns
        -------
        handle
            A handle to the created task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `task_write` function failing to write those outputs.

        Examples
        --------
        Create a task to write to the first four analog output channels and the first two PWM output channels.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> card.task_create_writer(samples_in_buffer,
        ...                         analog_channels, num_analog_channels
        ...                         encoder_channels, num_encoder_channels,
        ...                         None, 0,
        ...                         None, 0)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> samples_in_buffer = 1000
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> card.task_create_writer(samples_in_buffer,
        ...                         analog_channels, num_analog_channels
        ...                         encoder_channels, num_encoder_channels,
        ...                         None, 0,
        ...                         None, 0)
        >>> # ...
        ...
        >>> card.close()

        """
        task = ffi.new("t_task *")

        result = hil_lib.hil_task_create_writer(self._card if self._card is not None else ffi.NULL,
                                                samples_in_buffer,
                                                ffi.from_buffer(_UINT32_ARRAY, analog_channels) if analog_channels is not None else ffi.NULL,
                                                num_analog_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, pwm_channels) if pwm_channels is not None else ffi.NULL,
                                                num_pwm_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, digital_channels) if digital_channels is not None else ffi.NULL,
                                                num_digital_channels,
                                                ffi.from_buffer(_UINT32_ARRAY, other_channels) if other_channels is not None else ffi.NULL,
                                                num_other_channels,
                                                task)
        if result < 0:
            raise HILError(result)
        return task

    def task_set_buffer_overflow_mode(self, task, mode):
        """Determines how buffer overflows are handled for a task.
                
        The task buffer overflows when samples are not being read fast enough by `task_read_xxx` to keep up 
        with the data being read by the card at its inputs, or when samples are not being written fast 
        enough by `task_write_xxx` to stay ahead of the data being written by the card to its outputs. 
        Buffering is used to handle cases where the application is momentarily interrupted and the size 
        of the buffer determines how long an interruption is permitted. If increasing the buffer size 
        does not prevent buffer overflow then the application is simply not capable of keeping up with 
        real time.
    
        By default, an error will be returned by the next `task_read_xxx` or `task_write_xxx` call
        when a buffer overflow occurs and the task will need to be stopped. The reason this is the default
        behaviour is that the HIL API is intended for real-time applications where missing samples is
        regarded as a fatal error.

        However, for those applications where samples may be missed then the buffer overflow handling
        can be altered using the `task_set_buffer_overflow_mode` function (if the card supports it).
        There are three possible modes:

        `BufferOverflowMode.ERROR_ON_OVERFLOW`:

        This is the default mode in which buffer overflows cause a QERR_BUFFER_OVERFLOW error to be
        returned by the next hil_tas_read_xxx or hil_task_write_xxx. The task should be stopped at
        that point.

        `BufferOverflowMode.OVERWRITE_ON_OVERFLOW`:

        In this mode, old samples in the buffer are discarded to make room for new samples if the
        buffer overflows. For writer tasks, this means that there may be unexpected discontinuities in
        the output waveforms. For reader tasks, it means that samples may be lost and only the more
        recent samples will be read.

        `BufferOverflowMode.DISCARD_ON_OVERFLOW`:

        In this mode, new samples are discarded if there is no room in the buffer. For writer tasks,
        this means that there may be unexpected discontinuities in the output waveforms. For reader
        tasks, it means that samples may be lost and only the oldest samples will be read.

        `BufferOverflowMode.WAIT_ON_OVERFLOW`:
    
        In this mode, the task waits on buffer overflow for space to become available. This mode is
        not supported by hardware cards but is only for use by simulated cards.

        `BufferOverflowMode.SYNCHRONIZE`:
    
        In this mode, the task provides complete buffer synchronization. This mode is not supported
        by hardware cards but is only for use by simulated cards.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        mode : BufferOverflowMode
            The buffer overflow mode to use as a `BufferOverflowMode` eumeration value.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Sets the buffer overflow mode for a task to overwrite old samples on overflow.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0] * num_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_set_buffer_overflow_mode(task, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_set_buffer_overflow_mode(task, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_task_set_buffer_overflow_mode(task[0] if task is not None else ffi.NULL, mode)
        if result < 0:
            raise HILError(result)

    def task_get_buffer_overflows(self, task):
        """Returns the number of buffer overflows that have occurred since the task was started.
                
        This function is only relevant when the buffer overflow mode has been changed from the default mode
        i.e., when the overflow mode is not BUFFER_MODE_ERROR_ON_OVERFLOW.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.

        Returns
        -------
        int
            The number of buffer overflows that have occurred for the task.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Gets the number of buffer overflows for a task.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0] * num_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_set_buffer_overflow_mode(task, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        >>> num_overflows = card.task_get_buffer_overflows(task)
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_set_buffer_overflow_mode(task, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        >>> num_overflows = card.task_get_buffer_overflows(task)
        ...
        >>> card.close()

        """
        result = hil_lib.hil_task_get_buffer_overflows(task[0] if task is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_start(self, task, clock, frequency, num_samples):
        """Starts a task running. The task runs at the sampling frequency specified and processes the number of samples
        specified. If the number of samples is set to INFINITE, then the task runs until `task_stop` is called.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        clock : int
            The clock used to time the operation. Note that some clocks allow faster sampling rates than others.
        frequency : double
            The frequency in Hertz at which to process samples. For example, if `frequency` is set to 1000, then the
            `task_start` function causes the task to process one sample every millisecond.
        num_samples : int
            The total number of samples to process. Each "sample" consists of all the channels specified when the task
            was created. For example, if `frequency` is set to 1000 and `num_samples` is set to 5000, then the task will
            run for 5 seconds, processing 5000 samples. If the number of samples is set to INFINITE, then the task will
            run until `task_stop` is called.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Start a task to read 5000 samples at 1 kHz from the first four analog input channels using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> buffer = array('d', [0.0] * num_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_task_start(task[0] if task is not None else ffi.NULL, clock, frequency, num_samples)
        if result < 0:
            raise HILError(result)

    def task_flush(self, task):
        """Flushes the task buffer for a writer or read-writer task. This function has no effect on reader tasks.
        Flushing the task buffer ensures that all the data written to the task buffer has been transferred to the actual
        hardware. This function does not return until all the data in the task buffer has been flushed to the hardware
        or the task is stopped.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Writes 5000 samples at 1 kHz to the first four analog output channels using SYSTEM_CLOCK_1. Flushes the buffer
        to ensure that all data is written to the hardware.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 100
        >>> buffer = array('d', [0.0] * samples_to_write * num_channels)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(0, samples, samples_to_write):
        ...     # Fill the buffer
        ...     buffer[:] = array('d', [x for x in range(samples_to_write)])
        ...     # Does not wait for data to be written to the hardware; it only waits for space in the task buffer.
        ...     card.task_write_analog(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_flush(task)  # Ensure all data has been written to the hardware
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 100
        >>> buffer = np.zeros(samples_to_write * num_channels, dtype=np.float64)
        >>> task = card.task_create_analog_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(0, samples, samples_to_write):
        ...     # Fill the buffer
        ...     buffer[:] = np.array([x for x in range(samples_to_write)], dtype=np.float64)
        ...     # Does not wait for data to be written to the hardware; it only waits for space in the task buffer.
        ...     card.task_write_analog(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_flush(task)  # Ensure all data has been written to the hardware
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_flush(task[0] if task is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def task_stop(self, task):
        """Stops a task that is running. A task may be stopped before it has processed all of its samples. Tasks may
        also be restarted using the `task_start` function.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Stop the specified task after processing.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_stop(task[0] if task is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def task_stop_all(self):
        """Stops all running tasks that are associated with the given card. Tasks may be stopped before they have
        processed all of their samples. Tasks may also be restarted using the `task_start` function. This function is
        useful in exception handling where a specific task handle may be lost.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Stop all tasks associated with the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(analog_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = array('d', [0.0] * num_analog_channels)
        >>> encoder_buffer = array('i', [0] * num_encoder_channels)
        >>> analog_task = card.task_create_analog_reader(samples_in_buffer, analog_channels, num_analog_channels)
        >>> encoder_task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> try:
        ...     card.task_start(analog_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     card.task_start(encoder_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     for index in range(samples):
        ...         card.task_read_analog(analog_task, samples_to_read, analog_buffer)
        ...         card.task_read_encoder(encoder_task, samples_to_read, encoder_buffer)
        ...         # ...
        ...
        ... except HILError:
        ...     card.task_stop_all()
        ...     card.task_delete_all()
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.int32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = np.zeros(num_analog_channels, dtype=np.float64)
        >>> encoder_buffer = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> analog_task = card.task_create_analog_reader(samples_in_buffer, analog_channels, num_encoder_channels)
        >>> encoder_task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> try:
        ...     card.task_start(analog_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     card.task_start(encoder_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     for index in range(samples):
        ...         card.task_read_analog(analog_task, samples_to_read, analog_buffer)
        ...         card.task_read_encoder(encoder_task, samples_to_read, encoder_buffer)
        ...         # ...
        ...
        ... except HILError:
        ...     card.task_stop_all()
        ...     card.task_delete_all()
        >>> card.close()

        """
        result = hil_lib.hil_task_stop_all(self._card if self._card is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def task_delete(self, task):
        """Deletes a task, freeing up any system resources and hardware resources used by the task. If the task is
        running, then it is stopped prior to being deleted. Once task has been deleted, the task handle becomes invalid
        and the task may no longer be used.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Delete the specified task after use.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """

        result = hil_lib.hil_task_delete(task[0] if task is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def task_delete_all(self):
        """Deletes all tasks that are associated with the given card. Any tasks that are running, will be stopped prior
        to being deleted. All task handles associated with the card become invalid and may no longer be used.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Deletes all tasks associated with the board.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(analog_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = array('d', [0.0] * num_analog_channels)
        >>> encoder_buffer = array('i', [0] * num_encoder_channels)
        >>> analog_task = card.task_create_analog_reader(samples_in_buffer, analog_channels, num_analog_channels)
        >>> encoder_task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> try:
        ...     card.task_start(analog_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     card.task_start(encoder_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     for index in range(samples):
        ...         card.task_read_analog(analog_task, samples_to_read, analog_buffer)
        ...         card.task_read_encoder(encoder_task, samples_to_read, encoder_buffer)
        ...         # ...
        ...
        ... except HILError:
        ...     card.task_stop_all()
        ...     card.task_delete_all()
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.int32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = np.zeros(num_analog_channels, dtype=np.float64)
        >>> encoder_buffer = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> analog_task = card.task_create_analog_reader(samples_in_buffer, analog_channels, num_encoder_channels)
        >>> encoder_task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> try:
        ...     card.task_start(analog_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     card.task_start(encoder_task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        ...     for index in range(samples):
        ...         card.task_read_analog(analog_task, samples_to_read, analog_buffer)
        ...         card.task_read_encoder(encoder_task, samples_to_read, encoder_buffer)
        ...         # ...
        ...
        ... except HILError:
        ...     card.task_stop_all()
        ...     card.task_delete_all()
        >>> card.close()

        """
        result = hil_lib.hil_task_delete_all(self._card if self._card is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)

    def task_read_analog(self, task, num_samples, buffer):
        """Reads the specified number of samples from the task buffer of a task created using
        `task_create_analog_reader`. If there's not enough samples in the task buffer, then this function will block
        until the requested number of samples becomes available or the task stops. Since the task reads the hardware at
        the sampling rate specified in the call to `task_start`, and stores the data in the task buffer, this function
        will never block for longer than the requested number of samples times the sampling period.

        Because this function blocks until enough data is available and the task buffer is filled at a given sampling
        rate, calling this function synchronizes the caller to that sampling rate (provided the task buffer is not being
        filled faster than we can read the data). Thus, the `task_read_analog` function may be used to implement control
        systems, system identification, synchronous data streaming, and other operations requiring a fixed sampling
        rate. For control systems, the `num_samples` parameter is typically 1, since control calculations need to be
        performed on each sample. For data streaming, the `num_samples` parameter is typically half the number of
        samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to read from the task buffer. Each "sample" consists of all the analog input channels
            specified when the task was created using `task_create_analog_reader`. For example, if `num_samples` is 5
            and the task is configured to read 3 channels, then the output buffer will contain 15 elements.
        buffer : array_like
            An array for receiving the voltage values read from the analog inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if analog input channels 0, 1 and 3 are being read, then the data appears in
            the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples read from the task buffer. This value may be less than the requested number of samples
            (including 0) if the task is stopped or has finished processing the total number of samples indicated in the
            call to `task_start`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Reads 5000 samples at 1 kHz from the first four analog input channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_analog_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_analog(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_read_analog(task[0] if task is not None else ffi.NULL,
                                              num_samples,
                                              ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_read_encoder(self, task, num_samples, buffer):
        """Reads the specified number of samples from the task buffer of a task created using
        `task_create_encoder_reader`. If there's not enough samples in the task buffer, then this function will block
        until the requested number of samples becomes available or the task stops. Since the task reads the hardware at
        the sampling rate specified in the call to `task_start`, and stores the data in the task buffer, this function
        will never block for longer than the requested number of samples times the sampling period.

        Because this function blocks until enough data is available and the task buffer is filled at a given sampling
        rate, calling this function synchronizes the caller to that sampling rate (provided the task buffer is not being
        filled faster than we can read the data). Thus, the `task_read_encoder` function may be used to implement control
        systems, system identification, synchronous data streaming, and other operations requiring a fixed sampling
        rate. For control systems, the `num_samples` parameter is typically 1, since control calculations need to be
        performed on each sample. For data streaming, the `num_samples` parameter is typically half the number of
        samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to read from the task buffer. Each "sample" consists of all the encoder input channels
            specified when the task was created using `task_create_encoder_reader`. For example, if `num_samples` is 5
            and the task is configured to read 3 channels, then the output buffer will contain 15 elements.
        buffer : array_like
            An array for receiving the count values read from the encoder inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if encoder input channels 0, 1 and 3 are being read, then the data appears
            in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples read from the task buffer. This value may be less than the requested number of samples
            (including 0) if the task is stopped or has finished processing the total number of samples indicated in the
            call to `task_start`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Reads 5000 samples at 1 kHz from the first four encoder input channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('i', [0] * num_channels)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.int32)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_read_encoder(task[0] if task is not None else ffi.NULL,
                                               num_samples,
                                               ffi.from_buffer(_INT32_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_read_digital(self, task, num_samples, buffer):
        """Reads the specified number of samples from the task buffer of a task created using
        `task_create_digital_reader`. If there's not enough samples in the task buffer, then this function will block
        until the requested number of samples becomes available or the task stops. Since the task reads the hardware at
        the sampling rate specified in the call to `task_start`, and stores the data in the task buffer, this function
        will never block for longer than the requested number of samples times the sampling period.

        Because this function blocks until enough data is available and the task buffer is filled at a given sampling
        rate, calling this function synchronizes the caller to that sampling rate (provided the task buffer is not being
        filled faster than we can read the data). Thus, the `task_read_digital` function may be used to implement
        control systems, system identification, synchronous data streaming, and other operations requiring a fixed
        sampling rate. For control systems, the `num_samples` parameter is typically 1, since control calculations need
        to be performed on each sample. For data streaming, the `num_samples` parameter is typically half the number of
        samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to read from the task buffer. Each "sample" consists of all the digital input channels
            specified when the task was created using `task_create_digital_reader`. For example, if `num_samples` is 5
            and the task is configured to read 3 channels, then the output buffer will contain 15 elements.
        buffer : array_like
            An array for receiving the values read from the digital inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if digital input channels 0, 1 and 3 are being read, then the data appears
            in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples read from the task buffer. This value may be less than the requested number of samples
            (including 0) if the task is stopped or has finished processing the total number of samples indicated in the
            call to `task_start`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital inputs or outputs must be configured accordingly using this function. Failure to configure the
        digital I/O may result in the `task_read_digital` function failing to read or write the digital I/O as expected.

        Examples
        --------
        Reads 5000 samples at 1 kHz from the first four digital input channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('b', [0] * num_channels)
        >>> task = card.task_create_digital_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_digital(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.int8)
        >>> task = card.task_create_digital_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_digital(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_read_digital(task[0] if task is not None else ffi.NULL,
                                               num_samples,
                                               ffi.from_buffer(_BOOLEAN_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_read_other(self, task, num_samples, buffer):
        """Reads the specified number of samples from the task buffer of a task created using
        `task_create_other_reader`. If there's not enough samples in the task buffer, then this function will block
        until the requested number of samples becomes available or the task stops. Since the task reads the hardware at
        the sampling rate specified in the call to `task_start`, and stores the data in the task buffer, this function
        will never block for longer than the requested number of samples times the sampling period.

        Because this function blocks until enough data is available and the task buffer is filled at a given sampling
        rate, calling this function synchronizes the caller to that sampling rate (provided the task buffer is not being
        filled faster than we can read the data). Thus, the `task_read_other` function may be used to implement control
        systems, system identification, synchronous data streaming, and other operations requiring a fixed sampling
        rate. For control systems, the `num_samples` parameter is typically 1, since control calculations need to be
        performed on each sample. For data streaming, the `num_samples` parameter is typically half the number of
        samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to read from the task buffer. Each "sample" consists of all the other input channels
            specified when the task was created using `task_create_other_reader`. For example, if `num_samples` is 5
            and the task is configured to read 3 channels, then the output buffer will contain 15 elements.
        buffer : array_like
            An array for receiving the values read from the other inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if other input channels 0, 1 and 3 are being read, then the data appears in
            the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples read from the task buffer. This value may be less than the requested number of samples
            (including 0) if the task is stopped or has finished processing the total number of samples indicated in the
            call to `task_start`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Reads 5000 samples at 1 kHz from the first two other input channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_other_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_other(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_other_reader(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_other(task, samples_to_read, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_read_other(task[0] if task is not None else ffi.NULL,
                                             num_samples,
                                             ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_read(self, task, num_samples, analog_buffer, encoder_buffer, digital_buffer, other_buffer):
        """Reads the specified number of samples from the task buffer of a task created using
        `task_create_reader`. If there's not enough samples in the task buffer, then this function will block
        until the requested number of samples becomes available or the task stops. Since the task reads the hardware at
        the sampling rate specified in the call to `task_start`, and stores the data in the task buffer, this function
        will never block for longer than the requested number of samples times the sampling period.

        Because this function blocks until enough data is available and the task buffer is filled at a given sampling
        rate, calling this function synchronizes the caller to that sampling rate (provided the task buffer is not being
        filled faster than we can read the data). Thus, the `task_read` function may be used to implement control
        systems, system identification, synchronous data streaming, and other operations requiring a fixed sampling
        rate. For control systems, the `num_samples` parameter is typically 1, since control calculations need to be
        performed on each sample. For data streaming, the `num_samples` parameter is typically half the number of
        samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to read from the task buffer. Each "sample" consists of all the input channels
            specified when the task was created using `task_create_reader`. For example, if `num_samples` is 5
            and the task is configured to read 3 analog channels and 2 encoder channels, then the analog output buffer
            will contain 15 elements and the encoder output buffer will contain 10 elements.
        analog_buffer : array_like
            An array for receiving the voltage values read from the analog inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if analog input channels 0, 1 and 3 are being read, then the data appears
            in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].
        encoder_buffer : array_like
            An array for receiving the count values read from the encoder inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if encoder input channels 0, 1 and 3 are being read, then the data appears
            in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].
        digital_buffer : array_like
            An array for receiving the values read from the digital inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if digital input channels 0, 1 and 3 are being read, then the data appears
            in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].
        other_buffer : array_like
            An array for receiving the values read from the other inputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array is organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if other input channels 0, 1 and 3 are being read, then the data appears in
            the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples read from the task buffer. This value may be less than the requested number of samples
            (including 0) if the task is stopped or has finished processing the total number of samples indicated in the
            call to `task_start`.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital inputs or outputs must be configured accordingly using this function. Failure to configure the
        digital I/O may result in the `task_read_digital` function failing to read or write the digital I/O as expected.

        Examples
        --------
        Reads 5000 samples at 1 kHz from the first four analog input channels and the first two encoder input channels,
        using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = array('d', [0.0] * num_analog_channels)
        >>> encoder_buffer = array('i', [0] * num_encoder_channels)
        >>> task = card.task_create_reader(samples_in_buffer,
        ...                                analog_channels, num_analog_channels,
        ...                                encoder_channels, num_encoder_channels,
        ...                                None, 0,
        ...                                None, 0)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read(task, samples_to_read, analog_buffer, encoder_buffer, None, None)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> analog_buffer = np.zeros(num_analog_channels, dtype=np.float64)
        >>> encoder_buffer = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> task = card.task_create_reader(samples_in_buffer,
        ...                                analog_channels, num_analog_channels,
        ...                                encoder_channels, num_encoder_channels,
        ...                                None, 0,
        ...                                None, 0)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read(task, samples_to_read, analog_buffer, encoder_buffer, None, None)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_read(task[0] if task is not None else ffi.NULL,
                                       num_samples,
                                       ffi.from_buffer(_DOUBLE_ARRAY, analog_buffer) if analog_buffer is not None else ffi.NULL,
                                       ffi.from_buffer(_INT32_ARRAY, encoder_buffer) if encoder_buffer is not None else ffi.NULL,
                                       ffi.from_buffer(_BOOLEAN_ARRAY, digital_buffer) if digital_buffer is not None else ffi.NULL,
                                       ffi.from_buffer(_DOUBLE_ARRAY, other_buffer) if other_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_write_analog(self, task, num_samples, buffer):
        """Writes the specified number of samples to the task buffer of a task created using
        `task_create_analog_writer.` If there's not enough space in the task buffer, then this function will block until
        there is space in the task buffer or the task stops. Since the task removes data from the task buffer and writes
        it to the hardware at the sampling rate specified in the call to `task_start`, this function will never block
        for longer than the given number of samples times the sampling period.

        Note that this function only blocks until there is enough space available in the task buffer. Because the task
        buffer is depleted at a given sampling rate, calling this function only synchronizes the caller to that sampling
        rate if the task buffer is kept full. Data must be written to the task buffer before the task buffer is
        completely depleted or else the next attempt to write to the task buffer will return with a
        `QERR_BUFFER_OVERFLOW` error. As a result, `task_write_analog` should be used to put data into the task buffer
        prior to starting the task.

        Writer tasks are typically used to stream data to HIL hardware. In this case, the `num_samples` parameter is
        typically half the number of samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to write to the task buffer. Each "sample" consists of all the analog output channels
            specified when the task was created using `task_create_analog_writer`. For example, if `num_samples` is 5
            and the task is configured to write 3 channels, then the input buffer must contain at least 15 elements.
        buffer : array_like
            An array containing the voltage values to write to the analog outputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array must be organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if analog output channels 0, 1 and 3 are being written, then the data must
            appear in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples written to the task buffer. This value may be less than the requested number of
            samples (including 0) if the task buffer does not have sufficient space and the task is stopped or has
            finished processing the total number of samples indicated in the call to `task_start`.

            Note that successive calls to `task_write_analog` can write more samples in total then the total number of
            samples specified in `task_start`. However, only the number of samples specified in `task_start` will
            actually be processed and written to the hardware.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Writes 5000 samples at 1 kHz to the first four analog output channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_analog_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_analog(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_analog_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_analog(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_write_analog(task[0] if task is not None else ffi.NULL,
                                               num_samples,
                                               ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_write_pwm(self, task, num_samples, buffer):
        """Writes the specified number of samples to the task buffer of a task created using `task_create_pwm_writer.`
        If there's not enough space in the task buffer, then this function will block until there is space in the task
        buffer or the task stops. Since the task removes data from the task buffer and writes it to the hardware at the
        sampling rate specified in the call to `task_start`, this function will never block for longer than the given
        number of samples times the sampling period.

        Note that this function only blocks until there is enough space available in the task buffer. Because the task
        buffer is depleted at a given sampling rate, calling this function only synchronizes the caller to that sampling
        rate if the task buffer is kept full. Data must be written to the task buffer before the task buffer is
        completely depleted or else the next attempt to write to the task buffer will return with a
        `QERR_BUFFER_OVERFLOW` error. As a result, `task_write_pwm` should be used to put data into the task buffer
        prior to starting the task.

        Writer tasks are typically used to stream data to HIL hardware. In this case, the `num_samples` parameter is
        typically half the number of samples in the task buffer to implement double-buffering.

        The interpretation of the PWM samples to be written depends upon the PWM mode. Typically, the data is
        interpreted as a duty cycle, in which a magnitude of 0.0 denotes a 0% duty cycle and magnitude of 1.0 indicates
        a 100% duty cycle. The sign determines the polarity of the output for those boards supporting bidirectional
        PWM outputs. However, other PWM modes are possible with some boards. Refer to the `set_pwm_mode` function for
        details.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to write to the task buffer. Each "sample" consists of all the analog output channels
            specified when the task was created using `task_create_pwm_writer`. For example, if `num_samples` is 5
            and the task is configured to write 3 channels, then the input buffer must contain at least 15 elements.
        buffer : array_like
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `et_pwm_mode` function. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array must be organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if PWM output channels 0, 1 and 3 are being written, then the data must
            appear in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples written to the task buffer. This value may be less than the requested number of
            samples (including 0) if the task buffer does not have sufficient space and the task is stopped or has
            finished processing the total number of samples indicated in the call to `task_start`.

            Note that successive calls to `task_write_pwm` can write more samples in total then the total number of
            samples specified in `task_start`. However, only the number of samples specified in `task_start` will
            actually be processed and written to the hardware.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Writes 5000 samples at 1 kHz to the first two PWM output channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_pwm_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_pwm(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_pwm_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_pwm(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_write_pwm(task[0] if task is not None else ffi.NULL,
                                            num_samples,
                                            ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_write_digital(self, task, num_samples, buffer):
        """Writes the specified number of samples to the task buffer of a task created using
        `task_create_digital_writer.` If there's not enough space in the task buffer, then this function will block until
        there is space in the task buffer or the task stops. Since the task removes data from the task buffer and writes
        it to the hardware at the sampling rate specified in the call to `task_start`, this function will never block
        for longer than the given number of samples times the sampling period.

        Note that this function only blocks until there is enough space available in the task buffer. Because the task
        buffer is depleted at a given sampling rate, calling this function only synchronizes the caller to that sampling
        rate if the task buffer is kept full. Data must be written to the task buffer before the task buffer is
        completely depleted or else the next attempt to write to the task buffer will return with a
        `QERR_BUFFER_OVERFLOW` error. As a result, `task_write_digital` should be used to put data into the task buffer
        prior to starting the task.

        Writer tasks are typically used to stream data to HIL hardware. In this case, the `num_samples` parameter is
        typically half the number of samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to write to the task buffer. Each "sample" consists of all the digital output channels
            specified when the task was created using `task_create_digital_writer`. For example, if `num_samples` is 5
            and the task is configured to write 3 channels, then the input buffer must contain at least 15 elements.
        buffer : array_like
            An array containing the values to write to the digital outputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array must be organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if digital output channels 0, 1 and 3 are being written, then the data must
            appear in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples written to the task buffer. This value may be less than the requested number of
            samples (including 0) if the task buffer does not have sufficient space and the task is stopped or has
            finished processing the total number of samples indicated in the call to `task_start`.

            Note that successive calls to `task_write_digital` can write more samples in total then the total number of
            samples specified in `task_start`. However, only the number of samples specified in `task_start` will
            actually be processed and written to the hardware.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.
            
        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the set_digital_directions function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `watchdog_set_digital_expiration_state` function failing to write those outputs when the watchdog
        expires.

        Examples
        --------
        Writes 5000 samples at 1 kHz to the first four digital output channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = array('b', [0] * num_channels)
        >>> task = card.task_create_digital_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_digital(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = np.zeros(num_channels, dtype=np.int8)
        >>> task = card.task_create_digital_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_digital(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_write_digital(task[0] if task is not None else ffi.NULL,
                                                num_samples,
                                                ffi.from_buffer(_BOOLEAN_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_write_other(self, task, num_samples, buffer):
        """Writes the specified number of samples to the task buffer of a task created using
        `task_create_other_writer.` If there's not enough space in the task buffer, then this function will block until
        there is space in the task buffer or the task stops. Since the task removes data from the task buffer and writes
        it to the hardware at the sampling rate specified in the call to `task_start`, this function will never block
        for longer than the given number of samples times the sampling period.

        Note that this function only blocks until there is enough space available in the task buffer. Because the task
        buffer is depleted at a given sampling rate, calling this function only synchronizes the caller to that sampling
        rate if the task buffer is kept full. Data must be written to the task buffer before the task buffer is
        completely depleted or else the next attempt to write to the task buffer will return with a
        `QERR_BUFFER_OVERFLOW` error. As a result, `task_write_other` should be used to put data into the task buffer
        prior to starting the task.

        Writer tasks are typically used to stream data to HIL hardware. In this case, the `num_samples` parameter is
        typically half the number of samples in the task buffer to implement double-buffering.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to write to the task buffer. Each "sample" consists of all the other output channels
            specified when the task was created using `task_create_other_writer`. For example, if `num_samples` is 5
            and the task is configured to write 3 channels, then the input buffer must contain at least 15 elements.
        buffer : array_like
            An array containing the values to write to the other outputs. The array must contain
            `num_channels` * `num_samples` elements, where `num_channels` is the number of channels specified when the
            task was created. The array must be organized as a linear array of samples, with each sample consisting of a
            group of channels. For example, if other output channels 0, 1 and 3 are being written, then the data must
            appear in the array as follows, where the numbers correspond to channel numbers: [0, 1, 3, 0, 1, 3, ...].

        Returns
        -------
        int
            The number of samples written to the task buffer. This value may be less than the requested number of
            samples (including 0) if the task buffer does not have sufficient space and the task is stopped or has
            finished processing the total number of samples indicated in the call to `task_start`.

            Note that successive calls to `task_write_other` can write more samples in total then the total number of
            samples specified in `task_start`. However, only the number of samples specified in `task_start` will
            actually be processed and written to the hardware.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Writes 5000 samples at 1 kHz to the first four other output channels, using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2, 3])
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = array('d', [0.0] * num_channels)
        >>> task = card.task_create_other_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_other(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> buffer = np.zeros(num_channels, dtype=np.float64)
        >>> task = card.task_create_other_writer(samples_in_buffer, channels, num_channels)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write_other(task, samples_to_write, buffer)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_write_other(task[0] if task is not None else ffi.NULL,
                                              num_samples,
                                              ffi.from_buffer(_DOUBLE_ARRAY, buffer) if buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    def task_write(self, task, num_samples, analog_buffer, pwm_buffer, digital_buffer, other_buffer):
        """writes the specified number of samples to the task buffer of a task created using `task_create_writer`. If
        there's not enough space in the task buffer, then this function will block until there is space in the task
        buffer or the task stops. Since the task removes data from the task buffer and writes it to the hardware at the
        sampling rate specified in the call to hil_task_start, this function will never block for longer than the given
        number of samples times the sampling period.

        Note that this function only blocks until there is enough space available in the task buffer. Because the task
        buffer is depleted at a given sampling rate, calling this function only synchronizes the caller to that sampling
        rate if the task buffer is kept full. Data must be written to the task buffer before the task buffer is
        completely depleted or else the next attempt to write to the task buffer will return with a
        `QERR_BUFFER_OVERFLOW` error. As a result, `task_write` should be used to put data into the task buffer prior to
        starting the task.

        Writer tasks are typically used to stream data to HIL hardware. In this case, the `num_samples` parameter is
        typically half the number of samples in the task buffer to implement double-buffering.

        The interpretation of the PWM data to be written depends upon the PWM mode. Typically, the data is interpreted
        as a duty cycle, in which a magnitude of 0.0 denotes a 0% duty cycle and magnitude of 1.0 indicates a 100% duty
        cycle. The sign determines the polarity of the output for those boards supporting bidirectional PWM outputs.
        However, other PWM modes are possible with some boards. Refer to the `set_pwm_mode` function for details.

        Parameters
        ----------
        task : handle
            A handle to the task, as returned by one of the task creation functions.
        num_samples : int
            The number of samples to write to the task buffer. Each "sample" consists of all the output channels
            specified when the task was created using `task_create_writer`. For example, if `num_samples` is 5
            and the task is configured to write 3 analog channels and 2 PWM channels, then the analog input buffer will
            contain at least 15 elements and the PWM input buffer must contain at least 10 elements.
        analog_buffer : array_like or None
            An array containing the voltage values to write to the analog outputs. The array must contain
            `num_analog_channels` * `num_samples elements`, where `num_analog_channels` is the number of channels
            specified when the task was created. The array must be organized as a linear array of samples, with each
            sample consisting of a group of channels. For example, if analog output channels 0, 1 and 3 are being
            written, then the data must appear in the array as follows, where the numbers correspond to channel numbers:
            [0, 1, 3, 0, 1, 3, ...]. If no analog channels were specified in the call to `task_create_writer`, then this
            parameter may be ``None``.
        pwm_buffer : array_like or None
            An array containing the values to write to the PWM outputs. How these values are interpreted depends on the
            PWM mode. The PWM mode is configured using the `set_pwm_mode` function. The array must contain
            `num_pwm_channels` * `num_samples` elements, where `num_pwm_channels` is the number of channels specified
            when the task was created. The array must be organized as a linear array of samples, with each sample
            consisting of a group of channels. For example, if PWM output channels 0, 1 and 3 are being written, then
            the data must appear in the array as follows, where the numbers correspond to channel numbers:
            [0, 1, 3, 0, 1, 3, ...]. If no PWM channels were specified in the call to `task_create_writer`, then this
            parameter may be ``None``.
        digital_buffer : array_like or None
            An array containing the values to write to the digital outputs. The array must contain
            `num_digital_channels` * `num_samples elements`, where `num_digital_channels` is the number of channels
            specified when the task was created. The array must be organized as a linear array of samples, with each
            sample consisting of a group of channels. For example, if digital output channels 0, 1 and 3 are being
            written, then the data must appear in the array as follows, where the numbers correspond to channel numbers:
            [0, 1, 3, 0, 1, 3, ...].  If no digital channels were specified in the call to `task_create_writer`, then
            this parameter may be ``None``.
        other_buffer : array_like or None
            An array containing the values to write to the other outputs. The array must contain
            `num_other_channels` * `num_samples elements`, where `num_other_channels` is the number of channels
            specified when the task was created. The array must be organized as a linear array of samples, with each
            sample consisting of a group of channels. For example, if other output channels 0, 1 and 3 are being
            written, then the data must appear in the array as follows, where the numbers correspond to channel numbers:
            [0, 1, 3, 0, 1, 3, ...].  If no other channels were specified in the call to `task_create_writer`, then
            this parameter may be ``None``.

        Returns
        -------
        int
            The number of samples written to the task buffer. This value may be less than the requested number of
            samples (including 0) if the task is stopped or has finished processing the total number of samples
            indicated in the call to `task_start`.

            Note that successive calls to `task_write` can write more samples in total then the total number of samples
            specified in `task_start`. However, only the number of samples specified in `task_start` will actually be
            processed and written to the hardware.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the `set_digital_directions` function. All the channels which will be used
        as digital inputs or outputs must be configured accordingly using this function. Failure to configure the
        digital I/O may result in the `task_read_digital` function failing to read or write the digital I/O as expected.

        Examples
        --------
        Writes 5000 samples at 1 kHz from the first four analog input channels and the first two encoder input channels,
        using ``SYSTEM_CLOCK_1``.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = array('I', [0, 1, 2, 3])
        >>> encoder_channels = array('I', [0, 1])
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> analog_buffer = array('d', [0.0] * num_analog_channels)
        >>> encoder_buffer = array('i', [0] * num_encoder_channels)
        >>> task = card.task_create_writer(samples_in_buffer,
        ...                                analog_channels, num_analog_channels,
        ...                                encoder_channels, num_encoder_channels,
        ...                                None, 0,
        ...                                None, 0)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write(task, samples_to_write, analog_buffer, encoder_buffer, None, None)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock
        >>> card = HIL("q8_usb", "0")
        >>> analog_channels = np.array([0, 1, 2, 3], dtype=np.uint32)
        >>> encoder_channels = np.array([0, 1], dtype=np.uint32)
        >>> num_analog_channels = len(analog_channels)
        >>> num_encoder_channels = len(encoder_channels)
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_write = 1
        >>> analog_buffer = np.zeros(num_analog_channels, dtype=np.float64)
        >>> encoder_buffer = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> task = card.task_create_writer(samples_in_buffer,
        ...                                analog_channels, num_analog_channels,
        ...                                encoder_channels, num_encoder_channels,
        ...                                None, 0,
        ...                                None, 0)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_write(task, samples_to_write, analog_buffer, encoder_buffer, None, None)
        ...     # ...
        ...
        >>> card.task_stop(task)
        >>> card.task_delete(task)
        >>> card.close()

        """
        result = hil_lib.hil_task_write(task[0] if task is not None else ffi.NULL,
                                        num_samples,
                                        ffi.from_buffer(_DOUBLE_ARRAY, analog_buffer) if analog_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_DOUBLE_ARRAY, pwm_buffer) if pwm_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_BOOLEAN_ARRAY, digital_buffer) if digital_buffer is not None else ffi.NULL,
                                        ffi.from_buffer(_DOUBLE_ARRAY, other_buffer) if other_buffer is not None else ffi.NULL)
        if result < 0:
            raise HILError(result)
        return result

    # endregion

    # region Watchdog

    def watchdog_set_analog_expiration_state(self, channels, num_channels, voltages):
        """Sets the state that the analog outputs will be set to if the watchdog expires. Most cards do not allow this
        state to be configured. The expiration states must be set prior to starting the watchdog timer using
        `watchdog_start`. The Quanser Q8-series cards may be configured to reset the analog outputs to 0V. In this case,
        the digital outputs must also be configured to go tristate. If no expiration states are configured for the
        Q8-series, then the analog and digital outputs will not be reconfigured when the watchdog expires.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the analog output channels for which the expiration state should be set.
            Channel numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the channels array.
        voltages : array_like
            An array containing the analog voltages to which to set the corresponding channel in the channels array upon
            watchdog expiration. This array must be the same size as the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure the first three analog outputs to go to 0V upon watchdog expiration.

        Using array:

        >>> from array as array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2])
        >>> num_channels = len(channels)
        >>> voltages = array('d', [0.0, 0.0, 0.0])
        >>> card.watchdog_set_analog_expiration_state(channels, num_channels, voltages)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> voltages = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        >>> card.watchdog_set_analog_expiration_state(channels, num_channels, voltages)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_set_analog_expiration_state(self._card if self._card is not None else ffi.NULL,
                                                                  ffi.from_buffer(_UINT_ARRAY, channels) if channels is not None else ffi.NULL,
                                                                  num_channels,
                                                                  ffi.from_buffer(_DOUBLE_ARRAY, voltages) if voltages is not None else ffi.NULL)
        
        if result < 0:
            raise HILError(result)

    def watchdog_set_pwm_expiration_state(self, channels, num_channels, duty_cycles):
        """Sets the state that the PWM outputs will be set to if the watchdog expires. Most cards do not allow this
        state to be configured. The expiration states must be set prior to starting the watchdog timer using
        `watchdog_start`. Currently, there are no cards which allow this state to be configured.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the PWM output channels for which the expiration state should be set.
            Channel numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the channels array.
        duty_cycles : array_like
            An array of doubles in which each element contains the PWM duty cycle, frequency or period to which to set
            the corresponding channel in the channels array upon watchdog expiration. The interpretation of this
            parameter depends upon the PWM mode set using the `set_pwm_mode` function. This array must be the same size
            as the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure the first two PWM outputs to go to 0V upon watchdog expiration.

        Using array:

        >>> from array as array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> duty_cycles = array('d', [0.0, 0.0])
        >>> card.watchdog_set_pwm_expiration_state(channels, num_channels, duty_cycles)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> duty_cycles = np.array([0.0, 0.0], dtype=np.float64)
        >>> card.watchdog_set_pwm_expiration_state(channels, num_channels, duty_cycles)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_set_pwm_expiration_state(self._card if self._card is not None else ffi.NULL,
                                                               ffi.from_buffer(_UINT_ARRAY, channels) if channels is not None else ffi.NULL,
                                                               num_channels,
                                                               ffi.from_buffer(_DOUBLE_ARRAY, duty_cycles) if duty_cycles is not None else ffi.NULL)
        
        if result < 0:
            raise HILError(result)

    def watchdog_set_digital_expiration_state(self, channels, num_channels, states):
        """Sets the state that the digital outputs will be set to if the watchdog expires. Most cards do not allow this
        state to be configured. The expiration states must be set prior to starting the watchdog timer using
        `watchdog_start`. Valid output states are:
        ``DigitalState.LOW`` = Set the digital output low (ground).
        ``DigitalState.HIGH`` = Set the digital output high (Vcc).
        ``DigitalState.TRISTATE`` = Set the digital output tristate.
        ``DigitalState.NO_CHANGE`` = Do not change the expiration state of this digital output.

        The Q8-series cards may be configured to reset the digital outputs to tri-state. In this case, the analog
        outputs must also be configured to go to 0V. If no expiration states are configured for the Q8-series, then the
        analog and digital outputs will not be reconfigured when the watchdog expires.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the digital output channels for which the expiration state should be set.
            Channel numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the channels array.
        states : array_like
            An array of ``DigitalState`` constants in which each element contains the digital state to which to set the
            corresponding channel in the `channels` array upon watchdog expiration. This array must be the same size as
            the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Warnings
        --------
        Many cards allow the digital I/O lines to be programmed as inputs or outputs. The digital I/O lines are
        configured as inputs or outputs using the set_digital_directions function. All the channels which will be used
        as digital outputs must be configured as outputs using this function. Failure to configure the digital I/O may
        result in the `watchdog_set_digital_expiration_state` function failing to write those outputs when the watchdog
        expires.

        Examples
        --------
        Configure the first three digital outputs to go tristate upon watchdog expiration.

        Using array:

        >>> from array as array
        >>> from quanser.hardware import HIL, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1, 2])
        >>> num_channels = len(channels)
        >>> states = array('i', [DigitalState.TRISTATE, DigitalState.TRISTATE, DigitalState.TRISTATE])
        >>> card.watchdog_set_digital_expiration_state(channels, num_channels, states)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1, 2], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> states = np.array([DigitalState.TRISTATE, DigitalState.TRISTATE, DigitalState.TRISTATE], dtype=np.int32)
        >>> card.watchdog_set_digital_expiration_state(channels, num_channels, states)
        >>> # ...
        ...
        >>> card.close()

        """

        result = hil_lib.hil_watchdog_set_digital_expiration_state(self._card if self._card is not None else ffi.NULL,
                                                                   ffi.from_buffer(_UINT_ARRAY, channels) if channels is not None else ffi.NULL,
                                                                   num_channels,
                                                                   ffi.from_buffer(_DIGITAL_STATE_ARRAY, states) if states is not None else ffi.NULL)
        
        if result < 0:
            raise HILError(result)

    def watchdog_set_other_expiration_state(self, channels, num_channels, states):
        """Sets the state that the other outputs will be set to if the watchdog expires. The expiration states must be
        set prior to starting the watchdog timer using watchdog_start. Currently there are no cards which allow this
        state to be configured.

        Parameters
        ----------
        channels : array_like
            An array containing the numbers of the other output channels for which the expiration state should be set.
            Channel numbers are zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
        num_channels : int
            The number of channels specified in the channels array.
        states : array_like
            An array of doubles in which each element contains the other value to which to set the corresponding channel
            in the `channels` array upon watchdog expiration. This array must be the same size as the `channels` array.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure the first two other outputs to go to 0 upon watchdog expiration.

        Using array:

        >>> from array as array
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = array('I', [0, 1])
        >>> num_channels = len(channels)
        >>> values = array('d', [0.0] * num_channels)
        >>> card.watchdog_set_other_expiration_state(channels, num_channels, values)
        >>> # ...
        ...
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> channels = np.array([0, 1], dtype=np.uint32)
        >>> num_channels = len(channels)
        >>> values = np.zeros(num_channels, dtype=np.float64)
        >>> card.watchdog_set_other_expiration_state(channels, num_channels, values)
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_set_other_expiration_state(self._card if self._card is not None else ffi.NULL,
                                                                 ffi.from_buffer(_UINT_ARRAY, channels) if channels is not None else ffi.NULL,
                                                                 num_channels,
                                                                 ffi.from_buffer(_DOUBLE_ARRAY, states) if states is not None else ffi.NULL)
        
        if result < 0:
            raise HILError(result)

    def watchdog_start(self, timeout):
        """Starts the watchdog timer with the given timeout interval. It should only be called after the expiration
        states have been configured using the watchdog_set_xxxx_expiration_state functions. Once the watchdog timer has
        been started, it must be reloaded each time before it expires using the watchdog_reload function.

        Parameters
        ----------
        timeout : double
            The expiration timeout interval in seconds.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure a watchdog timer that will expire every 0.1 seconds and reset the analog outputs to 0V and the digital
        outputs to tristate upon expiration. Also create a task for performing real-time control that reads four encoder
        channels every millisecond. The watchdog is reloaded every sampling instant.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> timeout = 100 / frequency
        >>> num_analog_channels = 4
        >>> num_encoder_channels = 4
        >>> num_digital_channels = 16
        >>> analog_channels = array('I', [x for x in range(num_analog_channels)])
        >>> encoder_channels = array('I', [x for x in range(num_encoder_channels)])
        >>> digital_channels = array('I', [x for x in range(num_digital_channels)])
        >>> voltages = array('d', [0.0] * num_analog_channels])
        >>> states = array('i', [DigitalState.TRISTATE] * num_digital_channels)
        >>> counts = array('i', [0] * num_encoder_channels)
        >>> card.watchdog_set_analog_expiration_state(analog_channels, num_analog_channels, voltages)
        >>> card.watchdog_set_digital_expiration_state(digital_channels, num_digital_channels, states)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> card.watchdog_start(timeout)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, counts)  # Returns every millisecond with next sample
        ...     card.watchdog_reload()  # Reload watchdog before using counts for control
        ...     # Do control calculations and output motor torques
        ...
        >>> card.task_stop()
        >>> card.task_delete()
        >>> card.watchdog_stop()
        >>> card.close()
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> timeout = 100 / frequency
        >>> num_analog_channels = 4
        >>> num_encoder_channels = 4
        >>> num_digital_channels = 16
        >>> analog_channels = np.array([x for x in range(num_analog_channels)], dtype=np.uint32)
        >>> encoder_channels = np.array([x for x in range(num_encoder_channels)], dtype=np.uint32)
        >>> digital_channels = np.array([x for x in range(num_digital_channels)], dtype=np.uint32)
        >>> voltages = np.array([0.0] * num_analog_channels], dtype=np.float64)
        >>> states = np.array([DigitalState.TRISTATE] * num_digital_channels, dtype=np.int32)
        >>> counts = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> card.watchdog_set_analog_expiration_state(analog_channels, num_analog_channels, voltages)
        >>> card.watchdog_set_digital_expiration_state(digital_channels, num_digital_channels, states)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> card.watchdog_start(timeout)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, counts)  # Returns every millisecond with next sample
        ...     card.watchdog_reload()  # Reload watchdog before using counts for control
        ...     # Do control calculations and output motor torques
        ...
        >>> card.task_stop()
        >>> card.task_delete()
        >>> card.watchdog_stop()
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_start(self._card if self._card is not None else ffi.NULL, timeout)

        if result < 0:
            raise HILError(result)

    def watchdog_stop(self):
        """Stops the watchdog timer. The watchdog timer will no longer expire so the `watchdog_reload` function need no
        longer be called. Stopping the watchdog timer does not clear the watchdog state if the watchdog has already
        expired. Use the `watchdog_clear` function for this purpose.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------

        >>> import time
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> timeout = 0.2
        >>> card.watchdog_start(timeout)
        >>> for i in range(10):
        ...     time.sleep(0.1)
        ...     # ...
        ...
        >>> card.watchdog_stop()
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_stop(self._card if self._card is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

    def watchdog_reload(self):
        """Reloads the watchdog timer. It is typically called to reload the watchdog timer before it expires at the top
        of the control loop.

        Returns
        ----------
        int 
            Returns ``True`` if the watchdog timer was reloaded prior to expiration. Returns ``False`` if the watchdog
            timer had expired before being reloaded.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Configure a watchdog timer that will expire every 0.1 seconds and reset the analog outputs to 0V and the digital
        outputs to tristate upon expiration. Also create a task for performing real-time control that reads four encoder
        channels every millisecond. The watchdog is reloaded every sampling instant.

        Using array:

        >>> from array import array
        >>> from quanser.hardware import HIL, Clock, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> timeout = 100 / frequency
        >>> num_analog_channels = 4
        >>> num_encoder_channels = 4
        >>> num_digital_channels = 16
        >>> analog_channels = array('I', [x for x in range(num_analog_channels)])
        >>> encoder_channels = array('I', [x for x in range(num_encoder_channels)])
        >>> digital_channels = array('I', [x for x in range(num_digital_channels)])
        >>> voltages = array('d', [0.0] * num_analog_channels])
        >>> states = array('i', [DigitalState.TRISTATE] * num_digital_channels)
        >>> counts = array('i', [0] * num_encoder_channels)
        >>> card.watchdog_set_analog_expiration_state(analog_channels, num_analog_channels, voltages)
        >>> card.watchdog_set_digital_expiration_state(digital_channels, num_digital_channels, states)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> card.watchdog_start(timeout)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, counts)  # Returns every millisecond with next sample
        ...     card.watchdog_reload()  # Reload watchdog before using counts for control
        ...     # Do control calculations and output motor torques
        ...
        >>> card.task_stop()
        >>> card.task_delete()
        >>> card.watchdog_stop()
        >>> card.close()

        Using numpy:

        >>> import numpy as np
        >>> from quanser.hardware import HIL, Clock, DigitalState
        >>> card = HIL("q8_usb", "0")
        >>> frequency = 1000.0
        >>> samples = 5000
        >>> samples_in_buffer = int(frequency)
        >>> samples_to_read = 1
        >>> timeout = 100 / frequency
        >>> num_analog_channels = 4
        >>> num_encoder_channels = 4
        >>> num_digital_channels = 16
        >>> analog_channels = np.array([x for x in range(num_analog_channels)], dtype=np.uint32)
        >>> encoder_channels = np.array([x for x in range(num_encoder_channels)], dtype=np.uint32)
        >>> digital_channels = np.array([x for x in range(num_digital_channels)], dtype=np.uint32)
        >>> voltages = np.array([0.0] * num_analog_channels], dtype=np.float64)
        >>> states = np.array([DigitalState.TRISTATE] * num_digital_channels, dtype=np.int32)
        >>> counts = np.zeros(num_encoder_channels, dtype=np.int32)
        >>> card.watchdog_set_analog_expiration_state(analog_channels, num_analog_channels, voltages)
        >>> card.watchdog_set_digital_expiration_state(digital_channels, num_digital_channels, states)
        >>> task = card.task_create_encoder_reader(samples_in_buffer, encoder_channels, num_encoder_channels)
        >>> card.watchdog_start(timeout)
        >>> card.task_start(task, Clock.SYSTEM_CLOCK_1, frequency, samples)
        >>> for index in range(samples):
        ...     card.task_read_encoder(task, samples_to_read, counts)  # Returns every millisecond with next sample
        ...     card.watchdog_reload()  # Reload watchdog before using counts for control
        ...     # Do control calculations and output motor torques
        ...
        >>> card.task_stop()
        >>> card.task_delete()
        >>> card.watchdog_stop()
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_reload(self._card if self._card is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

        return True if result else False

    def watchdog_is_expired(self):
        """Indicates whether the watchdog has expired. It is not typically required because the `watchdog_reload`
        function's return value also indicates whether the watchdog has expired.

        Returns
        -------
        int 
            ``True`` if the watchdog has expired; ``False`` otherwise.

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------

        >>> import time
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> timeout = 0.2
        >>> card.watchdog_start(timeout)
        >>> time.sleep(0.5)
        >>> is_watchdog_expired = card.watchdog_is_expired()
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_is_expired(self._card if self._card is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

        return True if result else False

    def watchdog_clear(self):
        """Clears the watchdog state after expiration. When the watchdog timer expires, it prevents further access to
        the hardware after setting the outputs to the configured expiration states. In order to clear this "protected"
        state and allow access to the hardware again, the `watchdog_clear` function must be called. This function
        estores the hardware to its state prior to the watchdog timer expiring, if possible.

        For example, for the Q8-series cards it reprograms the digital directions and analog modes to their original
        values since these are reset by the watchdog expiration (if the analog and digital output expiration states have
        been configured).

        Raises
        ------
        HILError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        If the watchdog expires before reload, clear the watchdog state so that we can continue to control the hardware.

        >>> import time
        >>> from quanser.hardware import HIL
        >>> card = HIL("q8_usb", "0")
        >>> timeout = 0.1
        >>> card.watchdog_start(timeout)
        >>> time.sleep(0.2)
        >>> if not card.watchdog_reload():
        ...     card.watchdog_clear()
        ...
        >>> # ...
        ...
        >>> card.close()

        """
        result = hil_lib.hil_watchdog_clear(self._card if self._card is not None else ffi.NULL)

        if result < 0:
            raise HILError(result)

    # endregion

# endregion
