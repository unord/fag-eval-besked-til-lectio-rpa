from datetime import datetime, timedelta
from decouple import config
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib
import win32com.client as win32


def receive_email():
    monitoring_status_312 = 2
    monitoring_status_096 = 2
    last_email_date_312 = 0
    last_email_date_096 = 0
    search_period = datetime.now() - timedelta(hours=72)
    print(search_period)

    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace("MAPI")

    for account in mapi.Accounts:
        print(account.DeliveryStore.DisplayName)

    inbox = mapi.GetDefaultFolder(6)

    # *** - ubot@unord.dk indbakke
    messages = mapi.Folders('ubot@unord.dk').Folders("Indbakke").Items

    today = datetime.today()
    start_time = search_period.strftime('%d-%m-%Y %H:%M %p')
    end_time = today.now().strftime('%d-%m-%Y %H:%M %p')

    messages = messages.Restrict("[ReceivedTime] >= '" + start_time + "' And [ReceivedTime] <= '" + end_time + "'")

    messages.Sort("[ReceivedTime]", Descending=False)

    for msg in list(messages):
        print(msg.Subject + " kl. " + str(msg.ReceivedTime))
        if msg.Subject[0:21] == "RPA-312 - Status: 200":
            last_email_date_312 = msg.ReceivedTime
            monitoring_status_312 = 1
        elif msg.Subject[0:10] == "Proces 096":
            last_email_date_096 = msg.ReceivedTime
            monitoring_status_096 = 1
    print("Last date 312: " + str(last_email_date_312))
    print("Last date 096: " + str(last_email_date_096))

    # *** - robotmail indbox
    print("Robotmail indbakke")

    messages = mapi.Folders("robotmail").Folders("Inbox").Items

    messages = messages.Restrict("[ReceivedTime] >= '" + start_time
                                 + "' And [ReceivedTime] <= '" + end_time + "'")

    messages.Sort("[ReceivedTime]", Descending=True)

    for msg in list(messages):
        print(msg.Subject)
        if msg.Subject[0:19] == "Fejl ved proces 312" and msg.ReceivedTime > last_email_date_312:
            monitoring_status_312 = 2
        elif msg.Subject[0:19] == "Fejl ved proces 096" and msg.ReceivedTime > last_email_date_096:
            monitoring_status_096 = 2

    print(monitoring_status_312)
    print(monitoring_status_096)



def send_email_with_attachments(sender: str, receivers: list, subject: str, body: str,
                                ccs: list, bccs: list, files: list = []):

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if files is not None:
        for file in files:
            with open(file, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(file)
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
            msg.attach(part)
    if ccs is not None:
        msg['Cc'] = ', '.join(ccs)
    if bccs is not None:
        msg['Bcc'] = ', '.join(bccs)
    receivers = receivers + ccs + bccs
    server = smtplib.SMTP('smtp.efif.dk', 25)
    server.starttls()
    server.login(config('EMAIL_USER'), config('EMAIL_PASSWORD'))
    text = msg.as_string()
    server.sendmail(sender,  receivers, text)
    server.quit()


def main():
    pass


if __name__ == '__main__':
    main()
