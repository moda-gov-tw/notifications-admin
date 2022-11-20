from flask_babel import _


def features_nav():
    return [
        {
            "name": _("Features"),
            "link": "main.features",
            "sub_navigation_items": [
                {
                    "name": _("Emails"),
                    "link": "main.features_email",
                },
                {
                    "name": _("Text messages"),
                    "link": "main.features_sms",
                },
                {
                    "name": _("Letters"),
                    "link": "main.features_letters",
                },
            ],
        },
        {
            "name": _("Roadmap"),
            "link": "main.roadmap",
        },
        {
            "name": _("Who can use Notify"),
            "link": "main.who_can_use_notify",
        },
        {
            "name": _("Security"),
            "link": "main.security",
        },
        {
            "name": _("Terms of use"),
            "link": "main.terms",
        },
    ]


def pricing_nav():
    return [
        {
            "name": _("Pricing"),
            "link": "main.pricing",
        },
        {
            "name": _("How to pay"),
            "link": "main.how_to_pay",
        },
        {
            "name": _("Billing details"),
            "link": "main.billing_details",
        },
    ]


def using_notify_nav():
    return [
        {
            "name": _("Get started"),
            "link": "main.get_started",
        },
        {
            "name": _("Trial mode"),
            "link": "main.trial_mode_new",
        },
        {
            "name": _("Delivery status"),
            "link": "main.message_status",
        },
        {
            "name": _("Guidance"),
            "link": "main.guidance_index",
            "sub_navigation_items": [
                {
                    "name": _("Formatting"),
                    "link": "main.edit_and_format_messages",
                },
                {
                    "name": _("Branding"),
                    "link": "main.branding_and_customisation",
                },
                {
                    "name": _("Send files by email"),
                    "link": "main.send_files_by_email",
                },
                {
                    "name": _("Upload a letter"),
                    "link": "main.upload_a_letter",
                },
                {
                    "name": _("Letter specification"),
                    "link": "main.letter_specification",
                },
            ],
        },
        {
            "name": _("API documentation"),
            "link": "main.documentation",
        },
    ]
