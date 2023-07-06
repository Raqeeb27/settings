import os
from time import sleep, strftime, localtime
from random import choice
from re import match
from colorama import Fore as f, Style as s

start_time = localtime()
start_hour = int(strftime("%H", start_time))
start_min = int(strftime("%M", start_time))
start_sec = int(strftime("%S", start_time))

torch_state = False
notificationList = ['Say \'SubhanAllah\' X 3',
                    'Say \'Allhamdulillah\' X 3',
                    'Say \'AllahuAkbar\' X 4',
                    'Say \'Laa Ilaaha Illah....\'',
                    'Say \'Subhanallahi Wabihamdihi....\'',
                    'Recite \'3rd Kalima\' (Subhanallahi Walhamdulillahi....)',
                    'Recite \'4th Kalima\' (Laa Ilaaha Illalahu Wahdahu.....)',
                    'Recite \'Surah Ikhlaas\' X 3',
                    'Recite \'Duruud-e-Shareef\'',
                    'Say \'Astagfirullah\' X 3',
                    '\'Allahu Akbar\' while Climbing \'UP\'',
                    '\'SubhanAllah\' while Climbing \'DOWN\'']
allowedPhoneNumberChar = r'^[0-9*+#]+$'

cyan = f.CYAN
light_cyan = f.LIGHTCYAN_EX
yellow = f.YELLOW
red = f.RED
bold = s.BRIGHT
dim, reset = s.DIM, s.RESET_ALL

