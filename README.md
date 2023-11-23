# pyNumatoGPIO

> **⚠️ Warning ⚠️**
>
> Disclaimer: The author cannot be hold responsible for any damage caused by the use of pyNumatoGPIO

An abstraction library to connect to Numato GPIO devices. This library behaves as a driver, converting commands to serial communication messages toward Numato GPIO devices.

## Device object

This object represent a physical Numato GPIO device. It is intantiate using the serial port address. A couple of methods (i.e., ```Connect``` and ```Disconnect```) and a property (i.e., ```IsConnected```) manage connection/disconnection procedures.

Methods to sent raw string commands to the GPIO device (i.e., ```Read```, ```Write```, and ```Query```) are public. But their use is up to pyNumatoGPIO user.

```Device``` also defines a list of ```Channel``` objects that represent physical GPIO channel accessible to the user.

## Channel object

> **Still in development**
>
> While documented in Numato GPIO manuals, setting a channel as an input has not been achieved yet. So, channels are only digital outputs.
>
> And the same is true for analog reading.

Digital output state can be set with the help of the ```State``` property of ```Channel```.