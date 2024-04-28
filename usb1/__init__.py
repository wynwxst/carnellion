# Copyright (C) 2010-2021  Vincent Pelletier <plr.vincent@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

# pylint: disable=invalid-name, too-many-locals, too-many-arguments
# pylint: disable=too-many-public-methods, too-many-instance-attributes
# pylint: disable=missing-docstring, too-many-lines
"""
Pythonic wrapper for libusb-1.0.

The first thing you must do is to get an "USB context". To do so, create an
USBContext instance.
Then, you can use it to browse available USB devices and open the one you want
to talk to.
At this point, you should have a USBDeviceHandle instance (as returned by
USBContext or USBDevice instances), and you can start exchanging with the
device.

Features:
- Basic device settings (configuration & interface selection, ...)
- String descriptor lookups (ASCII & unicode), and list supported language
  codes
- Synchronous I/O (control, bulk, interrupt)
- Asynchronous I/O (control, bulk, interrupt, isochronous)
  Note: Isochronous support is not well tested.
  See USBPoller, USBTransfer and USBTransferHelper.

All LIBUSB_* constants are available in this module, without the LIBUSB_
prefix - with one exception: LIBUSB_5GBPS_OPERATION is available as
SUPER_SPEED_OPERATION, so it is a valid python identifier.

All LIBUSB_ERROR_* constants are available in this module as exception classes,
subclassing USBError.
"""

from .classes import *
from . import iosb
from . import consts