from flask import render_template, current_app

from app.services.email.email_service import EmailService


def send_email(to, subject, content, template):
    try:
        body = render_template(template, email=to, content=content)

        EmailService().send_aws(to, subject, body)
    except Exception as e:
        current_app.logger.error(f"Error while trying to send order email.\n{e}")
