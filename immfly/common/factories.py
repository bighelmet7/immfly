import factory

from common.models import Language
from utils import random_letters


class LanguageFactory(factory.DjangoModelFactory):

    class Meta:
        model = Language

    code = factory.LazyAttribute(lambda x: random_letters(2))
    name = factory.LazyAttribute(lambda x: random_letters(10))
