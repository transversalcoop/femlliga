import json

from django.shortcuts import aget_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Agreement, Message, Organization
from .utils import create_agreement_message


class AgreementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.organization_id = kwargs["organization_id"]
        self.agreement_id = kwargs["agreement_id"]

        # check user owns agreement; we need to prefetch, or else it raises exceptions because of sync operations
        self.organization = await aget_object_or_404(
            Organization.objects.prefetch_related("creator"), pk=self.organization_id
        )
        if self.scope["user"] != self.organization.creator:
            raise PermissionDenied()

        self.agreement = await aget_object_or_404(
            Agreement.objects.prefetch_related("solicitor", "solicitee"),
            pk=self.agreement_id,
        )
        if (
            self.agreement.solicitor != self.organization
            and self.agreement.solicitee != self.organization
        ):
            raise PermissionDenied()

        await self.channel_layer.group_add(self.agreement_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.agreement_id, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)["message"]
        m = await create_agreement_message(self.agreement, self.organization, message)
        if m:
            await self.channel_layer.group_send(
                self.agreement_id,
                {
                    "type": "chat.message",
                    "id": str(m.id),
                    "message": message,
                    "sent_on": m.sent_on.isoformat(),
                    "sent_by": str(self.organization.id),
                },
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "id": event["id"],
                    "message": event["message"],
                    "sent_on": event["sent_on"],
                    "sent_by": event["sent_by"],
                    "read": False,
                }
            )
        )
