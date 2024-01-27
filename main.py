import os
import shutil
from tkinter import filedialog
import customtkinter
import sounddevice as sd
from scipy.io.wavfile import write
from spire.doc import *
from spire.doc.common import *

import wavio as wv
import threading
from multiprocessing import Process
from Backend.speech_text import transcribe_audio_to_text

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

default_save_path = "./database/"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("WEC 2024")
        self.update()
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}+0+0')

        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, height=self.height, width=100, corner_radius=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="WEC 2024",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebar_frame.pack(side="left", fill="y")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="WEC 2024",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.work_button = customtkinter.CTkButton(self.sidebar_frame, text="Work",
                                                          height=100, font=("Arial", 36), command= lambda: self.change_context("work"))
        self.school_button = customtkinter.CTkButton(self.sidebar_frame, text="School",
                                                   height=100, font=("Arial", 36),
                                                   command=lambda: self.change_context("school"))
        self.personal_button = customtkinter.CTkButton(self.sidebar_frame, text="Personal",
                                                   height=100, font=("Arial", 36),
                                                   command=lambda: self.change_context("personal"))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")

        self.appearance_mode_options = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                   values=["Light", "Dark", "System"],
                                                                   font=("Arial", 36),
                                                                   command=self.change_appearance_mode_event)

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        self.scaling_options = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                           values=["80%", "100%", "120%", "140%", "160%"],
                                                           font=("Arial", 36),
                                                           command=self.change_scaling_event)

        self.logo_label.pack(side="top", padx=20, pady=(20, 10))
        self.work_button.pack(side="top", padx=20, pady=(0, 10), fill="x")
        self.school_button.pack(side="top", padx=20, pady=(0, 10), fill="x")
        self.personal_button.pack(side="top", padx=20, pady=(0, 10), fill="x")
        self.scaling_options.pack(side="bottom", padx=20, pady=(0, 20), fill="x")
        #self.scaling_label.pack(side="bottom", padx=20, pady=0)
        self.appearance_mode_options.pack(side="bottom", padx=20, pady=(0, 20), fill="x")
        #self.appearance_mode_label.pack(side="bottom", padx=20, pady=0)

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self, height=self.height - 30, width=self.width, corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=(20, 0), pady=0)

        # Main Frame Buttons
        self.button_frame = customtkinter.CTkFrame(self.main_frame, height=100, width=self.width - 120, corner_radius=0)
        upload_recording_button = customtkinter.CTkButton(self.button_frame, text="Upload Speech",
                                                          height=100, width=200, font=("Arial", 36), command= lambda: self.save_file("audio"))
        record_button = customtkinter.CTkButton(self.button_frame, text="Record Speech",
                                                height=100, width=200, font=("Arial", 36), command=self.open_recording_dialog)
        upload_photo_button = customtkinter.CTkButton(self.button_frame, text="Upload Photo",
                                                      height=100, width=200, font=("Arial", 36), command= lambda: self.save_file("image"))
        camera_button = customtkinter.CTkButton(self.button_frame, text="Take Photo",
                                                height=100, width=200, font=("Arial", 36))

        self.button_frame.pack(side="top", fill="x")
        record_button.pack(side="left", padx=(10, 10), pady=10, fill="both")
        upload_recording_button.pack(side="left", padx=(0, 10), pady=10, fill="both")
        camera_button.pack(side="left", padx=(0, 10), pady=10, fill="both")
        upload_photo_button.pack(side="left", padx=(0, 20), pady=10, fill="both")

        # set default values
        self.appearance_mode_options.set("Dark")
        self.scaling_options.set("120%")
        self.context = None
        self.notes = []
        self.note_buttons = []
        self.record_dialog = ""

    def open_recording_dialog(self):
        if self.record_dialog is None or not self.record_dialog.winfo_exists():
            self.record_dialog = RecordingWindow(self)  # create window if its None or destroyed
            self.record_dialog.focus()
        else:
            self.record_dialog.focus()  # if window exists focus it

    def change_context(self, context):
        self.update()
        self.notes.clear()
        for note_button in self.note_buttons:
            note_button.destroy()
        self.note_buttons.clear()
        self.context = context
        for directory in os.listdir(default_save_path):
            if not os.path.isdir(os.path.join(default_save_path, directory)):
                continue
            if os.path.basename(directory) == self.context:
                for note in os.listdir(os.path.join(default_save_path, directory)):
                    if os.path.isdir(os.path.join(default_save_path, directory, note)):
                        self.notes.append(note)
        for note in self.notes:
            note_button = customtkinter.CTkButton(self.main_frame, text=os.path.basename(note),
                                    height=100, width=200, font=("Arial", 36))
            note_button.pack(side="left", padx=20, pady=20)
            self.note_buttons.append(note_button)

    def save_file(self, file_type):
        file = filedialog.askopenfilename()
        if not os.path.exists(file):
            return
        if not os.path.exists(default_save_path):
            os.mkdir(default_save_path)

        # Open the custom save dialog to ask for a file name
        save_dialog = SaveDialog(self, "Save File As")
        user_defined_name = save_dialog.get_user_input()
        if not user_defined_name:
            messagebox.showinfo("Save File", "File save cancelled.")
            return

        # Define save paths for text, recordings, and photos
        text_save_path = os.path.join(default_save_path, "text")
        if not os.path.exists(text_save_path):
            os.mkdir(text_save_path)

        # Handling recordings
        if file_type == 0:
            recording_save_path = os.path.join(default_save_path, "recordings")
            if not os.path.exists(recording_save_path):
                os.mkdir(recording_save_path)

            # Use the user-defined name for saving the recording and text file
            recording_path = os.path.join(recording_save_path, user_defined_name + ".wav")
            text_path = os.path.join(text_save_path, user_defined_name + ".txt")

            shutil.copyfile(file, recording_path)
            transcribe_audio_to_text(recording_path, text_path)
            self.convert_text_to_doc(text_path, recording_path)

        # Handling photos
        else:
            photo_save_path = os.path.join(default_save_path, "photos")
            if not os.path.exists(photo_save_path):
                os.mkdir(photo_save_path)

            # Use the user-defined name for saving the photo
            photo_path = os.path.join(photo_save_path, user_defined_name + os.path.splitext(file)[-1])
            shutil.copyfile(file, photo_path)

    def convert_text_to_doc(self, text_path, recording_path):
        document = Document()
        document.LoadFromFile(text_path)
        base = os.path.splitext(os.path.basename(recording_path))[0] + ".docx"
        document.SaveToFile(base, FileFormat.Docx)
        print(base)
        document.Close()
        self.format_doc(base)

    def format_doc(self, doc_path):
        document = Document()
        document.LoadFromFile(doc_path)
        style = ParagraphStyle(document)
        style.Name = 'NewStyle'
        style.CharacterFormat.TextColor = Color.get_Black()
        style.CharacterFormat.FontName = 'Arial'
        style.CharacterFormat.FontSize = 32
        document.Styles.Add(style)

        for section in document.Sections:
            for paragraph in section:
                paragraph.ApplyStyle(style.Name)
        document.SaveToFile(doc_path, FileFormat.Docx)
        document.Close()
        print("Done formatting")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

class SaveDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, title="Save As"):
        super().__init__(parent)

        self.title(title)

        # Entry for file name with adjusted width and height
        self.entry = customtkinter.CTkEntry(self, width=400, height=60,
                                            font=("Arial", 18),  # Adjusted font size for better readability
                                            placeholder_text="Enter file name here")
        self.entry.pack(pady=20)  # Adjusted padding for spacing

        # Confirm button with adjusted size
        self.confirm_button = customtkinter.CTkButton(self, text="Save",
                                                      width=200, height=60,  # Adjusted size
                                                      font=("Arial", 18),  # Adjusted font size
                                                      command=self.on_confirm)
        self.confirm_button.pack(pady=10)

        # Set the size of the popup window after adding all widgets
        self.geometry("800x400")  # Adjusted size to make the window larger

        # Force the window to update its size
        self.update()

        # Center the dialog relative to the parent window
        self.center_window()

        # Make dialog modal and keep on top
        self.transient(parent)
        self.grab_set()

        # Keep this window above all others
        self.attributes('-topmost', True)

        # Variable to store the user's input
        self.user_input = None
        parent.wait_window(self)

    def on_confirm(self):
        self.user_input = self.entry.get()
        self.destroy()

    def get_user_input(self):
        return self.user_input

    def center_window(self):
        width = 800  # Desired width
        height = 400  # Desired height
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')  # Set the size and position



class RecordingWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.button = customtkinter.CTkButton(self, text="Stop Recording",
                                                height=100, font=("Arial", 36),
                                                command=self.stop_recording)
        self.button.place(relx=0.5)
        self.after(500, self.record_audio)
        # self.record_audio()

    def record_audio(self):
        duration = 7
        freq = 44100
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2, blocking=False)
        sd.wait()
        write("recording.wav", freq, recording)
        # wv.write("recording1.wav", recording, freq, sampwidth=2)
        # Record audio for the given number of seconds


    def stop_recording(self):
        sd.stop()


def get_timestamp():
    pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
