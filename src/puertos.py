import serial.tools.list_ports
import serial
import cv2
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Variable global para detener las vistas previas
stop_preview = False

def list_ports():
    """
    Lista los puertos COM disponibles.
    """
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

def test_arduino(port):
    """
    Prueba la comunicación con el Arduino enviando y recibiendo un mensaje.
    """

    try:
        ser = serial.Serial(port, 9600, timeout=1)
        ser.close()
        return True
    except:
        return False

def test_cameras():
    """
    Prueba las cámaras conectadas e identifica cuáles están funcionando.
    """
    working_cameras = []
    for idx in range(0, 5):  # Ajusta el rango según el número de cámaras conectadas
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Cámara en índice {idx} está funcionando.")
                working_cameras.append(idx)
            cap.release()
    return working_cameras

def save_config(selected_port, cam1, cam2, cam3):
    """
    Guarda la configuración de puertos y cámaras en un archivo JSON.
    """
    config = {
        "selected_port": selected_port,
        "camera_1": cam1,
        "camera_2": cam2,
        "camera_3": cam3
    }
    with open('puertos.conf', 'w') as json_file:
        json.dump(config, json_file, indent=4)
    print("Configuración guardada en 'puertos.conf'.")
    messagebox.showinfo("Éxito", "Configuración guardada exitosamente.")

def update_frame(cap, label):
    """
    Actualiza el frame de la cámara y lo muestra en el Label proporcionado.
    """
    ret, frame = cap.read()
    if ret:
        # Redimensionamos la imagen a 100x100 píxeles
        frame = cv2.resize(frame, (100, 100))
        # Convertimos el frame de OpenCV (BGR) a un formato que tkinter pueda mostrar (RGB)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Actualizamos la imagen en el Label correspondiente
        label.imgtk = imgtk
        label.config(image=imgtk)

    # Continuamos actualizando el frame después de 10 milisegundos
    label.after(10, lambda: update_frame(cap, label))

def start_camera_preview(camera_index, label, current_cap):
    """
    Inicia la captura de la cámara y actualiza el Label.
    Si ya hay una cámara capturando, la libera.
    """
    if current_cap:  # Si ya hay una cámara previa, la liberamos
        current_cap.release()

    # Creamos una nueva captura de la cámara seleccionada
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    update_frame(cap, label)
    
    return cap  # Devolvemos el objeto de la nueva captura

def on_closing(window, caps):
    """
    Función que se llama cuando se cierra la ventana de tkinter.
    """
    global stop_preview
    stop_preview = True  # Detenemos cualquier vista previa de cámara en curso
    # Liberamos todas las cámaras activas
    for cap in caps:
        if cap:
            cap.release()
    window.destroy()  # Cerramos la ventana de tkinter

