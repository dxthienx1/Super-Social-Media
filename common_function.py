import json
import sys
import os
import re
import shutil
import random
from natsort import natsorted
from datetime import datetime, timedelta, timezone, time as dtime
from time import sleep, time
import threading
import traceback
import winreg
from moviepy.video.fx import Resize as resize, Crop as crop, MirrorX as mirror_x, MultiplySpeed, CrossFadeIn
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, afx, vfx, CompositeVideoClip, ImageClip, ColorClip
from moviepy.audio.AudioClip import CompositeAudioClip
import requests
from unidecode import unidecode
import yt_dlp
import portalocker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import subprocess
import pickle
import uuid
import wmi
import platform
from tkinter import messagebox, filedialog
import customtkinter as ctk
import ctypes
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
import keyboard
import tempfile
import queue
from pathlib import Path
from selenium.webdriver.firefox.service import Service as ff_Service
from selenium.webdriver.firefox.options import Options
import zipfile
from imageio import imwrite
import cv2
import numpy as np
from noise import pnoise2
import copy

serials = {
    '0025_38B2_21C3_22BE.Default string':"2025-08-01", #thai
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28",
    "0000_0000_0000_0000_0026_B738_363E_5915./2XW1YR3/CNCMC0028S04C2/":"2026-01-01",
    "0025_38D2_1104_730B.WZ14MC006S":"2030-01-01",
    "50026B7782A933E5Default string":"2024-12-31",
    "MSQ2341256207069":"2025-01-10",
    "S0TYNEAD201037/8LK3382/CN129634APGGA0/":"2024-12-31",
    "AA000000056000001229/G6NFFS1/CN129611CT0352/":"2025-01-10",
    '9D11026003520Default string':"2025-01-06",
    '0025_38BA_31B0_4376.PTKQT1BNNK5D3K':"2025-01-10",
    'DSMB20A2205734/HZSBQC2/CN1296368R0037/':"2025-01-09",
    'AA000000000000003668CB17891576':"2025-01-10",
    'LDK778R002629/FJCKZ52/CN1296358M000A/':"2025-01-16",
    'SN11R03W18-1I93B23KBJG2916589467376324':"2025-01-29",
    "AA000000000000006941Default string":"2025-01-28",
    "51A907031FEB00027947/7NJBQ72/CN1296364E00F2/":"2025-02-09",
    "gggg":"2025-01-28",
    "gggg":"2025-01-28"
}

already_serial = [
    '50026B7782A933E5Default string',
    'MSQ2341256207069',
    'S0TYNEAD201037/8LK3382/CN129634APGGA0/',
    'AA000000056000001229/G6NFFS1/CN129611CT0352/',
    '9D11026003520Default string',
    '0025_38BA_31B0_4376.PTKQT1BNNK5D3K',
    'DSMB20A2205734/HZSBQC2/CN1296368R0037/',
    'AA000000000000003668CB17891576',
    'LDK778R002629/FJCKZ52/CN1296358M000A/',
    'SN11R03W18-1I93B23KBJG2916589467376324',
    '0025_38B2_21C3_22BE.YX04C6LZ',
    'AA000000000000006941Default string',
    '51A907031FEB00027947/7NJBQ72/CN1296364E00F2/',
    '0026_B768_407B_68E5.BSS-0123456789',
    '0000_0000_0000_0001_00A0_7519_257D_4E36.L415NRCV003LRHMB',
    'gggg',
    'gggg',
    'gggg'
]

ban_serials = []

def get_disk_and_mainboard_serial():
    c = wmi.WMI()
    disk_id = None
    for disk in c.Win32_DiskDrive():
        for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                if logical_disk.DeviceID.lower() == "c:":
                    disk_id = disk.SerialNumber
                    break
            if disk_id:
                break
        if disk_id:
            break
    mainboard_id = None
    for board in c.Win32_BaseBoard():
        mainboard_id = board.SerialNumber
        break
    if disk_id and mainboard_id:
        return f"{disk_id}{mainboard_id}"
    return "Không tìm thấy mã máy"

is_dev_enviroment = True
def get_current_dir():
    """Lấy thư mục đang chạy tệp thực thi"""
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
        is_dev_enviroment = False
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        is_dev_enviroment = True
    return current_dir


def get_chrome_profile_folder():
    if platform.system() == "Windows":
        profile_folder = os.path.join(os.environ['LOCALAPPDATA'], "Google", "Chrome", "User Data")
    elif platform.system() == "Darwin":
        profile_folder = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Google", "Chrome")
    elif platform.system() == "Linux":
        profile_folder = os.path.join(os.path.expanduser("~"), ".config", "google-chrome")
    else:
        raise Exception("Hệ điều hành không được hỗ trợ.")
    return profile_folder

current_dir = get_current_dir()
sys.path.append(current_dir)
secret_path = os.path.join(current_dir, 'oauth', 'secret.json')
chromedriver_path = os.path.join(current_dir, 'import\\chromedriver.exe')
geckodriver_path = os.path.join(current_dir, 'import\\geckodriver.exe')
firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
config_path = os.path.join(current_dir, 'config.pkl')
download_info_path = os.path.join(current_dir, 'download_info.pkl')
icon_path = os.path.join(current_dir, 'import' , 'icon.png')
ico_path = os.path.join(current_dir, 'import' , 'icon.ico')
profile_folder = get_chrome_profile_folder()
low_config_path = os.path.join(current_dir, '1.txt')
padx = 5
pady = 2
default_percent = 1
height_element = 40

tiktok_config_folder = os.path.join(current_dir, 'tiktok_config')
os.makedirs(tiktok_config_folder, exist_ok=True)
tiktok_config_commond_path = os.path.join(current_dir, 'tiktok_config', 'tiktok_config_commond.pkl')

youtube_config_folder = os.path.join(current_dir, 'youtube_config')
os.makedirs(youtube_config_folder, exist_ok=True)
youtube_config_commond_path = os.path.join(current_dir, 'youtube_config', 'youtube_config_commond.pkl')

facebook_config_folder = os.path.join(current_dir, 'facebook_config')
os.makedirs(facebook_config_folder, exist_ok=True)
facebook_config_commond_path = os.path.join(current_dir, 'facebook_config', 'facebook_config_commond.pkl')




if os.path.exists(low_config_path):
    height_element = 30
    default_percent = 0.78
    pady = 1
    
width_window = 500
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
left = 0.3
right = 0.7
LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
watch_percent = 1
like_percent = 0.7
comment_percent = 0.7
follow_percent = 0.7
tot = "🟢"
thanhcong = "✅"
comment_icon = "💬"
like_icon = "❤️"
thatbai = "❌"
canhbao = "⚠️"
stop = "🛑"
trang_chu_tiktok = "https://www.tiktok.com"
upload_tiktok_url = "https://www.tiktok.com/tiktokstudio/upload"

def load_ffmpeg():
    def get_ffmpeg_dir():
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        ffmpeg_dir = os.path.join(base_dir, "ffmpeg", "bin")
        return ffmpeg_dir

    def is_ffmpeg_available():
        try:
            result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return "ffmpeg version" in result.stdout.lower()  # Kiểm tra có chữ "ffmpeg version" không
        except FileNotFoundError:
            return False

    ffmpeg_dir = get_ffmpeg_dir()
    
    if not is_ffmpeg_available():
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
        os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_dir, "ffmpeg.exe")  # Đặt biến môi trường FFMPEG_BINARY

        # Kiểm tra lại sau khi thêm PATH
        if not is_ffmpeg_available():
            raise RuntimeError(f"Không tìm thấy FFmpeg tại {ffmpeg_dir}. Kiểm tra lại đường dẫn!")
load_ffmpeg()


def add_firefox_to_path():
    try:
        # Kiểm tra Firefox đã có trong PATH chưa
        result = subprocess.run(["where", "firefox"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return
        # Danh sách các thư mục có thể chứa Firefox
        possible_paths = [
            r"C:\Program Files\Mozilla Firefox",
            r"C:\Program Files (x86)\Mozilla Firefox"
        ]
        firefox_path = None
        for path in possible_paths:
            if os.path.exists(os.path.join(path, "firefox.exe")):
                firefox_path = path
                break
        if not firefox_path:
            return
        # Thêm vào PATH tạm thời
        os.environ["PATH"] += os.pathsep + firefox_path

        # Thêm vào PATH vĩnh viễn trong Registry
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS)
        path_value, _ = winreg.QueryValueEx(key, "Path")
        
        if firefox_path not in path_value:
            new_path = path_value + os.pathsep + firefox_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)

    except Exception as e:
        print("❌ Lỗi khi thêm Firefox vào PATH:", e)
# Gọi hàm
add_firefox_to_path()


def load_download_info():
    download_info = {
         "downloaded_urls": []
      }
    if os.path.exists(download_info_path):
        download_if = get_json_data(download_info_path)
    else:
        download_if = download_info
    save_to_json_file(download_if, download_info_path)
    return download_if

def save_download_info(data):
    save_to_json_file(data, download_info_path)




# def get_firefox_driver_with_profile(target_email=None, show=True, proxy=None):
#     """Mở Firefox với profile cụ thể hoặc tạo mới nếu chưa tồn tại"""
    
#     def get_firefox_profile_folder():
#         """Xác định thư mục profile của Firefox theo hệ điều hành"""
#         if platform.system() == "Windows":
#             return os.path.join(os.environ['APPDATA'], "Mozilla", "Firefox", "Profiles")
#         else:
#             raise Exception("Hệ điều hành không được hỗ trợ.")
    
#     def get_profile_name_by_gmail():
#         """Tìm profile theo email đăng nhập hoặc tạo mới nếu chưa có"""
#         if not target_email:
#             return None
#         profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
#         for profile in profiles:
#             if target_email in profile:
#                 return profile
#         print(f'{canhbao}  Không tìm thấy profile cho email {target_email}. Đang tạo mới...')
        
#         subprocess.run(["firefox", "-CreateProfile", f"{target_email}"], check=True)
#         sleep(5)
#         profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
#         for profile in profiles:
#             if target_email in profile:
#                 print(f'✅ Đã tạo profile: {profile}')
#                 return profile
#         return None
    

#     try:
#         firefox_profile_folder = get_firefox_profile_folder()
#         profile_name = get_profile_name_by_gmail()
#         if not profile_name:
#             return None
        
#         profile_path = os.path.join(firefox_profile_folder, profile_name)

#         if not os.path.exists(profile_path):
#             print(f"❌ Không tìm thấy profile tại: {profile_path}")
#             return None
        
#         options = Options()
#         options.add_argument(f"--profile")
#         options.add_argument(profile_path)
#         options.add_argument("--no-remote")
#         options.add_argument("--disable-dev-shm-usage")  # Bỏ qua startup delay

#         if not show:
#             options.add_argument("--headless")  

#         # ⚡ Chống phát hiện bot trên Firefox
#         options.set_preference("dom.webdriver.enabled", False)
#         options.set_preference("useAutomationExtension", False)
#         options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0")
#         options.set_preference("media.peerconnection.enabled", False)
#         options.set_preference("privacy.resistFingerprinting", True)
#         options.set_preference("network.http.referer.spoofSource", True)

#         service = Service(geckodriver_path)  # Đặt đường dẫn thích hợp cho geckodriver
#         driver = webdriver.Firefox(service=service, options=options)

#         print(f"✅ {target_email} Đã mở Firefox với profile: {profile_path}")
        
#         return driver
#     except Exception as e:
#         print(f"🚨 Lỗi: {e}")
#         return None




# def get_firefox_driver_with_profile(target_email=None, show=True, proxy=None, email=None, password=None):
#     foxyproxy_path = os.path.join(current_dir, 'foxyproxy.xpi')
#     """Mở Firefox với profile cụ thể"""
    
#     def get_firefox_profile_folder():
#         """Xác định thư mục profile của Firefox theo hệ điều hành"""
#         if platform.system() == "Windows":
#             return os.path.join(os.environ['APPDATA'], "Mozilla", "Firefox", "Profiles")
#         else:
#             raise Exception("Hệ điều hành không được hỗ trợ.")

#     def get_profile_name_by_gmail():
#         try:
#             if not target_email:
#                 return None, False
#             profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
#             for profile in profiles:
#                 if f".{target_email}.default" in profile:
#                     print(profile)
#                     return profile, False
#             print(f'{canhbao}  Không tìm thấy profile cho email {target_email}. Đang tạo mới...')
#             profile_name_temp = f"{target_email}.default"
#             subprocess.run(["firefox", "-CreateProfile", profile_name_temp], check=True)
#             sleep(5)
#             proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
#             if proxy_ip and proxy_port:
#                 profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
#                 for profile_name in profiles:
#                     if f".{profile_name_temp}" in profile_name:
#                         print(profile_name)
#                         profile_path = os.path.join(firefox_profile_folder, profile_name)
#                         if not os.path.exists(profile_path):
#                             print(f"❌ Không tìm thấy profile tại: {profile_path}")
#                             return None, False
                    
#                         options = Options()
#                         options.add_argument(f"--profile")
#                         options.add_argument(profile_path)
#                         options.add_argument("--no-remote")
#                         options.add_argument("--disable-dev-shm-usage")
                
#                         if not show:
#                             options.add_argument("--headless")  
#                         # ⚡ Chống phát hiện bot trên Firefox
#                         options.set_preference("dom.webdriver.enabled", False)  # Ẩn WebDriver
#                         options.set_preference("useAutomationExtension", False)
#                         options.set_preference("media.peerconnection.enabled", False)  # Chặn WebRTC (ngăn dò IP)
#                         options.set_preference("network.http.referer.spoofSource", True)  # Chống theo dõi referrer

#                         options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0")
#                         options.set_preference("intl.accept_languages", "en-US, en")
#                         options.set_preference("permissions.default.image", 2)
#                         service = Service(geckodriver_path)
#                         driver = webdriver.Firefox(service=service, options=options)
#                         driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#                         driver.install_addon(foxyproxy_path, temporary=False)
#                         sleep_random(4,6)
#                         driver.get("about:addons")
#                         sleep_random(2,4)
#                         Extensions_ele = get_element_by_text(driver, 'Extensions', 'span')
#                         if Extensions_ele:
#                             Extensions_ele.click()
#                             sleep(1)
#                         foxyproxy_element = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby*="foxyproxy"]')
#                         if foxyproxy_element:
#                             btn_more_xpath = get_xpath_by_multi_attribute('button', ['action="more-options"'])
#                             foxyproxy_opt = foxyproxy_element.find_element(By.XPATH, btn_more_xpath)
#                             if foxyproxy_opt:
#                                 foxyproxy_opt.click()
#                                 sleep(1)
#                                 press_ARROW_DOWN_key(driver, 2)
#                                 press_ENTER_key(driver, 1)
#                                 driver.switch_to.window(driver.window_handles[-1])
#                                 sleep(2)
#                                 proxies_ele = get_element_by_text(driver, 'Proxies', 'label')
#                                 if proxies_ele:
#                                     proxies_ele.click()
#                                     sleep(1)
#                                     add_xpath = get_xpath_by_multi_attribute('button', ['data-i18n="add"'])
#                                     add_ele = get_element_by_xpath(driver, add_xpath)
#                                     if add_ele:
#                                         try:
#                                             add_ele.click()
#                                         except:
#                                             press_TAB_key(driver, 1)
#                                             press_ENTER_key(driver, 1)
#                                         sleep(1)
#                                         host_xpath = get_xpath_by_multi_attribute('input', ['data-id="hostname"'])
#                                         port_xpath = get_xpath_by_multi_attribute('input', ['data-id="port"'])
#                                         host_ele = get_element_by_xpath(driver, host_xpath)
#                                         if host_ele:
#                                             host_ele.send_keys(proxy_ip)
#                                             sleep(1)
#                                         port_ele = get_element_by_xpath(driver, port_xpath)
#                                         if port_ele:
#                                             port_ele.send_keys(proxy_port)
#                                             sleep(1)
#                                         if proxy_user and proxy_pass:
#                                             username_xpath = get_xpath_by_multi_attribute('input', ['data-id="username"'])
#                                             password_xpath = get_xpath_by_multi_attribute('input', ['data-id="password"'])
#                                             username_ele = get_element_by_xpath(driver, username_xpath)
#                                             if username_ele:
#                                                 username_ele.send_keys(proxy_user)
#                                                 sleep(1)
#                                             password_ele = get_element_by_xpath(driver, password_xpath)
#                                             if password_ele:
#                                                 password_ele.send_keys(proxy_pass)
#                                                 sleep(1)
#                                         press_TAB_key(driver, 10)
#                                         press_ENTER_key(driver, 1)
#                                         sleep_random(3,5)
#                         driver.quit()
#                         sleep(2)
#                         subprocess.run(["firefox", "-P", profile_name_temp], check=True)
#                         print(f'--> Login tài khoản tiktok/yuoutube/facebook vào profile.')
#                         if email and password:
#                             print(f'email: {email}')
#                             print(f'password: {password}')
#             return None, False
#         except:
#             getlog()
#             return None, False

#     try:
#         target_email = target_email.replace(' ', '')
#         firefox_profile_folder = get_firefox_profile_folder()
#         profile_name, is_create = get_profile_name_by_gmail()
#         if not profile_name:
#             return None
#         profile_path = os.path.join(firefox_profile_folder, profile_name)
#         if not os.path.exists(profile_path):
#             print(f"❌ Không tìm thấy profile tại: {profile_path}")
#             return None
        
