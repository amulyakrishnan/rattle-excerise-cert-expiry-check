from urllib.request import ssl, socket
import datetime, smtplib
hostname = 'gorattle.com'
port = '443'
context = ssl.create_default_context()
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname = hostname) as ssock:
        certificate = ssock.getpeercert()
        #certificate variable contains the certificate data
        print(certificate)

certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
#Logging purpose
print(certExpires)
daysToExpiration = (certExpires - datetime.datetime.now()).days
print(daysToExpiration)

if daysToExpiration is not None or daysToExpiration < 15:
    send_notification(daysToExpiration)

def send_notification(days_to_expire):
    smtp_port = 587
    smtp_server = "smtp.domain.com"
    sender_email = "rattle-operations.com"
    receiver_email= = "rattle-sev2.com"
    password = input("Type your password and press enter: ")
    if days_to_expire == 1:
        days = "1 day"
    else:
        days = str(days_to_expire) + " days"
        
    message = """\
        Subject: Certificate Expiration
        The TLS Certificate for your site expires in {days}"""
    email_context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context = email_context)
        server.login(sender_email, password)
        server.sendmail(sender_email, 
                        receiver_email, 
                        message.format(days = days))

