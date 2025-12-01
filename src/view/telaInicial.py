import tkinter as tk

def CriarTelaInicial(container, mostrar_tela1, mostrar_tela2):
    frame = tk.Frame(container)
    
    title = tk.Label(frame, text="Cálculo Numérico - Trabalho Prático", font=("Arial", 16, "bold"))
    title.pack(pady=30)
    
    subtitle = tk.Label(frame, text="Selecione um capítulo para começar:", font=("Arial", 12))
    subtitle.pack(pady=10)
    
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=40)
    
    tk.Button(button_frame, text="Capítulo 02 - Busca de Raízes", command=mostrar_tela1, 
              width=25, height=2, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(button_frame, text="Capítulo 03 - Sistemas Lineares", command=mostrar_tela2,
              width=25, height=2, font=("Arial", 11, "bold"), bg="#2196F3", fg="white").pack(pady=10)
    
    return frame
