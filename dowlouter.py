import yt_dlp
from customtkinter import *
import threading
import pywinstyles
import os
from tkinter import filedialog
import pystray
from pystray import MenuItem as item
from PIL import Image

def quitwin(icon, item):
    icon.stop()
    app.destroy()
    

def showwin(icon, item):
    icon.stop()
    app.after(0, app.deiconify)

def witndraw():
    app.withdraw()
    
    image = Image.open("mini.ico")
    menu = (item("Show", showwin), item("Quit", quitwin))
    icon = pystray.Icon("name", image, "Sond33r Downloader", menu)
    threading.Thread(target=icon.run, daemon=True).start()
        

def quatl(choice):
    print(choice)
    return choice
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
            checkpb.configure(text="i idk lol")
        
    elif d['status'] == 'finished':
        checkpb.configure(text="✅ video downloaded")
def dowloutervideo():
    url = ltv.get()
    sd = wti.get()
    if os.path.isdir(sd) == False:
        sd = wti.get()
        
        if not os.path.isdir(sd):
            checkpb.configure(text="❌ Incorrect file path")
            return 
    qu = quality.get()
    qut = qu.replace("p", "")
    olypm3()
    if olypm3() == 1:
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
        nv.configure(text=info.get("title"))
        ydl.download([url])

        mp3omly.deselect()
        quality.configure(state="readonly")
    except Exception:
        checkpb.configure(text="❌ VPN/Internet Error or Video Blocked")

    


app = CTk()
#app.protocol('WM_DELETE_WINDOW', witndraw)
app.iconbitmap("mini.ico")
app.title("YouTube Video Downloader by s0nder")
try:
    pywinstyles.apply_style(app, "win7")
except Exception:
    pass 
set_appearance_mode("light")
app.geometry("500x360")
ims = Image.open("watermark.png")
button = CTkButton(master=app, text="DOWNLOAD", corner_radius=15, command=lambda: threading.Thread(target=dowloutervideo).start(), fg_color="#b5cee7", text_color="#000000", hover_color="#8091a1", width=330)
wti = CTkEntry(master=app, placeholder_text="where to install", width=330)
ltv = CTkEntry(master=app, placeholder_text="link to video", text_color="#000000", width=330)
nv = CTkLabel(master=app, text="", width=1, height=1)
checkpb = CTkLabel(master=app, text="", width=10, height=10)
mp3omly = CTkCheckBox(master=app, text="mp3 only",command=olypm3, checkmark_color="#000000", fg_color="#b5cee7")
logoimg = CTkLabel(master=app, text="", image=CTkImage(light_image=ims, size=(150,150)) )
quality = CTkOptionMenu(master=app, values=["1080p", "720p", "480p"], command=quatl, button_color="#b5cee7", dropdown_fg_color="#b5cee7", fg_color="#b5cee7", text_color="#000000", width=330)
foldessave = CTkButton(master=app, command=save_puth, width=10, height=25, text="📁", fg_color="#b5cee7", hover_color="#8091a1", text_color="#000000", )
logoimg.place(relx=0.5, rely=0.2, anchor=CENTER)

ltv.pack(pady=(165,0))
nv.place(relx=0.5, rely=0.39, anchor=CENTER)
foldessave.place(relx=0.854, rely=0.60, anchor=CENTER)
wti.place(relx=0.5, rely=0.6, anchor=CENTER)
quality.set("1080p")
quality.place(relx=0.5, rely=0.71, anchor=CENTER)
mp3omly.place()
button.place(relx=0.5, rely=0.82, anchor=CENTER)
checkpb.place(relx=0.5, rely=0.89, anchor=CENTER)
app.mainloop()
