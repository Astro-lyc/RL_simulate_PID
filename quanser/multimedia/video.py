import os

from cffi import FFI

from quanser.multimedia import (ImageDataType, ImageFormat, Video3DProperty, Video3DStreamType,
                                VideoCapturePropertyCode, VideoCaptureAttribute, MediaError)


# region Setup


ffi = FFI()
ffi.cdef("""
    /* Common Type Definitions */
    
    typedef char                t_boolean;
    typedef unsigned int        t_uint;
    typedef unsigned long long  t_ulong;
    typedef t_ulong             t_uint64;
    typedef signed int          t_int;
    typedef t_int               t_error;
    typedef float               t_single;
    typedef double              t_double;
 
    /* Video Capture Type Definitions */
    
    typedef struct tag_video_capture * t_video_capture;
    
    typedef enum tag_image_format
    {
        IMAGE_FORMAT_COL_MAJOR_PLANAR_RGB,
        IMAGE_FORMAT_COL_MAJOR_GREYSCALE,
        IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR,
        IMAGE_FORMAT_COMPRESSED,
    
        NUMBER_OF_IMAGE_FORMATS
    } t_image_format;
    
    typedef enum tag_image_data_type
    {
        IMAGE_DATA_TYPE_UINT8,
        IMAGE_DATA_TYPE_UINT16,
        IMAGE_DATA_TYPE_UINT32,
        IMAGE_DATA_TYPE_SINGLE,
        IMAGE_DATA_TYPE_DOUBLE,
    
        NUMBER_OF_IMAGE_DATA_TYPES
    } t_image_data_type;
    
    typedef enum tag_video_capture_property_code
    {
        VIDEO_CAPTURE_PROPERTY_BRIGHTNESS,
        VIDEO_CAPTURE_PROPERTY_CONTRAST,
        VIDEO_CAPTURE_PROPERTY_HUE,
        VIDEO_CAPTURE_PROPERTY_SATURATION,
        VIDEO_CAPTURE_PROPERTY_SHARPNESS,
        VIDEO_CAPTURE_PROPERTY_GAMMA,
        VIDEO_CAPTURE_PROPERTY_COLOREFFECT,
        VIDEO_CAPTURE_PROPERTY_WHITEBALANCE,
        VIDEO_CAPTURE_PROPERTY_BACKLIGHTCOMPENSATION,
        VIDEO_CAPTURE_PROPERTY_GAIN,
    
        VIDEO_CAPTURE_PROPERTY_PAN,
        VIDEO_CAPTURE_PROPERTY_TILT,
        VIDEO_CAPTURE_PROPERTY_ROLL,
        VIDEO_CAPTURE_PROPERTY_ZOOM,
        VIDEO_CAPTURE_PROPERTY_EXPOSURE,
        VIDEO_CAPTURE_PROPERTY_IRIS,
        VIDEO_CAPTURE_PROPERTY_FOCUS,
    
        NUMBER_OF_VIDEO_CAPTURE_PROPERTIES
        
    } t_video_capture_property_code;
    
    typedef enum tag_video_capture_color_effect
    {
        COLOR_EFFECT_NONE,
        COLOR_EFFECT_BLACK_AND_WHITE,
        COLOR_EFFECT_SEPIA,
        COLOR_EFFECT_NEGATIVE,
        COLOR_EFFECT_EMBOSS,
        COLOR_EFFECT_SKETCH,
        COLOR_EFFECT_SKY_BLUE,
        COLOR_EFFECT_GRASS_GREEN,
        COLOR_EFFECT_SKIN_WHITEN,
        COLOR_EFFECT_VIVID,
        COLOR_EFFECT_AQUA,
        COLOR_EFFECT_ART_FREEZE,
        COLOR_EFFECT_SILHOUETTE,
        COLOR_EFFECT_SOLARIZATION,
        COLOR_EFFECT_ANTIQUE,
    
        NUMBER_OF_COLOR_EFFECTS
    
    } t_video_capture_color_effect;
    
    typedef struct tag_video_capture_attribute
    {
        t_double                      value;
        t_video_capture_property_code property_code;
        t_boolean                     manual;
        t_boolean                     is_enumeration;
    } t_video_capture_attribute;
    
    /* Video Capture Functions */
    
    t_error video_capture_open(const char * url, t_double frame_rate, t_uint frame_width, t_uint frame_height,
                               t_image_format format, t_image_data_type data_type, t_video_capture * capture, 
                               t_video_capture_attribute * attr, t_uint num_attributes);

    t_error video_capture_close(t_video_capture capture);

    t_error video_capture_set_property(t_video_capture capture,
                                       t_video_capture_attribute * attributes, t_uint num_attributes);

    t_error video_capture_start(t_video_capture capture);
    t_error video_capture_read(t_video_capture capture, void * image_data);
    t_error video_capture_stop(t_video_capture capture);
    
    /* Video3D Type Definitions */
    
    typedef struct tag_video3d * t_video3d;
    typedef struct tag_video3d_stream * t_video3d_stream;
    typedef struct tag_video3d_frame * t_video3d_frame;

    typedef enum tag_video3d_property
    {
        VIDEO3D_PROPERTY_BACKLIGHT_COMPENSATION,
        VIDEO3D_PROPERTY_BRIGHTNESS,
        VIDEO3D_PROPERTY_CONTRAST,
        VIDEO3D_PROPERTY_EXPOSURE,
        VIDEO3D_PROPERTY_GAIN,
        VIDEO3D_PROPERTY_GAMMA,
        VIDEO3D_PROPERTY_HUE,
        VIDEO3D_PROPERTY_SATURATION,
        VIDEO3D_PROPERTY_SHARPNESS,
        VIDEO3D_PROPERTY_WHITE_BALANCE,
        VIDEO3D_PROPERTY_ENABLE_AUTO_EXPOSURE,
        VIDEO3D_PROPERTY_ENABLE_AUTO_WHITE_BALANCE,
        VIDEO3D_PROPERTY_ENABLE_EMITTER,
        VIDEO3D_PROPERTY_VISUAL_PRESET,
    
        NUMBER_OF_VIDEO3D_PROPERTIES
    } t_video3d_property;

    typedef enum tag_video3d_stream_type
    {
        VIDEO3D_STREAM_DEPTH,
        VIDEO3D_STREAM_COLOR,
        VIDEO3D_STREAM_INFRARED,
        VIDEO3D_STREAM_FISHEYE,
        VIDEO3D_STREAM_GYROSCOPE,
        VIDEO3D_STREAM_ACCELEROMETER,
        VIDEO3D_STREAM_POSE,
        /*VIDEO3D_STREAM_GPIO,*/

        NUMBER_OF_VIDEO3D_STREAMS
    } t_video3d_stream_type;

	typedef enum tag_video3d_distortion_model
	{
		VIDEO3D_DISTORTION_NONE,
		VIDEO3D_DISTORTION_MODIFIED_BROWN_CONRADY,
		VIDEO3D_DISTORTION_INVERSE_BROWN_CONRADY,
		VIDEO3D_DISTORTION_FTHETA,
		VIDEO3D_DISTORTION_BROWN_CONRADY,
		VIDEO3D_DISTORTION_KANNALA_BRANDT4,

		NUMBER_OF_VIDEO3D_DISTORTIONS
	} t_video3d_distortion_model;

    /* Video3D Functions */

    t_error video3d_open(const char * device_id, t_video3d * handle);
    
    t_error video3d_open_file(const char * device_file, t_video3d * handle);
    
    t_error video3d_close(t_video3d handle);

    /* Stream Functions */

    t_error video3d_stream_open(t_video3d handle,
                                t_video3d_stream_type type, t_uint index,
                                t_double frame_rate, t_uint frame_width, t_uint frame_height,
                                t_image_format format, t_image_data_type data_type,
                                t_video3d_stream * stream);
                                
    t_error video3d_stream_close(t_video3d_stream stream);
                                
    t_error video3d_stream_set_properties(t_video3d_stream stream,
                                          t_video3d_property * properties, size_t num_properties,
                                          double * values);

    t_error	video3d_stream_get_camera_intrinsics(t_video3d_stream stream, float intrinsics[3][3], t_video3d_distortion_model* distortion, float distortion_coefficients[5]);

    t_error	video3d_stream_get_extrinsics(t_video3d_stream from_stream, t_video3d_stream to_stream, t_single transform[4][4]);

    t_error video3d_start_streaming(t_video3d handle);

    t_error video3d_stop_streaming(t_video3d handle);

    t_error video3d_stream_get_frame(t_video3d_stream stream, t_video3d_frame * frame);
    
    /* Frame Functions */

    t_error video3d_frame_release(t_video3d_frame frame);

    t_error video3d_frame_get_number(t_video3d_frame frame, t_uint64 * number);

    t_error video3d_frame_get_timestamp(t_video3d_frame frame, t_double * timestamp);

    t_error video3d_frame_get_data(t_video3d_frame frame, void * data);
    
    t_error video3d_frame_get_meters(t_video3d_frame frame, t_single * data);
""")

