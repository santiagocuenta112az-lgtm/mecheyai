import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
import threading

# =========================
# APARIENCIA
# =========================

ctk.set_appearance_mode("dark")

# negro puro
ctk.set_default_color_theme("dark-blue")

# =========================
# VENTANA
# =========================

app = ctk.CTk()

app.title("Glamrock Freddy")

app.configure(fg_color="black")

app.update_idletasks()

app.geometry(
    f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0"
)

app.attributes("-fullscreen", True)
app.attributes("-topmost", True)

app.after(
    100,
    lambda: app.attributes("-fullscreen", True)
)

# salir con ESC
app.bind("<Escape>", lambda e: app.destroy())

# =========================
# FRAME PRINCIPAL
# =========================

main_frame = ctk.CTkFrame(
    app,
    fg_color="black"
)

main_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

# =========================
# GRID
# =========================

main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=4)
main_frame.rowconfigure(2, weight=2)
main_frame.rowconfigure(3, weight=1)

main_frame.columnconfigure(0, weight=1)

# =========================
# ESTADO
# =========================

texto_estado = ctk.CTkLabel(
    main_frame,
    text="Freddy listo",
    font=("Arial", 34),
    text_color="white"
)

texto_estado.grid(
    row=0,
    column=0,
    pady=10
)

# =========================
# IMÁGENES
# =========================

idle_img = Image.open(
    "/home/salvador/freddy_ai/freddy_idle.png"
)

listen_img = Image.open(
    "/home/salvador/freddy_ai/freddy_listening.png"
)

talk_img = Image.open(
    "/home/salvador/freddy_ai/freddy_talking.png"
)

# tamaño

idle_img = idle_img.resize((320, 320))
listen_img = listen_img.resize((320, 320))
talk_img = talk_img.resize((320, 320))

# convertir

idle_tk = ImageTk.PhotoImage(idle_img)
listen_tk = ImageTk.PhotoImage(listen_img)
talk_tk = ImageTk.PhotoImage(talk_img)

# =========================
# IMAGEN LABEL
# =========================

imagen_label = tk.Label(
    main_frame,
    image=idle_tk,
    bg="black",
    borderwidth=0,
    highlightthickness=0
)

imagen_label.grid(
    row=1,
    column=0,
    pady=10
)

# =========================
# RESPUESTA
# =========================

respuesta_label = ctk.CTkTextbox(
    main_frame,
    width=1100,
    height=100,
    font=("Arial", 20),
    wrap="word",
    fg_color="black",
    text_color="white",
    border_color="white",
    border_width=2
)

respuesta_label.insert(
    "1.0",
    "Hola superstar! Estoy listo para ayudarte."
)

respuesta_label.configure(
    state="disabled"
)

respuesta_label.grid(
    row=2,
    column=0,
    padx=20,
    pady=10
)

# =========================
# ACTUALIZAR TEXTO
# =========================

def actualizar_texto(texto):

    respuesta_label.configure(state="normal")

    respuesta_label.delete("1.0", "end")

    respuesta_label.insert(
        "1.0",
        texto
    )

    respuesta_label.configure(state="disabled")

# =========================
# FUNCIÓN IA
# =========================

def escuchar():

    texto_estado.configure(
        text="Escuchando..."
    )

    imagen_label.configure(
        image=listen_tk
    )

    actualizar_texto(
        "Freddy está escuchando..."
    )

    def ejecutar_ia():

        # ejecutar IA

        os.system(
            "bash -c 'cd /home/salvador/freddy_ai && "
            "source voice_env/bin/activate && "
            "python voice_ai.py'"
        )

        # cambiar imagen

        texto_estado.configure(
            text="Freddy hablando..."
        )

        imagen_label.configure(
            image=talk_tk
        )

        # leer respuesta

        try:

            with open(
                "/home/salvador/freddy_ai/respuesta.txt",
                "r",
                encoding="utf-8"
            ) as f:

                respuesta = f.read()

                actualizar_texto(
                    respuesta
                )

        except:

            actualizar_texto(
                "No pude leer la respuesta."
            )

        # volver a idle

        texto_estado.configure(
            text="Freddy listo"
        )

        imagen_label.configure(
            image=idle_tk
        )

    # threading

    threading.Thread(
        target=ejecutar_ia,
        daemon=True
    ).start()

# =========================
# BOTÓN
# =========================

boton = ctk.CTkButton(
    main_frame,
    text="ESCUCHAR",
    font=("Arial", 30),
    width=300,
    height=70,
    command=escuchar,
    fg_color="#222222",
    hover_color="#333333",
     text_color="white"
)

boton.grid(
    row=3,
    column=0,
    pady=20
)

# =========================
# ACTUALIZAR ESTADO VISUAL
# =========================

def actualizar_estado_visual():

    try:

        with open(
            "/home/salvador/freddy_ai/estado.txt",
            "r",
            encoding="utf-8"
        ) as f:

            estado = f.read().strip()

        if estado == "escuchando":

            imagen_label.configure(
                image=listen_tk
            )

            texto_estado.configure(
                text="Escuchando..."
            )

        elif estado == "pensando":

            imagen_label.configure(
                image=idle_tk
            )

            texto_estado.configure(
                text="Pensando..."
            )

        elif estado == "hablando":

            imagen_label.configure(
                image=talk_tk
            )

            texto_estado.configure(
                text="Hablando..."
            )

        else:

            imagen_label.configure(
                image=idle_tk
            )

            texto_estado.configure(
                text="Freddy listo"
            )

    except:
        pass

    app.after(
        200,
        actualizar_estado_visual
    )

# iniciar monitor visual

actualizar_estado_visual()

# =========================
# LOOP
# =========================

app.mainloop()
