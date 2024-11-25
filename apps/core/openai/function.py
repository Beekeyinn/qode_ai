SEND_MAIL = {
    "name": "send_mail",
    "description": "Sends mail to the reciever.",
    "parameters": {
        "type": "object",
        "properties": {
            "reciever": {
                "type": "string",
                "format": "email",
                "description": "Email address of the reciever",
            },
            "subject": {"type": "string", "description": "Subject of email address."},
            "message": {
                "type": "string",
                "description": "Email message to send to  the reciever.",
            },
        },
        "required": ["reciever", "subject", "message"],
    },
}
