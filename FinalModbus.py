import serial
import random
import time
import os
import requests
#CRC Calculation

def CRCcal(msg) :
    CRC = 0xFFFF
    CRCHi = 0xFF
    CRCLo = 0xFF
    CRCLSB = 0x00
    for i in range(0, len(msg)-2,+1):
        CRC = (CRC ^ msg[i])
        for j in range(0, 8):
            CRCLSB = (CRC & 0x0001);
            CRC = ((CRC >> 1) & 0x7FFF)

            if (CRCLSB == 1):
                CRC = (CRC ^ 0xA001)
    CRCHi = ((CRC >> 8) & 0xFF)
    CRCLo = (CRC & 0xFF)
    return (CRCLo,CRCHi)

#CRC Valdation
def CRCvalid(resp):
    CRC = CRCcal(resp)
    if (CRC[0]==resp[len(resp)-2]) & (CRC[1]==resp[len(resp)-1]):return True
    return False


#Modbus Function Code 03 = Read Holding Registers
def Func03Modbus(slave,start,NumOfPoints):
    #Function 3 request is always 8 bytes
    message = [0 for i in range(8)] 
    Slave_Address = slave
    Function = 3
    Starting_Address = start
    Number_of_Points = NumOfPoints

    #index0 = Slave Address
    message[0] = Slave_Address
    #index1 = Function
    message[1] = Function
    #index2 = Starting Address Hi
    message[2] = ((Starting_Address >> 8)& 0xFF)
    #index3 = Starting Address Lo
    message[3] = (Starting_Address& 0xFF)
    #index4 = Number of Points Hi
    message[4] = ((Number_of_Points >> 8)& 0xFF)
    #index5 = Number of Points Lo
    message[5] = (Number_of_Points& 0xFF)

    #CRC (Cyclical Redundancy Check) Calculation
    CRC = CRCcal(message)
   
    #index6= CRC Lo
    message[len(message) - 2] = CRC[0]#CRCLo
    #index7 = CRC Hi
    message[len(message) - 1] = CRC[1]#CRCHi
   
    if ser.isOpen:       
        ser.write("".join(chr(h) for h in message))
        responseFunc3total = 5 + 2 * Number_of_Points
        reading = ser.read(responseFunc3total)
        response = [0 for i in range(len(reading))]
        for i in range(0, len(reading)):
            response[i] = ord(reading[i])
       
        if len(response)==responseFunc3total:
            CRCok = CRCvalid(response)
            if CRCok & (response[0]==slave) & (response[1]==Function):
                #Byte Count in index 3 = responseFunc3[2]
                #Number of Registers = byte count / 2 = responseFunc3[2] / 2
                registers = ((response[2] / 2)& 0xFF)
                values = [0 for i in range(registers)]
                for i in range(0, len(values)):
                    #Data Hi and Registers1 from Index3
                    values[i] = response[2 * i + 3]
                    #Move to Hi
                    values[i] <<= 8
                    #Data Lo and Registers1 from Index4
                    values[i] += response[2 * i + 4]
                    negatif = values[i]>>15
                    if negatif==1:values[i]=values[i]*-1
                return values
    return ()

