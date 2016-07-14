# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase
from labour.querybuilder import QueryBuilder, add_prefix


# NIGHT_WORK_CHOICES = [
#     (u'miel', u'Työskentelen mielelläni yövuorossa'),
#     (u'tarv', u'Voin tarvittaessa työskennellä yövuorossa'),
#     (u'ei', u'En vaan voi työskennellä yövuorossa'),
# ]

SHIRT_SIZES = [
    (u'NO_SHIRT', u'Ei paitaa'),

    (u'XS', u'XS Unisex'),
    (u'S', u'S Unisex'),
    (u'M', u'M Unisex'),
    (u'L', u'L Unisex'),
    (u'XL', u'XL Unisex'),
    (u'XXL', u'XXL Unisex'),
    # (u'3XL', u'3XL Unisex'),
    # (u'4XL', u'4XL Unisex'),
    # (u'5XL', u'5XL Unisex'),

    # (u'LF_XS', u'XS Ladyfit'),
    (u'LF_S', u'S Ladyfit'),
    (u'LF_M', u'M Ladyfit'),
    (u'LF_L', u'L Ladyfit'),
    # (u'LF_XL', u'XL Ladyfit'),
]


SHIFT_TYPE_CHOICES = [
    (u'yksipitka', 'Yksi pitkä vuoro'),
    (u'montalyhytta', 'Monta lyhyempää vuoroa'),
    (u'kaikkikay', 'Kumpi tahansa käy'),
]

TOTAL_WORK_CHOICES = [
    (u'8h', 'Minimi - 8 tuntia'),
    (u'12h', '10–12 tuntia'),
    (u'yli12h', 'Työn Sankari! Yli 12 tuntia!'),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class EventDay(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(max_length=15,
        verbose_name=u'Toivottu työvuoron pituus',
        help_text=u'Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(max_length=15,
        verbose_name=u'Toivottu kokonaistyömäärä',
        help_text=u'Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).',
        choices=TOTAL_WORK_CHOICES,
    )

    # night_work = models.CharField(max_length=5,
    #     verbose_name=u'Voitko työskennellä yöllä?',
    #     help_text=u'Yötöitä voi olla ainoastaan lauantain ja sunnuntain välisenä yönä.',
    #     choices=NIGHT_WORK_CHOICES,
    # )

    # construction = models.BooleanField(
    #     default=False,
    #     verbose_name=u'Voin työskennellä jo perjantaina',
    #     # help_text=u'Huomaathan, että perjantain ja lauantain väliselle yölle ei ole tarjolla majoitusta.',
    # )

    work_days = models.ManyToManyField(EventDay,
        verbose_name=u'Tapahtumapäivät',
        help_text='Vänkärit: Minä päivinä olet halukas työskentelemään? Ohjelmanjärjestäjät: Tarjoatko ohjelmaasi Pyryconiin, Yukiconiin vai kumpaan tahansa?',
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name=u'Haluan todistuksen työskentelystäni Yukiconissa',
    )

    # certificate_delivery_address = models.TextField(
    #     blank=True,
    #     verbose_name=u'Työtodistuksen toimitusosoite',
    #     help_text=u'Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, '
    #         u'postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.',
    # )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name=u'Paidan koko',
        help_text=u'Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. '
            u'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
            u'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
            u'target="_blank">ladyfit-paita</a>',
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name=u'Erikoisruokavalio'
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name=u'Muu erikoisruokavalio',
        help_text=u'Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, '
            u'ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot '
            u'huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.'
    )

    # need_lodging = models.BooleanField(
    #     default=False,
    #     verbose_name=u'Tarvitsen lattiamajoitusta lauantain ja sunnuntain väliseksi yöksi',
    # )

    prior_experience = models.TextField(
        blank=True,
        verbose_name=u'Työkokemus',
        help_text=u'Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista '
            u'tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä '
            u'hakemassasi tehtävässä.'
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name=u'Alustavat työvuorotoiveet',
        help_text=u'Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat '
            u'osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.'
    )

    free_text = models.TextField(
        blank=True,
        verbose_name=u'Vapaa alue',
        help_text=u'Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole '
            u'omaa kenttää yllä, käytä tätä kenttää.'
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm
        return ProgrammeSignupExtraForm

    @staticmethod
    def get_query_class():
        raise NotImplementedError()
