def detect_service(port, banner):
    banner = banner.lower()

    if port == 22:
        return "SSH"
    if port in (80, 8080):
        return "HTTP"
    if port == 443:
        return "HTTPS"
    if port == 21:
        return "FTP"
    if port == 25:
        return "SMTP"
    if "mysql" in banner:
        return "MySQL"

    return "Unknown"