#Modbus Function Code 04 = Read Input Registers
def Func04Modbus(slave,start,NumOfPoints):
    #Function 4 request is always 8 bytes
    message = [0 for i in range(8)] 
    Slave_Address = slave
    Function = 4
    Starting_Address = start
    Number_of_Points = NumOfPoints

    #index0 = Slave Address
    message[0] = Slave_Address
    #index1 = Function
    message[1] = Function
    #index2 = Starting Address Hi
    message[2] = ((Starting_Address >> 8)& 0xFF)
    #index3 = Starting Address Lo
    message[3] = (Starting_Address& 0xFF)
    #index4 = Number of Points Hi
    message[4] = ((Number_of_Points >> 8)& 0xFF)
    #index5 = Number of Points Lo
    message[5] = (Number_of_Points& 0xFF)

    #CRC (Cyclical Redundancy Check) Calculation
    CRC = CRCcal(message)
   
    #index6= CRC Lo
    message[len(message) - 2] = CRC[0]#CRCLo
    #index7 = CRC Hi
    message[len(message) - 1] = CRC[1]#CRCHi
   
    if ser.isOpen:       
        ser.write("".join(chr(h) for h in message))
        responseFunc3total = 5 + 2 * Number_of_Points
        reading = ser.read(responseFunc3total)
        response = [0 for i in range(len(reading))]
        for i in range(0, len(reading)):
            response[i] = ord(reading[i])
       
        if len(response)==responseFunc3total:
            CRCok = CRCvalid(response)
            if CRCok & (response[0]==slave) & (response[1]==Function):
                #Byte Count in index 3 = responseFunc3[2]
                #Number of Registers = byte count / 2 = responseFunc3[2] / 2
                registers = ((response[2] / 2)& 0xFF)
                values = [0 for i in range(registers)]
                for i in range(0, len(values)):
                    #Data Hi and Registers1 from Index3
                    values[i] = response[2 * i + 3]
                    #Move to Hi
                    values[i] <<= 8
                    #Data Lo and Registers1 from Index4
                    values[i] += response[2 * i + 4]
                    negatif = values[i]>>15
                    if negatif==1:values[i]=values[i]*-1
                return values
    return ()


#Main Program
#Serial Port 19200,8,N,1
#Serial Open
try:
        ser = serial.Serial(
                port = '/dev/ttyUSB0',
                baudrate = 19200,
                bytesize = serial.EIGHTBITS,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                timeout = 1000
                
        )
except ValuuError :
        print "Port Can not be opened"


print "START"
while 1:       
    #Serial Open Check
    if not ser.isOpen:ser.open()

    #Read of Input Registers
    Slave_id = 1
    count = 0
    Start_address = [0 for i in range(5)]
    Start_address[0] = 151
    Start_address[1] = 200
    Start_address[2] = 221
    Start_address[3] = 256
    Start_address[4] = 350

    Number_of_Registers = [0 for i in range(5)]
    Number_of_Registers[0] = 1
    Number_of_Registers[1] = 5
    Number_of_Registers[2] = 1
    Number_of_Registers[3] = 1
    Number_of_Registers[4] = 7

    ModbusData = [0 for i in range(15)]
    
    for i in range(0,len(Start_address)):
        Func04ArrayValue = Func04Modbus(Slave_id,Start_address[i],Number_of_Registers[i])#slave,start,number of registers

        for j in range(0,len(Func04ArrayValue)):
            ModbusData[count] = Func04ArrayValue[j]
            count = count+1

    if len(ModbusData)>0:
        for i in range(0, len(ModbusData)):
            print "Read of Registers" + str(i) + " = " + str(ModbusData[i])
            
	#url = 'Set API'

	params = {
		'generatorID' : Slave_id,
		'staddress': Start_address,
		'reg1': ModbusData[0],
		'reg2': ModbusData[1],
		'reg3': ModbusData[2],
		'reg4': ModbusData[3],
		'reg5': ModbusData[4],
		'reg6': ModbusData[5],
		'reg7': ModbusData[6],
		'reg8': ModbusData[7],
		'reg9': ModbusData[8],
		'reg10': ModbusData[9],
                'reg11': ModbusData[10],
                'reg12': ModbusData[11],
                'reg13': ModbusData[12],
                'reg14': ModbusData[13],
                'reg15': ModbusData[14],
		'deviceID': '1'
		}
	results = requests.get(url, params = params)
	print results.content
    time.sleep(5)
    os.system('clear')
##    Fill Random Value for Write
##    totalvalue=2
##    val = [0 for i in range(totalvalue)]
##    for i in range(0, len(val)):
##        val[i] = random.randrange(-32767,32767) #Random Valiue from -32767 to max 32767
##
##    #Write of Registers
##    WriteValid = Func16Modbus(1,2,val)#slave,start,array value
##    if WriteValid:
##        for i in range(0, len(val)):
##            print "Write of Registers" + str(i) + " = " + str(val[i])
##
##        print "#################################"
    

    




