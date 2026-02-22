import yt_dlp
from customtkinter import *
import threading
import pywinstyles
from tkinter import filedialog
import pystray
from pystray import MenuItem as item
from PIL import Image
import json
import os
from yt_dlp.utils import DownloadError, ExtractorError
def save_data(path=""):
    to_save = {
        "last_folder": path,
    }


    with open("config.json", "w", encoding="utf-8") as file:

        json.dump(to_save, file, indent=1, ensure_ascii=False)

def quitwin(icon):
    icon.stop()
    app.destroy()
    

def showwin():
    app.after(0, app.deiconify)
image = Image.open("reaction/mini.ico")
menu = (item("Show", showwin), item("Quit", quitwin))
icon = pystray.Icon("name", image, "S0nder Downloader", menu)
threading.Thread(target=icon.run, daemon=True).start()
def withdraw_to_tray():
    app.withdraw()


def get_save_path():
    folder = filedialog.askdirectory()
    
    if folder:
        wti.delete(0, END)
        save_data(folder)
        wti.insert(0, folder)
def progresshook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total:
            percentage = downloaded / total * 100 
            s = f"{int(percentage)}%" 
            app.after(0, lambda: checkpb.configure(text=s))
        else:
            checkpb.configure(text="Unknown size")
        
    elif d['status'] == 'finished':
        checkpb.configure(text="✅ video downloaded")
def download_thumbnail():
    base_filename = "my_custom_preview" 
    sd = wti.get()
    url = ltv.get()
    ydl_opts = {
    'skip_download': True,
    'writethumbnail': True,
    'noplaylist': True,
    'outtmpl': f'{sd}/{base_filename}',
}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         
         ydl.download([url])
         ims2 = Image.open(f"{sd}/my_custom_preview.webp")
         ims3 = ims2.close()
         logoimg.configure(image=CTkImage(light_image=ims3, size=(250,145)))
