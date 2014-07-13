# -*- coding: utf-8 -*-
import os, re
import subprocess
import wmi

def SysInfo():
    values  = {}
    response = subprocess.Popen('systeminfo', stdout=subprocess.PIPE)
    response = response.communicate()[0]  # Получаем ответ на запрос
    #response = response.decode("UTF-8")
    # cache   = os.popen("SYSTEMINFO")
    # source  = cache.read().decode("windows-1251")
    # sysOpts = ["Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer", "System Model", "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory", "Available Physical Memory", "Logon Server"]

    c = wmi.WMI()
    systeminfo = c.Win32_OperatingSystem()[0]#Win32_ComputerSystem()[0]
    if str(systeminfo.OSLanguage)=='1049':pass
    pass

if __name__ == "__main__":
    x = SysInfo()
    print (x)