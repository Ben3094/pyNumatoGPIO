from serial import Serial

class Channel:
    __parentDevice__ = None
    __address__: int = None
    def __init__(self, parentDevice, address: int):
        self.__parentDevice__ = parentDevice
        self.__address__ = address

    @property
    def Address(self) -> int:
        return self.__address__
    BS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def _to_base(n, b): 
        if not n: return "0"
        return Channel._to_base(n//b, b).lstrip("0") + Channel.BS[n%b]
    @property
    def __NumatoAddress__(self) -> str:
        return Channel._to_base(self.__address__, len(Channel.BS))

    # @property
    # def IsOutput(self) -> bool:
    #     return self.__parentDevice__.__getChannelsDirection__()[self.__address__]
    # @IsOutput.setter
    # def IsOutput(self, value: bool) -> bool:
    #     if value != self.IsOutput:
    #         self.__parentDevice__.Write(f"gpio {'clear' if value else 'get'} {self.__NumatoAddress__}")
    #         # self.__parentDevice__.Write("gpio iomask {:0>8X}".format(1 << self.__address__))
    #         # self.__parentDevice__.Write(f"gpio iodir {'FFFFFFFF' if value else '00000000'}")
    #     return self.IsOutput

    __lastSetStatus__: bool = False
    @property
    def Status(self) -> bool:
        # if self.IsOutput: 
        return self.__lastSetStatus__
        # else:
        #     return self.__parentDevice__.__getChannelsStatus__()[self.__address__]
    @Status.setter
    def Status(self, value: bool) -> bool:
        if value != self.Status:
            # if self.IsOutput:
            self.__parentDevice__.Write(f"gpio {'set' if value else 'clear'} {self.__NumatoAddress__}")
            self.__lastSetStatus__ = value
            # else:
            #     raise Exception("Impossible to set status when not output")
        return self.Status
    
    VDD = 5 # V
    VDD_CODE = 1024
    @property
    def Voltage(self) -> float:
        if not self.IsOutput:
            return self.__parentDevice__.Query(f"adc read {self.__NumatoAddress__}") / Channel.VDD_CODE * Channel.VDD
        else:
            raise Exception("Impossible to read ADC when not output")

class Device:
    __serialPortAddress__: str = None
    __serialPort__: Serial = None
    DEFAULT_BAUDRATE = 19200
    DEFAULT_TIMEOUT = 1
    END_OF_LINE = b'\r'
    NEW_LINE = b'\n'
    END_OF_RECEPTION = b'\n\r>'

    __channels__ = dict()

    def __init__(self, serialPortAddress: str):
        self.__serialPortAddress__ = serialPortAddress
        self.__serialPort__ = Serial(baudrate=Device.DEFAULT_BAUDRATE, timeout=Device.DEFAULT_TIMEOUT)
        
    def Write(self, value: str):
        if self.IsConnected:
            self.__serialPort__.read_all()
            value = value.encode("ascii")
            self.__serialPort__.write(value + Device.END_OF_LINE)
            if value + Device.NEW_LINE != self.__serialPort__.readline():
                raise Exception("Unsuccessfully executed command")
        else:
            raise Exception("Device is not connected")
        
    def Read(self) -> bytes:
        if self.IsConnected:
            return self.__serialPort__.read_all().lstrip(Device.END_OF_LINE).rstrip(Device.END_OF_RECEPTION).decode()
        else:
            raise Exception("Device is not connected")

    def Query(self, value: str) -> bytes:
        self.Write(value)
        return self.Read()

    @property
    def IsConnected(self) -> bool:
        return self.__serialPort__.is_open
    def Connect(self) -> bool:
        if not self.IsConnected:
            self.__serialPort__.port = self.__serialPortAddress__
            self.__serialPort__.open()
            for address in range(self.__getChannelsLength__()):
                self.__channels__[address] = Channel(self, address)
        return self.IsConnected
    def Disconnect(self) -> bool:
        if self.IsConnected:
            self.__channels__ = dict()
            self.__serialPort__.close()
        return self.IsConnected

    @property
    def SerialPortAddress(self) -> str:
        return self.__serialPortAddress__
    @SerialPortAddress.setter
    def SerialPortAddress(self, value: str) -> str:
        if value != self.SerialPortAddress:
            self.Disconnect()
            self.__serialPortAddress__ = value
            self.Connect()
        return self.SerialPortAddress

    @property
    def Version(self) -> bytes:
        return self.Query('ver')
        
    @property
    def ID(self) -> str:
        return self.Query('id get')
    @ID.setter
    def ID(self, value: str) -> str:
        self.Write(f"id set {value}")
        if self.ID != value:
            raise Exception("Error while setting the new ID")
        else:
            return value
    
    INFO_DIRECTION_HEADER = "GPIO Power-On Direction : "
    INFO_STATUS_HEADER = "GPIO Power-On Status : "
    def __getChannelsLength__(self):
        directions = self.Query('info').splitlines()[0].removeprefix(Device.INFO_DIRECTION_HEADER)
        return len(directions) * 4
    def __getChannelsDirection__(self) -> dict[int, bool]:
        channelsDirection = dict()
        directions = self.Query('info').splitlines()[0].removeprefix(Device.INFO_DIRECTION_HEADER)
        channelsLength = len(directions) * 4
        directions = int(directions, 16)
        for address in range(channelsLength):
            channelsDirection[address] = bool((directions >> address) & 1)
        return channelsDirection
    def __getChannelsStatus__(self) -> dict[int, bool]:
        channelsStatus = dict()
        statuses = self.Query('info').splitlines()[2].removeprefix(Device.INFO_STATUS_HEADER)
        channelsLength = len(statuses) * 4
        statuses = int(statuses, 16)
        for address in range(channelsLength):
            channelsStatus[address] = bool((statuses >> address) & 1)
        return channelsStatus
    @property
    def Channels(self) -> dict[int, Channel]:
        return self.__channels__