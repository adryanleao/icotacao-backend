import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from app.services.sqlalchemy.extensions import ses


class EmailService(object):
    def __init__(self, *args, **kwargs):
        self.conn = ses

    def send_aws(self, recipient, subject, text, file=None, file_url=None, attachment_name=None,
                 sender='I-COTACAO <suporte@icotacao.com.br>'):

        if os.environ['APP_ENV'] == 'development':
            recipient = os.environ['EMAIL_TESTE']
            
        CHARSET = "UTF-8"
        BODY_TEXT = text
        BODY_HTML = text

        # Envio de anexo
        if file is not None:
            msg = MIMEMultipart('mixed')
            # Add subject, from and to lines.
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            msg_body = MIMEMultipart('alternative')
            textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
            htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
            # Add the text and HTML parts to the child container.
            msg_body.attach(textpart)
            msg_body.attach(htmlpart)
            # Define the attachment part and encode it using MIMEApplication.
            get_dir = os.getcwd()
            if attachment_name is None:
                attachment_name = file

            r = requests.get(file_url)
            if os.path.exists(f'{get_dir}/tmp'):
                pass
            else:
                os.mkdir(f'{get_dir}/tmp')
            with open(f'{get_dir}/tmp/{file}', 'wb') as f:
                f.write(r.content)
            att = MIMEApplication(open(f'{get_dir}/tmp/{file}', 'rb').read())
            att.add_header('Content-Disposition', 'attachment', filename=attachment_name)
            if os.path.exists(f'{get_dir}/tmp/{file}'):
                print("File exists")
            else:
                print("File does not exists")
            # Attach the multipart/alternative child container to the multipart/mixed
            # parent container.
            msg.attach(msg_body)
            # Add the attachment to the parent container.
            msg.attach(att)

        try:
            if file is None:
                response = self.conn.send_email(
                    Destination={
                        'ToAddresses': [
                            recipient,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': subject,
                        },
                    },
                    Source=sender
                )
            else:
                response = self.conn.send_raw_email(
                    Source=msg['From'],
                    Destinations=[
                        msg['To']
                    ],
                    RawMessage={
                        'Data': msg.as_string(),
                    }
                )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                os.remove(f'{get_dir}/tmp/{file}')
                return True
            else:
                os.remove(f'{get_dir}/tmp/{file}')
                return False
        except:
            return False