def setup_gui(ports, cameras):
    """
    Configura la interfaz gráfica para que el usuario seleccione el puerto y las cámaras.
    """
    window = tk.Tk()
    window.title("Configuración de puertos y cámaras")

    # Layout principal (Horizontal) - Formulario a la izquierda, cámaras a la derecha
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Frame para el formulario (lado izquierdo)
    form_frame = tk.Frame(main_frame)
    form_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Frame para las vistas previas de las cámaras (lado derecho)
    preview_frame = tk.Frame(main_frame)
    preview_frame.pack(side="right", padx=10, pady=10)

    # Si hay más de un puerto, mostrar un dropdown para seleccionarlo
    if len(ports) > 1:
        tk.Label(form_frame, text="Selecciona el puerto COM:").pack(pady=5)
        port_var = tk.StringVar(value=ports[0])
        port_dropdown = ttk.Combobox(form_frame, textvariable=port_var, values=ports)
        port_dropdown.pack(pady=5)
    else:
        port_var = tk.StringVar(value=ports[0])  # Solo un puerto, se selecciona automáticamente
        tk.Label(form_frame, text=f"Puerto seleccionado automáticamente: {ports[0]}").pack(pady=5)

    # Botón para probar el puerto con Arduino
    def on_test_arduino():
        selected_port = port_var.get()
        if test_arduino(selected_port):
            messagebox.showinfo("Éxito", f"El puerto {selected_port} se comunica correctamente con el Arduino.")
        else:
            messagebox.showerror("Error", f"No se pudo establecer comunicación con el Arduino en {selected_port}.")

    test_button = tk.Button(form_frame, text="Probar Arduino", command=on_test_arduino)
    test_button.pack(pady=10)

    # Variables para los dropdowns de las cámaras y las capturas activas
    cam1_var = tk.StringVar(value=cameras[0])
    cam2_var = tk.StringVar(value=cameras[1] if len(cameras) > 1 else cameras[0])
    cam3_var = tk.StringVar(value=cameras[2] if len(cameras) > 2 else cameras[0])

    # Creamos los objetos para las capturas de las cámaras
    cam1_cap = None
    cam2_cap = None
    cam3_cap = None

    # Labels donde se mostrarán las vistas previas de las cámaras (100x100 px)
    tk.Label(preview_frame, text="Vista previa Cámara 1:").pack(pady=5)
    cam1_label = tk.Label(preview_frame, width=100, height=100)
    cam1_label.pack(pady=5)

    tk.Label(preview_frame, text="Vista previa Cámara 2:").pack(pady=5)
    cam2_label = tk.Label(preview_frame, width=100, height=100)
    cam2_label.pack(pady=5)

    tk.Label(preview_frame, text="Vista previa Cámara 3:").pack(pady=5)
    cam3_label = tk.Label(preview_frame, width=100, height=100)
    cam3_label.pack(pady=5)

    # Iniciar las vistas previas de las cámaras seleccionadas
    cam1_cap = start_camera_preview(int(cam1_var.get()), cam1_label, cam1_cap)
    cam2_cap = start_camera_preview(int(cam2_var.get()), cam2_label, cam2_cap)
    cam3_cap = start_camera_preview(int(cam3_var.get()), cam3_label, cam3_cap)

    # Función que reinicia la vista previa al cambiar el índice de la cámara
    def on_camera_change(cam_var, label, current_cap, camera_num):
        if camera_num == 1:
            nonlocal cam1_cap
            cam1_cap = start_camera_preview(int(cam_var.get()), label, cam1_cap)
        elif camera_num == 2:
            nonlocal cam2_cap
            cam2_cap = start_camera_preview(int(cam_var.get()), label, cam2_cap)
        elif camera_num == 3:
            nonlocal cam3_cap
            cam3_cap = start_camera_preview(int(cam_var.get()), label, cam3_cap)

    # Dropdowns para seleccionar las cámaras y reiniciar las vistas previas
    tk.Label(form_frame, text="Selecciona la Cámara 1:").pack(pady=5)
    cam1_dropdown = ttk.Combobox(form_frame, textvariable=cam1_var, values=cameras)
    cam1_dropdown.pack(pady=5)
    cam1_dropdown.bind("<<ComboboxSelected>>", lambda e: on_camera_change(cam1_var, cam1_label, cam1_cap, 1))

    tk.Label(form_frame, text="Selecciona la Cámara 2:").pack(pady=5)
    cam2_dropdown = ttk.Combobox(form_frame, textvariable=cam2_var, values=cameras)
    cam2_dropdown.pack(pady=5)
    cam2_dropdown.bind("<<ComboboxSelected>>", lambda e: on_camera_change(cam2_var, cam2_label, cam2_cap, 2))

    tk.Label(form_frame, text="Selecciona la Cámara 3:").pack(pady=5)
    cam3_dropdown = ttk.Combobox(form_frame, textvariable=cam3_var, values=cameras)
    cam3_dropdown.pack(pady=5)
    cam3_dropdown.bind("<<ComboboxSelected>>", lambda e: on_camera_change(cam3_var, cam3_label, cam3_cap, 3))

    def on_save():
        selected_port = port_var.get()
        cam1 = cam1_var.get()
        cam2 = cam2_var.get()
        cam3 = cam3_var.get()
        if cam1 == cam2 or cam1 == cam3 or cam2 == cam3:
            messagebox.showerror("Error", "Las cámaras deben ser diferentes.")
        else:
            save_config(selected_port, cam1, cam2, cam3)
            on_closing(window, [cam1_cap, cam2_cap, cam3_cap])

    # Botón para guardar y cerrar
    save_button = tk.Button(form_frame, text="Guardar y cerrar", command=on_save)
    save_button.pack(pady=20)

    # Al cerrar la ventana principal de tkinter
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, [cam1_cap, cam2_cap, cam3_cap]))

    window.mainloop()

if __name__ == "__main__":
    # Listar puertos disponibles
    ports = list_ports()
    if not ports:
        print("No se encontraron puertos COM disponibles.")
        exit()

    # Probar cámaras
    cameras = test_cameras()
    if not cameras:
        print("No se encontraron cámaras disponibles.")
        exit()

    # Configurar GUI para que el usuario asigne el puerto y las cámaras
    setup_gui(ports, cameras)
