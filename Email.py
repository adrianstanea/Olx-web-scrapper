import configparser
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read('login.ini')

smtp_server = 'smtp.gmail.com'
port = 587

# nu am distribuit parola din motive de securitate
# pentru a recrea functinoalitatea e nevoie de un cont de google care dispune de two factor authentication

# din google account => security => app password se genereaza o parola care se va folosi in locul parolei de la gmail pentru contul introdus de utilizator
# LINK: https://support.google.com/accounts/answer/185833?hl=en

# TREBUIE MODIFICATE LA CONTUL PROPRIU PENTRU A PUTEA TRIMITE EMAIL din fisierul login.ini
password = config['AUTH']['password']
email_from = config['AUTH']['email']


def notify_user(data, prag_pret,  email_to, subject):
    data = filter(lambda x: int(x[0]) < int(prag_pret), data)
    print("Preparing to send email")

    if data:
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(email_from, password)
                print('logged in succesfully')

                # format email message
                msg = create_email(data, email_to, subject, prag_pret)
                print(msg)

                server.sendmail(email_from, email_to, msg)
                server.quit()
                print("*** Email sent successfully ***")
        except:
            print("Email could not be sent")
    else:
        print("No data to send")


def create_email(data: list, email_to: str, subject: str, prag_pret: str):
    print('create_email function was called')
    msg = MIMEMultipart()

    msg['Subject'] = "Subject: " + subject
    msg['From'] = email_from
    msg['To'] = email_to

    def format_data(x):
        price, title, link = x
        return f"""
        <li>
            <h2>Titlu: {title}</h2>
            <ul>
                <li><b>Pret</b>: {price} lei</li>
                <li><b>Link</b>: <a href='{link}'>{link}</a></li>
            </ul>
        </li>
    
    """
    formated_data = map(format_data, data)

    html = f'''
        <html>
            <body>
                <h1>Anunturi cu pretul mai mic de {prag_pret} lei</h1>
                <ul>
                    {''.join(formated_data)}
                </ul>
            </body>
        </html>
    '''

    msg.attach(MIMEText(html, 'html'))
    return msg.as_string()
