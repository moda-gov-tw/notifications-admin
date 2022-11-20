from flask_babel import _

from app.models.branding import EmailBranding


def get_email_choices(service):
    if service.can_use_govuk_branding and not service.email_branding.is_govuk:
        yield ("govuk", _("GOV.UK"))

    if service.is_nhs and not service.email_branding.is_nhs:
        yield (EmailBranding.NHS_ID, "NHS")

    if service.email_branding_pool:
        for branding in service.email_branding_pool.excluding(service.email_branding_id):
            yield (branding.id, branding.name)
    elif service.organisation:
        # fake branding options
        if (
            service.can_use_govuk_branding
            and service.email_branding.name.lower() != f"GOV.UK and {service.organisation.name}".lower()
        ):
            yield ("govuk_and_org", _("GOV.UK and %%s") % service.organisation.name)

        if not service.is_nhs and (
            not service.email_branding_id or service.email_branding_id != service.organisation.email_branding_id
        ):
            yield ("organisation", service.organisation.name)


def get_letter_choices(service):

    if service.is_nhs and not service.letter_branding.is_nhs:
        yield ("nhs", "NHS")

    if (
        service.organisation
        and not service.is_nhs
        and (not service.letter_branding_id or service.letter_branding_id != service.organisation.letter_branding_id)
    ):
        yield ("organisation", service.organisation.name)
