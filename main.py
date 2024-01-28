import os
import shutil
from tkinter import filedialog, messagebox
from tkinter import *
import customtkinter
import sounddevice as sd
from customtkinter import CTkImage
from scipy.io.wavfile import write
from spire.doc import *
from spire.doc.common import *

from Backend.speech_text import transcribe_audio_to_text
from Backend.speech_text import convert_text_to_speech
from Backend.image_to_text import image_to_text
from Backend.summary import gen_summary

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

default_save_path = "./database/"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Ez-Note")
        self.update()
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}+0+0')

        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, height=self.height, width=100, corner_radius=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ez-Note",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebar_frame.pack(side="left", fill="y")

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
        self.main_frame = customtkinter.CTkScrollableFrame(self, height=self.height - 30, width=self.width, corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=(20, 0), pady=0)

        # Images
        download_photo = PhotoImage(file=r"download.png")
        process_photo = PhotoImage(file=r"transcribe.png")
        transcribe_photo = PhotoImage(file=r"process.png")

        # Main Frame Buttons
        self.button_frame = customtkinter.CTkFrame(self.main_frame, height=100, width=self.width - 120, corner_radius=0)
        upload_recording_button = customtkinter.CTkButton(self.button_frame, text="Process Speech",
                                                          height=100, width=200, font=("Arial", 36),
                                                          command= lambda: self.save_file("audio"), image=process_photo)
        record_button = customtkinter.CTkButton(self.button_frame, text="Upload File",
                                                height=100, width=200, font=("Arial", 36),
                                                command= lambda: self.save_file("other"), image=download_photo)
        upload_photo_button = customtkinter.CTkButton(self.button_frame, text="Transcribe Speech",
                                                      height=100, width=200, font=("Arial", 36),
                                                      command= lambda: self.save_file("image"), image=transcribe_photo)
        # camera_button = customtkinter.CTkButton(self.button_frame, text="Take Photo",
        #                                         height=100, width=200, font=("Arial", 36))

        record_button.pack(side="left", padx=(10, 10), pady=10, fill="both")
        upload_recording_button.pack(side="left", padx=(0, 10), pady=10, fill="both")
        # camera_button.pack(side="left", padx=(0, 10), pady=10, fill="both")
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
        self.button_frame.pack(side="top", fill="x")
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
                    note_path = os.path.join(default_save_path, directory, note)
                    if os.path.isdir(os.path.join(default_save_path, directory, note)):
                        self.notes.append(note_path)
        for note in self.notes:
            note_button = customtkinter.CTkButton(self.main_frame, text=os.path.basename(note),
                                    height=100, width=200, font=("Arial", 36), command=lambda: self.open_note(note))
            note_button.pack(side="left", padx=20, pady=20, anchor="nw")
            self.note_buttons.append(note_button)

    def open_note(self, note):
        os.startfile(note)
    def save_file(self, file_type):
        # Prepare """database"""
        if not os.path.exists(default_save_path):
            os.mkdir(default_save_path)
        work_save_path = os.path.join(default_save_path, "work")
        if not os.path.exists(work_save_path):
            os.mkdir(work_save_path)
        school_save_path = os.path.join(default_save_path, "school")
        if not os.path.exists(school_save_path):
            os.mkdir(school_save_path)
        personal_save_path = os.path.join(default_save_path, "personal")
        if not os.path.exists(personal_save_path):
            os.mkdir(personal_save_path)

        # Get file to be saved
        file = filedialog.askopenfilename()
        if not os.path.exists(file):
            return

        # Open the custom save dialog to ask for a file name
        save_dialog = SaveDialog(self, "Note")
        user_defined_name = save_dialog.get_user_input()
        if not user_defined_name:
            messagebox.showinfo("Save File", "File save cancelled.")
            return

        # Save added file
        added_note = ""
        if self.context == "work":
            added_note = os.path.join(work_save_path, user_defined_name)
        elif self.context == "school":
            added_note = os.path.join(school_save_path, user_defined_name)
        elif self.context == "personal":
            added_note = os.path.join(personal_save_path, user_defined_name)
        else:
            return
        if not os.path.exists(added_note):
            os.mkdir(added_note)
        added_file = os.path.join(added_note, os.path.basename(file))
        added_file_no_ext = os.path.splitext(os.path.basename(file))[0]
        shutil.copyfile(file, added_file)

        transcribed_file = ""
        document_file = os.path.join(added_note, added_file_no_ext + ".docx")
        if file_type == "audio":
            transcribed_file = os.path.join(added_note, added_file_no_ext + ".txt")
            transcribe_audio_to_text(added_file, transcribed_file)
            summary_file = os.path.join(added_note, added_file_no_ext + "_summary.txt")
            summary_tts_file = os.path.join(added_note, added_file_no_ext + "_summary_tts.mp3")
            try:
                gen_summary(transcribed_file, summary_file)
            except:
                gen_summary(transcribed_file, summary_file, 1)
            convert_text_to_speech(summary_file, summary_tts_file)
        elif file_type == "image":
            transcribed_file = os.path.join(added_note, added_file_no_ext + "_ocr.txt")
            image_to_text(added_file, transcribed_file)
        else:
            self.change_context(self.context)
            return
        try:
            self.convert_text_to_doc(transcribed_file, document_file)
        except:
            pass
        self.change_context(self.context)

    def convert_text_to_doc(self, text_path, document_path):
        document = Document()
        document.LoadFromFile(text_path)
        document.SaveToFile(document_path, FileFormat.Docx)
        document.Close()
        self.format_doc(document_path)

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