def mySettings():

    print(f"{yellow}{bold}Choose the following function to perform on your phone :-\n{reset}")
    setting = input(f"{light_cyan}0. Exit         1. Torch on/off         "
                    f"2. Call \n3. Send SMS     4. WIFI on/off     5. Get Random Notifications\n"
                    f"6. Volume adjust\n\n---> {reset}")

    if setting in ['','0','exit'] :
        os.system("clear")
        exit()

    elif setting == '1' :
        global torch_state

        print(f"{yellow}{bold}\n------ TORCH ------\n{reset}")        
        if torch_state :
            os.system("termux-torch off")
            print(f"{bold}Torch is set \'OFF\'\n{reset}")
            torch_state = False
        else:
            os.system("termux-torch on")
            print(f"{bold}Torch is set \'ON\'\n{reset}")
            torch_state = True

    elif setting == '2' :
        while True:
            print(f"{yellow}{bold}\n------ CALL ------\n{reset}")
            phoneNumber = input("Enter Phone Number : ")
            if phoneNumber.count('+') == 1 :
                phoneNumberLength = 13
            else:
                phoneNumberLength = 10

            if phoneNumber in ['0','',' ']:
                print("Call Cancelled.\n")
                break

            if not (len(phoneNumber) in [4,5,phoneNumberLength] and phoneNumber.count('+') in [0,1] 
                    and match(allowedPhoneNumberChar, phoneNumber)):
                print(f"{red}\nInvalid Phone Number. Call not sent.\n{dim}"
                      f"Enter number as '0' if you want to Cancel{reset}")
                continue

            os.system(f"termux-telephony-call {phoneNumber}")
            print(f"\nCalling \'{phoneNumber}\'",end='',flush = True)
            for i in range(7):
                print(".",end = "", flush = True)
                sleep(0.25)
            print("\n")
            exit()

    elif setting == '3' :
        while True:
            try:
                print(f"{yellow}{bold}\n------ Send SMS ------\n{reset}")

                phoneNumber = int(input("Enter Phone Number : "))
                if phoneNumber in [0]:
                    print("SMS Cancelled.\n")
                    break

                if not (len(str(phoneNumber)) in [10]):
                    print(f"{red}\nInvalid Phone Number. SMS not sent.\n{dim}"
                          f"Enter number as '0' if you want to Cancel{reset}")
                    continue

                text = input("\nEnter message : ")
                if text.count(" ") == len(text) or len(text) == 0:
                    print(f"{red}\nEmpty message can't be sent\n{reset}")
                    break

                os.system(f"termux-sms-send -n {phoneNumber} {text}")
                print("\nSending",end = "", flush =True)
                for i in range(7):
                    print(".",end = "", flush = True)
                    sleep(0.25)

                print(f"\n\nMessage \"{text[:32]}\".... is sent to \'{phoneNumber}\'\n")
                break

            except ValueError:
                print(f"{red}\nInvalid Phone Number. SMS not sent.\n{dim}"
                      f"Enter phno. as '0' if you want to Cancel{reset}")

    elif setting == '4' :
        print(f"{yellow}{bold}\n------ WIFI ------{reset}\n")

        wifi_state = input("Enter ON (o) or OFF (f) : ").upper()

        if wifi_state in ['O','0'] :
            os.system("termux-wifi-enable true")
            print("WIFI is set \'ON\'\n")
        elif wifi_state == 'F' :
            os.system("termux-wifi-enable false")
            print("WIFI is set\'OFF\'\n")
        else :
            print(f"{red}{dim}Please enter between \'o\' or \'f\'\n{reset}")

    elif setting == '5' :
        global notificationList, start_hour, start_min

        notificationSound = input("\nPlay Notification sound.... "
                                  f"Phone will be removed from Silent Mode [\'y\' or \'n\'] : ").upper()
        if notificationSound in ['Y', 'YES'] :
            os.system("termux-volume ring 100")
            os.system("termux-volume notification 100")
            print()
        else:
            print("Notification Volume is Unaltered....\n")

        flash = input("Flash on Notification...[\'y\' or \'n\'] : ").upper()
        vibration = input("\nVibrate on Notification.....[\'y\' or \'n\'] : ").upper()

        try:
            notificationDelay = int(input("\nEnter Time Delay for next Notification (in Minutes <= 60) : "))
            if notificationDelay > 60 :
                print(f"{red}{dim}Enter Delay less than hour (60 min)\n{reset}")
                return
            elif notificationDelay <= 0:
                print(f"{red}{dim}\nMinutes should be a Positive Integer Value < \'60\'\n{reset}")
                return

        except ValueError :
            print(f"{red}{dim}\nMinutes should be a Positive Integer Value < \'60\'\n{reset}")
            return

        currentLocalTime = localtime()
        current_hour = int(strftime("%H", currentLocalTime)) 
        current_min = int(strftime("%M", currentLocalTime)) 

        if start_min != current_min:
            start_min = current_min

        print(f"{yellow}{bold}\n------ Getting Random Notification ------{reset}")
        if start_min + notificationDelay > 59:
            current_hour = current_hour + 1
            display_min = start_min + notificationDelay - 60
        else:
            display_min = start_min + notificationDelay
        if display_min < 10:
            print(f"{dim}Next Notification at : --- {current_hour}:0{display_min} ---{reset}")
        else:
            print(f"{dim}Next Notification at : --- {current_hour}:{display_min} ---{reset}")
        print(f"{dim}Press \' ctrl + c \' to Cancel...{reset}\n")

        while True:
            try:
                next_notification_min = start_min + notificationDelay
                randamNotification = choice(notificationList)

                currentLocalTime = localtime()
                current_hour = int(strftime("%H", currentLocalTime))
                current_min = int(strftime("%M", currentLocalTime))
                current_sec = int(strftime("%S", currentLocalTime))            

                if next_notification_min > 59 :
                    next_notification_min = next_notification_min - 60
                    current_hour = current_hour + 1

                if current_min == next_notification_min and current_sec == 0 :
                    os.system(f"termux-notification --content \"{randamNotification}\" ")
                    print(f"\n{randamNotification}\n")

                    if vibration in ['Y', 'YES'] :
                        os.system("termux-vibrate -f -d 1500")
                        pass
                    if flash in ['Y', 'YES'] :
                        os.system("termux-torch on")
                        sleep(0.25)
                        os.system("termux-torch off")

                    start_min = next_notification_min
                    print(f"{yellow}{bold}\n------ Getting Random Notification ------{reset}")
                    if start_min == 0:
                        print(f"{dim}Next Notification at : --- {current_hour - 1}:0{start_min + notificationDelay} ---{reset}")
                    elif start_min + notificationDelay < 10:
                        print(f"{dim}Next Notification at : --- {current_hour}:0{start_min + notificationDelay} ---{reset}")
                    elif start_min + notificationDelay == 60:
                        print(f"{dim}Next Notification at : --- {current_hour + 1}:00 ---{reset}")
                    else:
                        print(f"{dim}Next Notification at : --- {current_hour}:{start_min + notificationDelay} ---{reset}")
                    print(f"{dim}Press \' ctrl + c \' to Cancel...{reset}\n")
                    sleep(notificationDelay * 60 - 3)

            except KeyboardInterrupt:
                print(f"\nNotifications cancelled.\nExiting",end='',flush = True)
                for i in range(5):
                    print(".",end = "", flush = True)
                    sleep(0.2)
                print("\n")
                exit()

    elif setting == '6' :
        def volume_change(vol_name):
            while True:
                print(f"{yellow}{bold}\n------ {vol_name} ------\n{reset}")
                try:
                    volume = input(f"Enter {vol_name} Volume [0 - 100] : ")

                    if volume in ['',' ']:
                        print(f"\n{vol_name} Volume is Unaltered\n")
                        break
                    elif 0 <= int(volume) and int(volume) <= 100:
                        os.system(f'termux-volume {vol_name.lower()} {volume}')
                        print(f"\n{vol_name} Volume is set to {volume}\n")
                        break
                    else:
                        print(f"{red}\nInvalid Volume input. Please enter Integer value between "
                              f"[0 - 100]\n{dim}Just press \'Enter\' to Exit.{reset}")

                except:
                    print(f"{red}\nInvalid Volume input. Please enter Integer value between [0 - 100]\n"
                          f"{dim}Just press \'Enter\' to Exit.{reset}")

        while True :
            print(f"{yellow}{bold}\n------ Volume Adjust ------\n{reset}")

            volume_input = input(f"{cyan}0. Exit       1. System        2. Call        3. Ring\n"
                                 f"4. Music      5. Notification       6. Alarm{reset}\n\n---> ")

            if volume_input in ['',' ','0'] :
                print()
                break
            elif volume_input == '1' :
                volume_change("System")
            elif volume_input == '2' :
                volume_change("Call")
            elif volume_input == '3' :
                volume_change("Ring")
            elif volume_input == '4' :
                volume_change("Music")
            elif volume_input == '5' :
                volume_change("Notification")
            elif volume_input == '6' :
                volume_change("Alarm")
            else :
                print(f"{red}{bold}\nUnrecognised Input{reset}\n{red}{dim}Select any from [1 - 6]{reset}\n")            

    else:
        print(f"{red}{bold}\nUnrecognised Input{reset}\n{red}{dim}Select any from [0 - 5]{reset}\n")


while True:
    os.system("clear")
    mySettings()
    input(f"{dim}Press \'Enter\' to continue.... {reset} ")
