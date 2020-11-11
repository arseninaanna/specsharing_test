from celery import shared_task
from lxml import etree as et
import requests
from .models import CurrencyMap


CURRENCY_STORAGE_URL = "https://www.cbr-xml-daily.ru/daily.xml"


@shared_task
def sample_task():
    print("The sample task just ran.")


@shared_task
def update_currency():
    currency_xml = requests.get(CURRENCY_STORAGE_URL, allow_redirects=True)
    tree = et.fromstring(currency_xml.content)

    for element in tree:
        currency_code, value = None, None

        for child in element:
            if child.tag == "CharCode":
                currency_code = child.text
            if child.tag == "Value":
                value = child.text

        if currency_code and value:
            currency = CurrencyMap.objects.get(currency_code=currency_code)
            if currency:
                currency.value = float(value)
            else:
                currency = CurrencyMap(currency_code=currency_code, value=float(value))
            currency.save()
