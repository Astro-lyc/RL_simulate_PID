class BooleanProperty:
    """Used to get or set boolean properties of the stream."""
    __slots__ = ()

    IS_READ_ONLY = 0
    """Stream cannot be written but is read-only e.g. "myfile.txt?mode=r". Used by persistent streams."""

    IS_WRITE_ONLY = 1
    """Stream cannot be read but is write-only e.g. "myfile.txt?mode=w". Used by persistent streams."""

    IS_EXCLUSIVE = 2
    """Gain exclusive access to the stream. e.g. used with I2C to combine messages by sending/receiving without
    releasing the bus."""

    NO_READ_AHEAD = 3
    """Do not read ahead on receives i.e. do not attempt to fill receive buffer. Only read requested number of bytes."""

    SERIAL_DTR = 4
    """Used to set or clear the data-terminal-ready (DTR) signal of serial ports."""

    SERIAL_RTS = 5
    """Used to set or clear the ready-to-send (RTS) signal of serial ports."""

    SERIAL_DSR = 6
    """Used to get the data-set-ready (DSR) signal of serial ports."""

    SERIAL_CTS = 7
    """Used to get the clear-to-send (CTS) signal of serial ports."""


class PollFlag:
    """A bit mask indicating the conditions for which to check during a `poll`."""
    __slots__ = ()

    RECEIVE = 0x01
    """On a listening stream, check for connections pending from clients. On a client stream, check whether there is any
    data available to receive."""

    SEND = 0x02
    """Not valid on a listening stream. On a client stream, check whether there is space in the stream buffer to store
    any data."""

    ACCEPT = 0x04
    """Not valid on a client stream. On a listening stream, check whether there is a pending client connection."""

    CONNECT = 0x08
    """Not valid on a listening stream. On a client stream, check whether the connection has completed."""

    FLUSH = 0x80
    """Not valid on a listening stream. On a client stream, check whether it is possible to flush any more data without
    blocking."""
