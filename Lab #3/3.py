# АБГВА
# А: Gmail (через SMTP/IMAP с App Password)
# Б: HTML-письмо с форматированием
# Г: Генерация случайных тестовых данных
# В: Поиск писем с вложениями
# A: Пометить как прочитанное

import smtplib
import imaplib
import email
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

login = "mdelizov@gmail.com"
password = "anmu zocn zczg unxn"

# Отправка письма
rand_number = random.randint(5, 10)
rows = [
    (f"Item {i}", random.randint(1, 100), round(random.uniform(10, 999), 2))
    for i in range(1, 6)
]

html = f"""\
<html>
  <body>
    <div class="number">Случайное число: {rand_number}</div>
    <table>
      <tr>
        <th>Название</th>
        <th>Количество</th>
        <th>Цена</th>
      </tr>
      {''.join(f"<tr><td>{name}</td><td>{qty}</td><td>{price}</td></tr>" for name, qty, price in rows)}
    </table>
  </body>
</html>
"""

msg = MIMEMultipart()
msg["Subject"] = "HTML-письмо с форматированием + генерация случайных тестовых данных"
msg["From"] = login
msg["To"] = login
msg.attach(MIMEText(html, "html"))

server_smtp = smtplib.SMTP("smtp.gmail.com", 587)
server_smtp.starttls()
server_smtp.login(login, password)
server_smtp.sendmail(msg["From"], msg["To"], msg.as_string())
server_smtp.quit()


# Обработка входящей почты
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(login, password)
imap.select("inbox")

status, messages = imap.search(None, 'UNSEEN')
mail_ids = messages[0].split()

for mail_id in mail_ids:
    status, msg_data = imap.fetch(mail_id, '(BODY.PEEK[])')
    if status != 'OK':
        continue

    msg = email.message_from_bytes(msg_data[0][1])

    for part in msg.walk():
        content_disposition = part.get("Content-Disposition")
        if content_disposition and "attachment" in content_disposition.lower():
            imap.store(mail_id, '+FLAGS', '\\Seen')
            break

imap.logout()