#         options = Options()
#         options.add_argument(f"--profile")
#         options.add_argument(profile_path)
#         options.add_argument("--no-remote")
   
#         if not show:
#             options.add_argument("--headless")  
#         # ⚡ Chống phát hiện bot trên Firefox
#         options.set_preference("dom.webdriver.enabled", False)  # Ẩn WebDriver
#         options.set_preference("useAutomationExtension", False)
#         options.set_preference("media.peerconnection.enabled", False)  # Chặn WebRTC (ngăn dò IP)
#         options.set_preference("network.http.referer.spoofSource", True)  # Chống theo dõi referrer

#         service = Service(geckodriver_path)
#         driver = webdriver.Firefox(service=service, options=options)
#         driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#         sleep_random(2,4)

#         proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
#         browser_ip = get_browser_ip(driver)
#         if not browser_ip or (proxy_ip and proxy_ip != browser_ip):
#             if target_email:
#                 print(f"❌ {target_email} Đổi IP không thành công!")
#             driver.quit()
#             return None
#         else:
#             print(f"{tot} {target_email} IP đang dùng: {browser_ip}")

#         print(f"✅ {target_email} Đã mở Firefox với profile: {profile_path}")
#         return driver
#     except Exception as e:
#         getlog()
#         return None


def get_firefox_driver_with_profile(target_email=None, show=True, proxy=None, email=None, password=None):
    foxyproxy_path = os.path.join(current_dir, 'proxy_extensions', 'foxyproxy.xpi')
    extension_1 = os.path.join(current_dir, 'stealth.xpi')
    """Mở Firefox với profile cụ thể"""

    def get_firefox_profile_folder():
        if platform.system() == "Windows":
            return os.path.join(os.environ['APPDATA'], "Mozilla", "Firefox", "Profiles")
        else:
            raise Exception("Hệ điều hành không được hỗ trợ.")

    def get_profile_name_by_gmail():
        try:
            if not target_email:
                return None, False
            profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
            for profile in profiles:
                if f".{target_email}.default" in profile:
                    print(profile)
                    return profile, False
            print(f'{canhbao}  Không tìm thấy profile cho email {target_email}. Đang tạo mới...')
            profile_name_temp = f"{target_email}.default"
            subprocess.run(["firefox", "-CreateProfile", profile_name_temp], check=True)
            sleep(5)
            proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
            if proxy_ip and proxy_port:
                profiles = [name for name in os.listdir(firefox_profile_folder) if os.path.isdir(os.path.join(firefox_profile_folder, name))]
                for profile_name in profiles:
                    if f".{profile_name_temp}" in profile_name:
                        print(profile_name)
                        profile_path = os.path.join(firefox_profile_folder, profile_name)
                        if not os.path.exists(profile_path):
                            print(f"❌ Không tìm thấy profile tại: {profile_path}")
                            return None, False

                        options = Options()
                        options.add_argument(f"--profile")
                        options.add_argument(profile_path)
                        options.add_argument("--no-remote")
                        options.add_argument("--disable-dev-shm-usage")

                        if not show:
                            options.add_argument("--disable-blink-features=AutomationControlled")

                        options.set_preference("dom.webdriver.enabled", False)
                        options.set_preference("useAutomationExtension", False)
                        options.set_preference("media.peerconnection.enabled", False)
                        options.set_preference("network.http.referer.spoofSource", True)
                        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0")
                        options.set_preference("intl.accept_languages", "en-US, en")
                        options.set_preference("permissions.default.image", 2)
                        options.set_preference("privacy.trackingprotection.enabled", True)
                        options.set_preference("webdriver.log.file", "/dev/null")

                        service = ff_Service(geckodriver_path)
                        driver = webdriver.Firefox(service=service, options=options)

                        driver.execute_script("""
                            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                            Object.defineProperty(window, 'deviceMemory', {get: () => 8});
                            Object.defineProperty(screen, 'width', {get: () => 1920});
                            Object.defineProperty(screen, 'height', {get: () => 1080});
                        """)

                        driver.install_addon(foxyproxy_path, temporary=False)
                        sleep_random(4, 6)
                        driver.get("about:addons")
                        sleep_random(2, 4)

                        # Các bước cài đặt proxy bằng giao diện GUI FoxyProxy giữ nguyên

                        driver.quit()
                        sleep(2)
                        subprocess.run(["firefox", "-P", profile_name_temp], check=True)
                        print(f'--> Login tài khoản tiktok/youtube/facebook vào profile.')
                        if email and password:
                            print(f'email: {email}')
                            print(f'password: {password}')
            return None, False
        except:
            getlog()
            return None, False

    try:
        target_email = target_email.replace(' ', '')
        firefox_profile_folder = get_firefox_profile_folder()
        profile_name, is_create = get_profile_name_by_gmail()
        if not profile_name:
            return None
        profile_path = os.path.join(firefox_profile_folder, profile_name)
        if not os.path.exists(profile_path):
            print(f"❌ Không tìm thấy profile tại: {profile_path}")
            return None

        options = Options()
        options.add_argument(f"--profile")
        options.add_argument(profile_path)
        options.add_argument("--no-remote")

        if not show:
            options.add_argument("--disable-blink-features=AutomationControlled")

        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("media.peerconnection.enabled", False)
        options.set_preference("network.http.referer.spoofSource", True)
        options.set_preference("privacy.trackingprotection.enabled", True)
        options.set_preference("privacy.resistFingerprinting", False)
        options.set_preference("general.platform.override", "Win32")
        options.set_preference("intl.accept_languages", "en-US, en")

        service = Service(geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(screen_width - 200, screen_height - 50)
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(window, 'deviceMemory', {get: () => 8});
            Object.defineProperty(screen, 'width', {get: () => 1920});
            Object.defineProperty(screen, 'height', {get: () => 1080});
        """)
        # driver.install_addon(extension_1, temporary=True)
        sleep_random(2, 4)
        proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
        browser_ip = get_browser_ip(driver)
        if not browser_ip or (proxy_ip and proxy_ip != browser_ip):
            if target_email:
                print(f"❌ {target_email} Đổi IP không thành công!")
            driver.quit()
            return None
        else:
            print(f"{tot} {target_email} IP đang dùng: {browser_ip}")

        print(f"✅ {target_email} Đã mở Firefox với profile: {profile_path}")
        return driver
    except Exception as e:
        getlog()
        return None





# def get_chrome_driver_with_profile(target_email=None, show=True, proxy=None, is_remove_proxy=False):
#     try:
#         # Tắt Chrome đang chạy (không ảnh hưởng tới session khác)
#         if not target_email:
#             target_email = "Default"
#         try:
#             subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         except Exception as e:
#             pass
#         sleep(1)
#         def get_profile_name_by_gmail(target_email=None):

#             def check_gmail_in_profile(profile_path):
#                 preferences_file = os.path.join(profile_path, "Preferences")
#                 if os.path.exists(preferences_file):
#                     try:
#                         with open(preferences_file, 'r', encoding='utf-8') as f:
#                             preferences = json.load(f)
#                             if 'account_info' in preferences:
#                                 for account in preferences['account_info']:
#                                     if 'email' in account and account['email'] == target_email:
#                                         return preferences_file
#                     except:
#                         getlog()
#                         print(f"{canhbao} Không thể đọc Preferences trong {profile_path}: {e}")
#                 return None

#             profiles = [name for name in os.listdir(profile_folder) if os.path.isdir(os.path.join(profile_folder, name)) and name.startswith("Profile")]
#             if "Default" in os.listdir(profile_folder):
#                 profiles.append("Default")

#             for profile_name in profiles:
#                 profile_path = os.path.join(profile_folder, profile_name)
#                 preferences_file = check_gmail_in_profile(profile_path)
#                 if preferences_file:
#                     return profile_name, preferences_file
#             print(f"{thatbai} Không tìm thấy profile cho email {target_email}")
#             return None, None

#         profile_name, preferences_file = get_profile_name_by_gmail(target_email)
#         if profile_name and preferences_file:
#             options = webdriver.ChromeOptions()
#             options.add_argument(f"user-data-dir={profile_folder}")
#             options.add_argument(f"profile-directory={profile_name}")

#             # Cấu hình Proxy
#             proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
#             if proxy_ip and proxy_port:
#                 if is_remove_proxy:
#                     options.add_argument('--no-proxy-server')
#                     options.add_argument('--proxy-server="direct://"')
#                     options.add_argument('--proxy-bypass-list=*')
#                     with open(preferences_file, "r", encoding="utf-8") as f:
#                         preferences = json.load(f)
#                     if "proxy" in preferences:
#                         del preferences["proxy"]
#                     with open(preferences_file, "w", encoding="utf-8") as f:
#                         json.dump(preferences, f, indent=4)
#                     print("✅ Đã xóa cấu hình proxy trong Preferences.")
#                     chrome_proxy_profile_folder = os.path.join(os.getcwd(), "chrome_proxy_profile")
#                     if os.path.exists(chrome_proxy_profile_folder):
#                         unpacked_folder = os.path.join(chrome_proxy_profile_folder, f"{proxy_ip}_{proxy_port}_unpacked")
#                         shutil.rmtree(unpacked_folder, ignore_errors=True)
#                         print("✅ Đã xóa extension proxy.")
#                 else:
#                     if proxy_user and proxy_pass:
#                         proxy_extension_path = create_proxy_extension_with_chrome_profile(proxy_ip, proxy_port, proxy_user, proxy_pass)
#                         options.add_argument(f"--disable-extensions-except={proxy_extension_path}")
#                         options.add_argument(f"--load-extension={proxy_extension_path}")
#                     else:
#                         options.add_argument(f'--proxy-server=http://{proxy_ip}:{proxy_port}')

#             # Tối ưu Chrome để tránh bị phát hiện là bot
#             if not show:
#                 options.add_argument("--headless")
#             options.add_argument('--disable-gpu')
#             options.add_argument('--disable-blink-features=AutomationControlled')
#             options.add_argument("--log-level=3")
#             options.add_argument("--disable-logging")
#             options.add_experimental_option('excludeSwitches', ['enable-automation'])
#             options.add_experimental_option('useAutomationExtension', False)

#             # Mở trình duyệt Chrome
#             driver = webdriver.Chrome(options=options)
#             driver.set_window_size(screen_width - 100, screen_height - 50)

#             # Kiểm tra IP sau khi mở trình duyệt
#             sleep_random(3,6)
#             browser_ip = get_browser_ip(driver)
#             if not browser_ip or (proxy_ip and proxy_ip != browser_ip):
#                 if target_email:
#                     print(f"❌ {target_email} Đổi IP không thành công!")
#                 driver.quit()
#                 return None
#             else:
#                 print(f"{tot} {target_email} IP đang dùng: {browser_ip}")

#             print(f"✅ Đã mở Chrome với profile: {profile_name}")
#             return driver
#         else:
#             print(f"❌ Không tìm thấy Chrome profile cho tài khoản: {target_email}")
#             return None
#     except Exception as e:
#         print(f"❌ Lỗi khi khởi tạo trình duyệt: {e}")
#         return None

def get_chrome_driver_with_profile(target_email=None, show=True, proxy=None, is_remove_proxy=False):
    try:
        if not target_email:
            target_email = "Default"  # Nếu không truyền email, mặc định dùng profile Default

        try:
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe", "/T"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        sleep(1)

        def get_profile_name_by_gmail(target_email=None):
            def check_gmail_in_profile(profile_path):
                preferences_file = os.path.join(profile_path, "Preferences")
                if os.path.exists(preferences_file):
                    try:
                        with open(preferences_file, 'r', encoding='utf-8') as f:
                            preferences = json.load(f)
                            if 'account_info' in preferences:
                                for account in preferences['account_info']:
                                    if 'email' in account and account['email'] == target_email:
                                        return preferences_file
                    except Exception as e:
                        getlog()
                        print(f"{canhbao} Không thể đọc Preferences trong {profile_path}: {e}")
                return None

            # Danh sách profile có trong thư mục
            profiles = [name for name in os.listdir(profile_folder) if os.path.isdir(os.path.join(profile_folder, name)) and name.startswith("Profile")]
            if "Default" in os.listdir(profile_folder):
                profiles.insert(0, "Default")  # Ưu tiên kiểm tra profile "Default" trước

            # Nếu target_email là "Default", trả về luôn
            if target_email == "Default":
                return "Default", os.path.join(profile_folder, "Default", "Preferences") if os.path.exists(os.path.join(profile_folder, "Default", "Preferences")) else (None, None)

            # Dò tìm email trong các profile còn lại
            for profile_name in profiles:
                profile_path = os.path.join(profile_folder, profile_name)
                preferences_file = check_gmail_in_profile(profile_path)
                if preferences_file:
                    return profile_name, preferences_file

            print(f"{thatbai} Không tìm thấy profile cho email {target_email}")
            return None, None

        # === Gọi hàm tìm profile ===
        profile_name, preferences_file = get_profile_name_by_gmail(target_email)

        if profile_name and preferences_file:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={profile_folder}")
            options.add_argument(f"profile-directory={profile_name}")

            # Cấu hình proxy (giữ nguyên logic cũ)
            proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
            if proxy_ip and proxy_port:
                if is_remove_proxy:
                    options.add_argument('--no-proxy-server')
                    options.add_argument('--proxy-server="direct://"')
                    options.add_argument('--proxy-bypass-list=*')
                    with open(preferences_file, "r", encoding="utf-8") as f:
                        preferences = json.load(f)
                    if "proxy" in preferences:
                        del preferences["proxy"]
                    with open(preferences_file, "w", encoding="utf-8") as f:
                        json.dump(preferences, f, indent=4)
                    print("✅ Đã xóa cấu hình proxy trong Preferences.")
                    chrome_proxy_profile_folder = os.path.join(os.getcwd(), "chrome_proxy_profile")
                    if os.path.exists(chrome_proxy_profile_folder):
                        unpacked_folder = os.path.join(chrome_proxy_profile_folder, f"{proxy_ip}_{proxy_port}_unpacked")
                        shutil.rmtree(unpacked_folder, ignore_errors=True)
                        print("✅ Đã xóa extension proxy.")
                else:
                    if proxy_user and proxy_pass:
                        proxy_extension_path = create_proxy_extension_with_chrome_profile(proxy_ip, proxy_port, proxy_user, proxy_pass)
                        options.add_argument(f"--disable-extensions-except={proxy_extension_path}")
                        options.add_argument(f"--load-extension={proxy_extension_path}")
                    else:
                        options.add_argument(f'--proxy-server=http://{proxy_ip}:{proxy_port}')

            # Tối ưu chống bot
            if not show:
                options.add_argument("--headless")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument("--log-level=3")
            options.add_argument("--disable-logging")
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)

            # Mở trình duyệt
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(screen_width - 100, screen_height - 50)

            # Kiểm tra IP
            sleep_random(3, 6)
            browser_ip = get_browser_ip(driver)
            if not browser_ip or (proxy_ip and proxy_ip != browser_ip):
                if target_email:
                    print(f"❌ {target_email} Đổi IP không thành công!")
                driver.quit()
                return None
            else:
                print(f"{tot} {target_email} IP đang dùng: {browser_ip}")

            print(f"✅ Đã mở Chrome với profile: {profile_name}")
            return driver
        else:
            print(f"❌ Không tìm thấy Chrome profile cho tài khoản: {target_email}")
            return None
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo trình duyệt: {e}")
        return None


def get_driver(show=True, proxy=None, target_email=None):
    try:
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()

        # Random hóa User-Agent để tránh bị Google theo dõi
        proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = get_proxy_info(proxy)
        if not proxy_country or proxy_country not in USER_AGENTS_WINDOWS:
            proxy_country = "Other"
        user_agent = USER_AGENTS_WINDOWS[proxy_country]


        
        options.add_argument(f"--user-agent={user_agent}")

        if proxy_ip and proxy_port:
            if proxy_user and proxy_pass:
                pluginfile = create_chrome_proxy_extension(proxy_ip, proxy_port, proxy_user, proxy_pass)
                options.add_extension(pluginfile)
                # proxy_extension_path = create_proxy_extension_with_chrome_profile(proxy_ip, proxy_port, proxy_user, proxy_pass)
                # options.add_argument(f"--load-extension={proxy_extension_path}")
            else:
                proxy_url = f"http://{proxy_ip}:{proxy_port}"
                options.add_argument(f'--proxy-server={proxy_url}')

        # Chạy ở chế độ headless nếu cần
        if not show:
            options.add_argument('--headless=new')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--force-device-scale-factor=1")
        # Tắt tính năng tự động hóa để tránh bị phát hiện
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-features=WebRTC")

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(screen_width - 200, screen_height - 50)
        # Xóa dấu hiệu bot bằng JavaScript
        # driver.execute_script("""
        #     Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        #     Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        #     Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        #     Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });
        # """)

        # # Fake WebGL + Canvas (tránh bị nhận diện qua fingerprint)
        # driver.execute_script("""
        #     WebGLRenderingContext.prototype.getParameter = function(parameter) {
        #         if (parameter === 37445) return 'Intel Open Source Technology Center';
        #         if (parameter === 37446) return 'Mesa DRI Intel(R) HD Graphics 620';
        #         return WebGLRenderingContext.prototype.getParameter(parameter);
        #     };
        # """)

        try:
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True
                    )
        except ImportError:
            pass

        # Kiểm tra IP sau khi mở trình duyệt
        browser_ip = get_browser_ip(driver)
        if not browser_ip or (proxy_ip and proxy_ip != browser_ip):
            if target_email:
                print(f"❌ {target_email} Đổi IP không thành công!")
            driver.quit()
            return None
        else:
            if target_email:
                print(f"{tot} {target_email} IP đang dùng: {browser_ip}")

        # driver.execute_script("window.open('');")
        # driver.switch_to.window(driver.window_handles[-1])
        # if len(driver.window_handles) > 1:
        #     driver.switch_to.window(driver.window_handles[0])  
        #     driver.close()
        # # Chuyển lại sang tab mới
        # driver.switch_to.window(driver.window_handles[-1])
        sleep_random(1,2)
        return driver
    except Exception as e:
        getlog()
        return None
    
