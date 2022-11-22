from config import Config
from app.admin.notification.models import Notification, NotificationSend
from app.admin.user.models import User
from app.services.email.send_email import send_email
from app.services.utils.utils import float_to_real_money


def create_notification(quote, type="provider"):
    try:
        quote_id = quote["id"]
        quote_name = quote["name"]
    except:
        quote_id = quote.id
        quote_name = quote.name


    if type == "provider":
        if quote["status"] == 2:
            notification_dict = {
                "quote_id": quote_id,
                "icon": "https://img.icons8.com/material-rounded/24/000000/appointment-reminders.png",
                "name": f"Proposta aceita para a cotação: {quote_name}",
                "description": "A sua proposta foi aceita!"
            }
        else:
            notification_dict = {
                "quote_id": quote_id,
                "icon": "https://img.icons8.com/material-rounded/24/000000/appointment-reminders.png",
                "name": f"Nova cotação: {quote_name}",
                "description": "Uma nova cotação está disponível para oferta."
            }
    else:
        notification_dict = {
            "quote_id": quote_id,
            "icon": "https://img.icons8.com/material-rounded/24/000000/appointment-reminders.png",
            "name": f"Nova proposta!",
            "description": f"Uma nova proposta para a cotação: {quote_name} está disponível."
        }

    item = Notification().create_item(notification_dict).save()

    return item

def send_notification(user, notification):

    notification_dict = {
        "user_id": user.id,
        "notification_id": notification.id,
        "icon": notification.icon,
        "name": notification.name,
        "description": notification.description
    }

    NotificationSend().create_item(notification_dict).save()


def send_to_providers_email_notification(quote):
    providers = User.query.filter(User.receive_quotes == 1,
                                  User.deleted_at.is_(None),
                                  User.status == 1)

    # CREATE NOTIFICATION
    notification = create_notification(quote)

    subject = "Nova Cotação"
    template = "email/available_quote.html"
    content = quote
    for provider in providers:
        to = provider.email
        content["redirect_url"] = f"{Config.SITE_HTTPS}/user/quotations/{quote['id']}"

        # SEND EMAIL
        send_email(to, subject, content=content, template=template)

        # SEND NOTIFICATION
        send_notification(provider, notification)
        

def send_proposal_accepted_email(quote, company_id):
    provider = User.query.filter(User.company_id == company_id,
                                 User.deleted_at.is_(None),
                                 User.status == 1).first()

    # CREATE NOTIFICATION
    notification = create_notification(quote)

    subject = "Proposta aceita"
    template = "email/proposal_accepted.html"
    content = quote
    to = provider.email
    content["redirect_url"] = f"{Config.SITE_HTTPS}/user/quotations/{quote['id']}"

    # SEND EMAIL
    send_email(to, subject, content=content, template=template)

    # SEND NOTIFICATION
    send_notification(provider, notification)


def send_to_client_email(quote, proposal):
    client = User.query.filter(User.id == quote.user.id,
                                  User.deleted_at.is_(None),
                                  User.status == 1).first()

    notification = create_notification(quote, "client")

    subject = "Nova Proposta"
    template = "email/proposal.html"
    content = proposal
    if "price" in content:
        content["price"] = float_to_real_money(content["price"])
    content["client_name"] = quote.user.name
    content["quote_name"] = quote.name
    content["redirect_url"] = f"{Config.SITE_HTTPS}/user/quotations/{quote.id}"

    to = client.email
    send_email(to, subject, content=content, template=template)

    send_notification(client, notification)
