import smtplib
import emailconfig


def send_results(target_email, url, hash):
    if(target_email):
        gmail_user = emailconfig.email
        gmail_password = emailconfig.password

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)

        mail = """
        From: {}
        To: {}
        Subject: MD5

        URL: {}
        HASH: {}
        """.format(gmail_user, target_email, url, hash)

        server.sendmail(gmail_user, target_email, mail)
        server.close()
