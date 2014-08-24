import time
from os import system
from PyAutoItPy import AutoItX, WinHandle, WinState, MB_Flags

#��������� ������� ��������� ���������
CallRes=system('start notepad')
#���� ��������, �������.
if CallRes!=0:
    print('���������� ��������� �������!')
    exit(CallRes)

print ('������� �������')
#������� ��������� AutoItX
Automat=AutoItX()
#��� ��������� ��� ������ ���� � ������� AutoIt
Title='[CLASS:Notepad]'
#��� ������������� �������� � ������� AutoIt
Control='[CLASS:Edit; INSTANCE:1]'
#�� � ���� ������ Handle
Handle=None
#���� ��������� ����, ����� ��� �� ���������
Opened=Automat.WinWait(Title,5)
#�������, ���� �� ��������� �������� ��������.
if not Opened:
    print('���-�� ������� ��������... ��������, ����� �������!')
    exit(-1)
#���� ��������� - �������� Handle, ����� �������� � ��������� ������ �����.
Handle=WinHandle(Automat.WinGetHandle(Title))
#�������, ���� �� ������� �������� Handle ����.
if not Handle:
    print('���������� �������� Handle ��������!')
    exit(-1)
#����, ������� �����, ��� Handle �������, ������� Handle, �
print ('Handle ���� ��������: {}'.format(Handle))
#�������� ��������� ����, ��� �� ��������� ���.
State=WinState(Automat.WinGetState(Handle))
print ('��������� ���� ��������: {} {}'.format(State.StateNum, State.StateString))
#���������� ��������� � ������ ���� ��������
NotepadRect=Automat.WinGetPos(Handle)
#���������� ����, ����� ��������� ������� ����� �� ���������
Automat.WinActivate(Handle)
#�� ������ �� ������ ������ ���������� ����� ����� � ������ �������.
Automat.ControlFocus(Handle,Control)
#���� �������
time.sleep(1)
#�������� "������!".
Automat.ControlSetText(Handle, Control, '������!')
#������ �����
time.sleep(1)
#������ �������� ��� �� � ����������
Automat.Send('{END}')
Automat.Send('{BACKSPACE}',7)
#���� ��������
time.sleep(1)
#������ �������� ���� � ���������� ���� "��, ��������!"
Automat.ControlSend(Handle, Control, '�������� ������� ����{!}')
#�������� � ����
time.sleep(1)
#��������� ����� � ������������� ����.
for i in range(254,0,-1):
    Automat.WinSetTrans(Handle, i)
    time.sleep(0.005)
#������������� ����
Automat.WinMove(Handle, 100, 100, 350, 75)
#������� ����
time.sleep(1)
#������� �� ���� �����������
for i in range(1,256):
    Automat.WinSetTrans(Handle, i)
    time.sleep(0.005)
#��������� ����������� �����������
time.sleep(1)
#� ������ - ������� ����� � ���� "��� � ������". � ���� ������ - �������, � ���� ���� - ������. ���� �������� ���� �� ��������:)
#��� ������ ���������� ����� ����� �������������.
Interval=1
#���������� ����� ������ ������.
Start=time.clock()
#������ ����� ��������� ������������� (����� 10 ������)
Finish=Start+10
#������!
while Finish-Start>=0:
    #���������� ������(�������) � ��������� �����.
    Automat.WinMove(Handle,500,100)
    #���������� ����(������) � ����� ������.
    Automat.MouseMove(100, 100)
    #�������� ����-���� � ���� "�������".
    time.sleep(Interval)
    #� ��� ��� ��� ����.
    Automat.WinMove(Handle,500,500)
    Automat.MouseMove(500, 100)
    time.sleep(Interval)
    Automat.WinMove(Handle,100,500)
    Automat.MouseMove(500, 500)
    time.sleep(Interval)
    Automat.WinMove(Handle,100,100)
    Automat.MouseMove(100, 500)
    time.sleep(Interval)
    #������� �� ����
    Start=time.clock()
#��! ������ ��������, ����������!
time.sleep(1)
#������ ������ ������� �� �����.
Automat.WinMove(Handle, NotepadRect.X, NotepadRect.Y, NotepadRect.WIDTH, NotepadRect.HEIGHT)
#� ������� ��� ����������.
Automat.ControlSetText(Handle, Control, '')
#������� ��� ���������.
State.SetState(Automat.WinGetState(Handle))
#� ������� ����� ������� ����� MessageBox.
Automat.MsgBox(
               '��������',
               '���! ���� ��������!\n������� �� ����� ���������!\n��� �� �������� ���� �������� ���������:\n{}\n{}'.format(State.StateNum, State.StateString),
               MB_Flags.MB_ICONWARNING|MB_Flags.MB_OK|MB_Flags.MB_SYSTEMMODAL
               )
#���, ������������� ��������, �������! ��������� �������.
Automat.WinClose(Handle)