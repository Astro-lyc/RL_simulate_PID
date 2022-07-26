import os
import sys

from cffi import FFI

from quanser.common.exceptions import GenericError


def get_platform():
    os_platform = sys.platform
    if os_platform.startswith("win"):
        return "win"
    elif os_platform.startswith("mac"):
        return "mac"
    else:
        return "nix"

def add_quarc_path():
    if (sys.version_info[0] > 3) or ((sys.version_info[0] == 3) and (sys.version_info[1] >= 8)):
        quarc_dir = os.getenv('QUARC_DIR')
        if quarc_dir != None:
            os.add_dll_directory(quarc_dir)

ffi = FFI()
ffi.cdef("""
    typedef signed int  t_int;
    typedef t_int       t_error;

    t_error msg_get_current_localeW(wchar_t * buffer, size_t buffer_size);
    
    t_error msg_get_error_messageW(const wchar_t * locale, t_error error_code, wchar_t * buffer, size_t length);
""")

add_quarc_path()
runtime_lib = ffi.dlopen("quanser_runtime")

_WCHAR_T_PTR = "wchar_t *"
_WCHAR_T_ARRAY = "wchar_t[]"
MAX_STRING_LENGTH = 32767

def get_current_locale(size):
    """Gets the current locale."""
    buffer = ffi.new(_WCHAR_T_PTR)

    result = runtime_lib.msg_get_current_localeW(buffer, size)
    if result < 0:
        raise GenericError(result)

    return ffi.string(buffer)


def get_error_message(locale, error_code, length):
    """Gets an error message for the specified error code."""
    _locale = ffi.new(_WCHAR_T_ARRAY, locale) if locale is not None else ffi.NULL

    if (length < 0):
        length = runtime_lib.msg_get_error_messageW(_locale, error_code, ffi.NULL, MAX_STRING_LENGTH)
        if length < 0:
            raise GenericError(length)
        length += 2 # TODO: This should not have to be two, but should be one, no?
    
    buffer = ffi.new("wchar_t[%d]" % length)
    result = runtime_lib.msg_get_error_messageW(_locale, error_code, buffer, length)
    if result < 0:
        raise GenericError(result)

    return ffi.string(buffer)
