from datetime import datetime, timedelta

import pytz
from dateutil import parser
from flask import url_for
from flask_babel import _
from notifications_utils.formatters import unescaped_formatted_list
from notifications_utils.letter_timings import letter_can_be_cancelled
from notifications_utils.postal_address import PostalAddress
from notifications_utils.timezones import (
    convert_bst_to_utc,
    convert_utc_to_bst,
    utc_string_to_aware_gmt_datetime,
)


def printing_today_or_tomorrow(created_at):
    print_cutoff = convert_bst_to_utc(convert_utc_to_bst(datetime.utcnow()).replace(hour=17, minute=30)).replace(
        tzinfo=pytz.utc
    )
    created_at = utc_string_to_aware_gmt_datetime(created_at)

    if created_at < print_cutoff:
        return _("today")
    else:
        return _("tomorrow")


def get_letter_printing_statement(status, created_at, long_form=True):
    created_at_dt = parser.parse(created_at).replace(tzinfo=None)
    if letter_can_be_cancelled(status, created_at_dt):
        decription = _("Printing starts") if long_form else _("Printing")
        return _("%%s %%s at 5:30pm") % (decription, printing_today_or_tomorrow(created_at))
    else:
        printed_datetime = utc_string_to_aware_gmt_datetime(created_at) + timedelta(hours=6, minutes=30)
        if printed_datetime.date() == datetime.now().date():
            return _("Printed today at 5:30pm")
        elif printed_datetime.date() == datetime.now().date() - timedelta(days=1):
            return _("Printed yesterday at 5:30pm")

        printed_date = printed_datetime.strftime("%d %B").lstrip("0")
        description = _("Printed on") if long_form else _("Printed")

        return _("%%s %%s at 5:30pm") % (description, printed_date)


LETTER_VALIDATION_MESSAGES = {
    "letter-not-a4-portrait-oriented": {
        "title": _("Your letter is not A4 portrait size"),
        "detail": (
            _(
                "You need to change the size or orientation of {invalid_pages}. <br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--destructive" href="{letter_spec_guidance}" target="_blank">'
                "letter specification"
                "</a>."
            )
        ),
        "summary": (
            _(
                "Validation failed because {invalid_pages} {invalid_pages_are_or_is} not A4 portrait size.<br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--no-visited-state" href="{letter_spec_guidance}">'
                "letter specification"
                "</a>."
            )
        ),
    },
    "content-outside-printable-area": {
        "title": "Your content is outside the printable area",
        "detail": (
            _(
                "You need to edit {invalid_pages}.<br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--destructive" href="{letter_spec_guidance}">'
                "letter specification"
                "</a>."
            )
        ),
        "summary": (
            _(
                "Validation failed because content is outside the printable area on {invalid_pages}.<br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--no-visited-state" href="{letter_spec_guidance}" target="_blank">'
                "letter specification"
                "</a>."
            )
        ),
    },
    "letter-too-long": {
        "title": "Your letter is too long",
        "detail": (
            _(
                "Letters must be 10 pages or less (5 double-sided sheets of paper). <br>"
                "Your letter is {page_count} pages long."
            )
        ),
        "summary": (
            _(
                "Validation failed because this letter is {page_count} pages long.<br>"
                "Letters must be 10 pages or less (5 double-sided sheets of paper)."
            )
        ),
    },
    "no-encoded-string": {"title": _("Sanitise failed - No encoded string")},
    "unable-to-read-the-file": {
        "title": _("There’s a problem with your file"),
        "detail": _("Notify cannot read this PDF. <br>Save a new copy of your file and try again."),
        "summary": _(
            "Validation failed because Notify cannot read this PDF.<br> Save a new copy of your file and try again."
        ),
    },
    "address-is-empty": {
        "title": "The address block is empty",
        "detail": (
            _(
                "You need to add a recipient address.<br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--destructive" href="{letter_spec_guidance}" target="_blank">'
                "letter specification"
                "</a>."
            )
        ),
        "summary": (
            _(
                "Validation failed because the address block is empty.<br>"
                "Files must meet our "
                '<a class="govuk-link govuk-link--no-visited-state" href="{letter_spec_guidance}" target="_blank">'
                "letter specification"
                "</a>."
            )
        ),
    },
    "not-a-real-uk-postcode": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("The last line of the address must be a real UK postcode."),
        "summary": _("Validation failed because the last line of the address is not a real UK postcode."),
    },
    "cant-send-international-letters": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("You do not have permission to send letters to other countries."),
        "summary": _("Validation failed because your service cannot send letters to other countries."),
    },
    "not-a-real-uk-postcode-or-country": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("The last line of the address must be a UK postcode or " "another country."),
        "summary": _("Validation failed because the last line of the address is not a UK postcode or another country."),
    },
    "not-enough-address-lines": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("The address must be at least %s lines long.") % PostalAddress.MIN_LINES,
        "summary": (
            _("Validation failed because the address must be at least %s lines long.") % PostalAddress.MIN_LINES
        ),
    },
    "too-many-address-lines": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("The address must be no more than %s lines long.") % PostalAddress.MAX_LINES,
        "summary": (
            _("Validation failed because the address must be no more than %s lines long.") % PostalAddress.MAX_LINES
        ),
    },
    "invalid-char-in-address": {
        "title": _("There’s a problem with the address for this letter"),
        "detail": _("Address lines must not start with any of the following characters: @ ( ) = [ ] ” \\ / , < > ~"),
        "summary": (
            _(
                "Validation failed because address lines must not start with any of the "
                "following characters: @ ( ) = [ ] ” \\ / , < > ~"
            )
        ),
    },
    "notify-tag-found-in-content": {
        "title": _("There’s a problem with your letter"),
        "detail": (
            _("Your file includes a letter you’ve downloaded from Notify.<br> You need to edit {invalid_pages}.")
        ),
        "summary": (
            _("Validation failed because your file includes a letter you’ve downloaded from Notify on {invalid_pages}.")
        ),
    },
}


def get_letter_validation_error(validation_message, invalid_pages=None, page_count=None):
    if not invalid_pages:
        invalid_pages = []
    if validation_message not in LETTER_VALIDATION_MESSAGES:
        return {"title": _("Validation failed")}

    invalid_pages_are_or_is = _("is") if len(invalid_pages) == 1 else _("are")

    invalid_pages = unescaped_formatted_list(
        invalid_pages, before_each="", after_each="", prefix="page", prefix_plural="pages"
    )

    return {
        "title": LETTER_VALIDATION_MESSAGES[validation_message]["title"],
        "detail": LETTER_VALIDATION_MESSAGES[validation_message]["detail"].format(
            invalid_pages=invalid_pages,
            invalid_pages_are_or_is=invalid_pages_are_or_is,
            page_count=page_count,
            letter_spec_guidance=url_for(".letter_specification"),
        ),
        "summary": LETTER_VALIDATION_MESSAGES[validation_message]["summary"].format(
            invalid_pages=invalid_pages,
            invalid_pages_are_or_is=invalid_pages_are_or_is,
            page_count=page_count,
            letter_spec_guidance=url_for(".letter_specification"),
        ),
    }
