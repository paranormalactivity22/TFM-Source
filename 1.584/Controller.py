import time
import os

def main():
    data = os.system("Start.py")
    if data == 1:
        time.sleep(5)
        os.system("cls")
        main()
    """elif data in [5,1280]:
        print "[INFO] Error!"
        raw_input("")
    elif data in [11,2816]:
        print "[ERROR] There is error [10]"
        time.sleep(1)
        print "[ERROR] There is error [9]"
        time.sleep(1)
        print "[ERROR] There is error [8]"
        time.sleep(1)
        print "[ERROR] There is error [7]"
        time.sleep(1)
        print "[ERROR] There is error [6]"
        time.sleep(1)
        print "[ERROR] There is error [5]"
        time.sleep(1)
        print "[ERROR] There is error [4]"
        time.sleep(1)
        print "[ERROR] There is error [3]"
        time.sleep(1)
        print "[ERROR] There is error [2]"
        time.sleep(1)
        print "[ERROR] There is error [1]"
        time.sleep(1)
        os.system("cls")
        main()
    else:
        print "[FairyMice BOT] Error"
        time.sleep(3)
        os.system("cls")
        main()"""

if __name__=="__main__":
    main()
