"""
Local HTTP CONNECT proxy to route GitHub traffic through accessible edge IPs in restricted networks.
"""

import socket
import threading
import select
import sys

ROUTING = {
    "github.com": "20.205.243.166",
    "api.github.com": "20.205.243.168"
}

def forward_stream(src, dst):
    try:
        while True:
            r, _, _ = select.select([src], [], [], 180)
            if not r:
                break
            data = src.recv(32768)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            src.close()
        except:
            pass
        try:
            dst.close()
        except:
            pass

def handle_client(client_sock):
    try:
        req_line = client_sock.recv(4096).decode('latin1', 'ignore')
        if not req_line.startswith("CONNECT"):
            client_sock.close()
            return
        
        # Parse target host and port
        parts = req_line.split(" ")
        host_port = parts[1]
        host, port = host_port.split(":")
        port = int(port)
        
        target_ip = ROUTING.get(host, host)
        remote_sock = socket.create_connection((target_ip, port), timeout=10)
        client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        
        t1 = threading.Thread(target=forward_stream, args=(client_sock, remote_sock), daemon=True)
        t2 = threading.Thread(target=forward_stream, args=(remote_sock, client_sock), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        pass
    finally:
        try:
            client_sock.close()
        except:
            pass

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8989
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(50)
    print(f"Proxy server running on 127.0.0.1:{port}", flush=True)
    while True:
        try:
            client, _ = server.accept()
            th = threading.Thread(target=handle_client, args=(client,), daemon=True)
            th.start()
        except KeyboardInterrupt:
            break
        except Exception:
            pass

if __name__ == "__main__":
    main()
