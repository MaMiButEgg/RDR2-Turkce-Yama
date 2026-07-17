from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import os
import sys
import requests
import subprocess
import threading
import webbrowser
import platform
import hashlib

# ---------------- PLATFORM ----------------
IS_WINDOWS = platform.system() == "Windows"

# ---------------- GITHUB LINKS ----------------
ASI_URL = "https://raw.githubusercontent.com/MaMi5434/RDR2-Turkce-Yama-kaynak/main/rdr2-translator.asi"
XML_URL = "https://raw.githubusercontent.com/MaMi5434/RDR2-Turkce-Yama-kaynak/main/rdr2-translator.xml"
UNINSTALL_URL = "https://raw.githubusercontent.com/MaMi5434/RDR2-Turkce-Yama-kaynak/main/Uninstall.bat"

# ---------------- GUI ----------------
root = Tk()
root.title("RDR2 Türkçe Yama Kurucu")
root.geometry("675x450")
root.resizable(False, False)

# ---------------- PATH ----------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# ---------------- BACKGROUND ----------------
try:
    bg_image_path = os.path.join(base_path, "background.png")
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((675, 450), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="#1e1e1e")

# ---------------- VARIABLES ----------------
selected_path = StringVar()

# ---------------- STATUS ----------------
def set_status(text):
    root.title(f"RDR2 Yama - {text}")

# ---------------- SOUND ----------------
def play_success():
    if IS_WINDOWS:
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        except:
            pass

def play_error():
    if IS_WINDOWS:
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONHAND)
        except:
            pass

# ---------------- AUTO DETECT ----------------
def auto_find_rdr2():
    set_status("RDR2 aranıyor...")

    paths = [
        r"C:\Program Files\Rockstar Games\Red Dead Redemption 2",
        r"C:\Program Files (x86)\Steam\steamapps\common\Red Dead Redemption 2",
        r"C:\Program Files\Epic Games\RedDeadRedemption2"
    ]

    for p in paths:
        if os.path.exists(p):
            selected_path.set(p)
            set_status("RDR2 bulundu")
            return

    set_status("Manuel seçim gerekli")

# ---------------- BROWSE ----------------
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        selected_path.set(folder)

# ---------------- INSTALL ----------------
def install_thread():
    threading.Thread(target=install).start()

def install():
    gamepath = selected_path.get()

    if not gamepath:
        messagebox.showerror("Hata", "Klasör seç!")
        return

    try:
        set_status("Bağlanıyor...")
        progress['value'] = 5

        asi_path = os.path.join(gamepath, "rdr2-translator.asi")
        xml_path = os.path.join(gamepath, "rdr2-translator.xml")
        uninstall_path = os.path.join(gamepath, "Uninstall.bat")

        # ---------------- ASI ----------------
        set_status("ASI indiriliyor...")
        r = requests.get(ASI_URL, stream=True)
        total = int(r.headers.get('content-length', 0))
        done = 0

        with open(asi_path, "wb") as f:
            for c in r.iter_content(1024):
                if c:
                    f.write(c)
                    done += len(c)
                    if total:
                        progress['value'] = (done / total) * 40
                        root.update_idletasks()

        # ---------------- XML ----------------
        set_status("XML indiriliyor...")
        r = requests.get(XML_URL, stream=True)
        total = int(r.headers.get('content-length', 0))
        done = 0

        with open(xml_path, "wb") as f:
            for c in r.iter_content(1024):
                if c:
                    f.write(c)
                    done += len(c)
                    if total:
                        progress['value'] = 40 + (done / total) * 40
                        root.update_idletasks()

        # ---------------- UNINSTALL ----------------
        set_status("Uninstall indiriliyor...")
        r = requests.get(UNINSTALL_URL)

        with open(uninstall_path, "wb") as f:
            f.write(r.content)

        progress['value'] = 100

        play_success()
        messagebox.showinfo("Başarılı", "Kurulum tamamlandı!")

        progress['value'] = 0
        set_status("Hazır")

    except Exception as e:
        play_error()
        messagebox.showerror("Hata", str(e))
        progress['value'] = 0
        set_status("Hata")

# ---------------- REQUIREMENTS ----------------
def show_requirements():
    messagebox.showinfo("Gereksinimler", "ScriptHookV\nDinput8.dll\nRDR2")

# ---------------- YOUTUBE ----------------
def open_youtube():
    webbrowser.open("https://www.youtube.com/@mamiibutegg")

# ---------------- EXIT ----------------
def exit_app():
    root.destroy()

# ---------------- UI ----------------
Button(root, text="Çıkış", command=exit_app, bg="#f44336", fg="white").place(x=20, y=20)

Button(root, text="Otomatik Bul", command=auto_find_rdr2, bg="#607D8B", fg="white").place(x=120, y=20)

Button(root, text="Gereksinimler", command=show_requirements, bg="#2196F3", fg="white").place(x=535, y=20)

Label(root, text="RDR2 Klasörü:", bg="#ffffff").place(x=50, y=320)

Entry(root, textvariable=selected_path, width=50).place(x=180, y=322)

Button(root, text="...", command=browse_folder, width=3).place(x=550, y=318)

Button(
    root,
    text="Yama Yükle",
    command=install_thread,
    bg="#4CAF50",
    fg="white",
    width=20,
    height=2
).place(x=225, y=360)

progress = Progressbar(root, orient=HORIZONTAL, length=450, mode='determinate')
progress.place(x=110, y=415)

Button(root, text="YouTube", command=open_youtube, bg="#FF0000", fg="white").place(x=580, y=420)

set_status("Hazır")

root.mainloop()
