import gc
gc.collect()

from microApp import Client

####################################
"""
Пример инициализации микро веб-сервиса
для датчика (конечного клиента).
Функция writeData нужна для записи данных
в память. Функция getData нужна для чтения
данных из памяти. В данном примере данные 
записываются просто в переменную.
"""

# Адрес датчика
client = ''

def writeData(client_addr):
  """
  Функция записи данных. Должна иметь 1 аргумент (адрес датчика).
  """
  global client
  client = client_addr
  print(client)
  
def getData():
  """
  Функция чтения данных. Должна возвращать 1 значение (адрес датчика)
  """
  global client
  return client
  
# ssid точки WiFi 
ssid = 'Client'
# Пароль к точке WiFi 
password = 'password1'
# Экземпляр микро веб-сервиса
server = Client()
# Запуск точки WiFi 
server.start_wlan(ssid, password)
# Запуск микро веб-сервиса
server.start_app(writeData, getData)

####################################

import time

while 1:
  print("client: {}".format(client))
  time.sleep(10)
