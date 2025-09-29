import frappe
import json

@frappe.whitelist()
def generate_invoice_json(invoice_id):
    # --- Get Invoice ---
    invoice = frappe.get_doc("Ha Pos Invoice", invoice_id)

    # --- Get Company Info ---
    company_name = frappe.db.get_single_value('Global Defaults', 'default_company')
    company = frappe.get_doc("Company", company_name)
    currency = frappe.db.get_value('Company', company, 'default_currency')
    # --- Get Customer Info (custom doctype linked by customer name) ---
    customer_doc = frappe.get_doc("Customer", invoice.customer)

    # --- Get Logged-in User (Cashier) ---
    cashier_name = frappe.db.get_value("User", frappe.session.user, "full_name")

    # --- Get Invoice Items ---
    items = frappe.get_all(
        "Ha Pos Invoice Item",
        filters={"parent": invoice.name},
        fields=["item_name as ProductName", "item_code as productid", "qty as Qty",
                "rate as Price", "amount as Amount"]
    )
    #, "vat as vat"
    # --- Multi Currency Details ---
    multi_currency = [
        {"Key": currency, "Value": invoice.sub_total}
    ]

    # --- Build JSON Data ---
    data = {
        "CompanyName": company.company_name,
        "CompanyAddress": company.custom_company_email or "",
        "City": company.custom_city or "",
        "State": company.custom_state or "",
        "postcode": company.custom_post_code or "",
        "contact": company.custom_contact_number or "",
        "CompanyEmail": company.custom_company_email or "",
        "TIN": company.custom_tin or "",
        "VATNo": company.custom_vat or "",
        "Tel": company.custom_contact_number or "",

        "InvoiceNo": invoice.name,
        "InvoiceDate": str(invoice.creation),
        "CashierName": cashier_name,

        "CustomerName": customer_doc.customer_name,
        "CustomerContact": customer_doc.customer_name,   # You may adjust if you have a field for contact
        "CustomerTradeName": getattr(customer_doc, "trade_name", None),
        "CustomerEmail": getattr(customer_doc, "email_id", None),
        "CustomerTIN": getattr(customer_doc, "tin", None),
        "CustomerVAT": getattr(customer_doc, "vat", None),
        "Customeraddress": getattr(customer_doc, "customer_address", None),

        "itemlist": items,

        "AmountTendered": str(invoice.sub_total or "0"),
        "Change":  "0",
        "Currency": currency or "USD",
        "Footer": "Thank you for your purchase!",

        "MultiCurrencyDetails": multi_currency,

        "DeviceID": invoice.custom_device_id or "None",
        "DeviceSerial": invoice.custom_device_serial_no or "",
        "FiscalDay": invoice.custom_fiscal_day or "",
        "ReceiptNo": invoice.custom_receiptno or "",
        "CustomerRef":  "None",
        "VCode": invoice.custom_verification_code or "",
        "QRCode": invoice.custom_invoice_qr_code or "",

        "DiscAmt": "0.0",
        "Subtotal": invoice.sub_total,
        "TotalVat": "0.00",
        "GrandTotal": invoice.sub_total,
        "TaxType": "Standard VAT",
        "PaymentMode": "Cash",
    }

    return json.dumps(data, indent=2, default=str)
