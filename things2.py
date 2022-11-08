from machine import Pin, UART, I2C, ADC
import utime, time
import math

buz = Pin(4, Pin.OUT)    # 13 number in is Output
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

buz.value(0)
uart0 = machine.UART(0, baudrate=115200)
myHOST = 'api.thingspeak.com'
myPORT = '80'
myAPI = '50JN4A08ERYKEEIW'
def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res
def Connect_WiFi(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
    print()
def Send_AT_Cmd(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
    print()    
def Wait_ESP_Rsp(uart=uart0, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp) 
def wif_init():
  print ('Starting connection to ESP8266...')
  Send_AT_Cmd('AT\r\n')          #Test AT startup
  Send_AT_Cmd('AT+GMR\r\n')      #Check version information
  Send_AT_Cmd('AT+CIPSERVER=0\r\n')      #Check version information
  Send_AT_Cmd('AT+RST\r\n')      #Check version information
  Send_AT_Cmd('AT+RESTORE\r\n')  #Restore Factory Default Settings
  Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
  Send_AT_Cmd('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
  Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again
  Connect_WiFi('AT+CWJAP="POCO X3 Pro","pocox3pro"\r\n', timeout=5000) #Connect to AP
  Send_AT_Cmd('AT+CIFSR\r\n',timeout=5000)    #Obtain the Local IP Address
  Send_AT_Cmd('AT+CIPMUX=1\r\n')    #Obtain the Local IP Address
  utime.sleep(1.0)
wif_init()
kk=0
def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
   return distance
while True:
    distance=ultra()
    utime.sleep(1)
    if(distance<6):
        print ('Activated')
        buz.value(1)
        sendData = 'GET /update?api_key='+ myAPI +'&field1='+str(distance)
        Send_AT_Cmd('AT+CIPSTART=0,\"TCP\",\"'+ myHOST +'\",'+ myPORT+'\r\n')
        utime.sleep(1.0)
        Send_AT_Cmd('AT+CIPSEND=0,' +str(len(sendData)+4) +'\r\n')
        utime.sleep(1.0)
        Send_AT_Cmd(sendData +'\r\n')
        utime.sleep(4.0)
        Send_AT_Cmd('AT+CIPCLOSE=0'+'\r\n') # once file sent, close connection
        utime.sleep(4.0)
        print ('Data send to thing speak')
        
    time.sleep(2)


