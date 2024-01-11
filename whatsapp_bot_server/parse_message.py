d = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "8856996819413533",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "16505553333",
                            "phone_number_id": "27681414235104944"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Kerry Fisher"
                                },
                                "wa_id": "16315551234"
                            }
                        ],
                        "messages": [
                            {
                                "from": "16315551234",
                                "id": "wamid.ABGGFlCGg0cvAgo-sJQh43L5Pe4W",
                                "timestamp": "1603059201",
                                "text": {
                                    "body": "Hello this is an answer"
                                },
                                "type": "text"
                            }
                        ]
                    },
                    "field": "messages"
                }
            ]
        }
    ]
}

message = d["entry"][0]['changes'][0]["value"]['messages'][0]
message_type = message['type']
message_id = message['id']
message_text = message['text']['body']
message_from = message['from']



# print(message)
print(message_id, message_from, message_text)