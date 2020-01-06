import gc
gc.collect()

from microApp import Gateway

####################################
"""
Пример инициализации микро веб-сервиса
для шлюза.
Функция writeData нужна для записи данных
в память. Функция getData нужна для чтения
данных из памяти. В данном примере данные 
записываются просто в переменные.
"""

# Частота сбора данных
frequency = 30 # sec
# Список датчиков
clients = []

def writeData(freq, add_client, remove_client):
  """
  Функция записи данных. Должна иметь 3 аргумента:
    1) Частота опроса датчиков
    2) Новый датчик добавляемый в список
    3) Датчик удаляемый из списка
  """
  global frequency, clients
  print("New frequency:", freq)
  frequency = freq
  if add_client:
  	print("<add client '{}'>".format(add_client))
  	clients.append(add_client)
  if remove_client:
  	print("<remove client '{}'>".format(remove_client))
	clients.remove(remove_client)
  
def getData():
  """
  Функция чтения данных. Должна возвращать 2 значения:
    1) Частота опроса датчиков
    2) Список адресов датчиков в памяти
  """
  global frequency, clients
  return frequency, clients
  
# ssid точки WiFi 
ssid = 'Gateway'
# Пароль к точке WiFi 
password = 'password1'
# Экземпляр микро веб-сервиса
server = Gateway()
# Запуск точки WiFi 
server.start_wlan(ssid, password)
# Запуск микро веб-сервиса 
server.start_app(writeData, getData)

####################################

import time

while 1:
  print("Frequency:", frequency)
  print("Clients:", clients)
  time.sleep(10)
