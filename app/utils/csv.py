from flask_babel import _
from notifications_utils.recipients import RecipientCSV

from app.models.spreadsheet import Spreadsheet
from app.utils.templates import get_sample_template


def get_errors_for_csv(recipients, template_type):

    errors = []

    if any(recipients.rows_with_bad_recipients):
        number_of_bad_recipients = len(list(recipients.rows_with_bad_recipients))
        if "sms" == template_type:
            if 1 == number_of_bad_recipients:
                errors.append(_("fix 1 phone number"))
            else:
                errors.append(_("fix {} phone numbers").format(number_of_bad_recipients))
        elif "email" == template_type:
            if 1 == number_of_bad_recipients:
                errors.append(_("fix 1 email address"))
            else:
                errors.append(_("fix {} email addresses").format(number_of_bad_recipients))
        elif "letter" == template_type:
            if 1 == number_of_bad_recipients:
                errors.append(_("fix 1 address"))
            else:
                errors.append(_("fix {} addresses").format(number_of_bad_recipients))

    if any(recipients.rows_with_missing_data):
        number_of_rows_with_missing_data = len(list(recipients.rows_with_missing_data))
        if 1 == number_of_rows_with_missing_data:
            errors.append(_("enter missing data in 1 row"))
        else:
            errors.append(_("enter missing data in {} rows").format(number_of_rows_with_missing_data))

    if any(recipients.rows_with_message_too_long):
        number_of_rows_with_message_too_long = len(list(recipients.rows_with_message_too_long))
        if 1 == number_of_rows_with_message_too_long:
            errors.append(_("shorten the message in 1 row"))
        else:
            errors.append(_("shorten the messages in {} rows").format(number_of_rows_with_message_too_long))

    if any(recipients.rows_with_empty_message):
        number_of_rows_with_empty_message = len(list(recipients.rows_with_empty_message))
        if 1 == number_of_rows_with_empty_message:
            errors.append(_("check you have content for the empty message in 1 row"))
        else:
            errors.append(
                _("check you have content for the empty messages in {} rows").format(number_of_rows_with_empty_message)
            )

    return errors


def generate_notifications_csv(**kwargs):
    from app import notification_api_client
    from app.s3_client.s3_csv_client import s3download

    if "page" not in kwargs:
        kwargs["page"] = 1

    if kwargs.get("job_id"):
        original_file_contents = s3download(kwargs["service_id"], kwargs["job_id"])
        original_upload = RecipientCSV(
            original_file_contents,
            template=get_sample_template(kwargs["template_type"]),
        )
        original_column_headers = original_upload.column_headers
        fieldnames = (
            [_("Row number")] + original_column_headers + [_("Template"), _("Type"), _("Job"), _("Status"), _("Time")]
        )
    else:
        fieldnames = [
            _("Recipient"),
            _("Reference"),
            _("Template"),
            _("Type"),
            _("Sent by"),
            _("Sent by email"),
            _("Job"),
            _("Status"),
            _("Time"),
        ]

    yield ",".join(fieldnames) + "\n"

    while kwargs["page"]:
        notifications_resp = notification_api_client.get_notifications_for_service(**kwargs)
        for notification in notifications_resp["notifications"]:
            if kwargs.get("job_id"):
                values = (
                    [
                        notification["row_number"],
                    ]
                    + [
                        original_upload[notification["row_number"] - 1].get(header).data
                        for header in original_column_headers
                    ]
                    + [
                        notification["template_name"],
                        notification["template_type"],
                        notification["job_name"],
                        notification["status"],
                        notification["created_at"],
                    ]
                )
            else:
                values = [
                    # the recipient for precompiled letters is the full address block
                    notification["recipient"].splitlines()[0].lstrip().rstrip(" ,"),
                    notification["client_reference"],
                    notification["template_name"],
                    notification["template_type"],
                    notification["created_by_name"] or "",
                    notification["created_by_email_address"] or "",
                    notification["job_name"] or "",
                    notification["status"],
                    notification["created_at"],
                ]
            yield Spreadsheet.from_rows([map(str, values)]).as_csv_data

        if notifications_resp["links"].get("next"):
            kwargs["page"] += 1
        else:
            return
    raise Exception(_("Should never reach here"))
