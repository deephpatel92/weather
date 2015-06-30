from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

import time
import datetime
import json
import unirest


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

        wordformean = messageProtocolEntity.getBody().lower()
        response = self.GetCurrentScore(wordformean)

        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
                response,
                to = messageProtocolEntity.getFrom())

        self.toLower(receipt)
        self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery", entity.getFrom())
        self.toLower(ack)

    def GetCurrentScore(self, word):

        url = "https://montanaflynn-dictionary.p.mashape.com/define?word=" + word

        # These code snippets use an open-source library.
        response = unirest.get(url,
            headers={
                "X-Mashape-Key": "j6rDcjfVcVmshxp0Y102O2cL6vDrp16mL1FjsnsgRqpcl6fC3L",
                "Accept": "application/json"
            }
        )

        resp = word + '\n\n'

        data = json.dumps(response.body, separators=(',',':'))
        meanings = (json.loads(data))["definitions"]
        
        count = 0
        for meaning in meanings:
            count = count + 1
            resp = resp + 'm' + str(count) +' : ' + str(meaning["text"]) + '\n\n'

        # Create Text response
        text_response = str(resp)

        #Return details
        return str(text_response)