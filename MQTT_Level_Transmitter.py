from pymodbus.client.serial import ModbusSerialClient
import asyncio
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import ModbusRtuFramer
import time
import random
import paho.mqtt.client as mqtt

class modbus:
    def __init__(self, port,timeout,baudrate,bytesize,parity,stopbits):
        #modbus0=modbus("/dev/ttyUSB0",10,9600,"N",1,8)
        self.port=port
        self.framer=ModbusRtuFramer
        self.timeout=timeout
        self.baudrate=baudrate
        self.bytesize=bytesize
        self.parity=parity
        self.stopbits=stopbits
        
        self.client = ModbusSerialClient(self.port,self.framer,self.baudrate,self.bytesize,self.parity,self.stopbits,)
        #self.client.connect()
        #print("conectado al hmi")
        # test client is connected
    
    def leer(self,num_registros,esclavo):
        try:
            self.rr =self.client.read_holding_registers(0, num_registros, slave=esclavo)
        
        except Exception as exc:
            print(f"Error: {exc}")
            
        if self.rr.isError():
            print(f"Received Modbus library error({self.rr})")
        elif isinstance(self.rr, ExceptionResponse):
            print(f"Received Modbus library exception ({self.rr})")
        else:
            return self.rr.registers
        
    def escribir_register(self,registro,valor,esclavo):
        try:
            self.client.write_register(registro,valor, esclavo)
        except Exception as exc:
            print(f"Error de comunicación Modbus: {exc}")
    def escribir_coil(self,coil,valor,esclavo):
        try:
            self.client.write_coil(self,coil,valor,esclavo)
        except Exception as exc:
            print(f"Error de comunicacion modbus:{exc}")
      
hostname = "192.168.1.110"
broker_port = 1883
topic = "testTopic"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(hostname, broker_port)
    return client


# Programa Principal

try:
    
    connection = modbus("/dev/ttyUSB0",10,9600,8,"N",1)
    client = connect_mqtt()

    while True:

        # 4 -> Level in cm
        registers = connection.leer(num_registros = 20, esclavo = 1)
        water_level = registers[4]
        print(registers)

        client.loop_start()
        message = str(water_level)
        result = client.publish(topic, message)
        status = result[0]

        if status == 0:
            print(f"Send {message} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(2)
        client.loop_stop()
        # print(f"El nivel es de {registers[4]} cm")  

except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
