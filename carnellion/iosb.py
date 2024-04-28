import carnellion.classes as usb1


import pickle
import sys
from carnellion.lib import objects
import time
from ctypes import sizeof
import copy


from carnellion.consts import *








class device_descriptor:
    i_serial_number = None


class iosb:
    def __init__(self,handle:usb1.USBDeviceHandle,ctx:usb1.USBContext):
        # only for ios usb based dfu purposes
        self.handle = handle
        self.ctx = ctx
    def async_callback(self,transfer:usb1.USBTransfer):
        
        transfer.setUserData(1)
    def async_control_transfer(self,bmRequestType, bRequest, wValue, wIndex, data,wlen, timeout=0,callback=None):
        if callback == None:
            callback = self.async_callback
        start = time.time()
        req = None
        sz = wlen
        ret = None

        transfer = self.handle.getTransfer()
        buf = bytearray(usb1.libusb1.LIBUSB_CONTROL_SETUP_SIZE + wlen)
        if (bmRequestType & usb1.libusb1.LIBUSB_ENDPOINT_DIR_MASK) == 0x00:
            buf[usb1.libusb1.LIBUSB_CONTROL_SETUP_SIZE:usb1.libusb1.LIBUSB_CONTROL_SETUP_SIZE + wlen] = bytes(data.encode("utf-8"))
        cmp = 0

        

        #usb1.libusb1.libusb_fill_control_setup(bytes(buf),bmRequestType,bRequest,wValue,wIndex,wlen)
        #usb1.libusb1.libusb_fill_control_transfer(transfer,self.handle,buf,self.async_callback,cmp,usb_timeout)
        #transfer.setBuffer(bytes(str(buf.decode("utf-8")).encode("utf-8")))
        transfer.setControl(bmRequestType,bRequest,wValue,wIndex,buf,callback,cmp,usb_timeout)

        
        y = transfer.submit()
        preserved = {}


        
        while transfer.getUserData() == 0 and self.ctx.handleEventsTimeoutCompleted(tv=timeout/1000,completed=transfer.getUserData()) == 0:

                if transfer.getUserData() == 0:

                    preserved["req"] = copy.deepcopy(bytearray(transfer.getBuffer()[:transfer.getActualLength()]))
                    preserved["status"] = copy.deepcopy(transfer.getStatus())
                if transfer.getUserData() == 0:
                    #transfer.cancel()
                    usb1.libusb1.libusb_cancel_transfer(transfer.libr)


        if transfer.getUserData() != 0:
            #pass # deal with completed !=0 shit here

            if (bmRequestType & usb1.libusb1.USB_ENDPOINT_DIR_MASK) == 0x80:
                req = bytearray(transfer.getBuffer()[:transfer.getActualLength()])

                #data = transfer.getBuffer()[:transfer.getActualLength()]
            sz = transfer.getActualLength()
            if transfer.getStatus() == 0:
                ret = "ok"
            elif transfer.getStatus() == 4:
                ret = "stall"
            else:
                print(transfer.getStatus())
                ret = "error"
        usb1.libusb1.libusb_free_transfer(transfer.libr)

        return objects.model(["ret","req","sz","preserved","bool"])(ret,req,sz,preserved,transfer.getUserData()!=0)
    def async_no_data_control_transfer(self,bmRequestType, bRequest, wValue, wIndex, wlen, timeout=0,callback=None):
        if wlen == 0:
            return self.async_control_transfer(bmRequestType, bRequest, wValue, wIndex, "",0, timeout,callback)
        else:
            data = wlen*'\0'
            return self.async_control_transfer(bmRequestType, bRequest, wValue, wIndex, data,wlen, timeout,callback)


    def control_transfer(self,bmRequestType, bRequest, wValue, wIndex, data,wlen, timeout=None):
        if timeout == None:
            timeout = usb_timeout
        ret = None
        sz = wlen
        req = None
        e = None
        
        try:
            ret = self.handle._controlTransfer(bmRequestType,bRequest,wValue,wIndex,data,wlen,timeout)
            if type(ret) != int:
                req = ret
                sz = 0
            else:
                sz = ret
        except usb1.USBError as e:
            e = str(e).lower()
            
            if "-9" in e:
                ret = "stall"
            elif "-12" in e:
                pass # add other conditions l8r
            else:
                ret = "error"
        if e == None:
            ret = "ok"
        return objects.model(["ret","req","sz"])(ret,req,sz)
    def no_data_transfer(self,bmRequestType, bRequest, wValue, wIndex, data, timeout=None):
        if data == 0:
            return self.control_transfer(bmRequestType,bRequest,wValue,wIndex,"",0,timeout)
        else:
            data = '\0'*data
            return self.control_transfer(bmRequestType,bRequest,wValue,wIndex,data,len(data),timeout)
    def wait_usb_handle(self,cb=None,args=[]): # unused for now (could be reason why fail)
        handle = usb1.libusb1.libusb_open_device_with_vid_pid(self.handle.libr,0x5AC,0x1227)
        if handle != None:
            if handle.setConfiguration(1) == 0 and (cb == None or cb(args) == True):
                return True
            handle.close()
            time.sleep(usb_timeout/1000)
            return False
    def reset_usb_handle(self):
        usb1.libusb1.libusb_reset_device(self.handle.libr)
usb = iosb(None,None)