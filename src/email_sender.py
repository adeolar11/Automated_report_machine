import os
import smtplib

from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# ---------------------------------
# LOAD .ENV
# ---------------------------------

def load_env():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    env_path = os.path.join(
        base_dir,
        ".env"
    )

    if not os.path.exists(env_path):
        return

    with open(
        env_path,
        "r"
    ) as file:

        for line in file:

            line = line.strip()

            if (
                line
                and not line.startswith("#")
                and "=" in line
            ):

                key, value = line.split(
                    "=",
                    1
                )

                os.environ[
                    key.strip()
                ] = value.strip()


# ---------------------------------
# EMAIL REPORT
# ---------------------------------

def email_report(
    to_emails,
    report_path,
    chart_path,
    sender_email,
    sender_password
):

    if isinstance(
        to_emails,
        str
    ):

        to_emails = [
            email.strip()
            for email in to_emails.split(",")
            if email.strip()
        ]


    msg = MIMEMultipart()

    msg["From"] = sender_email

    msg["To"] = ", ".join(
        to_emails
    )

    msg["Subject"] = (
        "Weekly Sales Report - "
        + datetime.now().strftime(
            "%B %d, %Y"
        )
    )


    body = (
        "Hello Team,\n\n"

        "Please find attached the "
        "automated weekly sales report.\n\n"

        "The email contains:\n"
        "- Excel sales report\n"
        "- Sales performance dashboard\n\n"

        "Report generated on: "
        + datetime.now().strftime(
            "%B %d, %Y at %H:%M"
        )

        + "\n\n"

        "Best regards,\n"
        "Codex Team Automated Reporting System"
    )


    msg.attach(
        MIMEText(
            body,
            "plain"
        )
    )


    # ---------------------------------
    # ATTACHMENTS
    # ---------------------------------

    for file_path in [
        report_path,
        chart_path
    ]:

        if not os.path.exists(
            file_path
        ):

            print(
                f"Attachment not found: "
                f"{file_path}"
            )

            return False


        try:

            with open(
                file_path,
                "rb"
            ) as file:

                part = MIMEBase(
                    "application",
                    "octet-stream"
                )

                part.set_payload(
                    file.read()
                )

            encoders.encode_base64(
                part
            )

            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(file_path)}"'
            )

            msg.attach(part)

        except Exception as error:

            print(
                f"Failed to attach "
                f"{file_path}: {error}"
            )

            return False


    # ---------------------------------
    # SEND
    # ---------------------------------

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30
        ) as server:

            server.login(
                sender_email,
                sender_password
            )

            server.send_message(msg)


        print(
            f"Report emailed to "
            f"{len(to_emails)} recipient(s)"
        )

        return True


    except smtplib.SMTPAuthenticationError:

        print(
            "Email authentication failed."
        )

        print(
            "Use a Gmail App Password."
        )

        return False


    except Exception as error:

        print(
            f"Failed to send email: {error}"
        )

        return False