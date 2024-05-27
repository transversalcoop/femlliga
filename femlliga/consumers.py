import json

from django.shortcuts import aget_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Agreement, Message, Organization


class AgreementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.organization_id = kwargs["organization_id"]
        self.agreement_id = kwargs["agreement_id"]

        # TODO FL103 check user logged in and owns organization and agreement
        if True:
            self.agreement = await aget_object_or_404(Agreement, pk=self.agreement_id)
            self.organization = await aget_object_or_404(
                Organization, pk=self.organization_id
            )
            await self.channel_layer.group_add(self.agreement_id, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.agreement_id, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)["message"]
        m = await Message.objects.acreate(
            sent_by=self.organization,
            message=message,
            agreement=self.agreement,
        )
        await self.channel_layer.group_send(
            self.agreement_id,
            {
                "type": "chat.message",
                "message": message,
                "sent_on": m.sent_on.isoformat(),
                "sent_by": str(self.organization.id),
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sent_on": event["sent_on"],
                    "sent_by": event["sent_by"],
                }
            )
        )