def download_video():
    url = ltv.get()
    sd = wti.get()
    if os.path.isdir(sd) == False:
        sd = wti.get()
        checkpb.configure(text="❌ Incorrect file path")
        return
    qu = quality.get()
    qut = qu.replace("p", "")
    
    if preview_visible.get() == 1:
        download_thumbnail()
    else:
        if get_appearance_mode() == "Light":
         logoimg.configure(image=CTkImage(dark_image=ims, size=(150,150)))
        else:
         logoimg.configure(image=CTkImage(light_image=imsg, size=(150,150)))
    if mp3omly.get() == 1:
        if "pinterest.com" in url or "tiktok.com" in url:
            checkpb.configure(text="⚠️only supports MP4")
            return
        quality.configure(state="disabled")
        options = { 
        'outtmpl': f'{wti.get()}/%(title)s.%(ext)s',  
        'format': 'bestaudio[ext=mp3]/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
        'noplaylist': True,
        "progress_hooks": [progresshook]
        
    }
    else:
        if "soundcloud" in url:
            checkpb.configure(text="⚠️only supports MP3")
            return
        quality.configure(state="readonly")
        options = { 
        'outtmpl': f'{wti.get()}/%(title)s.%(ext)s',  
        'format': f'bestvideo[height<={qut}][ext=mp4]+bestaudio[height<={qut}][ext=m4a]/best',
        'noplaylist': True,
        "progress_hooks": [progresshook]

    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
           
            info = ydl.extract_info(url, download=False)
            app.after(0, lambda: nv.configure(text=info.get("title", "Unknown Title")))
            
            ydl.download([url])

        app.after(0, lambda: checkpb.configure(text="✅ video downloaded"))
        mp3omly.deselect()
        quality.configure(state="readonly")

    except DownloadError:
        app.after(0, lambda: checkpb.configure(text="❌ Download Error: Video unavailable"))
    
    except ExtractorError:
        app.after(0, lambda: checkpb.configure(text="❌ Site not supported or blocked"))
    
    except Exception as e:
        print(f"DEV BUG: {e}") 
        app.after(0, lambda: checkpb.configure(text="❌ Something went wrong (check console)"))





app = CTk()
def load_data():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as file:

            data = json.load(file)
            return data
    else:
        return {"last_folder": "", "theme": "" }

app.protocol('WM_DELETE_WINDOW', withdraw_to_tray )
app.iconbitmap("reaction/mini.ico")
app.title("YouTube Video Downloader by s0nder")
try:
    pywinstyles.apply_style(app, "win7")
except Exception:
    pass 
thme = None
def theme_switcher():
    if get_appearance_mode() == "Light":
        new_mode = "Dark"
        theme.configure(text="🌙        ", image=CTkImage(light_image=luna))
    else:
        new_mode = "Light"
        theme.configure(text="☀️", image=CTkImage(light_image=Sun))
    set_appearance_mode(new_mode)
    if new_mode == "Dark":
        pywinstyles.apply_style(app, "normal")
    else:
        pywinstyles.apply_style(app, "win7")
        
app.geometry("500x370")

ims = Image.open("reaction/watermark.png")
imsg = Image.open("reaction/glowwotermark.png")
luna = Image.open("reaction/moon.png")
Sun = Image.open("reaction/sun.png")
set_appearance_mode("light")
button = CTkButton(master=app, text="DOWNLOAD", corner_radius=15, command=lambda: threading.Thread(target=download_video).start(), fg_color=("#b5cee7", "#002f55"), text_color=("#000000", "#FFFFFF"),  hover_color=("#8091a1", "#516f8d"), width=330)
wti = CTkEntry(master=app, placeholder_text="where to install", width=330)
ltv = CTkEntry(master=app, placeholder_text="link to video",  text_color=("#000000", "#FFFFFF"), width=330)
nv = CTkLabel(master=app, text="", width=1, height=1, wraplength=500)
checkpb = CTkLabel(master=app, text="", width=10, height=10)
mp3omly = CTkCheckBox(master=app, text="mp3 only", checkmark_color="#000000", fg_color="#b5cee7")
preview_visible = CTkCheckBox(master=app, text="Preview Visible", checkmark_color="#000000", fg_color="#b5cee7")
logoimg = CTkLabel(master=app, text="",width=10, height=10, image=CTkImage(light_image=ims, dark_image=Image.open("reaction/glowwotermark.png"), size=(150,150)) )
quality = CTkOptionMenu(master=app, values=["1080p", "720p", "480p"],  button_color=("#b5cee7", "#516f8d"), dropdown_fg_color=("#b5cee7", "#002f55"), fg_color=("#b5cee7", "#002f55"),  text_color=("#000000", "#FFFFFF"),width=330)
foldessave = CTkButton(master=app, command=get_save_path, width=10, height=20, text="📁", fg_color="#b5cee7", hover_color="#8091a1", text_color="#000000", )
theme = CTkButton(master=app,command=theme_switcher, fg_color="transparent", text="☀️",width=10, height=10, text_color="#fdd700", image=CTkImage(dark_image=Sun),hover_color="#4B5E99")
logoimg.place(relx=0.5, rely=0.19, anchor=CENTER)
theme.place(relx=1, rely=0.05, anchor=CENTER)
ltv.place(relx=0.5, rely=0.5, anchor=CENTER)
nv.place(relx=0.5, rely=0.43, anchor=CENTER)
foldessave.place(relx=0.8, rely=0.60, anchor=CENTER)
wti.place(relx=0.5, rely=0.6, anchor=CENTER)
quality.set("1080p")
quality.place(relx=0.5, rely=0.71, anchor=CENTER)
mp3omly.place(relx=0.41, rely=0.79, anchor=CENTER)
preview_visible.place(relx=0.61, rely=0.79, anchor=CENTER)
button.place(relx=0.5, rely=0.87, anchor=CENTER)
checkpb.place(relx=0.5, rely=0.945, anchor=CENTER)
def loadall():
    settings = load_data()
    if settings["last_folder"]:
        wti.insert(0, settings["last_folder"])

loadall()
app.mainloop()



