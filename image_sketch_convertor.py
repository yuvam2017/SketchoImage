import os
from tkinter import messagebox
import cv2
import platform
import getpass
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
bgcolor = "#56c099"
system_platform = platform.system()
username = getpass.getuser()


class App:

    def __init__(self, root):
        self.root = root

        frame_parent = Frame(root, bg=bgcolor)
        self.frame_parent = frame_parent
        self.frame_parent.pack(anchor=CENTER, side='top', pady=30)

        self.choose_btn = Button(self.frame_parent, text="Choose Images",
                                 width=20, height=2, bg="white", fg="black", border=0, command=self.choose)
        self.choose_btn.grid(row=0, column=0, pady=3)

        self.choose_label = Label(
            frame_parent, text="No File Choosen!!", bg=bgcolor, fg="black")
        self.choose_label.grid(
            row=1, column=0, columnspan=2, pady=4, sticky='news')

        self.convert_button = Button(self.frame_parent, text="Convert Images", bg="#ff6600", fg="white", border=0,
                                     width=20, height=2, command=self.convert)
        self.convert_button.grid(row=2, column=0, pady=3, sticky='news')

    def choose(self):
        filetype = (
            ("All Types", '*.*'), ('PNG ', '*.png'),
            ('JPG', '*.jpg'), ('JPEG', '*.jpeg')
        )

        if system_platform == "Linux":
            self.path = askopenfilenames(initialdir=f"/home/{username}/Pictures/", title="Open a File",
                                         filetypes=filetype)
        elif system_platform == "Windows":
            self.path = askopenfilenames(initialdir=f"C:\\\\Users\\{username}\\My Pictures", title="Open a File",
                                         filetypes=filetype)

    def finaldirectory(self):
        if system_platform == "Linux":
            self.finaldirectory = askdirectory(
                title="Choose the final directory", initialdir=f"/home/{username}/Pictures/")
        elif system_platform == "Windows":
            self.finaldirectory = askdirectory(
                initialdir=f"C:\\\\Users\\{username}\\My Pictures", title="Choose the directory")

        return self.finaldirectory

    def convert(self):
        print(self.path)
        finaldirectory = self.finaldirectory()
        try:
            os.mkdir(f'{finaldirectory}/Sketch')
        except Exception as e:
            pass
        if system_platform == "Linux":
            for images in self.path:
                images_name_with_path = images.replace(" ", "\ ").replace(
                    "(", "\(").replace(")", "\)")
                print(images_name_with_path)
                filename = os.path.basename(images_name_with_path)
                print(filename)
                os.chdir(images_name_with_path.replace(filename,''))
                try:
                    imageName = cv2.imread(filename)
                    grey_img = cv2.cvtColor(imageName, cv2.COLOR_BGR2GRAY)
                    invert = cv2.bitwise_not(grey_img)
                    blur = cv2.GaussianBlur(invert, (21, 21), 0)
                    inverted_blur = cv2.bitwise_not(blur)
                    sketch = cv2.divide(grey_img, inverted_blur, scale=256.0)
                   
                    cv2.imwrite(
                        f"{finaldirectory}/Sketch/{filename}_Sketch.png", sketch)

                except Exception as e:
                    print(e)
                    showerror(title="Oops! Got An error", message=e)

        elif system_platform == "Windows":
            for images in self.path:
                print(images)
                filename = os.path.basename(images)
                print(filename)
                os.chdir(images.replace(filename,""))
                try:
                    imageName = cv2.imread(images_name_with_path)
                    grey_img = cv2.cvtColor(imageName, cv2.COLOR_BGR2GRAY)
                    invert = cv2.bitwise_not(grey_img)
                    blur = cv2.GaussianBlur(invert, (21, 21), 0)
                    inverted_blur = cv2.bitwise_not(blur)
                    sketch = cv2.divide(
                        grey_img, inverted_blur, scale=256.0)
                    cv2.imwrite(
                        f"{finaldirectory}\\Sketch\\{filename}_Sketch.png", sketch)

                except Exception as e:
                    print(e)
                    showerror(title="Oops! Got An error", message=e)

        showinfo(title="Successfully Converted",
                 message="Your Images are converted successfully")


if __name__ == "__main__":
    root = Tk()
    root.title("SketchoImage |  Convert Images to Sketch")
    root.geometry("500x300")
    root.config(bg=bgcolor)
    App(root)
    root.mainloop()