media_lib = ffi.dlopen("quanser_media")

# endregion

# region Constants

_WOULD_BLOCK = 34

_SINGLE_ARRAY = "t_single[]"
_DOUBLE_ARRAY = "t_double[]"

_VIDEO3D_PROPERTY_ARRAY = "t_video3d_property[]"

# endregion

# region Media Classes


class VideoCapture:
    """A Python wrapper for the Quanser Media 2D API.

    Valid URLs::

        C:/Users/Me/Videos      - capture video from a file (path specified without file: scheme)
        file://localhost/path   - capture video from a file
        http://host/path        - capture video from the web (only supported in Windows). The https scheme
        should also be supported (or other valid Internet schemes supported by Media Foundation).
        video://localhost:id    - capture video from a camera or other device
        Note that additional options could potentially be specified as query options in the URL.

    Parameters
    ----------
    url : string
        The URL.
    frame_rate : float
        The frame rate.
    frame_width : int
        The frame width.
    frame_height : int
        The frame height.
    image_format : ImageFormat
        The format argument describes the format for the image frames retrieved.

        If the image format is ``ImageFormat.ROW_MAJOR_INTERLEAVED_BGR``, then the data is stored in CV_8UC3 format, which is a
        row-major interleaved format. In other words, the BGR components of each pixel are stored contiguously, with
        one byte per colour component, and pixels are stored row by row. The data type must be ImageDataType.UINT8 in this case.

        If the image format is ``ImageFormat.ROW_MAJOR_GREYSCALE``, then the data is stored in CV_8UC1 format, which is
        a row-major format. In other words, there is one byte per pixel, and pixels are stored row by row. The data type
        must be ImageDataType.UINT8 in this case.

        If the image format is ``ImageFormat.COL_MAJOR_PLANAR_RGB``, then the data is stored in a column-major planar
        format. In other words, pixels are stored column by column, with all the red components stored together,
        followed by all the green components, and finally, all the blue components.

        If the image format is ``ImageFormat.COL_MAJOR_GREYSCALE``, then the data is stored in column-major format.
        In other words, there is one byte per pixel, and pixels are stored column by column.
    image_data_type : ImageDataType
        The image data type.
    attributes : array_like
        The video capture attributes.
    num_attributes : int
        The number of attributes in the `attributes` array.

    Raises
    ------
    MediaError
        On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

    Examples
    --------
    Constructs a new video capture object without opening a connection to a device.

    >>> from quanser.multimedia import VideoCapture
    >>> capture = VideoCapture()
    >>> # ...
    ...
    >>> capture.close()

    Constructs a new video capture object and opens a connection to the specified device with the specified parameters.

    >>> from quanser.multimedia import (VideoCapture, ImageFormat, ImageDataType,
    ...                                 VideoCaptureAttribute, VideoCapturePropertyCode)
    >>> url = "video://localhost:0"
    >>> frame_rate = 30.0
    >>> frame_width = 1920
    >>> frame_height = 1080
    >>> attributes = [
    ...     VideoCaptureAttribute(VideoCapturePropertyCode.BRIGHTNESS, 100.0, True),
    ...     VideoCaptureAttribute(VideoCapturePropertyCode.CONTRAST, 100.0, True)
    ... ]
    ...
    >>> capture = VideoCapture(url,
    ...                        frame_rate, frame_width, frame_height,
    ...                        ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
    ...                        attributes, len(attributes))
    ...
    >>> # ...
    ...
    >>> capture.close()

    """

    # region Life Cycle

    def __init__(self, url=None,
                 frame_rate=30.0, frame_width=1920, frame_height=1080,
                 image_format=ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, image_data_type=ImageDataType.UINT8,
                 attributes=None, num_attributes=0):
        self._capture = None

        # If non-default arguments are passed, attempt to open the device.
        if url is not None or attributes is not None:
            self.open(url,
                      frame_rate, frame_width, frame_height,
                      image_format, image_data_type,
                      attributes, num_attributes)

    # endregion

    # region Functions

    def open(self, url,
             frame_rate, frame_width, frame_height,
             image_format, image_data_type,
             attributes, num_attributes):
        """Opens a URL for video capture.

        Valid URLs::

            C:/Users/Me/Videos      - capture video from a file (path specified without file: scheme)
            file://localhost/path   - capture video from a file
            http://host/path        - capture video from the web (only supported in Windows). The https scheme
            should also be supported (or other valid Internet schemes supported by Media Foundation).
            video://localhost:id    - capture video from a camera or other device
            Note that additional options could potentially be specified as query options in the URL.

        Parameters
        ----------
        url : string
            The URL.
        frame_rate : float
            The frame rate.
        frame_width : int
            The frame width.
        frame_height : int
            The frame height.
        image_format : ImageFormat
            The format argument describes the format for the image frames retrieved.

            If the image format is ``ImageFormat.ROW_MAJOR_INTERLEAVED_BGR``, then the data is stored in CV_8UC3 format, which is a
            row-major interleaved format. In other words, the BGR components of each pixel are stored contiguously, with
            one byte per colour component, and pixels are stored row by row. The data type must be ImageDataType.UINT8 in this case.

            If the image format is ``ImageFormat.ROW_MAJOR_GREYSCALE``, then the data is stored in CV_8UC1 format, which is
            a row-major format. In other words, there is one byte per pixel, and pixels are stored row by row. The data type
            must be ImageDataType.UINT8 in this case.

            If the image format is ``ImageFormat.COL_MAJOR_PLANAR_RGB``, then the data is stored in a column-major planar
            format. In other words, pixels are stored column by column, with all the red components stored together,
            followed by all the green components, and finally, all the blue components.

            If the image format is ``ImageFormat.COL_MAJOR_GREYSCALE``, then the data is stored in column-major format.
            In other words, there is one byte per pixel, and pixels are stored column by column.
        image_data_type : ImageDataType
            The image data type.
        attributes : array_like
            The video capture attributes.
        num_attributes : int
            The number of attributes in the `attributes` array.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Examples
        --------
        Open the first camera on the local host.

        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> capture = VideoCapture()
        >>> capture.open(url,
        ...              frame_rate, frame_width, frame_height,
        ...              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...              None, 0)
        ...
        >>> # ...
        ...
        >>> capture.close()

        Open the first camera on the local host with the brightness and contrast both set to 100%.

        >>> from quanser.multimedia import (VideoCapture, ImageDataType, ImageFormat,
        ...                                 VideoCaptureAttribute, VideoCapturePropertyCode)
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> attributes = [
        ...     VideoCaptureAttribute(VideoCapturePropertyCode.BRIGHTNESS, 100.0, True),
        ...     VideoCaptureAttribute(VideoCapturePropertyCode.CONTRAST, 100.0, True)
        ... ]
        ...
        >>> capture = VideoCapture()
        >>> capture.open(url,
        ...              frame_rate, frame_width, frame_height,
        ...              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...              attributes, len(attributes)
        ...
        >>> # ...
        ...
        >>> capture.close()

        """
        if self._capture is not None:
            self.close()

        capture = ffi.new("t_video_capture *")

        attrs = VideoCapture._make_attributes(attributes, num_attributes)

        result = media_lib.video_capture_open(url.encode("UTF-8"),
                                              frame_rate, frame_width, frame_height,
                                              image_format, image_data_type,                                              
                                              capture,
                                              attrs, num_attributes)
        if result < 0:
            raise MediaError(result)

        self._capture = capture[0]

    def close(self):
        """Closes the handle to the underlying video capture object.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Close the first camera on the local host.

        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> capture = VideoCapture()
        >>> capture.open(url,
        ...              frame_rate, frame_width, frame_height,
        ...              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...              None, 0)
        ...
        >>> # ...
        ...
        >>> capture.close()

        """
        result = media_lib.video_capture_close(self._capture if self._capture is not None else ffi.NULL)
        if result < 0:
            raise MediaError(result)

        self._capture = None

    def set_property(self, attributes, num_attributes):
        """Set properties for the video capture. The property values will be updated when the next frame is read.

        Parameters
        ----------
        attributes : array_like
            The video capture attributes.
        num_attributes : int
            The number of attributes in the `attributes` array.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Set the brightness and contrast to 100%.

        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> capture = VideoCapture(url,
        ...                        frame_rate, frame_width, frame_height,
        ...                        ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...                        None, 0)
        ...
        >>> # ...
        ...
        >>> attributes = [
        ...     VideoCaptureAttribute(VideoCapturePropertyCode.BRIGHTNESS, 100.0, True),
        ...     VideoCaptureAttribute(VideoCapturePropertyCode.CONTRAST, 100.0, True)
        ... ]
        ...
        >>> capture.set_property(attributes, len(attributes))
        >>> # ...
        ...
        >>> capture.close()

        """
        attrs = VideoCapture._make_attributes(attributes, num_attributes)

        result = media_lib.video_capture_set_property(self._capture if self._capture is not None else ffi.NULL,
                                                      attrs, num_attributes)
        if result < 0:
            raise MediaError(result)

    def start(self):
        """Starts streaming from the video capture source.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Start streaming from the first camera.

        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> capture = VideoCapture()
        >>> capture.open(url,
        ...              frame_rate, frame_width, frame_height,
        ...              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...              None, 0)
        ...
        >>> capture.start()
        ...
        >>> capture.stop()
        >>> capture.close()

        """
        result = media_lib.video_capture_start(self._capture if self._capture is not None else ffi.NULL)
        if result < 0:
            raise MediaError(result)

    def read(self, image_data):
        """Read one frame from the image source. Returns ``True`` if a new image is read. Returns ``False`` if no new
        image is currently available. Otherwise, raises an exception.

        If the format argument is ``ImageFormat.MAT``, then the `image_data` argument should be a pointer to the
        cv::Mat object. The `colour_mode` and frame dimensions from the `open` call determine the type of Mat data
        returned. For greyscale images, a Mat containing uchar elements is returned (CV_8UC1), while for RGB images, a
        Mat containing Vec3b elements is returned (CV_8UC3) in which the Vec3b elements are in blue, green, red (BGR)
        order.

        If the format argument is ``ImageFormat.SIMULINK``, then the `image_data` argument should be a pointer to a
        uint8_T array that will be filled with the image data. The `colour_mode` and frame dimensions from the `open`
        call determine the amount of data written to the buffer (greyscale or RGB). For greyscale images, the
        `image_data` must have width * height elements. For RGB images, the `image_data` must have width * height * 3
        elements. The data is stored in memory in the order suitable for an HxWxF matrix, in which F=1 for greyscale
        images and F=3 for RGB images.

        Parameters
        ----------
        image_data : array_like
             An array to hold the image data. `image_data` must point to memory large enough to hold the image in the
             specified format and data type (HxWx3 or HxW).

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Read 1000 frames from the camera.

        >>> import numpy as np
        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> image_data = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        >>> capture = VideoCapture(url,
        ...                        frame_rate, frame_width, frame_height,
        ...                        ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...                        None, 0)
        ...
        >>> capture.start()
        >>> for i in range(1000):
        ...     capture.read(image_data)
        ...     # ...
        ...
        >>> capture.stop()
        >>> capture.close()

        """
        result = media_lib.video_capture_read(self._capture if self._capture is not None else ffi.NULL, ffi.from_buffer(image_data))
        if result < 0:
            raise MediaError(result)

        return True if result else False

    def stop(self):
        """Stops streaming from the video capture source.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Stop streaming from the first camera.

        >>> from quanser.multimedia import VideoCapture, ImageDataType, ImageFormat
        >>> url = "video://localhost:0"
        >>> frame_rate = 30.0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> capture = VideoCapture()
        >>> capture.open(url,
        ...              frame_rate, frame_width, frame_height,
        ...              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8,
        ...              None, 0)
        ...
        >>> capture.start()
        ...
        >>> capture.stop()
        >>> capture.close()

        """
        result = media_lib.video_capture_stop(self._capture if self._capture is not None else ffi.NULL)
        if result < 0:
            raise MediaError(result)

    @staticmethod
    def _make_attributes(attributes, num_attributes):
        attrs = ffi.new("t_video_capture_attribute[%d]" % num_attributes)
        for i in range(num_attributes):
            attrs[i].property_code = attributes[i].property_code
            attrs[i].value = attributes[i].value
            attrs[i].manual = b'\x01' if attributes[i].manual else b'\x00'
            attrs[i].is_enumeration = b'\x01' if attributes[i].is_enumeration else b'\x00'

        return attrs

    # endregion


