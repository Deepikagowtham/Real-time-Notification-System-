import socket
import tkinter as tk
from tkinter import scrolledtext
import threading


def receive_alerts():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            alert_message = data.decode()
            log_area.insert(tk.END, f"Alert received: {alert_message}\n")
            log_area.see(tk.END)
        except Exception as e:
            log_area.insert(tk.END, f"Error receiving alert: {e}\n")
            break


server_address = ('10.1.34.203', 65432)  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


root = tk.Tk()
root.title("TCP Notification Client")
root.geometry("500x400")

header_label = tk.Label(root, text="KONGU ENGINEERING COLLEGE\nNotification Client", font=("Helvetica", 20, "bold"), fg="black")
header_label.pack(pady=10)


log_area = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD, font=("Arial", 12))
log_area.pack(pady=10)
log_area.insert(tk.END, "Listening for alerts...\n")


receive_thread = threading.Thread(target=receive_alerts, daemon=True)
receive_thread.start()


root.mainloop()


client_socket.close()
