import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("WEC 2024")
        self.update()
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{width}x{height}+0+0')


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, height=self.winfo_height(), width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="WEC 2024", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=0)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 20))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=0)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=0, pady=(0, 20))

        # create scrollable frame
        self.frame = customtkinter.CTkFrame(self, height=self.winfo_height(), width=self.winfo_height()-120, corner_radius=0)
        self.notes = customtkinter.CTkFrame(self, height=self.winfo_height(), width=self.winfo_height()-120, corner_radius=0)  #Frame for transcription and image conversion
        # self.scrollable_frame = customtkinter.CTkScrollableFrame(self, height=500, width=800, corner_radius=0)
        self.frame.grid(row=0, column=1, padx=(20, 0), pady=0, sticky="nsew")
        button = customtkinter.CTkButton(self.frame, text="Notes", command=self.button_function, height=300, width=500, font=("Arial", 36))
        button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def button_function(self):
        print("button pressed")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.attributes('-fullscreen', True)
    app.mainloop()