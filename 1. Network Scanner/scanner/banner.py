def grab_banner(sock, target, port):
    try:
        sock.settimeout(2)

        if port == 80:
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"User-Agent: Mozilla/5.0\r\n"
                f"Connection: close\r\n\r\n"
            )
            sock.sendall(request.encode())

            response = b""
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                response += data

            text = response.decode(errors="ignore")
            for line in text.split("\r\n"):
                if line.lower().startswith("server:"):
                    return line

        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner if banner else "No banner"

    except:
        return "No banner"
