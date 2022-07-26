class ImageFormat:
    """The image format."""
    __slots__ = ()

    COL_MAJOR_PLANAR_RGB = 0
    """Column-major planar RGB H x W x 3"""

    COL_MAJOR_GREYSCALE = 1
    """Column major H x W"""

    ROW_MAJOR_INTERLEAVED_BGR = 2
    """Row-major interleaved BGR 3 x W x H suitable for OpenCV ``CV_8UC3`` matrices (must be ``ImageDataType.UINT8`` in
    this case)."""

    ROW_MAJOR_GREYSCALE = 3
    """Row-major W x H suitable for OpenCV ``CV_8UC1`` matrices (image data type must be ``IMAGE_DATA_TYPE_UINT8 or
    ``IMAGE_DATA_TYPE_UINT16`` in this case)"""

    COMPRESSED = 4
    """Compressed image (must be ``ImageDataType.UINT8`` in this case)"""


class ImageDataType:
    """The image data type."""
    __slots__ = ()

    UINT8 = 0
    """8-bit unsigned integer."""

    UINT16 = 1
    """16-bit unsigned integer."""

    UINT32 = 2
    """32-bit unsigned integer."""

    SINGLE = 3
    """Single-precision floating-point number."""

    DOUBLE = 4
    """Double-precision floating-point number."""


class VideoCapturePropertyCode:
    """The video capture property code."""
    __slots__ = ()

    BRIGHTNESS = 0
    """The brightness."""

    CONTRAST = 1
    """The contrast."""

    HUE = 2
    """The hue."""

    SATURATION = 3
    """The saturation."""

    SHARPNESS = 4
    """The sharpness."""

    GAMMA = 5
    """The gamma."""

    COLOR_EFFECT = 6
    """The color effect."""

    WHITE_BALANCE = 7
    """The white balance."""

    BACKLIGHT_COMPENSATION = 8
    """The backlight compensation."""

    GAIN = 9
    """The gain."""

    PAN = 10
    """The pan."""

    TILT = 11
    """The tilt."""

    ROLL = 12
    """The roll."""

    ZOOM = 13
    """The zoom."""

    EXPOSURE = 14
    """The exposure."""

    IRIS = 15
    """Iris."""

    FOCUS = 16
    """The focus."""


class VideoCaptureColorEffect:
    """The video capture color effect."""
    __slots__ = ()

    NONE = 0
    """No color effect."""

    BLACK_AND_WHITE = 1
    """A black and white color effect."""

    SEPIA = 2
    """A Sepia color effect."""

    NEGATIVE = 3
    """A negative color effect."""

    EMBOSS = 4
    """An emboss color effect."""

    SKETCH = 5
    """A sketch color efffect."""

    SKY_BLUE = 6
    """A sky blue color effect."""

    GRASS_GREEN = 7
    """A grass green color effect."""

    SKIN_WHITEN = 8
    """A skin whiten color effect."""

    VIVID = 9
    """A vivid color effect."""

    AQUA = 10
    """An aqua color effect."""

    ART_FREEZE = 11
    """An art freeze color effect."""

    SILHOUETTE = 12
    """A silhouette color effect."""

    SOLARIZATION = 13
    """A solarization color effect."""

    ANTIQUE = 14
    """An antique color effect."""


class Video3DStreamType:
    """The video3d stream type."""
    __slots__ = ()

    DEPTH = 0
    """Indicates a depth stream."""

    COLOR = 1
    """Indicates a color stream."""

    INFRARED = 2
    """Indicates an infrared stream."""

    FISHEYE = 3
    """Indicates a fisheye stream."""

    GYROSCOPE = 4
    """Indicates a gyroscope stream."""

    ACCELEROMETER = 5
    """Indicates an accelerometer stream."""

    POSE = 6
    """Indicates a pose stream."""


class Video3DProperty:
    """The video3d property code."""
    __slots__ = ()

    BACKLIGHT_COMPENSATION = 0
    """The backlight compensation property."""

    BRIGHTNESS = 1
    """The brightness property."""

    CONTRAST = 2
    """The contrast property."""

    EXPOSURE = 3
    """The exposure property."""

    GAIN = 4
    """THe gain property."""

    GAMMA = 5
    """The gamma property."""

    HUE = 6
    """The hue property."""

    SATURATION = 7
    """The saturation property."""

    SHARPNESS = 8
    """The sharpness property."""

    WHITE_BALANCE = 9
    """The white balance property."""

    ENABLE_AUTO_EXPOSURE = 10
    """The enable auto exposure property."""

    ENABLE_AUTO_WHITE_BALANCE = 11
    """The enable auto white balance property."""

    ENABLE_EMITTER = 12
    """The enable emitter property."""

    VISUAL_PRESET = 13
    """The visual preset property."""

class Video3DDistortionModel:
    """The video3d distortion model code."""
    __slots__ = ()

    NONE = 0
    """Mo distortion"""

    MODIFIED_BROWN_CONRADY = 1
    """Modified Brown-Conrady distortion"""

    INVERSE_BROWN_CONRADY = 2
    """Inverse Brown-Conrady distortion"""

    FTHETA = 3
    """F-Theta distortion"""

    BROWN_CONRADY = 4
    """Brown-Conrady distortion"""

    KANNALA_BRANDT4 = 5
    """Kannala-Brandt4 distortion"""