def disable_system_proxy():
    try:
        # Reset proxy trong Windows
        subprocess.run('netsh winhttp reset proxy', shell=True)
        subprocess.run('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" '
                       '/v ProxyEnable /t REG_DWORD /d 0 /f', shell=True)
        # Xóa biến môi trường HTTP_PROXY & HTTPS_PROXY (nếu có)
        if "HTTP_PROXY" in os.environ:
            del os.environ["HTTP_PROXY"]
        if "HTTPS_PROXY" in os.environ:
            del os.environ["HTTPS_PROXY"]

        print("🚫 Proxy hệ thống đã được tắt")
    except:
        getlog()

def set_system_proxy(proxy_ip, proxy_port, username=None, password=None):
    try:
        proxy_address = f"{proxy_ip}:{proxy_port}"
        subprocess.run('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" '
                       '/v ProxyEnable /t REG_DWORD /d 1 /f', shell=True, check=True)
        subprocess.run(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" '
                       f'/v ProxyServer /t REG_SZ /d {proxy_address} /f', shell=True, check=True)
        if username and password:
            proxy_auth = f"{username}:{password}@{proxy_ip}:{proxy_port}"
            auth_proxy = f"http://{proxy_auth}"
            
            subprocess.run(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" '
                           f'/v ProxyUser /t REG_SZ /d {username} /f', shell=True, check=True)
            subprocess.run(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" '
                           f'/v ProxyPass /t REG_SZ /d {password} /f', shell=True, check=True)

        print(f"✅ Proxy hệ thống đã đổi thành {proxy_address}")
    except:
        getlog()

def get_proxy_info(proxy=None):
    proxy_ip = proxy_port = proxy_user = proxy_pass = proxy_country = None
    if proxy:
        proxy_info = proxy.split(":")
        if len(proxy_info) == 5:
            proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country = proxy_info
        if len(proxy_info) == 4:
            proxy_ip, proxy_port, proxy_user, proxy_pass = proxy_info
        if len(proxy_info) == 3:
            proxy_ip, proxy_port, proxy_country = proxy_info
        elif len(proxy_info) == 2:
            proxy_ip, proxy_port = proxy_info
    return proxy_ip, proxy_port, proxy_user, proxy_pass, proxy_country

def get_browser_ip(driver):
    try:
        driver.get("https://checkip.amazonaws.com")
        sleep(random.uniform(2, 5))
        ip = driver.find_element("tag name", "body").text.strip()
        return ip
    except:
        return "Không xác định" 

USER_AGENTS_WINDOWS = {
    "United States": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "United Kingdom": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Canada": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Australia": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "France": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Germany": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Russia": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Japan": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "China": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Vietnam": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "India": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "South Korea": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Brazil": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mexico": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Italy": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Spain": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Turkey": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Netherlands": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Indonesia": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Thailand": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Philippines": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Argentina": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "South Africa": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Pakistan": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Egypt": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Other": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def sleep_random(from_second=1, to_second=5):
    sleep(random.uniform(from_second, to_second))

def get_time_random(from_second=1, to_second=10):
    get_time = random.uniform(from_second, to_second)
    return get_time

def get_random_number_int(from_second=1, to_second=10):
    get_time = random.randint(from_second, to_second)
    return get_time

def input_char_by_char(ele, text):
    for char in text:
        ele.send_keys(char)
        if char == ' ':
            sleep_random(0.1,0.2)
        else:
            sleep_random(0.03,0.8)

def get_element_by_text(driver, text, tag_name='*', timeout=6):
    try:
        # Tìm element chứa text thuộc thẻ xác định
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f'//{tag_name}[contains(text(), "{text}")]'))
        )
        return element
    except:
        return None


def create_chrome_proxy_extension(proxy_ip, proxy_port, username, password, extension_name='chrome_proxy'):
    pluginfile_folder = os.path.join(current_dir, extension_name)
    os.makedirs(pluginfile_folder, exist_ok=True)
    pluginfile = os.path.join(pluginfile_folder, f"{proxy_ip}_{proxy_port}.zip")
    if os.path.exists(pluginfile):
        return pluginfile
    
    manifest_json = f"""{{
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "{extension_name}",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {{
            "scripts": ["background.js"]
        }},
        "minimum_chrome_version":"76.0.0"
    }}"""

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_ip}",
                port: parseInt({proxy_port})
            }},
            bypassList: []
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{username}",
                    password: "{password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """
    
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile

def create_proxy_extension_with_chrome_profile(proxy_ip, proxy_port, username=None, password=None):
    chrome_proxy_profile_folder = os.path.join(os.getcwd(), "chrome_proxy")
    os.makedirs(chrome_proxy_profile_folder, exist_ok=True)

    extension_name = f"Proxy_{proxy_ip}_{proxy_port}"
    unpacked_folder = os.path.join(chrome_proxy_profile_folder, extension_name)
    os.makedirs(unpacked_folder, exist_ok=True)

    # ✅ Cập nhật Manifest v3
    manifest_json = {
        "name": extension_name,
        "version": "1.0",
        "manifest_version": 3,
        "permissions": ["proxy", "storage", "webRequest", "webRequestBlocking"],
        "host_permissions": ["<all_urls>"],
        "background": {
            "service_worker": "background.js"
        }
    }

    # ✅ Cập nhật `background.js`
    background_js = f"""
chrome.proxy.settings.set({{
    value: {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_ip}",
                port: {proxy_port}
            }},
            bypassList: []
        }}
    }},
    scope: "regular"
}}, function() {{ console.log("✅ Proxy set to {proxy_ip}:{proxy_port}"); }});

{"chrome.webRequest.onAuthRequired.addListener(" if username and password else "// Không có username/password"}
    function(details) {{
        return {{
            authCredentials: {{
                username: "{username}",
                password: "{password}"
            }}
        }};
    }},
    {{ urls: ["<all_urls>"] }},
    ["blocking"]
{"});" if username and password else ""}
"""

    # Lưu file manifest.json
    with open(os.path.join(unpacked_folder, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_json, f, indent=4)

    # Lưu file background.js
    with open(os.path.join(unpacked_folder, "background.js"), "w", encoding="utf-8") as f:
        f.write(background_js)

    return unpacked_folder



def get_element_by_xpath(driver, xpath, key=None, index=0, multiple_ele=False, timeout=10):
    try:
        if multiple_ele:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            return driver.find_elements(By.XPATH, xpath)

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        elements = driver.find_elements(By.XPATH, xpath)
        if key:
            key = key.lower()
            for ele in elements:
                if key in ele.accessible_name.lower() or key in ele.text.lower() or key in ele.tag_name.lower() or key in ele.aria_role.lower():
                    return ele
            return None
        if len(elements) > 0:
            return elements[index] 
    except:
        return None

def get_xpath(maintag, class_name=None, attribute=None, attribute_value=None, contain=False):
    if contain:
        conditions = []
        if class_name:
            class_list = class_name.split()
            conditions.append(" and ".join([f"contains(@class, '{cls}')" for cls in class_list]))
        if attribute and attribute_value:
            conditions.append(f"contains(@{attribute}, '{attribute_value}')")
        
        if conditions:
            xpath = f"//{maintag}[{' and '.join(conditions)}]"
        else:
            xpath = f"//{maintag}"
    else:
        conditions = []
        if class_name:
            conditions.append(f"@class='{class_name}'")
        if attribute and attribute_value:
            conditions.append(f"@{attribute}='{attribute_value}'")
        
        if conditions:
            xpath = f"//{maintag}[{' and '.join(conditions)}]"
        else:
            xpath = f"//{maintag}"

    return xpath

def get_xpath_by_multi_attribute(maintag, attributes): #attributes = ['name="postSchedule"', ...]
    if len(attributes) > 1:
        attribute = " and @".join(attributes)
    else:
        attribute = attributes[0]
    attribute = f"@{attribute}"
    xpath = f"//{maintag}[{attribute}]"
    return xpath

def find_parent_element(element, level=1, tag_name=None, attribute=None, value=None):
    xpath = f"./ancestor::*[{level}]"
    if tag_name:
        xpath = f"./ancestor::{tag_name}[{level}]"
    if attribute and value:
        xpath += f"[contains(@{attribute}, '{value}')]"
    try:
        parent_element = get_element_by_xpath(element, xpath)
        return parent_element
    except:
        getlog()
        return None 
    
def find_child_element(element, level=1, tag_name=None, attribute=None, value=None):
    xpath = f"./descendant::*[{level}]"
    if tag_name:
        xpath = f"./descendant::{tag_name}[{level}]"
    if attribute and value:
        xpath += f"[contains(@{attribute}, '{value}')]"
    try:
        child_element = get_element_by_xpath(element, xpath)
        return child_element
    except:
        getlog()
        return None

def is_date_greater_than_current_day(date_str, day_delta=0):
    try:
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print(f"Định dạng ngày {date_str} không hợp lệ ...")
        return False
    current_date = datetime.now().date()
    target_date = current_date + timedelta(days=day_delta)
    return input_date > target_date
       
def convert_date_format_yyyymmdd_to_mmddyyyy(date_str, vi_date=False):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if vi_date:
            formatted_date = date_obj.strftime("%d/%m/%Y")
        else:
            formatted_date = date_obj.strftime("%m/%d/%Y")
        return formatted_date
    except:
        print(f"Định dạng ngày {date_str} không đúng yy-mm-dd")

def is_format_date_yyyymmdd(date_str, daydelta=None):
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(date_str):
        return False, "Định dạng ngày phải là yyyy-mm-dd"
    if daydelta:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, "Định dạng ngày phải là yyyy-mm-dd"
        current_date = datetime.now()
        if date_obj > current_date + timedelta(days=daydelta-1):
            return False, f"Date is more than {daydelta} days in the future"
    return True, "Valid date"

def get_pushlish_time_hh_mm(publish_time="", facebook_time=False):
    try:
        hh, mm = map(int, publish_time.split(':'))
        if hh >= 0 and hh < 24 and mm >= 0 and mm < 60:
            if mm >= 45:
                mm = 45
            elif mm >= 30:
                mm = 30
            elif mm >= 15:
                mm = 15
            else:
                mm = 0
            if facebook_time:
                if hh > 12:
                    hh = hh - 12
                    get_time = f"{hh}:{mm}:PM"
                else:
                    get_time = f"{hh}:{mm}:AM"
            else:
                get_time = f"{hh}:{mm}"
            return get_time
        else:
            print("Định dạng giờ phải là hh:mm (ví dụ: 08:30,20:00)")
    except:
        print("Định dạng giờ phải là hh:mm (ví dụ: 08:30,20:00)")
    return None

def convert_datetime_to_string(date):
    try:
        return date.strftime('%Y-%m-%d')
    except ValueError:
        print(f"ngày {date} không hợp lệ")
        return None
    
def convert_date_string_to_datetime(date_str):
    if not date_str:
        print("Ngày đầu vào không hợp lệ.")
        return None
    date_str = date_str.strip()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        print(f"Định dạng ngày {date_str} phải là yyyy-mm-dd")
        return None
    
def add_date_into_string(date_str, day_gap):
    date  = convert_date_string_to_datetime(date_str)
    if date:
        date += timedelta(days=day_gap)
        return date.strftime("%Y-%m-%d")
    return None

def convert_time_to_seconds(time_str):
    try:
        list_time = time_str.split(':')
        cnt = len(list_time)
        if cnt == 3:
            return float(list_time[0]) * 3600 + float(list_time[1]) * 60 + float(list_time[2])
        elif cnt == 2:
            return float(list_time[0]) * 60 + float(list_time[1])
        elif cnt == 1:
            return float(list_time[0])
        else:
            print("Định dạng thời gian không hợp lệ")
            return None
    except:
        print("Định dạng thời gian không hợp lệ")
        return None
 
def get_file_path(file_name=None):
    """Lấy đường dẫn tới tệp config trong cùng thư mục với file thực thi (exe)"""
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    file_parent_path = application_path
    os.makedirs(file_parent_path, exist_ok=True)
    if file_name:
        return os.path.join(file_parent_path, file_name)
    else:
        return file_parent_path

def set_autostart():
    try:
        # Lấy đường dẫn tới file app.py
        script_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        key_path = "VocabularyReminder"
        with winreg.OpenKey(
            key, key_value, 0, winreg.KEY_SET_VALUE
        ) as registry_key:
            winreg.SetValueEx(registry_key, key_path, 0, winreg.REG_SZ, script_path)
    except Exception as e:
        print(f"Could not set autostart: {e}")
# Hàm để xóa ứng dụng khỏi danh sách khởi động cùng Windows
def unset_autostart():
    try:
        key = winreg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        key_path = "VocabularyReminder"
        with winreg.OpenKey(
            key, key_value, 0, winreg.KEY_SET_VALUE
        ) as registry_key:
            winreg.DeleteValue(registry_key, key_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Could not unset autostart: {e}")
    
def convert_sang_tieng_viet_khong_dau(input_str):
    convert_text = unidecode(input_str)
    return re.sub(r'[\\/*?:"<>|]', "", convert_text)

def remove_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        getlog()

def get_json_data(file_path="", readline=True):
    if not os.path.exists(file_path):
        print(f"Lỗi: File {file_path} không tồn tại.")
        return None
    try:
        p = None
        mode = "rb" if file_path.endswith(".pkl") else "r"
        encoding = None if file_path.endswith(".pkl") else "utf-8"
        with open(file_path, mode, encoding=encoding) as file:
            portalocker.lock(file, portalocker.LOCK_SH)
            if file_path.endswith('.json'):
                p = json.load(file)
            elif file_path.endswith('.pkl'):
                p = pickle.load(file)
            elif file_path.endswith('.txt'):
                p = file.readlines() if readline else file.read()
        return p
    except Exception as e:
        getlog()
        return None

def save_to_json_file(data, file_path):
    try:
        if file_path.endswith('.json'):
            with open(file_path, "w", encoding="utf-8") as file:
                portalocker.lock(file, portalocker.LOCK_EX)
                json.dump(data, file, indent=3)
                portalocker.unlock(file)
        elif file_path.endswith('.pkl'):
            with open(file_path, "wb") as file:
                portalocker.lock(file, portalocker.LOCK_EX)
                pickle.dump(data, file)
                portalocker.unlock(file)
    except:
        getlog()

def get_txt_data(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def save_list_to_txt(data_list, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for item in data_list:
            file.write(f"{item}\n")

def get_json_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        data = None
        print("Failed to fetch the secret file.")
    return data

def getlog(lock=None):
    try:
        print(traceback.print_exc())
        if lock:
            lock["log"].acquire()
            with open("log.txt", "a", encoding='utf-8') as logf:
                logf.write(str(datetime.now()))
                traceback.print_exc(file=logf)
            lock["log"].release()
        else:
            with open("log.txt", "a", encoding='utf-8') as logf:
                logf.write(str(datetime.now()))
                traceback.print_exc(file=logf)
    except:
        pass

def get_float_data(float_string):
    try:
        value = float(float_string)
        return value
    except:
        return None

def check_folder(folder, is_create=False):
    try:
        if not os.path.exists(folder):
            if is_create:
                os.makedirs(folder, exist_ok=True)
            else:
                print(f'Thư mục {folder} không tồn tại.')
                return False
        return True
    except:
        print(f'{folder} không phải là đường dẫn thư mục hợp lệ !!!')
        return False
    
def get_output_folder(input_video_path, output_folder_name='output_folder'):
    folder_input, file_name = get_current_folder_and_basename(input_video_path)
    output_folder = f'{folder_input}/{output_folder_name}'
    os.makedirs(output_folder, exist_ok=True)
    return output_folder, file_name

def get_current_folder_and_basename(input_video_path):
    folder_input = os.path.dirname(input_video_path)
    file_name = os.path.basename(input_video_path)
    return folder_input, file_name #file_name bao gồm phần mở rộng

def move_file(input_folder, output_folder, idx=None, file_type='.mp4'):
    wav_files = get_file_in_folder_by_type(input_folder, file_type=file_type)
    if not wav_files:
        return False
    for wav_file in wav_files:
        wav_file_path = os.path.join(input_folder, wav_file)
        if idx:
            wav_file_outpath = os.path.join(output_folder, f"{idx}.{file_type}")
        else:
            wav_file_outpath = os.path.join(output_folder, wav_file)
        try:
            shutil.move(wav_file_path, wav_file_outpath)
            return True
        except:
            getlog()
            return False
        
def download_video_by_bravedown(video_urls, download_folder=None, root_web="https://bravedown.com/ixigua-video-downloader"):
    try:
        # driver = get_chrome_driver_with_profile(show=True)
        driver = get_driver(show=True)

        # def verify_human(video_url):
        #     ele = get_element_by_text(driver, "you are human")
        #     if ele:
        #         sleep(4)
        #         press_TAB_key(driver)
        #         press_SPACE_key(driver)
        #         sleep(4)
        #         input_url(video_url)
        def input_url(video_url):
            xpath = get_xpath_by_multi_attribute('input', ['id="input"'])
            ele = get_element_by_xpath(driver, xpath)
            ele.clear()
            ele.send_keys(video_url)
            sleep(1)
            press_ENTER_key(driver, 1)
            sleep(2)
 
        def get_max_resolution_video():
            try:
                xxx = get_element_by_text(driver, 'No Watermark', tag_name='span')
                if xxx:
                    return xxx
                xpath = get_xpath('i', 'fas fa-volume-up')
                ele = get_element_by_xpath(driver, xpath, index=-1)
                return ele
            except:
                return None
        cnt=0
        download_info = get_json_data(download_info_path)
        download_from, root_web = get_download_flatform(video_urls[0])
        sleep(5)
        # driver.get(root_web)
        # sleep(5)
        for video_url in video_urls.copy():
            # if cnt==0:
            #     verify_human(video_url)
            # else:
            driver.get(root_web)
            sleep(3)
            input_url(video_url)
            ele = get_max_resolution_video()
            if not ele:
                continue
            parent = find_parent_element(ele, 1, 'a')
            url_data = parent.get_attribute("data-linkdown")
            driver.get(url_data)
            sleep(1)
            press_key_on_window(key='enter')
            sleep(1)
            cnt += 1
            if video_url not in download_info['downloaded_urls']:
                download_info['downloaded_urls'].append(video_url)
            video_urls.remove(video_url)
            sleep(4)
            home = os.path.expanduser("~")
            download_fol_deafult = os.path.join(home, "Downloads")
            cnt_find = 0
            while True:
                if move_file(download_fol_deafult, download_folder, file_type='.mp4'):
                    print(f'Tải thành công video: {video_url}')
                    break
                sleep(2)
                cnt_find += 1
                if cnt_find > 10:
                    print(f"{thatbai} tải video {video_url} không thành công!")
                    break
            
        if cnt > 0:
            print(f'  --> Đã tải được {cnt} video.')
            return True
        else:
            return False
    except:
        getlog()
        print("Có lỗi khi tải video từ web !!!")
        return False
    finally:
        if driver:
            driver.quit()

def get_download_flatform(video_url):
    if "//www.douyin.com/" in video_url:
        download_flatform = "douyin"
        root_web = "https://bravedown.com/douyin-video-downloader"
    elif "//www.facebook.com/" in video_url:
        download_flatform = "facebook"
        root_web = "https://bravedown.com/facebook-video-downloader"
    elif "//www.instagram.com/" in video_url:
        download_flatform = "instagram"
        root_web = "https://bravedown.com/instagram-video-downloader"
    elif "//www.twitter.com/" in video_url or "//twitter.com/" in video_url:
        download_flatform = "twitter"
        root_web = "https://bravedown.com/twitter-video-downloader"
    elif "//www.tiktok.com/" in video_url:
        download_flatform = "tiktok"
        root_web = "https://bravedown.com/tiktok-downloader"
    elif "//www.vimeo.com/" in video_url:
        download_flatform = "vimeo"
        root_web = "https://bravedown.com/vimeo-downloader"
    elif "//www.reddit.com/" in video_url:
        download_flatform = "reddit"
        root_web = "https://bravedown.com/reddit-downloader"
    elif "//www.dailymotion.com/" in video_url:
        download_flatform = "dailymotion"
        root_web = "https://bravedown.com/dailymotion-video-downloader"
    elif "//www.vk.com/" in video_url:
        download_flatform = "vk"
        root_web = "https://bravedown.com/vk-video-downloader"
    elif "//www.bilibili.com/" in video_url:
        download_flatform = "bilibili"
        root_web = "https://bravedown.com/bilibili-downloader"
    elif "//www.snapchat.com/" in video_url:
        download_flatform = "snapchat"
        root_web = "https://bravedown.com/snapchat-video-downloader"
    elif "baidu.com/" in video_url:
        download_flatform = "baidu"
        root_web = "https://bravedown.com/baidu-video-downloader"
    elif "www.threads.net/" in video_url:
        download_flatform = "threads"
        root_web = "https://bravedown.com/threads-downloader"
    elif "kuaishou.com/" in video_url:
        download_flatform = "kuaishou"
        root_web = "https://bravedown.com/kuaishou-video-downloader"
    else:
        if 'youtube.com/' in video_url:
            download_flatform = 'youtube'
        else:
            download_flatform = "ixigua"
        root_web = "https://bravedown.com/ixigua-video-downloader"
    return download_flatform, root_web

def download_video_by_url(url, download_folder=None, file_path=None, sleep_time=10, return_file_path=False):
    t = time()
    if not url:
        return False
    try:
        if file_path:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': file_path,
                'http_headers': {
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
                },
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        else:
            if not download_folder:
                return False
            def get_file_path(file_name):
                chars = ["/", "\\", ":", "|", "?", "*", "<", ">", "\"", "."]
                for char in chars:
                    if char in file_name:
                        file_name = file_name.replace(char, "")
                    if len(file_name) > 100:
                        file_name = file_name[:100]
                file_path = os.path.join(download_folder, f"{file_name}.mp4")
                return file_path
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': f'{download_folder}/%(title)s.%(ext)s'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', 'video')
                if title == 'video':
                    cnt = 1
                    while True:
                        file_path = os.path.join(download_folder, f"{title}_{cnt}.mp4")
                        if os.path.exists(file_path):
                            cnt += 1
                        else:
                            break
                else:
                    file_path = get_file_path(title)
                    cnt = 0
                    while True:
                        if os.path.exists(file_path):
                            cnt += 1
                            file_path = f"{file_path.split('.mp4')[0]}_{cnt}.mp4"
                        else:
                            break
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': file_path,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        t1 = time() - t
        if t1 < sleep_time:
            sleep(sleep_time-t1)
        print(f'Tải thành công video: {file_path}')
        if return_file_path:
            return file_path
        else:
            return True
    except:
        getlog()
        return None
    
def get_info_by_url(url, download_folder=None, is_download=False):
    if not url:
        return None
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'writesubtitles': True,
            'allsubtitles': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'addmetadata': False,
            'nocheckcertificate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_video = ydl.extract_info(url, download=False)
            if is_download:
                ydl.download(url)
                video_path = f"{info_video['title']}.mp4"
                video_path = os.path.join(download_folder, video_path)
                sleep(1)
                return video_path
            else:
                return info_video
    except:
        getlog()
        return None

def rename_files_by_index(folder_path, base_name="", extension=None, start_index=1):
    if not extension:
        extension = '.mp4'
    try:
        start_index = int(start_index)
    except:
        start_index = 1
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(extension)]
    files = natsorted(files)
    for index, file_name in enumerate(files, start=start_index):
        old_file_path = os.path.join(folder_path, file_name)
        if '<index>' in base_name:
            name = base_name.replace('<index>', str(index))
            new_file_name = f'{name}{extension}'
        else:
            print("Không có chuỗi <index> trong tên chung nên số thứ tự sẽ được đặt ở cuối tên file.")
            new_file_name = f"{base_name}{index}{extension}"
        new_file_path = os.path.join(folder_path, new_file_name)
        try:
            os.rename(old_file_path, new_file_path)
            print(f"Đã đổi tên {old_file_path} thành {new_file_path}")
        except:
            print(f"Đổi tên file {old_file_path} không thành công")

def remove_char_in_file_name(folder_path, chars_want_to_remove, extension=None):
    if not extension:
        extension = '.mp4'
    try:
        chars = chars_want_to_remove.split(',')
        if len(chars) == 0:
            return
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(extension)]
        files = natsorted(files)
        for i, file_name in enumerate(files):
            base_name = file_name.split(extension)[0]
            for char in chars:
                if char in base_name:
                    base_name = base_name.replace(char, "")
            old_file_path = os.path.join(folder_path, file_name)
            new_file_name = f"{base_name}{extension}"
            new_file_path = os.path.join(folder_path, new_file_name)
            try:
                os.rename(old_file_path, new_file_path)
                print(f"Đã đổi tên {old_file_path} thành {new_file_path}")
            except:
                print(f"Đổi tên file {old_file_path} không thành công")
    except:
        pass

def remove_or_move_file(input_video_path, is_delete=False, finish_folder_name='finished folder'):
    try:
        if is_delete:
            os.remove(input_video_path)
        else:
            videos_folder = os.path.dirname(input_video_path)
            finish_folder = os.path.join(videos_folder, f'{finish_folder_name}')
            os.makedirs(finish_folder, exist_ok=True)
            base_name = os.path.basename(input_video_path)
            move_file_path = os.path.join(finish_folder, base_name)
            shutil.move(input_video_path, move_file_path)
    except:
        print(f"Không thể xóa hoặc di chuyển file {input_video_path}")
        

def check_datetime_input(date_str, time_str):
    try:
        input_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        current_time_plus_30 = datetime.now() + timedelta(minutes=30)
        if input_time <= current_time_plus_30:
            print(f'Thời gian muốn đăng vào là {time_str} ngày {date_str} không hợp lệ --> Phải đăng sau 30 phút so với thời điểm hiện tại.')
            return False
        return True
    except:
        print("Định dạng giờ không đúng hh:mm")
        return False

def get_upload_date(upload_date, next_day=False):
    current_date = datetime.now().date()
    if isinstance(upload_date, str):
        try:
            upload_date = convert_date_string_to_datetime(upload_date)
        except:
            upload_date = current_date
    try:
        if upload_date <= current_date:
            upload_date = current_date
    except:
        upload_date = current_date
    if next_day and upload_date == current_date:
        upload_date = upload_date + timedelta(days=1)
    return upload_date

def get_day_gap(day_gap):
    if not day_gap:
        day_gap = "1"
    try:
        day_gap = int(day_gap.strip())
    except:
        day_gap = 1
    return day_gap

def get_number_of_days(number_of_days):
    if not number_of_days:
        number_of_days = "10"
    try:
        number_of_days = int(number_of_days.strip())
    except:
        number_of_days = 1
    return number_of_days

def convert_boolean_to_Yes_No(value):
    if value:
        return 'Yes'
    else:
        return 'No'
    
def press_esc_key(cnt=1, driver=None):
    if driver:
        for i in range(cnt):
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
            sleep(0.3)

def press_TAB_key(driver, cnt=1):
    try:
        for i in range(cnt):
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).perform()
            sleep(0.3)
    except:
        print("Không thể bấm nút TAB")

