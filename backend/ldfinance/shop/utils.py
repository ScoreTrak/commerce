import os

import requests


def send_order_notification(order):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url is None:
        return
    message = f"**{order.product.name}** purchased by **{order.sale.source.name}**"
    response = requests.post(
        webhook_url,
        json={
            "allowed_mentions": {"parse": ["roles"]},
            "content": f":moneybag: <@&780990293515960340>: {message}",
            "embeds": [
                {
                    "title": answer.question.text,
                    "description": answer.text,
                }
                for answer in order.answer_set.all()
            ]
        },
    )
