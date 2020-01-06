class Client :
  """
  Класс для управления микро веб-сервисом датчика.
  """
  
  # Код странички с формой
  page1 = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Client</title>
    </head>

    <body>
      <form method="POST" action="/post">
        Client addres:<br>
        <input type="text" name="client" placeholder="(обязательно)" value="{}"><br><br>
        
        <input type="submit" value="Submit">
      </form>
    </body>
    </html>
    """
  
  # Код страничик обработчика. На самом деле вообще не важно что здесь, 
  # главное чтоб переменная не была пустой.
  page2 = '<a href="/">Back to settings</a>'

  def start_wlan(self, ssid='Monitor', password='password'):
    """
    Функция активации точки WiFi.
    На вход соответственно принимает ssid и пароль.
    """
    import network
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    ap.active(True)

  def start_app(self, write_func, get_func):
    """
    Функция запуска веб-приложения.
    На вход принимает 2 функции.
    1. Функция записи данных. Должна иметь 1 аргумент (адрес датчика)
    2. Функция чтения данных. Должна возвращать 1 значение (адрес датчика)

    У веб-приложения 2 маршрута:
    1. Форма
    2. Обработчик формы
    Их нельзя объединить из-за особенности библиотеки
    """
    from microWebSrv import MicroWebSrv
    
    # Форма
    @MicroWebSrv.route('/')
    def handlerFuncGet(httpClient, httpResponse):
      httpResponse.WriteResponseOk( headers         = None,
                                    contentType     = "text/html",
                                    contentCharset  = "UTF-8",
                                    content         = self.page1.format(get_func()) )

    # Обработчик формы
    @MicroWebSrv.route('/post', 'POST')
    def post_data(httpClient, httpResponse):
      formData  = httpClient.ReadRequestPostedFormData()
      write_func(formData['client'])
      httpResponse.WriteResponseOk( headers         = None,
                                    contentType     = "text/html",
                                    contentCharset  = "UTF-8",
                                    content         = self.page2 )
    
    # MicroWebSrv.SetNotFoundPageUrl('/')
    mws = MicroWebSrv()
    # Приложение запускается как отдельный поток
    mws.Start(threaded=True)

class Gateway :
  """
  Класс для управления микро веб-сервисом шлюза.
  """
  
  # Код странички с формой
  page1 = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Gateway</title>
    </head>

    <body>
      <form method="POST" action="/post">
        Frequency:<br>
        <input type="text" name="frequency" placeholder="(обязательно)" value="{}"><br>

        Add new client addres:<br>
        <input type="text" name="add_client" placeholder="(опционально)"><br>

        Remove client addres:<br>
        <input type="text" name="remove_client" placeholder="(опционально)"><br><br>
        
        <input type="submit" value="Submit">
      </form><br>
      <p>{}</p>
    </body>
    </html>
    """
  
  # Код страничик обработчика. На самом деле вообще не важно что здесь, 
  # главное чтоб переменная не была пустой.
  page2 = '<a href="/">Back to settings</a>'

  def start_wlan(self, ssid='Monitor', password='password'):
    """
    Функция активации точки WiFi.
    На вход соответственно принимает ssid и пароль.
    """
    import network
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    ap.active(True)

  def start_app(self, write_func, get_func):
    """
    Функция запуска веб-приложения.
    На вход принимает 2 функции.
    1. Функция записи данных. Должна иметь 3 аргумента:
      1) Частота опроса датчиков
      2) Новый датчик добавляемый в список
      3) Датчик удаляемый из списка
    2. Функция чтения данных. Должна возвращать 2 значения:
      1) Частота опроса датчиков
      2) Список адресов датчиков в памяти

    У веб-приложения 2 маршрута:
    1. Форма
    2. Обработчик формы
    Их нельзя объединить из-за особенности библиотеки
    """
    from microWebSrv import MicroWebSrv
    
    # Форма
    @MicroWebSrv.route('/')
    def handlerFuncGet(httpClient, httpResponse):
      frequency, clients = get_func()
      clients_list = 'Clients:<br>'
      for client in clients:
        clients_list += client + '<br>'
      httpResponse.WriteResponseOk( headers         = None,
                                    contentType     = "text/html",
                                    contentCharset  = "UTF-8",
                                    content         = self.page1.format(frequency, clients_list) )

    # Обработчик формы
    @MicroWebSrv.route('/post', 'POST')
    def post_data(httpClient, httpResponse):
      formData  = httpClient.ReadRequestPostedFormData()
      if formData['frequency']:
        try:
          frequency = int(formData['frequency'])
          write_func(frequency, formData['add_client'], formData['remove_client'])
        except:
          pass

      httpResponse.WriteResponseOk( headers         = None,
                                    contentType     = "text/html",
                                    contentCharset  = "UTF-8",
                                    content         = self.page2 )
    
    # MicroWebSrv.SetNotFoundPageUrl('/')
    mws = MicroWebSrv()
    # Приложение запускается как отдельный поток
    mws.Start(threaded=True)
