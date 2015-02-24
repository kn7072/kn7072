for x in range(10):
    try:
        if x > 5 :
            raise Exception
        print(x)
    except:
        print(str(x)+"xxx")
file_to_save = r'D:\git_hub_new\kn7072\chart\DRIVERS\alienware_laptops\alienware-m14x\\xxx.txt'
with open(file_to_save, encoding='utf-8', mode='w') as f:
    pass