def press_SPACE_key(driver, cnt=1):
    try:
        for i in range(cnt):
            actions = ActionChains(driver)
            actions.send_keys(Keys.SPACE).perform()
            sleep(0.3)
    except:
        print("Không thể bấm nút SPACE")

def press_ENTER_key(driver, cnt=1):
    try:
        for i in range(cnt):
            actions = ActionChains(driver)
            actions.send_keys(Keys.ENTER).perform()
            sleep(0.3)
    except:
        print("Không thể bấm nút ENTER")

def input_text_to_driver(driver, text):
    """Nhập văn bản vào trình duyệt"""
    try:
        actions = ActionChains(driver)
        actions.send_keys(text).perform()
        sleep(0.5)
    except:
        print("Không thể nhập văn bản")

def press_ARROW_DOWN_key(driver, cnt=1):
    try:
        for i in range(cnt):
            actions = ActionChains(driver)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.3)
    except:
        print("Không thể bấm nút Xuống")

def press_key_on_window(key, cnt=1):
    """Bấm một phím trên Windows nhiều lần với khoảng nghỉ giữa các lần bấm."""
    try:
        for _ in range(cnt):
            keyboard.send(key)
            sleep(0.3)
    except:
        print(f"Không thể bấm nút {key.upper()}")

def get_views_text(views_ele):
    match = re.search(r'(\d+(?:\.\d+)?)([KMB]?)', views_ele)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        return f'{number}{unit}'
    return None

def get_view_count(view_count=""):
    if view_count:
        try:
            view_count = view_count.split('views')[0].strip()
            if 'B' in view_count:
                view_count = float(view_count.replace('B', '')) * 1000000000
            elif 'M' in view_count:
                view_count = float(view_count.replace('M', '')) * 1000000
            elif 'K' in view_count:
                view_count = float(view_count.replace('K', '')) * 1000
            else:
                view_count = int(float(view_count))
        except:
                getlog()
                view_count = 0
    else:
        view_count = 0
    return view_count

def get_image_from_video(videos_folder, position=None, noti=True):
    try:
        if position:
            time_position = convert_time_to_seconds(position)
        else:
            print("Hãy chọn thời điểm trích xuất ảnh từ video.")
            return
    except:
        print("Định dạng thời điểm trích xuất ảnh không hợp lệ.")
        return
    videos = os.listdir(videos_folder)
    videos = [k for k in videos if k.endswith('.mp4')]      
    if len(videos) == 0:
        if noti:
            print(f"Không tìm thấy video trong thư mục {videos_folder}")
        return
    try:
        output_folder = os.path.join(videos_folder, 'images')
        os.makedirs(output_folder, exist_ok=True)
        for i, video_file in enumerate(videos):
            video_path = os.path.join(videos_folder, video_file)
            video_name = os.path.splitext(video_file)[0]
            image_path = os.path.join(output_folder, f'{video_name}.png')
            if os.path.exists(image_path):
                continue
            video = VideoFileClip(video_path)
            if ':' in position:
                extraction_time = time_position
            else:
                extraction_time = video.duration - time_position
            if extraction_time < 0 or extraction_time > video.duration:
                print(f'Thời điểm trích xuất ảnh vượt quá thời lượng của video {video_file}. Lấy thời điểm trích xuất ở cuối video')
                extraction_time = video.duration
            frame = video.get_frame(extraction_time)
            
            imwrite(image_path, frame)
            video.close()
    except:
        getlog()
        print("Có lỗi trong quá trình trích xuất ảnh từ video !!!")

def get_time_check_cycle(time_check_string):
    try:
        time_check = int(float(time_check_string))
    except:
        time_check = 0
    return time_check * 60

def check_folder(folder):
    if not folder:
        print("Hãy chọn thư mục lưu video.")
        return False
    if not os.path.isdir(folder):
        print(f"Thư mục {folder} không tồn tại.")
        return False
    return True

def get_random_audio_path(new_audio_folder):
    audios = get_file_in_folder_by_type(new_audio_folder, file_type=".mp3", is_sort=False)
    if not audios:
        return None
    return os.path.join(new_audio_folder, random.choice(audios))
    
def get_file_in_folder_by_type(folder, file_type=".mp4", is_sort=True, noti=True):
    try:
        if not os.path.exists(folder):
            if noti:
                print(f"Thư mục {folder} không tồn tại !!!")
            return None
        list_files = os.listdir(folder)
        list_files = [k for k in list_files if k.endswith(file_type)]      
        if len(list_files) == 0:
            if noti:
                print(f"Không tìm thấy file {file_type} trong thư mục {folder} !!!")
            return None
        if is_sort:
            list_files = natsorted(list_files)
        return list_files
    except:
        return None

def move_file_from_folder_to_folder(folder1, folder2):
    try:
        for filename in os.listdir(folder1):
            folder1_file = os.path.join(folder1, filename)
            folder2_file = os.path.join(folder2, filename)
            if os.path.isfile(folder1_file):
                shutil.move(folder1_file, folder2_file)
    except:
        pass
        

#--------------------------CTK----------------------------

def choose_folder():
    folder_path = filedialog.askdirectory()
    return folder_path

def choose_file():
    file_path = filedialog.askopenfilename( title="Select a file", filetypes=(("All files", "*.*"),) )
    return file_path

def message_aks(message):
    messagebox.askquestion(title="Question", message=message)
def warning_message(message):
    messagebox.showinfo(title="WARNING", message=message)
def notification(parent=None, message=""):
    try:
        if parent:
            parent.after(0, lambda: messagebox.showinfo(title="Notification", message=message))
        else:
            messagebox.showinfo(title="Notification", message=message)
    except:
        pass

def error_message(message):
    messagebox.showinfo(title="ERROR", message=message)

def clear_widgets(root):
    for widget in root.winfo_children():
        widget.pack_forget()

def create_button_icon(frame = None, command=None, image=None, side=None, width=60):
    button = ctk.CTkButton( master=frame, text="", command=command, image=image, width=width)
    if side:
        button.pack(side=side, padx=0, pady=0)
    else:    
        button.pack(padx=0, pady=0)
    return button

def create_button(frame = None, text="", command=None, width=width_window, compound="left", anchor="center", image=None, side=None, pady=pady, padx=padx):
    button = ctk.CTkButton(master=frame, text=text, command=command, image=image, width=width, height= height_element, compound=compound, anchor=anchor, )
    if side:
        button.pack(side=side, pady=pady, padx=padx)
    else:    
        button.pack(pady=pady, padx=padx)
    return button

def create_label(frame=None, text="", compound="center", anchor="w", width=width_window, height=height_element, wraplength=None, side=None):
    if not width:
        width = width
    wraplength = width - 20
    label = ctk.CTkLabel(master=frame, text=text, width=width, height= height_element, wraplength=wraplength, anchor=anchor, compound=compound)
    if side:
        label.pack(side=side, pady=pady, padx=padx)
    else:
        label.pack(pady=pady, padx=padx)
    return label

