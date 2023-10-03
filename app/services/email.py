class EmailSender:
    def __init__(self):
        self.from_email = "notification@mail.com"

    def send_email(self, subject, message, to_email):
        """
        When the smtp server is configured use that to send real Emails
        :param subject:
        :param message:
        :param to_email:
        :param from_email:
        :return:
        """
        print(f"from: {self.from_email}")
        print(f"Subject: {subject}")
        print(f"To: {to_email}")
        print(f"Message: {message}")
