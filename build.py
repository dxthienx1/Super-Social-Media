import subprocess

# Lệnh pyinstaller được viết thành dạng danh sách để dễ quản lý
command = [
    "pyinstaller",
    "--onefile",
    "--add-data", "import/icon.ico;.",
    "--add-data", "import/icon.png;.",
    "--add-data", "common_function.py;.",
    "--add-data", "facebook.py;.",
    "--add-data", "youtube.py;.",
    "--add-data", "tiktok.py;.",
    "--collect-data", "selenium_stealth",
    "--hidden-import", "imageio_ffmpeg.binaries",
    "--icon", "import/icon.ico",
    "app.py"
]

try:
    # Thực thi lệnh bằng subprocess
    subprocess.run(command, check=True, shell=True)
    print("Build thành công!")
except subprocess.CalledProcessError as e:
    print(f"Lỗi khi chạy PyInstaller: {e}")
except FileNotFoundError:
    print("PyInstaller chưa được cài đặt. Hãy cài bằng lệnh 'pip install pyinstaller'.")