def create_frame(frame, fill='x', side=None):
    frame = ctk.CTkFrame(master=frame, height=height_element*0.9)
    frame.pack(padx=padx, pady=pady, fill=fill, side=side)
    return frame

def create_text_input(frame, width=width_window, placeholder=None, side="right", default="", is_password=False):
    if not width:
        width = width
    if is_password:
        text_input = ctk.CTkEntry(master=frame, width=width, height=height_element*0.8, placeholder_text=placeholder, textvariable=default, show="*")
    else:
        text_input = ctk.CTkEntry(master=frame, width=width, height=height_element*0.8, placeholder_text=placeholder, textvariable=default)
    text_input.pack(pady=pady, padx=padx, side=side)
    return text_input

def create_combobox(frame, values=None, variable=None, side=RIGHT, width=width_window, height=height_element):
    val=None
    if variable:
        val = ctk.StringVar(value=str(variable))

    combobox = ctk.CTkComboBox(master=frame, values=values, variable=val, width=width, height=height)
    combobox.pack(side=side, padx=padx, pady=pady)
    return combobox

def create_frame_label_and_progress_bar(frame, text="", width=width_window, left=left, right=right):
    label = create_label(frame=frame, text=text, side=LEFT, width=width*left, compound=LEFT)
    processbar = create_progress_bar(frame=frame, width=width*right, side=RIGHT)
    return frame, processbar

def create_progress_bar(frame=None, width=width_window):
    processbar = ctk.CTkProgressBar(master=frame, width=width)
    processbar.pack(padx=padx, pady=pady)
    return processbar

def create_frame_label_input_input(root, text="", place_holder1=None, place_holder2=None, width=width_window, left=0.25, mid=0.56, right=0.19):
    frame = create_frame(root)
    label = create_label(frame=frame, text=text, side=LEFT, width=width*left, compound=LEFT, anchor='w')
    entry1 = create_text_input(frame=frame, width=width*mid, placeholder=place_holder1, side=RIGHT)
    entry2 = create_text_input(frame=frame, width=width*right, placeholder=place_holder2)
    return entry1, entry2

def create_frame_label_and_input(root, text="", place_holder=None, width=width_window, left=left, right=right, is_password=False):
    frame = create_frame(root)
    label = create_label(frame=frame, text=text, side=LEFT, width=width*left, compound=LEFT, anchor='w')
    entry = create_text_input(frame=frame, width=width*right, placeholder=place_holder, is_password=is_password)

    return entry

def create_frame_button_input_input(root,text, width=width_window, place_holder1=None, place_holder2=None, command=None, left=0.25, mid=0.56, right=0.19):
    frame = create_frame(root)
    button = create_button(frame=frame, text=text, width=width*left, side=LEFT, command=command)
    entry1 = create_text_input(frame, width=width*mid, placeholder=place_holder1, side=RIGHT)
    entry2 = create_text_input(frame, width=width*right, placeholder=place_holder2)
    return entry1, entry2

def create_frame_button_and_input(root, text, width=width_window, place_holder=None, command=None, left=left, right=right):
    frame = create_frame(root)
    button = create_button(frame=frame, text=text, width=width*left, side=LEFT, command=command)
    entry = create_text_input(frame, width=width*right, placeholder=place_holder)
    return entry

def create_frame_button_and_combobox(root, text, command=None, width=width_window, values=None, variable=None, left=left, right=right):
    frame = create_frame(root)
    button = create_button(frame=frame, text=text, width=width*left, side=LEFT, command=command)
    combobox = create_combobox(frame, width=width*right, side=RIGHT, values=values, variable=variable)
    return combobox

def create_frame_button_and_button(root, text1, text2, command1=None, command2=None, width=width_window, left=left, right=right):
    frame = create_frame(root)
    button1 = create_button(frame=frame, text=text1, width=width*left , side=LEFT, command=command1)
    button2 = create_button(frame=frame, text=text2, width=width*right -15, side=RIGHT, command=command2)
    return button1, button2

#----------------------edit video/ audio--------------------------------

def run_command_ffmpeg(command, hide=True):
    try:
        if hide:
            subprocess.run(command, check=True, text=True, encoding='utf-8', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, check=True, text=True, encoding='utf-8', stdout=subprocess.DEVNULL)
        return True
    except:
        getlog()
        return False

def run_command_with_progress(command, duration):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',
        )

        current_time = 0.0
        check=False
        for line in process.stdout:
            if 'out_time_ms=' in line:
                match = re.search(r'out_time_ms=(\d+)', line)
                if match:
                    out_time_ms = int(match.group(1))
                    current_time = out_time_ms / 1000000.0
                    percent_complete = (current_time / duration) * 100
                    sys.stdout.write(f'\rĐã xử lý: {percent_complete:.2f}%')
                    sys.stdout.flush()
                    check = True
        process.wait()
        return check
    except:
        getlog()
        return False

def get_video_info(input_file):
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate,duration',
            '-of', 'json',
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        video_info = info['streams'][0]
        width = video_info['width']
        height = video_info['height']
        duration = video_info['duration']
        r_frame_rate = video_info.get('r_frame_rate', '0/1')
        numerator, denominator = map(int, r_frame_rate.split('/'))
        fps = numerator / denominator if denominator != 0 else 0
        return {
            'width': width,
            'height': height,
            'fps': fps,
            'duration': duration
        }
    except:
        try:
            clip = VideoFileClip(input_file)
            video_info = {}
            width, height = clip.size
            duration = clip.duration
            fps = clip.fps
            clip.close()
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'duration': duration
            }
        except:
            return None

def get_audio_info(audio_path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", audio_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = json.loads(result.stdout)
    streams_info = info.get("streams", [])
    if not streams_info:
        print(f"Lỗi: Không thể tìm thấy thông tin của audio {audio_path}")
        return None
    streams_info = streams_info[0]
    return streams_info

def cut_video_by_timeline_use_ffmpeg(input_video_path, segments, is_connect='no', is_delete=False, fast_cut=True, get_audio=False):
    ti = time()
    if fast_cut:
        print("..........................")
        print("Bắt đầu cắt nhanh video...")
    else:
        print("Bắt đầu cắt video...")
    try:
        output_folder, file_name = get_output_folder(input_video_path, output_folder_name='cut_video')
        output_file_path = os.path.join(output_folder, file_name)
        temp_list_file = os.path.join(output_folder, "temp_list.txt")
        remove_file(temp_list_file)
        combine_videos = []
        video_info = get_video_info(input_video_path)
        if not video_info:
            return None, f"Không lấy được thông tin video {input_video_path}"
        duration = float(video_info['duration'])
        end = "0"
        try:
            segments = segments.split(',')
        except:
            print("Định dạng thời gian cắt là start-end với start,end là hh:mm:ss hoặc mm:ss hoặc ss")
            return None, "Có lỗi khi cắt video"
        for i, segment in enumerate(segments, start=0):
            segment = segment.strip()
            if i==0 and '-' not in segment:
                start, end = "0", segment
            elif '-' not in segment:
                start = str(end)
                end = segment
            else:
                start, end = segment.split('-')
            start = convert_time_to_seconds(start)
            end = convert_time_to_seconds(end)
            if start is None or end is None:
                print("Thời gian cắt không hợp lệ.")
                return
            if end > duration:
                end = duration
            base_name = file_name.split('.mp4')[0]
            index = 1
            if len(segments) == 1:
                segment_file_path = os.path.join(output_folder, file_name)
                if os.path.exists(segment_file_path):
                    segment_file_path = os.path.join(output_folder, f"{base_name}_{index}.mp4")
            else:
                segment_file_path = os.path.join(output_folder, f"{base_name}_{index}.mp4")
            while True:
                if os.path.exists(segment_file_path):
                    index +=1
                    segment_file_path = os.path.join(output_folder, f"{base_name}_{index}.mp4")
                else:
                    break

            if fast_cut:
                command = [
                    'ffmpeg', '-progress', 'pipe:1', '-accurate_seek', '-ss', str(start), '-i', input_video_path,
                    '-to', str(end - start), '-c:v', 'copy', '-c:a', 'copy', '-fps_mode', 'cfr',
                    '-y', segment_file_path, '-loglevel', 'quiet'
                ]
            else:
                command = [
                    'ffmpeg', '-progress', 'pipe:1', '-i', input_video_path, '-ss', str(start), '-to', str(end), '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', '-b:a', '192k', '-y', segment_file_path, '-loglevel', 'quiet'
                ]
            if not run_command_with_progress(command, duration):
                cut_video_by_moviepy(input_video_path, segment_file_path, start, end)

            if get_audio:
                download_folder = os.path.join(output_folder, "extracted_audio")
                os.makedirs(download_folder, exist_ok=True)
                extract_audio_ffmpeg(video_path=segment_file_path, download_folder=download_folder)
            if is_connect:
                combine_videos.append(segment_file_path)


        if is_connect != 'no' and len(combine_videos) > 1:
            try:
                with open(temp_list_file, 'w', encoding= 'utf-8') as f:
                    for video in combine_videos:
                        f.write(f"file '{video}'\n")
                command = connect_video(temp_list_file, output_file_path, fast_connect=is_connect == 'fast connect')
                run_command_ffmpeg(command)
                try:
                    for video in combine_videos:
                        remove_file(video)
                    remove_file(temp_list_file)
                except:
                    pass
            except:
                merge_videos_use_moviepy(videos_list=combine_videos, file_path=output_file_path, is_delete=is_delete, fps=int(video_info['fps']))
        cat = time() - ti
        print(f'---> Thời gian cắt video {input_video_path} là {int(cat)}s')
        return True, None
    except:
        return cut_video_by_timeline_use_moviepy(input_video_path, segments, is_connect, is_delete=is_delete)

        
def cut_video_by_moviepy(input_video_path, output_file_path, start, end):
    try:
        clip = VideoFileClip(input_video_path)
        sub_clip = clip.subclip(start, end)
        sub_clip.write_videofile(output_file_path, codec='libx264')
        sub_clip.close()
        clip.close()
    except:
        print(f"!!! Cắt video {input_video_path} thất bại !!!")

def cut_video_by_timeline_use_moviepy(input_video_path, segments, is_connect, is_delete=False):
    try:
        output_folder, file_name = get_output_folder(input_video_path, output_folder_name='cut_video')
        clips = []
        i = 0
        video = VideoFileClip(input_video_path)
        duration = video.duration
        try:
            segments = segments.split(',')
        except:
            print("Định dạng thời gian cắt là start-end với start,end là hh:mm:ss hoặc mm:ss hoặc ss")
            return None, "Có lỗi khi cắt video"
        for segment in segments:
            segment = segment.strip()
            start, end = segment.split('-')
            list_start = start.split(':')
            cnt = len(list_start)
            if cnt == 3:
                start = int(list_start[0]) * 3600 + int(list_start[1]) * 60 + int(list_start[2])
            elif cnt == 2:
                start = int(list_start[0]) * 60 + int(list_start[1])
            elif cnt == 1:
                start = int(list_start[0])
            else:
                message = "Định dạng thời gian cắt ở đầu video không đúng. Định dạng đúng là hh:mm:ss-hh:mm:ss hoặc mm:ss-mm:ss hoặc ss-ss"
                return False, message

            # Chuyển đổi thời gian kết thúc
            list_end = end.split(':')
            cnt = len(list_end)
            if cnt == 3:
                end = int(list_end[0]) * 3600 + int(list_end[1]) * 60 + int(list_end[2])
            elif cnt == 2:
                end = int(list_end[0]) * 60 + int(list_end[1])
            elif cnt == 1:
                end = int(list_end[0])
            else:
                message = "Định dạng thời gian cắt ở đầu video không đúng. Định dạng đúng là hh:mm:ss-hh:mm:ss hoặc mm:ss-mm:ss hoặc ss-ss"
                return False, message
            if end > duration:
                end = duration
            clip = video.subclip(start, end)
            if is_connect:
                clips.append(clip)
                sleep(1)
            else:
                i += 1
                file_path = f"{output_folder}\\{file_name}"
                clip.write_videofile(file_path, codec='libx264')
                clip.close()
                sleep(1)
        if is_connect and len(clips) > 0:
            final_clip = concatenate_videoclips(clips, method="compose")
            file_path = f"{output_folder}\\{file_name.split('.mp4')[0]}_1.mp4"
            final_clip.write_videofile(file_path, codec='libx264')
            final_clip.close()
            for clip in clips:
                clip.close()
        video.close()
        return True, None
    except Exception as e:
        if video:
            video.close()
        getlog()
        return False, "Có lỗi trong quá trình cắt video."


def merge_videos_use_ffmpeg(videos_folder, file_name=None, is_delete=False, videos_path=None, fast_combine=True):
    ti = time()
    if fast_combine:
        print("..........................")
        print("Bắt đầu nối nhanh video...")
    else:
        print("Bắt đầu nối video...")

    temp_file_path = os.path.join(videos_folder, "temp.txt")
    max_fps = 24
    if not videos_path:
        videos = get_file_in_folder_by_type(videos_folder)
        if not videos:
            return
        if len(videos) <= 1:
            return False, "Phải có ít nhất 2 video trong videos folder"
        videos_path = []
        with open(temp_file_path, 'w') as f:
            for video in videos:
                if video.endswith('.mp4'):
                    video_path = os.path.join(videos_folder, video)
                    video_info = get_video_info(video_path)
                    if not video_info:
                        warning_message(f"Dừng gộp video vì không lấy được thông tin từ video {video_path}")
                        return
                    fps = video_info['fps']
                    if fps > max_fps:
                        max_fps = fps
                    f.write(f"file '{video_path}'\n")
                    videos_path.append(video_path)
    else:
        with open(temp_file_path, 'w') as f:
            for video_path in videos_path:
                video_info = get_video_info(video_path)
                if not video_info:
                    warning_message(f"Dừng gộp video vì không lấy được thông tin từ video {video_path}")
                    return
                fps = video_info['fps']
                if fps > max_fps:
                    max_fps = fps
                if video_path.endswith('.mp4'):
                    f.write(f"file '{video_path}'\n")
        
    output_folder = f"{videos_folder}\\merge_videos"
    os.makedirs(output_folder, exist_ok=True)
    if file_name:
        file_path = f"{output_folder}\\{file_name}.mp4"
    else:
        file_path = f"{output_folder}\\merge_video.mp4"
    command = connect_video(temp_file_path, file_path, fast_connect=fast_combine, max_fps=max_fps)
    try:
        run_command_ffmpeg(command)
        try:
            remove_file(temp_file_path)
            if is_delete:
                for video_path in videos_path:
                    remove_file(video_path)
        except:
            pass
        noi = time() - ti
        print(f'Tổng thời gian nối là {noi}')
        return True, f"Gộp video thành công vào file {file_path}"
    except:
        merge_videos_use_moviepy(videos_folder, file_path, is_delete, fps=max_fps)
        noi = time() - ti
        print(f'Tổng thời gian nối là {noi}')

def merge_audio_use_ffmpeg(videos_folder, file_name=None, fast_combine=True):
    if fast_combine:
        print("..........................")
        print("Bắt đầu nối nhanh audio...")
    else:
        print("Bắt đầu nối audio...")

    temp_file_path = os.path.join(videos_folder, "temp.txt")
    audios = get_file_in_folder_by_type(videos_folder, file_type=".mp3")
    if not audios:
        return
    if len(audios) <= 1:
        return False, "Phải có ít nhất 2 video trong videos folder"
    with open(temp_file_path, 'w') as f:
        for audio in audios:
            if audio.endswith('.mp3'):
                audio_path = os.path.join(videos_folder, audio)
                f.write(f"file '{audio_path}'\n")
    output_folder = f"{videos_folder}\\merge_audios"
    os.makedirs(output_folder, exist_ok=True)
    if file_name:
        file_path = f"{output_folder}\\{file_name}.mp3"
    else:
        file_path = f"{output_folder}\\merge_audio.mp3"
    command = connect_audio(temp_file_path, file_path, fast_connect=fast_combine)
    try:
        if run_command_ffmpeg(command):
            try:
                remove_file(temp_file_path)
            except:
                pass
            return True, f"Gộp audio thành công vào file {file_path}"
    except:
        getlog()
    return False, "Có lỗi khi gộp audio"

def merge_videos_use_moviepy(videos_folder, file_path=None, is_delete=False, videos_list=None, fps=30):
    try:
        if videos_list:
            edit_videos = videos_list
        else:
            edit_videos = get_file_in_folder_by_type(videos_folder)
            if not edit_videos:
                return
            if len(edit_videos) <= 1:
                warning_message("Phải có ít nhất 2 video trong videos folder")
                return
        output_folder = f'{videos_folder}\\merge_videos'
        os.makedirs(output_folder, exist_ok=True)
        clips = []
        remove_videos = []
        for i, video_file in enumerate(edit_videos):
            video_path = f'{videos_folder}\\{video_file}'
            remove_videos.append(video_path)
            clip = VideoFileClip(video_path)
            clips.append(clip)
        if len(clips) > 0:
            final_clip = concatenate_videoclips(clips, method="compose")
            if not file_path:
                file_path = f"{output_folder}\\combine_video.mp4"
            final_clip.write_videofile(file_path, codec='libx264', fps=fps)
            final_clip.close()
            for clip in clips:
                clip.close()
            for clip in clips:
                clip.close()
        for video_path in remove_videos:
            remove_or_move_file(video_path, is_delete=is_delete)
    except:
        print(f"Có lỗi khi nối video !!!")


def connect_video(temp_file_path, output_file_path, fast_connect=True, max_fps=None):
    if fast_connect:
        print("---> đang nối nhanh video...")
        command = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file_path, 
            '-vf', 'fps=30', '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', 
            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-y', output_file_path, '-loglevel', 'quiet'
        ]
    else:
        print("---> đang nối video...")
        if max_fps:
            command = [
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file_path, '-c:v', 'libx264', '-c:a', 'aac', '-r', f'{max_fps}', '-y', output_file_path, '-loglevel', 'quiet'
            ]
        else:
            command = [
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file_path, '-c:v', 'libx264', '-c:a', 'aac', '-y', output_file_path, '-loglevel', 'quiet'
            ]
    return command

