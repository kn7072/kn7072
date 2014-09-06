import time
from os import system
from PyAutoItPy import AutoItX, WinHandle, WinState, MB_Flags

#Создаем экземпляр AutoItX
Automat=AutoItX()
#Это заголовок для поиска окна в формате AutoIt
Title2='[CLASS:Notepad]'
Title = '[CLASS:WindowsForms10.Window.8.app.0.245fb7_r11_ad1]'
Title3 = '[HANDLE:0x0001033E]' #['Handle:0x0003059c']
#Это идентификатор контрола в формате AutoIt
Control='[CLASS:WindowsForms10.BUTTON.app.0.245fb7_r11_ad1; INSTANCE:5]'
Control2='[CLASS:Edit; INSTANCE:1]'
Control3=['Handle:0x00020576']
#Ну и пока пустой Handle
Handle=None
#Ждем появления окна, вдруг еще не открылось
Opened=Automat.WinWait(Title,1)
Handle=WinHandle(Automat.WinGetHandle(Title))
print(Opened, Handle)
u = Automat.WinActivate(Handle)
foc = Automat.ControlFocus(Handle,Control)
print(foc)
text = Automat.ControlGetText(Handle,Control)
#Automat.ControlSetText(Handle, Control, 'ee')
r = Automat.ControlClick(Handle,Control, X=1, Y=1) # Mouse , Text='Go'
time.sleep(2)
get_focus = Automat.ControlGetFocus(Title3)
Automat.ControlShow(Handle,Control)
#Automat.ControlSend(Handle,Control,String="FF")
a = Automat.Send('{F5}',Flag=1)
time.sleep(1)
Automat.Send('{F5}',Flag=0)
time.sleep(1)
Automat.Send('{F5}')
print()