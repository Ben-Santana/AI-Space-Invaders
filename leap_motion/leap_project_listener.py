import socket
import json
import threading

def leap_data_listener(worldstate, screen_width, handle_shooting):
    host, port = '127.0.0.1', 65432
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            leap_data = json.loads(data.decode())
            leap_x = leap_data['x']
            shoot_signal = leap_data.get("shoot", False)

            # Map Leap Motion x-range to screen width
            screen_x = int((leap_x + 150) * (screen_width / 300))
            worldstate.player.x = max(0, min(screen_width - worldstate.player.width, screen_x))

            # Trigger shooting if shoot_signal is True
            if shoot_signal:
                handle_shooting(worldstate)
        
        except Exception as e:
            print(f"Error in leap_data_listener: {e}")

# Function to start the listener in a new thread
def start_leap_listener(worldstate, screen_width, handle_shooting):
    listener_thread = threading.Thread(target=leap_data_listener, args=(worldstate, screen_width, handle_shooting))
    listener_thread.daemon = True
    listener_thread.start()