class Video3D:
    """A Python wrapper for the Quanser Media 3D API.

    Parameters
    ----------
    device_id : string
        The device identifier. If `device_id` is a number, such as "3", then it will open the device based on its
        index in the device list. The number may be octal or hexadecimal as well. Otherwise, it will identify the
        device by serial number.

    Raises
    ------
    MediaError
        On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

    Examples
    --------
    Constructs a new Video3D object without opening a connection to a device.

    >>> from quanser.multimedia import Video3D
    >>> video3d = Video3D()
    >>> # ...
    ...
    >>> video3d.close()

    Constructs a new Video3D object and opens a connection to the specified video3d device.

    >>> from quanser.multimedia import Video3D
    >>> video3d = Video3D("0")
    >>> # ...
    ...
    >>> video3d.close()

    """
    # region Life Cycle

    def __init__(self, device_id=None):
        self._video = None

        # If non-default arguments are passed, attempt to connect to the device.
        if device_id is not None:
            self.open(device_id)

    # endregion

    # region Functions

    def open(self, device_id):
        """Opens a video3d device.

        Parameters
        ----------
        device_id : string
            The device identifier. If `device_id` is a number, such as "3", then it will open the device based on its
            index in the device list. The number may be octal or hexadecimal as well. Otherwise, it will identify the
            device by serial number.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Opens the specified video3d device.

        >>> from quanser.multimedia import Video3D
        >>> video3d = Video3D()
        >>> video3d.open("0")
        >>> # ...
        ...
        >>> video3d.close()

        """
        video = ffi.new("t_video3d *")
        result = media_lib.video3d_open(device_id.encode("UTF-8"), video)

        if result < 0:
            raise MediaError(result)

        self._video = video[0]

    def open_file(self, device_file):
        """Opens a video3d file to emulate a device.

        Parameters
        ----------
        device_file : string
            The path to the video3d file.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        >>> from os import path
        >>> from quanser.multimedia import Video3D
        >>> file_path = path.join("path", "to", "ros.bag")
        >>> video3d = Video3D()
        >>> video3d.open_file(file_path)
        >>> # ...
        ...
        >>> video3d.close()

        """
        video = ffi.new("t_video3d *")
        result = media_lib.video3d_open_file(device_file.encode("UTF-8"), video)

        if result < 0:
            raise MediaError(result)

        self._video = video[0]

    def close(self):
        """Closes a video3d device.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        >>> from quanser.multimedia import Video3D
        >>> video3d = Video3D()
        >>> video3d.open("0")
        >>> # ...
        ...
        >>> video3d.close()

        """
        result = media_lib.video3d_close(self._video if self._video is not None else ffi.NULL)

        if result < 0:
            raise MediaError(result)

        self._video = None

    def stream_open(self, stream_type, index, frame_rate, frame_width, frame_height, image_format, image_data_type):
        """Enables a video3d stream.

        This function looks for an exact match for the stream type, frame width, and frame height, but is more lenient
        with regards to the frame rate, finding the closest rate.

        Parameters
        ----------
        stream_type : Video3DStreamType
            The type of image data to be enabled (e.g. depth, infrared, color, etc.)
        index : int
            The zero-based index of the stream.
        frame_rate : float
            The frame rate in Hz.
        frame_width : int
            The frame width.
        frame_height : int
            The frame height.
        image_format : ImageFormat
            The format argument describes the format for the image frames retrieved.

            If the image format is ``ImageFormat.ROW_MAJOR_INTERLEAVED_BGR``, then the data is stored in CV_8UC3 format, which is a
            row-major interleaved format. In other words, the BGR components of each pixel are stored contiguously, with
            one byte per colour component, and pixels are stored row by row. The data type must be ImageDataType.UINT8 in this case.

            If the image format is ``ImageFormat.ROW_MAJOR_GREYSCALE``, then the data is stored in CV_8UC1 format, which is
            a row-major format. In other words, there is one byte per pixel, and pixels are stored row by row. The data type
            must be ImageDataType.UINT8 in this case.

            If the image format is ``ImageFormat.COL_MAJOR_PLANAR_RGB``, then the data is stored in a column-major planar
            format. In other words, pixels are stored column by column, with all the red components stored together,
            followed by all the green components, and finally, all the blue components.

            If the image format is ``ImageFormat.COL_MAJOR_GREYSCALE``, then the data is stored in column-major format.
            In other words, there is one byte per pixel, and pixels are stored column by column.
        image_data_type : ImageDataType
            The image data type.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Open a color stream on a live camera.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> stream_index = 0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.COLOR, stream_index,
        ...                              frame_rate, frame_width, frame_height,
        ...                              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
        ...
        >>> # ...
        ...
        >>> stream.close()
        >>> video3d.close()

        Open a depth stream on a live camera.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> stream_index = 0
        >>> frame_width = 1280
        >>> frame_height = 720
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, stream_index,
        ...                              frame_rate, frame_width, frame_height,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT16)
        ...
        >>> # ...
        ...
        >>> stream.close()
        >>> video3d.close()

        """
        stream = ffi.new("t_video3d_stream *")
        result = media_lib.video3d_stream_open(self._video if self._video is not None else ffi.NULL,
                                               stream_type, index,
                                               frame_rate, frame_width, frame_height,
                                               image_format, image_data_type,
                                               stream)

        if result < 0:
            raise MediaError(result)

        return Video3DStream(stream[0])

    def start_streaming(self):
        """Starts streaming on all open streams.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Starts streaming the depth and color streams, both at 1280x720 @30fps, on a live camera.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> stream_index = 0
        >>> frame_width = 1280
        >>> frame_height = 720
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> depth_stream = video3d.stream_open(Video3DStreamType.DEPTH, stream_index,
        ...                                    frame_rate, frame_width, frame_height,
        ...                                    ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT16)
        ...
        >>> color_stream = video3d.stream_open(Video3DStreamType.COLOR, stream_index,
        ...                                    frame_rate, frame_width, frame_height,
        ...                                    ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> # ...
        ...
        >>> video3d.stop_streaming()
        >>> depth_stream.close()
        >>> color_stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_start_streaming(self._video if self._video is not None else ffi.NULL)

        if result < 0:
            raise MediaError(result)

    def stop_streaming(self):
        """Stops streaming on all open streams.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Stops streaming the depth and color streams on a live camera.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat
        >>> stream_index = 0
        >>> frame_width = 1280
        >>> frame_height = 720
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> depth_stream = video3d.stream_open(Video3DStreamType.DEPTH, stream_index,
        ...                                    frame_rate, frame_width, frame_height,
        ...                                    ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT16)
        ...
        >>> color_stream = video3d.stream_open(Video3DStreamType.COLOR, stream_index,
        ...                                    frame_rate, frame_width, frame_height,
        ...                                    ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> # ...
        ...
        >>> video3d.stop_streaming()
        >>> depth_stream.close()
        >>> color_stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_stop_streaming(self._video if self._video is not None else ffi.NULL)

        if result < 0:
            raise MediaError(result)

    # endregion


class Video3DStream:
    """A python wrapper for a video3d stream. You should not need to create an instance of this class yourself."""
    # region Life Cycle

    def __init__(self, stream):
        self._stream = stream

    # endregion

    # region Functions

    def close(self):
        """Closes a stream.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Close an open depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> # ...
        ...
        >>> stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_stream_close(self._stream if self._stream is not None else ffi.NULL)

        if result < 0:
            raise MediaError(result)

        self._stream = None

    def set_properties(self, properties, num_properties, values):
        """Sets the value of one or more properties of a stream. For boolean options, use a value of ``0.0`` or ``1.0``.
        All other options should have a range of ``0.0`` to ``1.0`` inclusive. The function will do the appropriate
        scaling for the internal camera settings. Any values outside the range will be saturated to lie within the
        range.

        Parameters
        ----------
        properties : array_like
            An array of ``Video3DProperty`` to set.
        num_properties : int
            The number of properties in the `properties` array.
        values : array_like
            An array of values. Each element in the `values` array corresponds to the same element in the `properties`
            array.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Set the brightness to 100% and the contrast to 50% on a depth stream.

        >>> import numpy as np
        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DProperty
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> properties = np.array([Video3DProperty.BRIGHTNESS, Video3DProperty.CONTRAST], dtype=np.int32)
        >>> num_properties = len(properties)
        >>> values = np.array([1.0, 0.5], dtype=np.float64)
        >>> stream.set_properties(properties, num_properties, values)
        >>> # ...
        ...
        >>> stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_stream_set_properties(self._stream if self._stream is not None else ffi.NULL,
                                                         ffi.from_buffer(_VIDEO3D_PROPERTY_ARRAY, properties),
                                                         num_properties,
                                                         ffi.from_buffer(_DOUBLE_ARRAY, values))

        if result < 0:
            raise MediaError(result)

    def get_camera_intrinsics(self, intrinsics, coefficients):
        """Gets the camera intrinsics and the distortion model for the given stream.

        Parameters
        ----------
        intrinsics : array_like
            A (3,3) array to fill with the camera intrinsic matrix.
        coefficients : array_like
            A 5-element array to fill with the distortion model coefficients.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Get the camera intrinsics and distortion model for the depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType, Video3DDistortionModel
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> intrinsics = np.zeros((3, 3), dtype=np.float32)
        >>> coefficients = np.zeros((5), dtype=np.float32)
        >>> model = stream.get_camera_intrinsics(intrinsics, coefficients)
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()
        
        """
        model = ffi.new('t_video3d_distortion_model *')

        result = media_lib.video3d_stream_get_camera_intrinsics(self.stream if self._stream is not None else ffi.NULL,
                                                                ffi.from_buffer(_SINGLE_ARRAY, intrinsics) if intrinsics is not None else ffi.NULL,
                                                                model, ffi.from_buffer(_SINGLE_ARRAY, coefficients) if coefficients is not None else ffi.NULL)
        if result < 0:
            raise MediaError(result)

        return Video3DDistortionModel(model[0])

    def get_extrinsics(self, to_stream, extrinsics):
        """Gets the extrinsics transformation from this stream to the given stream.

        Parameters
        ----------
        extrinsics : array_like
            A (4,4) array to fill with the homogeneous transformation matrix representing the extrinsics.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Get the extrinsics transform from the current stream to the given stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> video3d = Video3D("0")
        >>> depth_stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        >>> rgb_stream = video3d.stream_open(Video3DStreamType.COLOR, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_RGB, ImageDataType.UINT8)
        ...
        >>> extrinsics = np.zeros((4, 4), dtype=np.float32)
        >>> depth_stream.get_extrinsics(rgb_stream, extrinsics)
        ...
        >>> video3d.stop_streaming()
        >>> rgb_stream.close()
        >>> depth_stream.close()
        >>> video3d.close()
        
        """
        result = media_lib.video3d_stream_get_extrinsics(self.stream if self._stream is not None else ffi.NULL,
                                                         to_stream if to_stream is not None else ffi.NULL, ffi.from_buffer(_SINGLE_ARRAY, extrinsics))
        if result < 0:
            raise MediaError(result)

    def get_frame(self):
        """Get the latest frame for the given stream. If no frame is available, then it raises ``QERR_WOULD_BLOCK``.
        Only one frame may be retrieved at a time and the frame must be released before getting a new frame.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Capture and process 1000 frames from the depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     # Process...
        ...     frame.release()
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()

        """
        frame = ffi.new("t_video3d_frame *")

        result = media_lib.video3d_stream_get_frame(self._stream if self._stream is not None else ffi.NULL,
                                                    frame)

        if result == -_WOULD_BLOCK:
            return None

        if result < 0:
            raise MediaError(result)

        return Video3DFrame(frame[0])

    # endregion


class Video3DFrame:
    """A Python wrapper for a video3d frame. You should not need to create an instance of this class yourself."""
    # region Life Cycle

    def __init__(self, frame):
        self._frame = frame

    # endregion

    # region Functions

    def release(self):
        """Releases the frame so that a new frame may be captured.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Capture and process 1000 frames from the depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     # Process...
        ...     frame.release()
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()
        """
        result = media_lib.video3d_frame_release(self._frame if self._frame is not None else ffi.NULL)

        if result < 0:
            raise MediaError(result)

        self._frame = None

    def get_number(self):
        """Gets the frame number.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Returns
        -------
        int
            The frame number.

        Example
        -------
        Get the frame number of the first 1000 frames from the depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     number = frame.get_number()
        ...     # ...
        ...     frame.release()
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()

        """
        number = ffi.new("t_uint64 *")
        result = media_lib.video3d_frame_get_number(self._frame if self._frame is not None else ffi.NULL,
                                                    number)
        if result < 0:
            raise MediaError(result)

        return number[0]

    def get_timestamp(self):
        """Gets the frame number.

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Returns
        -------
        float
            The timestamp in fractional seconds since January 1, 1970.

        Example
        -------
        Get the frame timestamp of the first 1000 frames from the depth stream.

        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, 0, 30.0, 1280, 720,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     timestamp = frame.get_timestamp()
        ...     # ...
        ...     frame.release()
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()

        """
        timestamp = ffi.new("t_double *")
        result = media_lib.video3d_frame_get_timestamp(self._frame if self._frame is not None else ffi.NULL,
                                                       timestamp)
        if result < 0:
            raise MediaError(result)

        return timestamp[0]

    def get_data(self, data):
        """Gets the frame data in the specified image format and data type.

        Parameters
        ----------
        data : array_like
             An array to hold the frame data. `data` must point to memory large enough to hold the image in the
             specified format and data type (HxWx3 or HxW).

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Get the frame data of the first 1000 frames from the color stream.

        >>> import numpy as np
        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> stream_index = 0
        >>> frame_width = 1920
        >>> frame_height = 1080
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, stream_index,
        ...                              frame_rate, frame_width, frame_height,
        ...                              ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
        ...
        >>> image_data = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     frame.get_data(image_data)
        ...     frame.release()
        ...     # ...
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_frame_get_data(self._frame if self._frame is not None else ffi.NULL,
                                                  ffi.from_buffer(data))
        if result < 0:
            raise MediaError(result)

    def get_meters(self, data):
        """Gets the frame data in meters (only valid for depth streams).

        Parameters
        ----------
        data : array_like
             An array to hold the frame data. `data` must point to memory large enough to hold the image
             (HxW array of singles).

        Raises
        ------
        MediaError
            On non-zero return code. A suitable error message may be retrieved using `get_error_message`.

        Example
        -------
        Get the frame data in meters of the first 1000 frames from the depth stream.

        >>> import numpy as np
        >>> from quanser.multimedia import Video3D, ImageDataType, ImageFormat, Video3DStreamType
        >>> stream_index = 0
        >>> frame_width = 1280
        >>> frame_height = 720
        >>> frame_rate = 30.0
        >>> video3d = Video3D("0")
        >>> stream = video3d.stream_open(Video3DStreamType.DEPTH, stream_index,
        ...                              frame_rate, frame_width, frame_height,
        ...                              ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
        ...
        >>> image_data = np.zeros((frame_height, frame_width), dtype=np.float32)
        >>> video3d.start_streaming()
        >>> for i in range(1000):
        ...     frame = stream.get_frame()
        ...     frame.get_meters(image_data)
        ...     frame.release()
        ...     # ...
        ...
        >>> video3d.stop_streaming()
        >>> stream.close()
        >>> video3d.close()

        """
        result = media_lib.video3d_frame_get_meters(self._frame if self._frame is not None else ffi.NULL,
                                                    ffi.from_buffer(_SINGLE_ARRAY, data))
        if result < 0:
            raise MediaError(result)

    # endregion

# endregion
