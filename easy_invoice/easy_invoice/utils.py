import json
import os

from datetime import date
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils.data import get_url_to_form
import io
from pyqrcode import create


def create_qr(doc, method=None):
    # Creating a fied for QR code if it doesn't exist
    if not hasattr(doc, "easy_invoice_qr"):
        create_custom_fields(
            {
                doc.doctype: [
                    dict(
                        fieldname="easy_invoice_qr",
                        label="Easy Sales Invoice QR",
                        fieldtype="Attach Image",
                        read_only=1,
                        no_copy=1,
                        hidden=1,
                    )
                ]
            }
        )

    # Checking if a qr code is already generated
    qr_code = doc.get("easy_invoice_qr")
    if qr_code and frappe.db.exists({"doctype": "File", "file_url": qr_code}):
        return

    qr_code_function = (
        frappe.db.get_single_value("Easy Invoice Settings", "qr_code_function")
        or "Redirect"
    )
    if qr_code_function == "Redirect":
        # Getting the URL to the document
        doc_url = get_url_to_form(doc.doctype, doc.name)
    elif qr_code_function == "JSON":
        # Getting the JSON of the document
        doc_url = get_si_json(doc)
    elif qr_code_function == "TLV":
        # GEtting the TLV formatted document
        doc_url = get_si_tlv(doc)

    # Generating QR image
    qr_image = io.BytesIO()
    url = create(doc_url, error="L")
    url.png(qr_image, scale=2, quiet_zone=1)

    name = frappe.generate_hash(doc.name, 5)

    # Uploading the QR and attaching it to the document
    filename = f"QRCode-{name}.png".replace(os.path.sep, "__")
    _file = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": filename,
            "is_private": 0,
            "content": qr_image.getvalue(),
            "attached_to_doctype": doc.get("doctype"),
            "attached_to_name": doc.get("name"),
            "attached_to_field": "easy_invoice_qr",
        }
    )

    _file.save()

    # assigning to document
    doc.db_set("easy_invoice_qr", _file.file_url)
    doc.notify_update()


def get_si_json(doc):
    # Define the list of essential fields
    essential_fields = [
        "customer",
        "name",
        "posting_date",
        "due_date",
        "company",
        "taxes",
        "discount_amount",
        "grand_total",
        "payments",
        "remarks",
    ]

    # Create a dictionary to store the field values
    invoice_data = {}

    # Extract the field values from the document object
    for field in essential_fields:
        value = doc.get(field)

        # Convert datetime.date objects to string representation
        if isinstance(value, date):
            value = value.strftime("%Y-%m-%d")

        invoice_data[field] = value

    # Extract essential fields from each sales invoice item
    items_data = []
    for item in doc.items:
        item_data = {
            "item_name": item.item_name,
            "item_quantity": item.qty,
            "item_rate": item.rate,
            # Add other relevant item fields as needed
        }
        items_data.append(item_data)

    # Add the items data to the invoice data dictionary
    invoice_data["items"] = items_data

    # Convert the dictionary to JSON
    json_data = json.dumps(invoice_data, indent=4)

    return json_data


def get_si_tlv(doc):
    # Define the TLV data
    tlv_data = ""

    # Function to convert data to TLV format
    def convert_to_tlv(tag, value):
        length = len(value)
        return f"Tag: {tag}\nLength: {length}\nValue: {value}\n\n"

    # Add essential fields to the TLV data
    tlv_data += convert_to_tlv("0x01", doc.customer)
    tlv_data += convert_to_tlv("0x02", doc.name)
    tlv_data += convert_to_tlv("0x03", str(doc.posting_date))
    tlv_data += convert_to_tlv("0x04", str(doc.due_date))
    tlv_data += convert_to_tlv("0x05", doc.company)
    tlv_data += convert_to_tlv("0x06", str(doc.taxes))
    tlv_data += convert_to_tlv("0x07", str(doc.discount_amount))
    tlv_data += convert_to_tlv("0x08", str(doc.grand_total))
    tlv_data += convert_to_tlv("0x09", str(doc.payments))
    tlv_data += convert_to_tlv("0x0A", doc.remarks)

    # Add items to the TLV data
    for item in doc.items:
        item_data = ""
        item_data += convert_to_tlv("0x0B", item.item_name)
        item_data += convert_to_tlv("0x0C", str(item.qty))
        item_data += convert_to_tlv("0x0D", str(item.rate))
        # Add other relevant item fields as needed

        # Add item data to the main TLV data
        tlv_data += convert_to_tlv("0x0E", item_data)

    return tlv_data