def connect_audio(temp_file_path, output_file_path, fast_connect=True):
    if fast_connect:
        print("---> đang nối nhanh audio...")
        command = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file_path, 
            '-c:a', 'libmp3lame', '-b:a', '192k', '-y', output_file_path, '-loglevel', 'quiet'
        ]
    else:
        print("---> đang nối audio...")
        command = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file_path, 
            '-c:a', 'libmp3lame', '-b:a', '192k', '-y', output_file_path, '-loglevel', 'quiet'
        ]
    return command


def get_index_of_temp_file (input_path):
    return int(input_path.split('temp')[-1].split('.mp4')[0])
    
def strip_first_and_end_video(clip, first_cut, end_cut):
    try:
        first_cut = int(first_cut)
    except:
        first_cut = 0
    try:
        end_cut = int(end_cut)
    except:
        end_cut = 0

    if first_cut < 0:
        first_cut = 0
    if end_cut < 0 or end_cut >= clip.duration:
        warning_message("Thời gian cắt video không hợp lệ.")
        return None
    return clip.subclip(first_cut, clip.duration - end_cut)

def zoom_and_crop(clip, zoom_factor, vertical_position='center', horizontal_position='center'):
    resized_clip = clip.resize(zoom_factor)
    new_width, new_height = resized_clip.size
    y1, y2 = 0, new_height
    x1, x2 = 0, new_width
    if vertical_position == 'center':
        y1 = (new_height - clip.h) // 2
        y2 = y1 + clip.h
    elif vertical_position == 'top':
        y1 = 0
        y2 = clip.h
    elif vertical_position == 'bottom':
        y1 = new_height - clip.h
        y2 = new_height
    if horizontal_position == 'center':
        x1 = (new_width - clip.w) // 2
        x2 = x1 + clip.w
    elif horizontal_position == 'left':
        x1 = 0
        x2 = clip.w
    elif horizontal_position == 'right':
        x1 = new_width - clip.w
        x2 = new_width
    cropped_clip = resized_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
    return cropped_clip

def apply_zoom(clip, zoom_factor, vertical_position, horizontal_position):
    if not zoom_factor:
        return clip
    zoom_factor = float(zoom_factor)
    if zoom_factor < 0 or zoom_factor > 3:
        warning_message('Tỷ lệ zoom không hợp lệ.')
        return None
    return zoom_and_crop(clip, zoom_factor, vertical_position, horizontal_position)

def zoom_video_random_intervals(clip, max_zoom_size, vertical_position='center', horizontal_position='center', is_random_zoom="3-5"):
    try:
        min_time_to_change_zoom, max_time_to_change_zoom = is_random_zoom.split('-')
        min_time_to_change_zoom = int(float(min_time_to_change_zoom.strip()))
        max_time_to_change_zoom = int(float(max_time_to_change_zoom.strip()))
    except:
        print("Thời gian zoom ngẫu nhiên không phù hợp !!!")
        return None
    try:
        max_zoom_size = float(max_zoom_size)
    except:
        print("Tỷ lệ zoom không đúng định dạng số !!!")
        return None
    if max_time_to_change_zoom > clip.duration:
        max_time_to_change_zoom = clip.duration
    start_times = []
    current_time = 0
    while current_time < clip.duration:
        start_times.append(current_time)
        current_time += random.uniform(min_time_to_change_zoom, max_time_to_change_zoom)
    if start_times[-1] < clip.duration:
        start_times.append(clip.duration)
    zoom_factors = []
    last_zoom_factor = None
    for _ in range(len(start_times) - 1):
        while True:
            new_zoom = round(random.uniform(1.01, max_zoom_size), 2)
            if new_zoom != last_zoom_factor:
                zoom_factors.append(new_zoom)
                last_zoom_factor = new_zoom
                break
    zoomed_clips = []
    try:
        for i, start_time in enumerate(start_times[:-1]):
            end_time = start_times[i + 1]
            sub_clip = clip.subclip(start_time, end_time)
            zoomed_clip = apply_zoom(sub_clip, zoom_factors[i], vertical_position, horizontal_position)
            zoomed_clips.append(zoomed_clip)
    
        final_zoom_clip = concatenate_videoclips(zoomed_clips, method="compose")
        return final_zoom_clip
    except Exception as e:
        getlog()
        return None

def speed_up_clip(clip, speed):
    speed = float(speed)
    if speed < 0 or speed > 3:
        warning_message('invalid speed up')
        return None
    fff = MultiplySpeed(speed)
    sped_up_clip = fff.apply(clip)
    return sped_up_clip

def get_clip_ratio(clip, tolerance=0.02):  #Kiểm tra video thuộc tỷ lệ 16:9 hay 9:16
    clip_width, clip_height = clip.size
    ratio = clip_width / clip_height
    if abs(ratio - (16/9)) < tolerance:  # Kiểm tra xem tỷ lệ gần bằng 16:9
        return (16,9)
    elif abs(ratio - (9/16)) < tolerance:  # Kiểm tra xem tỷ lệ gần bằng 9:16
        return (9,16)
    else:
        return None
    
def resize_clip(clip, re_size=0.999):
    try:
        target_ratio = get_clip_ratio(clip)
        clip_width, clip_height = clip.size
        if target_ratio:
            target_width, target_height = target_ratio
            if clip_width / clip_height != target_width / target_height:
                clip_width = clip_height * target_width / target_height
            
            width = int(clip_width * re_size)
            height = int(clip_height * re_size)
            try:
                clip = resize(clip, newsize=(width, height))
            except:
                ratio = clip_width/clip_height
                new_height = 720/ratio
                clip = resize(clip, newsize=(720, new_height))
        else:
            ratio = clip_width/clip_height
            new_height = 720/ratio
            clip = resize(clip, newsize=(720, new_height))
        return clip
    except:
        getlog()
        return None

def flip_clip(clip):
    # Áp dụng hiệu ứng đối xứng (flip) theo chiều ngang
    flipped_clip = mirror_x(clip)
    return flipped_clip

def increase_video_quality(input_path, output_path): #Tăng chất lượng video
    try:
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', 'unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=1.5,'
                    'eq=contrast=1.2:saturation=1.2',  # Tăng cường độ sắc nét và điều chỉnh độ tương phản
            '-c:a', 'copy', '-y',  # Sao chép âm thanh gốc
            output_path 
        ]
        subprocess.run(ffmpeg_command, check=True)
        print(f"Xử lý tăng độ phân giải thành công: \n{output_path}")
        return True
    except:
        print(f"Có lỗi trong quá trình tăng chất lượng video: \n{input_path}")
        return False
    
def add_watermark_by_ffmpeg(video_width, video_height, horizontal_watermark_position, vertical_watermark_position):
    try:
        if horizontal_watermark_position == 'center':
            horizontal_watermark_position = 50
        elif horizontal_watermark_position == 'left':
            horizontal_watermark_position = 0
        elif horizontal_watermark_position == 'right':
            horizontal_watermark_position = 100
        else:
            try:
                horizontal_watermark_position = float(horizontal_watermark_position)
                if horizontal_watermark_position > 100:
                    horizontal_watermark_position = 100
                elif horizontal_watermark_position < 0:
                    horizontal_watermark_position = 0
            except:
                horizontal_watermark_position = 50
        if vertical_watermark_position == 'center':
            vertical_watermark_position = 50
        elif vertical_watermark_position == 'top':
            vertical_watermark_position = 0
        elif vertical_watermark_position == 'bottom':
            vertical_watermark_position = 100
        else:
            try:
                vertical_watermark_position = float(vertical_watermark_position)
                if vertical_watermark_position > 100:
                    vertical_watermark_position = 100
                elif vertical_watermark_position < 0:
                    vertical_watermark_position = 0
            except:
                vertical_watermark_position = 50
        watermark_x = int(video_width * horizontal_watermark_position / 100)
        watermark_y = int(video_height * vertical_watermark_position / 100)
        return watermark_x, watermark_y
    except:
        return None, None

def add_image_watermark_into_video(clip, top_bot_overlay_height='2,2', left_right_overlay_width='2,2', watermark=None, vertical_watermark_position=0, horizontal_watermark_position=0, watermark_scale='1,1'):
    w, h = clip.size
    try:
        if not top_bot_overlay_height:
            top_bot_overlay_height = '2,2'
        top_overlay_height, bot_overlay_height = top_bot_overlay_height.split(',')
        if not top_overlay_height or int(top_overlay_height) < 0 or int(top_overlay_height) >= h:
            top_overlay_height = 2
        else:
            top_overlay_height = int(top_overlay_height)
        if not bot_overlay_height or int(bot_overlay_height) < 0 or int(bot_overlay_height) >= (h-top_overlay_height):
            bot_overlay_height = 2
        else:
            bot_overlay_height = int(bot_overlay_height)
    except:
        print("kích thước lớp phủ trên và dưới đã nhập không hợp lệ, lấy kích thước lớp phủ mặc định là 2")
        bot_overlay_height = top_overlay_height = 2

    try:
        if not left_right_overlay_width:
            left_right_overlay_width = '2,2'
        left_overlay_width, right_overlay_width = left_right_overlay_width.split(',')
        if not left_overlay_width or int(left_overlay_width) < 0 or int(left_overlay_width) >= w:
            left_overlay_width = 2
        else:
            left_overlay_width = int(left_overlay_width)
        if not right_overlay_width or int(right_overlay_width) < 0 or int(right_overlay_width) >= (w - left_overlay_width):
            right_overlay_width = 2
        else:
            right_overlay_width = int(right_overlay_width)
    except:
        print("kích thước lớp phủ trái và phải đã nhập không hợp lệ, lấy kích thước lớp phủ mặc định là 2")
        left_overlay_width = right_overlay_width = 2

    try:
        width, height = clip.size
        top_image = ColorClip(size=(width, top_overlay_height), color=(0, 0, 0)).set_position(('center', 0)).set_duration(clip.duration)
        bottom_image = ColorClip(size=(width, bot_overlay_height), color=(0, 0, 0)).set_position(('center', height - bot_overlay_height)).set_duration(clip.duration)
        left_image = ColorClip(size=(left_overlay_width, height), color=(0, 0, 0)).set_position((0, 'center')).set_duration(clip.duration)
        right_image = ColorClip(size=(right_overlay_width, height), color=(0, 0, 0)).set_position((width - right_overlay_width, 'center')).set_duration(clip.duration)

        if watermark:
            try:
                scale_w, scale_h = [float(s) for s in watermark_scale.split(',')]
            except:
                scale_w = scale_h = 1.0
            watermark_image = ImageClip(watermark).set_duration(clip.duration)
            watermark_width, watermark_height = watermark_image.size
            scaled_width = int(watermark_width * scale_w)
            scaled_height = int(watermark_height * scale_h)

            watermark_image = watermark_image.resize((scaled_width, scaled_height))
            if horizontal_watermark_position == 'center':
                horizontal_watermark_position = (width - scaled_width) / 2
            elif horizontal_watermark_position == 'left':
                horizontal_watermark_position = 0
            elif horizontal_watermark_position == 'right':
                horizontal_watermark_position = width - scaled_width
            else:
                try:
                    horizontal_watermark_position = int(float(horizontal_watermark_position) * width / 100)
                except ValueError:
                    horizontal_watermark_position = (width - scaled_width) / 2

            if vertical_watermark_position == 'center':
                vertical_watermark_position = (height - scaled_height) / 2
            elif vertical_watermark_position == 'top':
                vertical_watermark_position = 0
            elif vertical_watermark_position == 'bottom':
                vertical_watermark_position = height - scaled_height
            else:
                try:
                    vertical_watermark_position = int(float(vertical_watermark_position) * height / 100)
                except ValueError:
                    vertical_watermark_position = (height - scaled_height) / 2

            watermark_image = watermark_image.set_position((horizontal_watermark_position, vertical_watermark_position))
            final_clip = CompositeVideoClip([clip, top_image, bottom_image, left_image, right_image, watermark_image])
        else:
            final_clip = CompositeVideoClip([clip, top_image, bottom_image, left_image, right_image])
        return final_clip

    except Exception as e:
        print(f"Lỗi khi thêm watermark: {e}")
        return None

def convert_video_169_to_916(input_video_path, zoom_size=None, resolution="1080x1920", is_delete=False):
    try:
        output_folder, file_name = get_output_folder(input_video_path, output_folder_name='converted_videos')
        output_file_path = os.path.join(output_folder, file_name)
        video = VideoFileClip(input_video_path)
        width, height = video.size
        if not zoom_size:
            zoom_size = 0.9
        else:
            zoom_size = float(zoom_size)
        target_width, target_height = list(map(int, resolution.split('x')))
        video_display_height = target_height * zoom_size
        zoom = video_display_height / height
        zoomed_video = video.resize(newsize=(int(width * zoom), int(height * zoom)))
        zoomed_width, zoomed_height = zoomed_video.size
        background = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=video.duration)
        x_pos = (target_width - zoomed_width) / 2
        y_pos = (target_height - zoomed_height) / 2
        final_video = CompositeVideoClip([background, zoomed_video.set_position((x_pos, y_pos))], size=(target_width, target_height))
        final_video.write_videofile(output_file_path, codec='libx264', audio_codec='aac')
        final_video.close()
        zoomed_video.close()
        video.close()
        remove_or_move_file(input_video_path, is_delete=is_delete)
        return True
    except Exception as e:
        getlog()
        return False
    
def convert_video_916_to_169(input_video_path, resolution="1920x1080", is_delete=False):
    try:
        if not resolution:
            resolution = '1920x1080'
        resolution = resolution.split('x')
        output_folder, file_name = get_output_folder(input_video_path, output_folder_name='converted_videos')
        output_file_path = os.path.join(output_folder, file_name)
        video = VideoFileClip(input_video_path)
        input_width, input_height = video.size
        new_height = input_width * 9 / 16
        if new_height <= input_height:
            y1 = (input_height - new_height) / 2
            y2 = y1 + new_height
            cropped_video = video.crop(x1=0, x2=input_width, y1=y1, y2=y2)
        else:
            new_width = input_height * 16 / 9
            black_bar = ColorClip(size=(int(new_width), input_height), color=(0, 0, 0))
            video = video.set_position(("center", "center"))
            cropped_video = CompositeVideoClip([black_bar, video]).set_duration(video.duration)
        resized_video = cropped_video.resize(newsize=(resolution[0], resolution[1]))
        resized_video.write_videofile(output_file_path, codec='libx264', audio_codec='aac')
        resized_video.close()
        video.close()
        sleep(1)
        remove_or_move_file(input_video_path, is_delete=is_delete)
        return True
    except:
        getlog()
        return False

def get_and_adjust_resolution_from_clip(clip, scale_factor=0.997):
    width = int(clip.size[0] * scale_factor)
    height = int(clip.size[1] * scale_factor)
    resized_video = clip.resize((width, height))
    return resized_video

def check_vietnamese_characters(filename):
    vietnamese_pattern = re.compile(
        r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
        r'ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]'
    )
    return bool(vietnamese_pattern.search(filename))

def remove_audio_from_clip(clip):
    return clip.without_audio()

def set_audio_for_clip(clip, background_music, background_music_volume="10"):
    try:
        volume = float(background_music_volume)/100
        background_music = AudioFileClip(background_music)
        background_music = background_music.volumex(volume)
        background_music = afx.audio_loop(background_music, duration=clip.duration)
        current_audio = clip.audio
        if current_audio is None:
            clip = clip.set_audio(background_music)
        else:
            combined_audio = CompositeAudioClip([current_audio, background_music])
            clip = clip.set_audio(combined_audio)
        return clip
    except:
        print("Có lỗi ghi ghép audio vào video")

