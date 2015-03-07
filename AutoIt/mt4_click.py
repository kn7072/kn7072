import time
from os import system
from PyAutoItPy import AutoItX, WinHandle, WinState, MB_Flags

#Создаем экземпляр AutoItX
Automat=AutoItX()
#Это заголовок для поиска окна в формате AutoIt
Title2='[CLASS:Notepad]'
Title = '[CLASS:#32770]'
Title3 = '[HANDLE:0x0001033E]' #['Handle:0x0003059c']
#Это идентификатор контрола в формате AutoIt
Control_btn_buy='[CLASS:Button; INSTANCE:2]' # buy
Control_btn_sell='[CLASS:Button; INSTANCE:1]' # sell
Control_takeprofit_inp = '[CLASS:Edit; INSTANCE:3]' # takeprofit
Control_stoploss_inp = '[CLASS:Edit; INSTANCE:2]' # stoploss
Control2='[CLASS:Edit; INSTANCE:1]'
Control3=['Handle:0x0002047C']

Handle=None
Opened=Automat.WinWait(Title,1)
Handle=WinHandle(Automat.WinGetHandle(Title))
#Automat.ControlSend(Handle,Control,"{ENTER}")
#Automat.Send('{F5}',Flag=1)

res = Automat.ControlSetText(Handle,Control_takeprofit_inp,"1.2975") # утановили тейк профит
Automat.ControlClick(Handle,Control_btn_buy, X=1, Y=1)  # ControlMouseClick  10, 17
print(Opened, Handle)
u = Automat.WinActivate(Handle)  # True
foc = Automat.ControlFocus(Handle,Control)