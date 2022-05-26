from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass
# Если вы будете создавать APK файл, то раскомментируйте строки ниже
# Они закомментированы для корректного отображения на ПК
#BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
#BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
#BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
#UUID = autoclass('java.util.UUID')

# Соединение HC-05:
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
        # Для входа в систему EDR
        self.recv_stream, self.send_stream=None,None
        # Графический интерфейс
        Layout=BoxLayout(orientation='vertical',spacing=20,padding=(0,20))
        self.Haut_Layout=GridLayout(cols=2, size_hint=(0.6,0.1),pos_hint={'x':.05, 'y':.1})
        self.orientation='veritcal' # Максимальное количество столбцов
        
        # Добавляем в главное окно
        Layout.add_widget(self.Haut_Layout)
        
        self.BoutonConnect=Button(text='Connection')
        self.BoutonConnect.bind(on_press=self.connect)
        # Добавляем кнопку на дисплее
        self.Haut_Layout.add_widget(self.BoutonConnect)
                
        self.BoutonConnect1=Button(text='Line')
        self.BoutonConnect1.size_hint=(0.8, 0.2)
        self.BoutonConnect1.pos_hint={'x':.5, 'y':.5}
        self.BoutonConnect1.bind(on_press=self.send)
        self.BoutonConnect1.id='6'
        # Добавляем кнопку на дисплее
        self.Haut_Layout.add_widget(self.BoutonConnect1)
        
        self.Bas_Layout=GridLayout(cols=3, spacing=10, size_hint=(0.9, 0.9),pos_hint={'x':.05, 'y':.1})

        # Добавляем в главное окно
        Layout.add_widget(self.Bas_Layout)
        
        # Создаем кнопку
        self.Bouton1=Button()
        # 1 цвет фона
        self.Bouton1.background_color=[0,0,0,0]
        # Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton1)
       
        # Создаем кнопку
        self.Bouton2=Button()
        
        self.Bouton2.background_normal="images/go1.png"   
        self.Bouton2.background_down="images/go.png"           
        self.Bouton2.bind(on_press=self.send)
        self.Bouton2.id='1'
        # Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton2)
        
        self.Bouton3=Button(text="STOP", font_size=40)
        self.Bouton3.color = (1, 0, 0, 1)
        self.Bouton3.background_color=[0.3,0.3,0.3,0.3]
        
        self.Bouton3.bind(on_press=self.send)
        self.Bouton3.id='3'
        self.Bas_Layout.add_widget(self.Bouton3)
        
        self.Bouton4=Button()
        self.Bouton4.background_down="images/left.png"  
        self.Bouton4.background_normal="images/left1.png"  
        self.Bouton4.bind(on_press=self.send)
        self.Bouton4.id='4'
        # Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton4)

        self.Bouton5=Button()
        self.Bouton5.background_down="images/back.png"  
        self.Bouton5.background_normal="images/back1.png"  
        self.Bouton5.bind(on_press=self.send)
        self.Bouton5.id='2'
        # Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton5)
        
        self.Bouton6=Button()
        self.Bouton6.background_down="images/rigth.png"  
        self.Bouton6.background_normal="images/rigth1.png"  
        self.Bouton6.bind(on_press=self.send)
        self.Bouton6.id='5'
        # Добавляем в основное окно
        self.Bas_Layout.add_widget(self.Bouton6)
        
        return Layout
 
    def connect(self,instance):
        try:
            self.recv_stream, self.send_stream = get_socket_stream("HC-05")
        except:
            instance.background_color=[1,0,0,1]
        if self.send_stream!=None:
            instance.background_color=[0,1,0,1]
            instance.text="Connected"
        else:
            instance.background_color=[1,0,0,1]
            instance.text="No connection"
 
    def send(self, instance):
        if self.send_stream!=None:
            self.send_stream.write(int(instance.id))
            self.send_stream.flush()
 
if __name__ == '__main__':
    Application().run()