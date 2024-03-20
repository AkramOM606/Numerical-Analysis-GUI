import numexpr as ne
import numpy as np
from PIL import Image

import customtkinter as ctk
from resources.helperfunctions.Gauss import resoudre_equation_gauss
from resources.helperfunctions.Integrals import *
from resources.helperfunctions.LLT import resolution_choleski
from resources.helperfunctions.LU import resolution_LU

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Dialog(ctk.CTkToplevel):
    def __init__(self, title, mainlabel, textlabels, fgcolor):
        super().__init__()

        self.title(title)
        self.attributes("-topmost", True)
        self.textEntry = []
        self.grab_set()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)

        self.geometry("+{}+{}".format(positionRight, positionDown))

        mainLabel = ctk.CTkLabel(self, text=mainlabel, font=("Trebuchet MS Bold", 16))
        mainLabel.pack()
        mainFrame = ctk.CTkFrame(self, fg_color=fgcolor)
        mainFrame.pack(padx=5, pady=5)

        for i in range(len(textlabels)):
            tmpFrame = ctk.CTkFrame(mainFrame, fg_color=fgcolor)
            tmpFrame.pack()
            textLabel = ctk.CTkLabel(
                tmpFrame, text=textlabels[i], font=("Trebuchet MS Bold", 16)
            )
            textLabel.grid(row=0, column=0, padx=5, pady=5)
            self.textEntry.append(ctk.CTkEntry(tmpFrame, font=("Trebuchet MS", 16)))
            self.textEntry[i].grid(row=0, column=1, padx=5, pady=5)

        buttonFrame = ctk.CTkFrame(self, fg_color=fgcolor)
        buttonFrame.pack()
        SubmitButton = ctk.CTkButton(
            buttonFrame,
            text="OK",
            command=lambda: self.apply(len(textlabels)),
            width=50,
            font=("Trebuchet MS Bold", 16),
        )
        SubmitButton.grid(row=0, column=0, padx=5, pady=5)
        self.bind("<Return>", lambda event: SubmitButton.invoke())
        CancelButton = ctk.CTkButton(
            buttonFrame,
            text="Cancel",
            command=lambda: self.destroy(),
            width=50,
            font=("Trebuchet MS Bold", 16),
        )
        CancelButton.grid(row=0, column=1, padx=5, pady=5)

        self._user_input = []

    def apply(self, n):
        for i in range(n):
            self._user_input.append(self.textEntry[i].get())
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self._user_input


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.home_text_var = ctk.StringVar()

        # Configuration
        self.title("TP : Numerical Analysis")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 1100
        window_height = 580

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", anchor="n", fill="x")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.header_sub_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_sub_frame.pack(side="right", anchor="ne")

        self.home_button = ctk.CTkButton(
            self.header_sub_frame,
            width=40,
            height=40,
            corner_radius=8,
            text="",
            hover_color="red",
            command=lambda title="home": self.display_page(title),
            image=ctk.CTkImage(
                light_image=Image.open("./resources/images/home.png"), size=(40, 40)
            ),
        )
        self.home_button.pack(side="right", anchor="ne", padx=5, pady=5)

        button_exit = ctk.CTkButton(
            self.header_sub_frame,
            width=40,
            height=40,
            corner_radius=8,
            text="",
            fg_color="red",
            hover_color="#FF0",
            command=self.quit,
            image=ctk.CTkImage(
                light_image=Image.open("./resources/images/exit.png"), size=(40, 40)
            ),
        )
        button_exit.pack(side="right", anchor="ne", pady=5)

        self.home_text_var.set(value="Welcome to Numerical Analysis !")

        main_label = ctk.CTkLabel(
            self.header_frame,
            textvariable=self.home_text_var,
            font=("Trebuchet MS Bold", 24),
        )
        main_label.place(relx=0.5, rely=0.5, anchor="center")

        button_images = [
            "./resources/images/button1.png",
            "./resources/images/button2.png",
        ]
        button_titles = ["Linear Systems", "Numerical Integration"]

        for i in range(len(button_images)):
            button = ctk.CTkButton(
                self.left_frame,
                command=lambda title=button_titles[i]: self.display_page(title),
                corner_radius=8,
                text=button_titles[i],
                compound="top",
                font=("Trebuchet MS Bold", 16),
                hover_color="red",
                image=ctk.CTkImage(
                    light_image=Image.open(button_images[i]), size=(180, 100)
                ),
            )
            button.pack(padx=1, pady=2)

    def display_page(self, button_title):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        print(button_title)
        if button_title == "home":
            self.home_text_var.set(value="Welcome to Numerical Analysis !")
        elif button_title == "Linear Systems":
            self.home_text_var.set(value="Linear Systems (Ax=B)")

            dialog = Dialog(
                "Matrix dimensions",
                "Enter the dimensions of your matrix",
                ["N", "M"],
                "transparent",
            )
            dim = dialog.get_input()

            try:
                result = (dim[0] == dim[1]) and (int(dim[0]) > 0)
            except (IndexError, ValueError, TypeError):
                result = False

            if result:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                dataFrame.pack(fill="x", padx=5, pady=5)
                dataFrame.columnconfigure(0, weight=1)
                dataFrame.columnconfigure(1, weight=2)
                dataFrame.columnconfigure(3, weight=2)
                dataFrame.columnconfigure(4, weight=1)

                subdataFrame = []
                idata = ["A", "*", "X", "=", "B"]
                for i in range(2):
                    subdataFrame.append([])
                    for j in range(5):
                        subdataFrame[i].append(
                            ctk.CTkFrame(dataFrame, fg_color="transparent")
                        )
                        subdataFrame[i][j].grid(row=i, column=j, sticky="nswe")

                for i in range(len(idata)):
                    tempLab = ctk.CTkLabel(
                        subdataFrame[0][i],
                        text=idata[i],
                        font=("Trebuchet MS Bold", 24),
                    )
                    tempLab.pack()

                AEntries = []
                BEntries = []
                subdataFrame[1][4].columnconfigure(0, weight=1)
                for i in range(int(dim[0])):
                    AEntries.append([])
                    BEntries.append(
                        ctk.CTkEntry(subdataFrame[1][4], font=("Trebuchet MS Bold", 16))
                    )
                    BEntries[i].grid(row=i, column=0, padx=5, pady=5)
                    for j in range(int(dim[1])):
                        if i == 0:
                            subdataFrame[1][0].columnconfigure(j, weight=1)
                        AEntries[i].append(
                            ctk.CTkEntry(
                                subdataFrame[1][0], font=("Trebuchet MS Bold", 16)
                            )
                        )
                        AEntries[i][j].grid(row=i, column=j, padx=5, pady=5)

                tmpLabel = ctk.CTkLabel(
                    subdataFrame[1][1], text="*", font=("Trebuchet MS Bold", 24)
                )
                tmpLabel.pack(expand="True")
                tmpLabel = ctk.CTkLabel(
                    subdataFrame[1][2], text="?", font=("Trebuchet MS Bold", 24)
                )
                tmpLabel.pack(expand="True")
                tmpLabel = ctk.CTkLabel(
                    subdataFrame[1][3], text="=", font=("Trebuchet MS Bold", 24)
                )
                tmpLabel.pack(expand="True")

                typeFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                typeFrame.pack(anchor="center", pady=10)

                radio_var = ctk.IntVar()
                methodList = [
                    "Inverse of A",
                    "Gaussian Elimination",
                    "LU Decomposition",
                    "Cholesky Decomposition",
                ]
                radiobuttons = []
                for i in range(len(methodList)):
                    radiobuttons.append(
                        ctk.CTkRadioButton(
                            typeFrame,
                            text=methodList[i],
                            font=("Trebuchet MS Bold", 20),
                            variable=radio_var,
                            value=i,
                        )
                    )
                    radiobuttons[i].pack(side="left", anchor="center", padx=5, pady=5)

                SolveButton = ctk.CTkButton(
                    self.main_frame,
                    text="Solve for X !",
                    hover_color="red",
                    font=("Trebuchet MS Bold", 20),
                    command=lambda: solveX(radio_var.get()),
                )
                SolveButton.pack()
                self.bind("<Return>", lambda event: SolveButton.invoke())

                SolutionFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                SolutionFrame.pack(padx=10, pady=10)

                def solveX(radiovar):
                    for widgets in SolutionFrame.winfo_children():
                        widgets.destroy()

                    SoluLabel = ctk.CTkLabel(
                        SolutionFrame, text="X = ", font=("Trebuchet MS Bold", 24)
                    )
                    SoluLabel.grid(row=0, column=0)

                    SubSoluFrame = ctk.CTkFrame(SolutionFrame, fg_color="red")
                    SubSoluFrame.grid(row=0, column=1)

                    SolutionFrame.columnconfigure(0, weight=1)
                    SolutionFrame.columnconfigure(1, weight=1)

                    A = []
                    B = np.array([])

                    for i in range(int(dim[0])):
                        A.append([])
                        B = np.append(B, float(BEntries[i].get()))
                        for j in range(int(dim[1])):
                            A[i].append(float(AEntries[i][j].get()))

                    X = None

                    if radiovar == 0:
                        X = np.matmul(np.linalg.inv(A), B.T)
                    elif radiovar == 1:
                        X = resoudre_equation_gauss(A, B)
                    elif radiovar == 2:
                        X = resolution_LU(A, B)
                    elif radiovar == 3:
                        X = resolution_choleski(A, B)

                    XEntries = []

                    if isinstance(X, np.ndarray):
                        if np.any(X != "E"):
                            for i in range(int(dim[0])):
                                XEntries.append(
                                    ctk.CTkLabel(
                                        SubSoluFrame,
                                        text=X[i].round(3),
                                        font=("Trebuchet MS Bold", 24),
                                    )
                                )
                                XEntries[i].grid(row=i, column=0, padx=5, pady=5)
                    else:
                        Caution_Label = ctk.CTkLabel(
                            SubSoluFrame,
                            text="ACHTUNG !\nInkompatible Matrix !\n-------\nWarning !\nIncompatible Matrix !\n-------\nAttention !\nMatrice incompatible !",
                            font=("Trebuchet MS Bold", 22),
                            text_color="white",
                            corner_radius=10,
                        )
                        Caution_Label.pack(pady=10)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nInkompatible Matrixdimensionen !\n-------\nWarning !\nIncompatible Matrix dimensions !\n-------\nAttention !\nDimensions de matrice incompatibles !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(pady=10)

        elif button_title == "Numerical Integration":
            self.home_text_var.set(value="Numerical Integration (∫ f(x)dx)")

            dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            dataFrame.pack(padx=5, pady=5)

            intLabel = ctk.CTkLabel(
                dataFrame,
                text="I = ",
                font=("Trebuchet MS Bold", 32),
                compound="right",
                image=ctk.CTkImage(
                    light_image=Image.open("./resources/images/integral.png"),
                    size=(60, 160),
                ),
            )
            intLabel.grid(row=0, column=0, rowspan=3)

            bEntry = ctk.CTkEntry(
                dataFrame, width=40, height=40, font=("Trebuchet MS Bold", 20)
            )
            bEntry.grid(row=0, column=1, padx=5, pady=5)

            aEntry = ctk.CTkEntry(
                dataFrame, width=40, height=40, font=("Trebuchet MS Bold", 20)
            )
            aEntry.grid(row=2, column=1, padx=5, pady=5)

            intEntry = ctk.CTkEntry(
                dataFrame, width=140, height=40, font=("Trebuchet MS Bold", 20)
            )
            intEntry.grid(row=1, column=2, padx=5, pady=5)

            dxLabel = ctk.CTkLabel(dataFrame, text="dx", font=("Trebuchet MS Bold", 24))
            dxLabel.grid(row=1, column=3, padx=5, pady=5)

            helperFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            helperFrame.pack()

            radio_var = ctk.IntVar()
            methodList = ["Trapezoidal rule", "Simpson's rule"]
            radiobuttons = []
            for i in range(len(methodList)):
                radiobuttons.append(
                    ctk.CTkRadioButton(
                        helperFrame,
                        text=methodList[i],
                        font=("Trebuchet MS Bold", 20),
                        variable=radio_var,
                        value=i,
                    )
                )
                radiobuttons[i].pack(side="left", anchor="center", padx=5, pady=10)

            SolveButton = ctk.CTkButton(
                self.main_frame,
                text="Solve for X !",
                hover_color="red",
                font=("Trebuchet MS Bold", 20),
                command=lambda: solveX(radio_var.get()),
            )
            SolveButton.pack(padx=10, pady=10)
            self.bind("<Return>", lambda event: SolveButton.invoke())

            SFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            SFrame.pack(padx=10, pady=10)

            def solveX(radiovar):
                for widgets in SFrame.winfo_children():
                    widgets.destroy()

                dialog = Dialog(
                    "Length of subintervals",
                    "Enter the value of h\nLength of subintervals",
                    ["h"],
                    "transparent",
                )

                h = float(dialog.get_input()[0])
                a = float(aEntry.get())
                b = float(bEntry.get())

                exp = intEntry.get()

                SolutionFrame = ctk.CTkFrame(SFrame, fg_color="red")
                SolutionFrame.pack(padx=10, pady=10)

                if radiovar == 0:
                    if a < b:
                        f = ne.evaluate(exp)
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {trapezes(a, b, f, h)}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()
                    elif a > b:
                        f = ne.evaluate(exp)
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {-trapezes(b, a, f, h)}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()
                    else:
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {0}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()
                elif radiovar == 1:
                    if a < b:
                        x = np.arange(a, b + (h / 2), h / 2)
                        f = ne.evaluate(exp)
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {simpson(a, b, f, h)}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()
                    elif a > b:
                        x = np.arange(b, a + (h / 2), h / 2)
                        f = ne.evaluate(exp)
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {-simpson(b, a, f, h)}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()
                    else:
                        SoluLabel = ctk.CTkLabel(
                            SolutionFrame,
                            text=f"I = {0}",
                            font=("Trebuchet MS Bold", 24),
                        )
                        SoluLabel.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
