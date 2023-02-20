from pyNumatoGPIO.Device import Device, Channel

gpioManager = Device('COM13')
gpioManager.Connect()
print(f"Version: {gpioManager.Version}")
print(f"Channels number: {len(gpioManager.Channels)}")
channel10 = gpioManager.Channels[10]
channel10.IsOutput = True
print(f"Channel 10 status: {'on' if channel10.Status else 'off'}")
channel10.Status = True
print(f"Channel 10 status: {'on' if channel10.Status else 'off'}")
channel10.Status = False
print(f"Channel 10 status: {'on' if channel10.Status else 'off'}")
channel10.IsOutput = False
print(f"Channel 10 status: {'on' if channel10.Status else 'off'}")
print(f"Channel 10 ADC value: {channel10.Voltage}")