def edit_audio_ffmpeg(input_audio_folder, start_cut="0", end_cut="0", pitch_factor=None, speed=None, cut_silence=False, aecho=None, flanger='8', chorus='0.05'):
    try:
        speed = get_float_data(speed)
        if not speed:
            speed = 1
        if aecho:
            aecho = get_float_data(aecho)
            if not aecho:
                print("Thời gian thiết lập tạo tiếng vang cho audio không hợp lệ --> Không áp dụng tạo tiếng vang")
        pitch_factor = get_float_data(pitch_factor)
        if not pitch_factor:
            print("Cao độ không hợp lệ --> Đặt về 1")
            pitch_factor = 1.0
        try:
            start_cut = float(start_cut)
            end_cut = float(end_cut)
        except:
            print("Giá trị của start_cut và end_cut không hợp lệ. Đặt về 0.")
            start_cut = end_cut = 0

        audios = get_file_in_folder_by_type(input_audio_folder, ".mp3")
        if not audios:
            return
        for audio in audios:
            input_audio_path = os.path.join(input_audio_folder, audio)
            audio_info = get_audio_info(input_audio_path)
            if not audio_info:
                return
            duration = float(audio_info.get("duration", 0))
            if start_cut + end_cut >= duration:
                print("Thời gian cắt không hợp lệ. Đảm bảo rằng start_cut và end_cut không lớn hơn thời gian của audio.")
                return
            cut_duration = duration - start_cut - end_cut
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
                temp_audio_path = temp_audio_file.name
            ffmpeg_cmd_cut = [
                "ffmpeg", "-y",
                '-loglevel', 'quiet',
                "-ss", str(start_cut),
                "-i", input_audio_path,
                "-t", str(cut_duration),
                "-c:a", "copy",
                temp_audio_path
            ]
            if not run_command_ffmpeg(ffmpeg_cmd_cut):
                print(f"Lỗi khi xử lý audio {input_audio_path}!")
                return
            streams_info = get_audio_info(temp_audio_path)
            if not streams_info:
                return
            output_audio_folder, file_name = get_output_folder(input_audio_path, output_folder_name="edited_audios")
            output_audio_path = os.path.join(output_audio_folder, file_name)
            metadata = {"artist": "None", "album": "None", "title": "None", "encoder": "FFmpeg 6.0"}
            original_sample_rate = int(streams_info.get("sample_rate", 0))
            sample_rate = 44100 if original_sample_rate == 48000 else 48000
            original_bitrate = streams_info.get("bit_rate", "192k")
            bitrate = "256k" if original_bitrate == "192000" else "192k"
            channels = 1 if streams_info.get("channels") == 2 else 2
            volume = "4dB"
            eq_adjust = "equalizer=f=120:width_type=h:width=300:g=7, equalizer=f=1000:width_type=h:width=300:g=-1"
            ffmpeg_cmd_adjust = ["ffmpeg", '-loglevel', 'quiet', "-y", "-i", temp_audio_path]
            for key, value in metadata.items():
                ffmpeg_cmd_adjust += ["-metadata", f"{key}={value}"]
            ffmpeg_cmd_adjust += ["-ar", str(sample_rate), "-b:a", bitrate, "-ac", str(channels)]
            filters = [f"volume={volume}", eq_adjust]
            if speed != 1.0:
                filters.append(f"atempo={speed}")
            if cut_silence:
                filters.append("silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB")
            # Áp dụng hiệu ứng tùy chọn
            if pitch_factor != 1.0:
                filters.append(f"rubberband=pitch={pitch_factor}")
            if flanger:
                filters.append(f"flanger=delay={flanger}:depth=3:regen=-9:width=77:speed=0.7")
            if aecho:
                filters.append(f"aecho=0.8:0.9:{aecho}:0.2")
            if chorus:
                filters.append(f"chorus=0.8:0.9:50:{chorus}:{chorus}:3")

            if filters:
                ffmpeg_cmd_adjust += ["-af", ",".join(filters)]
            ffmpeg_cmd_adjust += ["-c:a", "libmp3lame", output_audio_path]
            if run_command_ffmpeg(ffmpeg_cmd_adjust):
                print(f"Chỉnh sửa thông tin audio thành công: {output_audio_path}")
            else:
                print(f"Lỗi khi thay đổi thông tin audio !!!")
            os.remove(temp_audio_path)
    except:
        print("Có lỗi trong quá trình chỉnh sửa audio !!!")

def extract_audio_ffmpeg(audio_path=None, video_path=None, video_url=None, video_folder=None, segments=None, download_folder=None, file_type='wav', speed='1.0'):
    try:
        if not segments:
            segments = "0-999999999999"
        try:
            segments = segments.split(',')
        except:
            print("Định dạng thời gian cắt là start-end với start,end là hh:mm:ss hoặc mm:ss hoặc ss")
            return
        try:
            speed = float(speed)
        except:
            speed = 1.0

        if video_url:
            video_path = download_video_by_url(video_url, download_folder, return_file_path=True)

        for segment in segments:
            segment = segment.strip()
            start, end = segment.split('-')
            start = convert_time_to_seconds(start)
            if start is None:
                return
            end = convert_time_to_seconds(end)
            if end is None:
                return
            target_paths = []
            if audio_path:
                target_path = audio_path
            elif video_path:
                target_path = video_path
            elif video_folder:
                videos =  get_file_in_folder_by_type(video_folder, ".mp4")   
                if not videos:
                    return
                for video in videos:
                    video_path = os.path.join(video_folder, video)
                    target_paths.append(video_path)
            else:
                warning_message("Vui lòng chọn nguồn để edit video")
                return
            if video_url or audio_path or video_path:
                target_paths.append(target_path)

            output_folder = os.path.join(os.path.dirname(target_path), 'extract_audios')
            os.makedirs(output_folder, exist_ok=True)
            for target_path in target_paths:
                video_clip = None
                if '.wav' in target_path or '.mp3' in target_path:
                    audio_clip = AudioFileClip(target_path)
                else:
                    video_clip = VideoFileClip(target_path)
                    audio_clip = video_clip.audio
                duration = audio_clip.duration
                if end > duration:
                    end = duration
                file_name = os.path.basename(target_path)
                audio_name = file_name.split('.')[0]
                cnt_cut = 1
                while True:
                    output_audio_path = f'{output_folder}/{audio_name}_{cnt_cut}.{file_type}'
                    if os.path.exists(output_audio_path):
                        cnt_cut += 1
                    else:
                        break
                try:
                    ffmpeg_cmd = [ "ffmpeg", "-y", "-i", target_path, "-ss", str(start), "-to", str(end), "-ac", "1", "-ar", "24000", "-filter:a", f"atempo={speed}", "-sample_fmt", "s16", output_audio_path ]
                    run_command_ffmpeg(ffmpeg_cmd)
                except:
                    getlog()
                    print(f'Có lỗi trong khi trích xuất audio')
                    
                if audio_clip:
                    audio_clip.close()
                if video_clip:
                    video_clip.close()
                print(f"  --> Trích xuất thành công audio từ video {target_path}")
        if video_url:
            remove_file(video_path)
    except:
        getlog()
        print("Có lỗi trong quá trình trích xuất audio !!!")


def edit_video_level_2(input_video_path, text_top_input=None, text_bottom_input=None, wave_amplitude=1.2, wave_frequency=0.1, line_spacing=10, line_thickness=1, line_opacity=0.1):
    if not input_video_path:
        return None
    print(f'\nXử lý cấp độ 2 cho video: {input_video_path}')
    try:
        temp_video = process_video(
                    input_video_path,
                    wave_amplitude=wave_amplitude,    # Biên độ gợn sóng (càng cao, sóng càng mạnh)
                    wave_frequency=wave_frequency, # Tần suất gợn sóng
                    line_spacing=line_spacing,     # Khoảng cách giữa các đường gạch ngang
                    line_thickness=line_thickness,    # Độ dày của đường gạch ngang
                    line_opacity=line_opacity,     # Độ mờ của đường gạch ngang (0.0 - 1.0)
                    text_top_input=text_top_input,
                    text_bottom_input=text_bottom_input
                )
        if temp_video:
            output_video_path = merge_audio(temp_video, input_video_path)
            remove_file(temp_video)
            return output_video_path
    except:
        getlog()
    return None



def process_video(input_path, wave_amplitude=3, wave_frequency=0.05, 
                  line_spacing=10, line_thickness=5, line_opacity=0.7,
                  text_top_input="", text_bottom_input=""):
    curr_folder = os.path.dirname(input_path)
    out_path = os.path.join(curr_folder, 'temp.mp4')
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Không thể mở video!")
        return None

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    print(f'{fps} - {width}x{height}')
    total_frames = get_total_frames(input_path)
    snow_particles = [
        (np.random.randint(0, width), np.random.randint(0, height), np.random.randint(1, 3))
        for _ in range(150)
    ]
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = add_effects(frame, frame_idx, wave_amplitude, wave_frequency, line_spacing, line_opacity, line_thickness, total_frames, text_top_input, text_bottom_input, fps=fps, snow_particles=snow_particles)
        out.write(processed_frame)
        frame_idx += 1
    
    cap.release()
    out.release()
    print("Xử lý video hoàn tất!")
    return out_path

def draw_multiline_text(image, text, font, scale, color, thickness, start_x, start_y, line_spacing=70):
    words, lines, current_line = text.split(), [], ""
    
    for word in words:
        test_line = f"{current_line} {word}" if current_line else word
        if cv2.getTextSize(test_line, font, scale, thickness)[0][0] < image.shape[1] - 100:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    for i, line in enumerate(lines):
        y = start_y + i * line_spacing
        x = (image.shape[1] - cv2.getTextSize(line, font, scale, thickness)[0][0]) // 2
        cv2.putText(image, line, (x, y), font, scale, color, thickness, cv2.LINE_AA)


# def add_effects(frame, frame_idx, wave_amplitude, wave_frequency, line_spacing, line_opacity,
#                 line_thickness, total_frames, text_top_input=None, text_bottom_input=None, fps=28, snow_particles=[]):
#     height, width, _ = frame.shape
#     transformed_frame = frame.copy()
    
#     fade_in_duration, fade_out_start = int(total_frames * 0.06), int(total_frames * 0.94)
    
#     if frame_idx < fade_in_duration:
#         fade_factor = frame_idx / fade_in_duration
#     elif frame_idx > fade_out_start:
#         fade_factor = 1 - (frame_idx - fade_out_start) / fade_in_duration
#     else:
#         fade_factor = None
    
#     if fade_factor is not None:
#         transformed_frame = cv2.addWeighted(frame, fade_factor, np.zeros_like(frame), 1 - fade_factor, 0)


#     # 2. Chỉnh độ sáng và độ tương phản (cố định)
#     alpha, beta = 1.06, 20
#     transformed_frame = cv2.convertScaleAbs(transformed_frame, alpha=alpha, beta=beta)
    
#     # 3. Biến đổi màu sắc
#     hsv = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2HSV)
#     hsv[..., 1] = np.clip(hsv[..., 1] * 1.10, 0, 255)  # Bão hòa nhẹ hơn
#     transformed_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
#     # 4. Hiệu ứng gợn sóng (giảm biên độ)
#     for i in range(height):
#         offset = int(wave_amplitude * 0.5 * np.sin(2 * np.pi * wave_frequency * (i + frame_idx) / height))
#         transformed_frame[i] = np.roll(transformed_frame[i], offset, axis=0)

#     # Thêm đường vạch ngang
#     overlay = transformed_frame.copy()
#     for i in range(0, height, line_spacing):
#         cv2.line(overlay, (0, i), (width, i), (150, 150, 150), line_thickness)
#     cv2.addWeighted(overlay, line_opacity, transformed_frame, 1 - line_opacity, 0, transformed_frame)

#     # # 1. Hiệu ứng biến dạng nhiệt (heat distortion) - tăng tốc bằng NumPy vector hóa
#     def generate_noise_map_vectorized(width, height, time_offset, scale=60.0):
#         x = np.linspace(0, width / scale, width, endpoint=False)
#         y = np.linspace(0, height / scale, height, endpoint=False) + time_offset
#         xv, yv = np.meshgrid(x, y)
#         noise_func = np.vectorize(lambda a, b: pnoise2(a, b, octaves=2))
#         noise_map = noise_func(xv, yv).astype(np.float32)
#         return cv2.normalize(noise_map, None, 0, 1, cv2.NORM_MINMAX)

#     # ==== Điều khiển sóng nhiệt theo FPS và thời gian thực ====
#     heat_scale = 60.0
#     base_strength = 20.0
#     heat_speed = 0.04  # tốc độ trôi của noise

#     # --- Cấu hình thời gian ---
#     cooldown_sec = 0.1   # 1s nghỉ
#     active_sec = 4.0     # 2s hiệu ứng

#     period = int((cooldown_sec + active_sec) * fps)  # Tổng chu kỳ theo frame
#     active_frames = int(active_sec * fps)            # Số frame có hiệu ứng

#     # Tính phase (0 → 2π trong mỗi chu kỳ)
#     phase = (frame_idx % period) / active_frames * np.pi  # scale riêng cho đoạn active

#     # Tạo sóng mượt nếu đang trong vùng active
#     if (frame_idx % period) < active_frames:
#         # Sóng nửa chu kỳ sin: 0 → π → tạo dạng mượt
#         strength_factor = np.sin(phase)  # từ 0 → 1 → 0
#         heat_strength = base_strength * strength_factor

#         # Sinh noise và áp hiệu ứng nếu strength đủ lớn
#         if heat_strength > 0.1:
#             noise_map = generate_noise_map_vectorized(width, height, frame_idx * heat_speed, scale=heat_scale)
#             dy = (noise_map - 0.5) * heat_strength
#             map_x = np.tile(np.arange(width, dtype=np.float32), (height, 1))
#             map_y = np.clip(np.add(np.arange(height).reshape(-1, 1), dy), 0, height - 1).astype(np.float32)
#             transformed_frame = cv2.remap(transformed_frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
        
#     # ==== Xoáy nhẹ khung hình (wave + scale xoay) ====
#     center = (width // 2, height // 2)
#     # Dao động góc nhỏ và mượt hơn (±1.2 độ, chu kỳ ~4s nếu 30fps)
#     angle = 4 * np.sin(2 * np.pi * frame_idx / (fps * 8))
#     # Scale nhẹ hơn, chu kỳ dài hơn để tránh chóng mặt
#     scale = 1.0 + 0.004 * np.sin(2 * np.pi * frame_idx / (fps * 5))
#     # Ma trận biến đổi
#     M = cv2.getRotationMatrix2D(center, angle, scale)
#     transformed_frame = cv2.warpAffine(transformed_frame, M, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

#     # ==== Mưa / Tuyết rơi nhẹ ====
#     for x, y0, radius in snow_particles:
#         y = (y0 + frame_idx * 2) % height  # chuyển động rơi theo thời gian
#         cv2.circle(transformed_frame, (x, y), radius, (255, 255, 255), -1)

#     # 5. Đường lưới máy ảnh
#     overlay = transformed_frame.copy()  # tạo lớp overlay để vẽ lưới
#     grid_color_outer = (0, 0, 0)       # Viền ngoài: đen
#     grid_color_inner = (255, 191, 0)   # Lưới chính: vàng sáng
#     # Vẽ viền ngoài đậm
#     for i in range(1, 5):
#         cv2.line(overlay, (0, i * height // 5), (width, i * height // 5), grid_color_outer, line_thickness + 2)
#     for i in range(1, 3):
#         cv2.line(overlay, (i * width // 3, 0), (i * width // 3, height), grid_color_outer, line_thickness + 2)
#     # Vẽ lưới chính nét mảnh hơn
#     for i in range(1, 5):
#         cv2.line(overlay, (0, i * height // 5), (width, i * height // 5), grid_color_inner, line_thickness)
#     for i in range(1, 3):
#         cv2.line(overlay, (i * width // 3, 0), (i * width // 3, height), grid_color_inner, line_thickness)
#     # Ghép overlay vào transformed_frame
#     cv2.addWeighted(overlay, 0.3, transformed_frame, 0.7, 0, transformed_frame)

#     # 6. Viền mềm mại hơn
#     border_thickness = max(1, int(min(width, height) * 0.005))
#     cv2.rectangle(transformed_frame, (border_thickness, border_thickness), 
#                   (width - border_thickness, height - border_thickness), 
#                   grid_color_inner, border_thickness)
#     # **Căn giữa chữ trên và dưới**
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     font_thickness = 5
#     font_color = (0, 255, 255)
#     if text_top_input:
#         text_top, font_top_position, font_top_scale  = get_text_top_or_bot(text_top_input)
#         draw_multiline_text(transformed_frame, text_top, font, font_top_scale, font_color, font_thickness, 50, int(height * font_top_position), 80)
#     if text_bottom_input:
#         text_bottom, font_bot_position, font_bot_scale  = get_text_top_or_bot(text_bottom_input)
#         draw_multiline_text(transformed_frame, text_bottom, font, font_bot_scale, font_color, font_thickness, 50, int(height * font_bot_position), 80)
#     return transformed_frame

