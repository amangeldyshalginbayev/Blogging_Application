from random import randint
from pprint import pprint
from flask import current_app
from messente_api import (OmnimessageApi, SMS, Omnimessage, Configuration,
                          ApiClient)
from messente_api.rest import ApiException


def send_sms_pin(recipient_phone_number):
    configuration = Configuration()
    configuration.username = current_app.config['MESSENTE_API_USERNAME']
    configuration.password = current_app.config['MESSENTE_API_PASSWORD']
    api_instance = OmnimessageApi(ApiClient(configuration))

    pin_code = randint(1000, 9999)

    sms = SMS(sender="+37258961369",
              text="{} is your FlaskBlog verification code.".format(pin_code))

    omnimessage = Omnimessage(messages=tuple([sms]), to=recipient_phone_number)

    try:
        response = api_instance.send_omnimessage(omnimessage)
        print("Successfully sent Omnimessage with id: %s that consists of "
              "the following messages:" % response.omnimessage_id)
        for message in response.messages:
            pprint(message)
    except ApiException as exception:
        print("Exception when sending an omnimessage: %s\n" % exception)
    else:
        return pin_code
