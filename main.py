from Image_enc import ImageEncryptor
from database import Datas
import capture
from Face_detect.detect1 import FaceDetector
from tkinter import messagebox, filedialog
import customtkinter
from PIL import Image, ImageTk  # For image processing
from tkinter import Canvas
import threading
import train

class Main():
    def __init__(self,other):
        self.IE=ImageEncryptor()
        self.datas=Datas()
        self.detector=FaceDetector()
        
        self.ui=other
        
        self.name=None
        
        
    def Encrypt(self):
        def encrypt():
            print('Encrypting...')
            key=int(self.datas.fetch(self.name))
            if self.IE._encrypt_file(file,key):
                messagebox.showinfo("Success","Encryption Success")
            else:
                messagebox.showerror("Error","An error occured")

        file1 = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*.jpg *.png')])
        file=self.IE.verify_image(file1)
        del file1
        if file:
            while True:
                messagebox.showwarning("Warning","Detecting Your Face")
                self.name=self.detector.face_detect()
                if self.name=="unknown":
                    def register():
                        messagebox.showwarning("Warning","Capturing your face. Look at the camera")
                        capture.snip(self.name)
                        progress_thread=threading.Thread(target=self.ui.progress)
                        progress_thread.start()
                        self.datas.insert(self.name)
                        progress_thread.join()
                        self.ui.msg.place_forget()
                        self.ui.pbar.place_forget()
                        self.ui.pperc.place_forget()
                        self.ui.encrypt_button.place(x=5, y=self.ui.winfo_height()/3.5)
                        self.ui.decrypt_button.place(x=5,y=(self.ui.winfo_height()/3.5)+(self.ui.winfo_height()/8))
                        
                        encrypt()
                        
                    textbox_thread=threading.Thread(target=self.ui.show_textbox,args=(register,))
                    textbox_thread.start()
                    textbox_thread.join()
                    break
                else:
                    result1=messagebox.askyesno("Verification", "'Are you "+self.name+" ?")
                    if result1:
                        encrypt()
                        break
                    else:
                        result=messagebox.askyesno("", "Do you want to try again?")
                        if result:
                            continue
                        else:
                            break
            
        else:
            messagebox.showerror("Error", "Selected image is already Encrypted or Corrupted.")
                
    def Decrypt(self):
        file1 = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*.jpg *.png')])
        file=self.IE.check_image(file1)
        del file1
        if file:
            while True:
                messagebox.showwarning("Warning","Detecting Your Face")
                self.name=self.detector.face_detect()
                if self.name!='unknown':
                    result=messagebox.askyesno("Verification", "'Are you "+self.name+" ?")
                    if result:
                        key=int(self.datas.fetch(self.name))
                        if self.IE._decrypt_file(file,key):
                            messagebox.showinfo("Success","Decryption Success")
                            break
                        else:
                            messagebox.showerror("Error","Face doesn't match")
                            break
                    else:
                        result=messagebox.askyesno("", "Do you want to try again?")
                        if result:
                            continue
                        else:
                            break
                else:
                    messagebox.showerror("Error", "Can't Recognize your face!")
                    result=messagebox.askyesno("", "Do you want to try again?")
                    if result:
                        continue
                    else:
                        break
        else:
            messagebox.showerror("Error", "Selected image is not encrypted.")
            
class ImageEncryptDecryptApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.main=Main(self)
        
        self.title("Image Encryption/Decryption App")
        self.geometry(str(self.winfo_screenwidth())+"x"+str(self.winfo_screenheight()))
        
        # Load the image
        image = Image.open("b2.png")
        image = image.resize((1920, 991), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)  # Make bg_image an instance variable
        
        # Create a Tkinter canvas on top of the customtkinter window
        self.canvas = Canvas(self)
        self.canvas.pack(fill='both', expand=True)
        
        # Add the image to the canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Create custom buttons with rounded corners and hover effects
        self.encrypt_button = customtkinter.CTkButton(
            master=self.canvas,  # Place the button on the canvas
            text="Encrypt",
            font=("Arial", 12),
            width=-1,
            command=self.init_encthread,
            corner_radius=30,
            hover_color="green",
            border_width=2,
            border_color="#001530",
            fg_color="#001530",
            bg_color="#001530"
        )
        self.encrypt_button.place(x=5, y=self.winfo_screenheight()/3.5)

        self.decrypt_button = customtkinter.CTkButton(
            master=self.canvas,  # Place the button on the canvas
            text="Decrypt",
            font=("Arial", 12),
            width=-1,
            command=self.init_decthread,
            corner_radius=30,
            hover_color="red",
            border_width=2,
            border_color="#001530",
            fg_color="#001530",
            bg_color="#001530"
        )
        self.decrypt_button.place(x=5,y=(self.winfo_screenheight()/3.5)+(self.winfo_screenheight())/8)
        
        self.bind("<Configure>", self.on_change)
        
    def init_encthread(self):
        enc=threading.Thread(target=self.main.Encrypt)
        enc.start()
        
    def init_decthread(self):
        dec=threading.Thread(target=self.main.Decrypt)
        dec.start()
        
    def on_change(self,event):
        window_w=self.winfo_width()
        window_h=self.winfo_height()
        gap=window_h/8
        button_w=(window_w)//4 - 20
        font_s=(window_w)//60
        self.encrypt_button.configure(width=button_w,font=("Arial", font_s))
        self.decrypt_button.configure(width=button_w,font=("Arial", font_s))
        if self.encrypt_button.winfo_ismapped():
            self.encrypt_button.place(x=5, y=window_h/3.5)
            self.decrypt_button.place(x=5,y=(window_h/3.5)+gap)
            
    def show_textbox(self,register):
        self.register=register
        self.encrypt_button.place_forget()
        self.decrypt_button.place_forget()
        self.label=customtkinter.CTkLabel(self.canvas,text="Enter Username:",fg_color="#000308",font=("Arial", 20,"bold"),bg_color="#000308")
        self.label.place(x=3,y=self.winfo_height()/3.5 - 100)
        
        self.entry=customtkinter.CTkEntry(self.canvas,width=self.winfo_width()//4 -20,height=25,fg_color="#001125",bg_color="#001125")
        self.entry.place(x=175,y=self.winfo_height()/3.5 - 97)
        
        self.ok=customtkinter.CTkButton(
            master=self.canvas,  # Place the button on the canvas
            text="Ok",
            font=("Arial", 18),
            width=-1,
            command=self.get_text_thread,
            corner_radius=30,
            hover_color="green",
            border_width=2,
            border_color="#010b17",
            fg_color="#010b17",
            bg_color="#010b17"
        )
        self.ok.place(x=200,y=self.winfo_height()/3.5 - 57)
        
    def get_text_thread(self):
        get_text_t=threading.Thread(target=self.get_text)
        get_text_t.start()
        
    def get_text(self):
        self.main.name=self.entry.get()
        self.label.place_forget()
        self.entry.place_forget()
        self.ok.place_forget()
        self.register()
        
    def progress(self):
        self.msg=customtkinter.CTkLabel(self.canvas,text="Registering Your Face...",fg_color="#001736",bg_color="#001736",font=("Arial", 20,"bold"))
        self.msg.place(x=400,y=self.winfo_height()/3.5 - 97)
        self.pbar=customtkinter.CTkProgressBar(self.canvas,width=400)
        self.pbar.set(0)
        self.pbar.place(x=300,y=self.winfo_height()/3.5 - 50)
        self.pperc=customtkinter.CTkLabel(self.canvas,text="0%",fg_color="#001736",bg_color="#001736")
        self.pperc.place(x=500,y=self.winfo_height()/3.5 - 20)
    
        for i in train.main():
            self.pperc.configure(text=str(i)+"%")
            self.pperc.update()
            self.pbar.set(i/100)
        self.detector_update()
        
    def detector_update(self):
        self.wait=customtkinter.CTkLabel(self.canvas,text="Please Wait...",fg_color="#001736",bg_color="#001736",font=("Arial", 18,))
        self.wait.place(x=475,y=self.winfo_height()/3.5 + 30)
        del self.main.detector
        self.main.detector=FaceDetector()
        self.wait.place_forget()
        
        
if __name__ == "__main__":
    app = ImageEncryptDecryptApp()
    app.mainloop()