def add_effects(frame, frame_idx, wave_amplitude, wave_frequency, line_spacing, line_opacity,
                line_thickness, total_frames, text_top_input=None, text_bottom_input=None, fps=28, snow_particles=[]):
    height, width, _ = frame.shape
    transformed_frame = frame.copy()

    # === Fade-out nhẹ ở cuối video ===
    fade_out_start = int(total_frames * 0.94)
    fade_out_duration = total_frames - fade_out_start
    if frame_idx > fade_out_start:
        fade_factor = 1 - (frame_idx - fade_out_start) / fade_out_duration
    else:
        fade_factor = None
    if fade_factor is not None:
        transformed_frame = cv2.addWeighted(frame, fade_factor, np.zeros_like(frame), 1 - fade_factor, 0)

    # === Tăng độ tương phản và sáng nhẹ ===
    alpha, beta = 1.06, 20
    transformed_frame = cv2.convertScaleAbs(transformed_frame, alpha=alpha, beta=beta)

    # === Tăng độ bão hòa màu ===
    hsv = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.10, 0, 255)
    transformed_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # === Làm méo sóng ngang động theo thời gian (wave effect) ===
    for i in range(height):
        offset = int(wave_amplitude * 0.5 * np.sin(2 * np.pi * wave_frequency * (i + frame_idx) / height))
        transformed_frame[i] = np.roll(transformed_frame[i], offset, axis=0)

    # === Thêm các đường kẻ ngang đều nhau ===
    overlay = transformed_frame.copy()
    for i in range(0, height, line_spacing):
        cv2.line(overlay, (0, i), (width, i), (150, 150, 150), line_thickness)
    cv2.addWeighted(overlay, line_opacity, transformed_frame, 1 - line_opacity, 0, transformed_frame)

    # === Hiệu ứng nóng kiểu "heatwave" động theo frame ===
    def generate_noise_map_vectorized(width, height, time_offset, scale=60.0):
        x = np.linspace(0, width / scale, width, endpoint=False)
        y = np.linspace(0, height / scale, height, endpoint=False) + time_offset
        xv, yv = np.meshgrid(x, y)
        noise_func = np.vectorize(lambda a, b: pnoise2(a, b, octaves=2))
        noise_map = noise_func(xv, yv).astype(np.float32)
        return cv2.normalize(noise_map, None, 0, 1, cv2.NORM_MINMAX)

    heat_scale = 60.0
    base_strength = 20.0
    heat_speed = 0.04

    cooldown_sec = 0
    active_sec = 4.0

    if cooldown_sec <= 0:
        # Luôn có hiệu ứng
        strength_factor = np.sin((frame_idx / (active_sec * fps)) * np.pi)
        heat_strength = base_strength * strength_factor

        if heat_strength > 0.1:
            noise_map = generate_noise_map_vectorized(width, height, frame_idx * heat_speed, scale=heat_scale)
            dy = (noise_map - 0.5) * heat_strength
            map_x = np.tile(np.arange(width, dtype=np.float32), (height, 1))
            map_y = np.clip(np.add(np.arange(height).reshape(-1, 1), dy), 0, height - 1).astype(np.float32)
            transformed_frame = cv2.remap(transformed_frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    else:
        # Có chu kỳ bật tắt
        period = int((cooldown_sec + active_sec) * fps)
        active_frames = int(active_sec * fps)

        if (frame_idx % period) < active_frames:
            phase = (frame_idx % period) / active_frames * np.pi
            strength_factor = np.sin(phase)
            heat_strength = base_strength * strength_factor

            if heat_strength > 0.1:
                noise_map = generate_noise_map_vectorized(width, height, frame_idx * heat_speed, scale=heat_scale)
                dy = (noise_map - 0.5) * heat_strength
                map_x = np.tile(np.arange(width, dtype=np.float32), (height, 1))
                map_y = np.clip(np.add(np.arange(height).reshape(-1, 1), dy), 0, height - 1).astype(np.float32)
                transformed_frame = cv2.remap(transformed_frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)

    # === Quay nhẹ và phóng to/thu nhỏ tuần hoàn (bồng bềnh nhẹ) ===
    center = (width // 2, height // 2)
    angle = 5 * np.sin(2 * np.pi * frame_idx / (fps * 6))
    scale = 1.0 + 0.005 * np.sin(2 * np.pi * frame_idx / (fps * 5))
    M = cv2.getRotationMatrix2D(center, angle, scale)
    transformed_frame = cv2.warpAffine(transformed_frame, M, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # === Thêm hiệu ứng tuyết rơi, bỏ qua frame đầu tiên ===
    if frame_idx > 30:
        for x, y0, radius in snow_particles:
            y = (y0 + frame_idx * 2) % height
            cv2.circle(transformed_frame, (x, y), radius, (255, 255, 255), -1)

    # === Vẽ lưới ô caro màu cam-vàng và đen ===
    overlay = transformed_frame.copy()
    grid_color_outer = (0, 0, 0)
    grid_color_inner = (255, 191, 0)
    for i in range(1, 5):
        cv2.line(overlay, (0, i * height // 5), (width, i * height // 5), grid_color_outer, line_thickness + 2)
    for i in range(1, 3):
        cv2.line(overlay, (i * width // 3, 0), (i * width // 3, height), grid_color_outer, line_thickness + 2)
    for i in range(1, 5):
        cv2.line(overlay, (0, i * height // 5), (width, i * height // 5), grid_color_inner, line_thickness)
    for i in range(1, 3):
        cv2.line(overlay, (i * width // 3, 0), (i * width // 3, height), grid_color_inner, line_thickness)
    cv2.addWeighted(overlay, 0.3, transformed_frame, 0.7, 0, transformed_frame)

    # === Viền khung quanh khung hình ===
    border_thickness = max(1, int(min(width, height) * 0.005))
    cv2.rectangle(transformed_frame, (border_thickness, border_thickness),
                  (width - border_thickness, height - border_thickness),
                  grid_color_inner, border_thickness)

    # === Thêm chữ (nếu có) trên và dưới ===
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_thickness = 5
    font_color = (0, 255, 255)
    if text_top_input:
        text_top, font_top_position, font_top_scale = get_text_top_or_bot(text_top_input)
        draw_multiline_text(transformed_frame, text_top, font, font_top_scale, font_color, font_thickness, 50, int(height * font_top_position), 80)
    if text_bottom_input:
        text_bottom, font_bot_position, font_bot_scale = get_text_top_or_bot(text_bottom_input)
        draw_multiline_text(transformed_frame, text_bottom, font, font_bot_scale, font_color, font_thickness, 50, int(height * font_bot_position), 80)

    # === Zoom 1.2x và pan (trượt) từ trên xuống dưới ===
    zoom_factor = 1.17
    pan_max_offset = int((zoom_factor - 1) * height)
    pan_offset = int(pan_max_offset * (frame_idx / total_frames))

    zoomed_height = int(height * zoom_factor)
    zoomed_width = int(width * zoom_factor)
    resized = cv2.resize(transformed_frame, (zoomed_width, zoomed_height), interpolation=cv2.INTER_LINEAR)

    start_y = pan_offset
    if start_y + height > resized.shape[0]:
        start_y = resized.shape[0] - height
    cropped = resized[start_y:start_y + height, (zoomed_width - width)//2:(zoomed_width + width)//2]

    transformed_frame = cropped.copy()

    return transformed_frame

def get_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

def get_text_top_or_bot(text_str=""):
    text_top = ""
    font_position = "0.1"
    font_scale = "1.6"
    text_list = text_str.split(',')
    try:
        if len(text_list) == 3:
            text_top, font_position, font_scale = text_list
        elif len(text_list) == 2:
            text_top, font_position = text_list
        else:
            text_top = text_list[0]
    except:
        pass
    return text_top.strip(), float(font_position.strip()), float(font_scale.strip())





def apply_wave_effect(frame, frame_count, amplitude, frequency):
    """ Tạo hiệu ứng gợn sóng động tùy chỉnh """
    height, width, _ = frame.shape
    wave_frame = np.zeros_like(frame)

    for i in range(height):
        shift_x = int(amplitude * np.sin(2 * np.pi * (i / 100) + frame_count * frequency))  
        # Điều chỉnh biên độ và tần số
        wave_frame[i] = np.roll(frame[i], shift_x, axis=0)

    return wave_frame

def merge_audio(video_path, original_video):
    try:
        output_folder = os.path.join(os.path.dirname(video_path), 'edit_level_2')
        os.makedirs(output_folder, exist_ok=True)
        file_name = os.path.basename(original_video)
        output_video = os.path.join(output_folder, file_name)
        command = [
            "ffmpeg", "-y",
            "-i", video_path,    # Video đã chỉnh sửa
            "-i", original_video, # Video gốc (chứa âm thanh)
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            "-map", "0:v:0",  # Lấy video từ file đã chỉnh sửa
            "-map", "1:a:0",  # Lấy âm thanh từ file gốc
            output_video
        ]
        run_command_ffmpeg(command, False)
        return output_video
    except:
        return None

#-----------------commond-------------------------------


def load_config():
    if os.path.exists(config_path):
        config = get_json_data(config_path)
    else:
        config = {
            "download_folder":"",
            "auto_start": False,
            "is_delete_video": False,
            "show_browser": True,
            "auto_upload_youtube": False,
            "auto_upload_facebook": False,
            "auto_upload_tiktok": False,
            "is_auto_and_schedule": True,
            "max_threads": "1",
            "time_check_auto_upload": "0",
            "time_check_status_video": "0",
            "current_tiktok_account": "",
            "current_channel": "",
            "current_page": "",
            "download_by_video_url": "",

            "file_name": "",
            "start_index": "1",
            "videos_edit_folder": "",
            "first_cut": "0",
            "end_cut": "0",
            "is_delete_original_audio": False,
            "background_music_path": "",
            "background_music_volume": "",
            "speed_up": "1.05",
            "max_zoom_size": "1.1",
            "is_random_zoom": False,
            "vertical_position": 'center',
            "horizontal_position": 'center',
            "flip_video": False,
            "water_path": "",
            "watermark_scale": "1,1",
            "vertical_watermark_position": "50",
            "horizontal_watermark_position": "50",
            "top_bot_overlay": "0,0,black,1",
            "left_right_overlay": "0,0,black,1",
            "top_text": "",
            "bot_text": "",
            "edit_level_2": True,

            "audios_edit_folder": "",
            "audio_speed": "1", 
            "pitch_factor": "1",
            "cut_silence": False,
            "aecho": "100",

            "audio_edit_path": "", 
            "speed_talk": "1", 
            "convert_multiple_record": False, 
            "video_get_audio_path": "", 
            "video_get_audio_url": "", 

            "insteract_now": False, 
            "video_number_interact": "6-20", 
            "watch_time": "10-40", 
            "watch_percent": "60", 
            "like_percent": "40", 
            "comment_percent": "20", 
            "follow_percent": "30", 
            "comments_texts": "", 

            "supported_languages": {
                "en-us": "English (United States)",
                "vi": "Vietnamese"
            }
        }
    save_to_json_file(config, config_path)
    return config

youtube_category = {
    "Film & Animation": "1",
    "Autos & Vehicles": "2",
    "Music": "10",
    "Pets & Animals": "15",
    "Sports": "17",
    "Short Movies": "18",
    "Travel & Events": "19",
    "Gaming": "20",
    "Videoblogging": "21",
    "People & Blogs": "22",
    "Comedy": "23",
    "Entertainment": "24",
    "News & Politics": "25",
    "Howto & Style": "26",
    "Education": "27",
    "Science & Technology": "28",
    "Nonprofits & Activism": "29",
    "Movies": "30",
    "Anime/Animation": "31",
    "Action/Adventure": "32",
    "Classics": "33",
    "Documentary": "35",
    "Drama": "36",
    "Family": "37",
    "Foreign": "38",
    "Horror": "39",
    "Sci-Fi/Fantasy": "40",
    "Thriller": "41",
    "Shorts": "42",
    "Shows": "43",
    "Trailers": "44"
}

youtube_config_commond = {
   "registered_emails": [],
   "registered_account": [],
   "check_youtube_channels": [],
   "check_tiktok_channels": [],
   "check_facebook_channels": [],
   "downloaded_urls": [],
   "current_channel": "",
   "download_folder": "",
   "download_url": "",
   "filter_by_like": "0",
   "filter_by_views": "0",
   "quantity_download": "2000",
   "use_cookies": True,
   "show_browser": True
   }

tiktok_config_commond = {
   "registered_account": [],
   "check_youtube_channels": [],
   "check_tiktok_channels": [],
   "check_facebook_channels": [],
   "downloaded_urls": [],
   "output_folder": "",
   "show_browser": True,
   "download_url": "",
   "download_folder": "",
   "is_delete_after_upload": False,
   "filter_by_like": "0",
   "filter_by_views": "0",
   "quantity_download": "2000"
}

facebook_config_commond = {
   "registered_account": [],
   "check_youtube_channels": [],
   "check_tiktok_channels": [],
   "check_facebook_channels": [],
   "downloaded_urls": [],
   "show_browser": True,
   "use_profile_facebook": False,
   "download_url": "",
   "download_folder": "",
   "filter_by_views": "0",
   "filter_by_like": "0",
   "quantity_download": "2000"
}






def load_tiktok_config(acc=None):
    try:
        if acc:
            acc_config_path = os.path.join(tiktok_config_folder, f'{acc}.pkl')
            config = get_json_data(acc_config_path) or {}
            if not config:
                config = {
                    "email":"",
                    "password":"",
                    "proxy":"",
                    "thumbnail_folder":"",
                    "upload_folder":"",
                    "description":"",
                    "hashtags":"#trendding,#fyp,#news",
                    "location":"",
                    "publish_times":"19:00",
                    "cnt_upload_in_day":0,
                    "title":"",
                    "is_title_plus_video_name":False,
                    "upload_date":datetime.now().strftime('%Y-%m-%d'),
                    "is_delete_after_upload":False,
                    "waiting_verify":"30",
                    "number_of_days":"1",
                    "day_gap":"1",
                    "first_login":True,
                    "video_number_interact_befor_upload":"không tương tác",
                    "auto_interact":True,
                    "use_profile_type":"Không dùng",
                    "follow_channels":{},
                    "youtube_edit_video_info":{
                        "first_cut": "0",
                        "end_cut": "0",
                        "is_delete_original_audio": False,
                        "background_music_path": "",
                        "background_music_volume": "",
                        "speed_up": "1.05",
                        "max_zoom_size": "1.1",
                        "is_random_zoom": False,
                        "vertical_position": 'center',
                        "horizontal_position": 'center',
                        "flip_video": False,
                        "water_path": "",
                        "watermark_scale": "1,1",
                        "vertical_watermark_position": "50",
                        "horizontal_watermark_position": "50",
                        "top_bot_overlay": "0,0,black,1",
                        "left_right_overlay": "0,0,black,1",
                        "top_text": "",
                        "bot_text": "",
                        "edit_level_2": True
                    },
                    "tiktok_edit_video_info":{},
                    "facebook_edit_video_info":{},

                    "chrome_cookies":[],
                    "firefox_cookies":[],
                    "mobi_cookies":[]
                }
                save_tiktok_config(acc, config)
        else:
            if os.path.exists(tiktok_config_commond_path):
                config = get_json_data(tiktok_config_commond_path) or {}
            else:
                config = tiktok_config_commond
                save_to_json_file(config, tiktok_config_commond_path)
        return config
    except:
        getlog()

def save_tiktok_config(acc=None, data=None):
    if not data:
        return
    if acc:
        acc_config_path = os.path.join(tiktok_config_folder, f'{acc}.pkl')
        save_to_json_file(data, acc_config_path)
    else:
        save_to_json_file(data, tiktok_config_commond_path)

default = {
    "title":"",
    "hashtag":"",
    "is_title_plus_video_name":True,
    "description":"",
    "altered_content":True,
    "upload_date":datetime.now().strftime('%Y-%m-%d'),
    "publish_times":"00:00",
    "thumbnail_folder":"",
    "upload_folder":"",
    "is_delete_after_upload":False,
    "number_of_days":"1",
    "day_gap":"1",
}
        
def load_youtube_config(acc=None):
    try:
        if acc:
            acc_config_path = os.path.join(youtube_config_folder, f'{acc}.pkl')
            config = get_json_data(acc_config_path) or {}
            if not config:
                config = {
                    "email":"",
                    "cnt_upload_in_day":0,
                    "playlist":[],
                    "curent_playlist":"default",
                    "playlist_info":{

                    },

                    "chrome_cookies":[],
                    "firefox_cookies":[],
                    "mobi_cookies":[]
                }
                save_youtube_config(acc, config)
        else:
            if os.path.exists(youtube_config_commond_path):
                config = get_json_data(youtube_config_commond_path) or {}
            else:
                config = youtube_config_commond
                save_to_json_file(config, youtube_config_commond_path)
        return config
    except:
        getlog()

def save_youtube_config(acc=None, data=None):
    if not data:
        return
    if acc:
        acc_config_path = os.path.join(youtube_config_folder, f'{acc}.pkl')
        save_to_json_file(data, acc_config_path)
    else:
        save_to_json_file(data, youtube_config_commond_path)

def load_facebook_config(acc=None):
    try:
        if acc:
            acc_config_path = os.path.join(facebook_config_folder, f'{acc}.pkl')
            config = get_json_data(acc_config_path) or {}
            if not config:
                config = {
                    "email":"",
                    "password":"",
                    "upload_folder":"",
                    "description":"",
                    "publish_times":"19:00",
                    "cnt_upload_in_day":0,
                    "title":"",
                    "is_title_plus_video_name":False,
                    "upload_date":datetime.now().strftime('%Y-%m-%d'),
                    "is_delete_after_upload":False,
                    "number_of_days":"1",
                    "day_gap":"1",
                    "is_reel_video":True,
                    "waiting_verify":"30",

                    "chrome_cookies":[],
                    "firefox_cookies":[],
                    "mobi_cookies":[],
                    "local_storage":{}
                }
                save_facebook_config(acc, config)
        else:
            if os.path.exists(facebook_config_commond_path):
                config = get_json_data(facebook_config_commond_path) or {}
            else:
                config = facebook_config_commond
                save_to_json_file(config, facebook_config_commond_path)
        return config
    except:
        getlog()

def save_facebook_config(acc=None,data=None):
    if not data:
        return
    if acc:
        acc_config_path = os.path.join(facebook_config_folder, f'{acc}.pkl')
        save_to_json_file(data, acc_config_path)
    else:
        save_to_json_file(data, facebook_config_commond_path)

