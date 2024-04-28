import carnellion
from carnellion.iosb import usb
from carnellion.consts import * 
def lanhua():
    ctx = carnellion.USBContext()
    handle = ctx.openByVendorIDAndProductID(0x5AC,0x1227,skip_on_error=True)
    if handle == None:
        print("unfound")
        exit()
    claim = handle.setConfiguration(1)
    print(claim)
    handle.claimInterface(0)
    print(handle.getSerialNumber())
    print(type(handle))
    #handle._controlTransfer()
    #handle._controlTransfer(0x21,4,0,0,0,0,10)
    sid = list(handle.controlRead(0x80,6,256,0,34,1000))[-2]
    usb.async_no_data_control_transfer(0x21,DFU_DNLOAD,0,0,DFU_MAX_TRANSFER_SZ,1000)
lanhua()

