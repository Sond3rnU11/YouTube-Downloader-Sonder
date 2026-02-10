import yt_dlp
from customtkinter import *
import threading
import pywinstyles
import os
from tkinter import filedialog
from PIL import Image
def olypm3():
    q = mp3omly.get()
    return q


def save_puth():
    folder = filedialog.askdirectory()
    
    if folder:
        wti.delete(0, END)
        wti.insert(0, folder)
def progresshook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total:
            percentage = downloaded / total * 100 
            s = f"{int(percentage)}%" 
            checkpb.configure(text=s)
        else:
            print("what")
        
    elif d['status'] == 'finished':
        checkpb.configure(text="✅ video downloaded")
def dowloutervideo():
    url = ltv.get()
    sd = wti.get()
    if os.path.isdir(sd) == False:
        save_puth()
        sd = wti.get()
        
        if not os.path.isdir(sd):
            checkpb.configure(text="❌ Incorrect file path")
            return 
    if "youtube.com" not in url and "youtu.be" not in url:
        checkpb.configure(text="wrong link")
        return
    olypm3()
    if olypm3() == 1:
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
        options = { 
        'outtmpl': f'{wti.get()}/%(title)s.%(ext)s',  
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        "progress_hooks": [progresshook]

    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        nv.configure(text=info.get("title"))
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError: checkpb.configure(text="❌ Didn't find the video :(")



app = CTk()
app.title("YouTube Video Downloader by s0nder")
try:
    pywinstyles.apply_style(app, "win7")
except Exception:
    pass 
set_appearance_mode("light")
app.geometry("500x330")
ims = Image.open("watermark.png")
button = CTkButton(master=app, text="ENTER", corner_radius=15, command=lambda: threading.Thread(target=dowloutervideo).start(),)
wti = CTkEntry(master=app, placeholder_text="where to install")
ltv = CTkEntry(master=app, placeholder_text="link to video", text_color="#000000", width=330)
nv = CTkLabel(master=app, text="name video")
checkpb = CTkLabel(master=app, text="")
mp3omly = CTkCheckBox(master=app, text="mp3 only",command=olypm3)
logoimg = CTkLabel(master=app, text="", image=CTkImage(light_image=ims, size=(150,150)) )

logoimg.pack(pady=(0,0))
ltv.pack(pady=(0,0))
nv.pack(pady=(0,0))
wti.pack(pady=(0,0))
mp3omly.pack()
button.pack(pady=(2,0))
checkpb.pack(pady=(0,0))

app.mainloop()
