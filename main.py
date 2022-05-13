from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

#Соединение HC-05:
def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    for device in paired_devices:
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    return recv_stream, send_stream
 
class Application(App):
    def build(self):
        #Для входа в систему EDR
        self.recv_stream, self.send_stream=None,None
        #Графический интерфейс
        Layout=BoxLayout(orientation='vertical',spacing=20,padding=(0,20))
        self.Haut_Layout=GridLayout(cols=1,size_hint=(0.3,0.3),pos_hint={'x':.1, 'y':.1})
        self.orientation='vertical' #Максимальное количество столбцов
        
        #Добавляем в главное окно
        Layout.add_widget(self.Haut_Layout)
        
        self.BoutonConnect=Button(text='Соединение')
        self.BoutonConnect.bind(on_press=self.connect)
        #Добавляем кнопку на дисплее
        self.Haut_Layout.add_widget(self.BoutonConnect)
        
        
        self.Bas_Layout=GridLayout(cols=3,size_hint=(0.8,0.7),pos_hint={'x':.1, 'y':.1},spacing=20)
        self.orientation='horizontal' #Максимальное количество столбцов
        self.spacing=8 #Пространство между объектами
        self.padding=30 #Внутренние поля макета
        
        #Добавляем в главное окно
        Layout.add_widget(self.Bas_Layout)
        
        #Создаем кнопку
        self.Bouton1=Button(text='Вперед')
        #Задаем размер в процентах
        self.Bouton1.size_hint=(0.5,0.5)
        #Позиция
        self.Bouton1.pos_hint={0.5: 0.5}
        #1 цвет фона
        #self.Bouton1.background_normal="go.png"
        self.Bouton1.bind(on_press=self.send)
        self.Bouton1.id='1'
        #Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton1)
        
        #Создаем кнопку
        self.Bouton2=Button(text='Назад')
        #Задаем размер в процентах
        self.Bouton2.size_hint=(0.5,0.5)
        #Позиция
        self.Bouton2.pos_hint={0.6: 0.6}
        #Цвет фона
        #self.Bouton2.background_normal="back.png"
        self.Bouton2.bind(on_press=self.send)
        self.Bouton2.id='2'
        #Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton2)
        
         
        self.Bouton3=Button(text='Стоп')
        self.Bouton3.size_hint=(0.5,0.5)
        self.Bouton3.pos_hint={0.9: 0.9}
        #self.Bouton3.background_normal="stop.png"
        self.Bouton3.bind(on_press=self.send)
        self.Bouton3.id='3'
        self.Bas_Layout.add_widget(self.Bouton3)
        
        
        return Layout
 
    def connect(self,instance):
        try:
            self.recv_stream, self.send_stream = get_socket_stream('HC-05')
        except:
            instance.background_color=[1,0,0,1]
        if self.send_stream!=None:
            instance.background_color=[0,1,0,1]
            instance.text="Соединение установлено"
        #else:
        #    instance.background_color=[1,0,0,1]
        #    instance.text="Соединение не установлено"
 
    def send(self, instance):
        if self.send_stream!=None:
            self.send_stream.write(int(instance.id))
            self.send_stream.flush()
 
if __name__ == '__main__':
    Application().run()