import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

clients = []


def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")


def send_alert():
    alert_message = alert_entry.get()
    if alert_message.lower() == "exit":
        root.quit()  
        return
    
    broadcast(alert_message)
    log_area.insert(tk.END, f"Alert sent: {alert_message}\n")
    log_area.see(tk.END)
    alert_entry.delete(0, tk.END)


def handle_client(client_socket):
    clients.append(client_socket)
    try:
        while True:
            pass  
    finally:
        clients.remove(client_socket)
        client_socket.close()


server_address = ('192.168.208.146', 65432)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen()
print("TCP Notification Server is listening...")


root = tk.Tk()
root.title("TCP Notification Server")
root.geometry("500x400")

header_label = tk.Label(root, text="KONGU ENGINEERING COLLEGE\nCN MINI PROJECT\nNotification Server", font=("Helvetica", 20, "bold"), fg="black")
header_label.pack(pady=10)


log_area = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD, font=("Arial", 12))
log_area.pack(pady=10)
log_area.insert(tk.END, "TCP Notification Server is listening...\n")


alert_entry = tk.Entry(root, width=30, font=("Arial", 14))
alert_entry.pack(pady=5)
send_button = tk.Button(root, text="Send Alert", command=send_alert, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
send_button.pack()


def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


accept_thread = threading.Thread(target=accept_clients, daemon=True)
accept_thread.start()


root.mainloop()


server_socket.close()
