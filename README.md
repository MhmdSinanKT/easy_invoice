## Easy Invoice

Makes Sharing and assessing Invoices easier by generating unique QR codes

### Introduction
The Easy Invoice app is made on Frappe and ERPNext to support the Accounts Module. This app will add qr codes for invoices (currently only Sales Invoice) which can be used depending on the user's choice

### Requriements
- Frappe (bench)
- ERPNext installed on the site, and all their dependencies

### Tutorial
- Once Easy Invoice app is installed on a site, A new single DocType named 'Easy Invoice Settings' can be used fine tune the functionalities of this app (currently only the qr code functionality can be changed).
  ![image](https://github.com/MhmdSinanKT/easy_invoice/assets/91651425/a8d903ea-ce25-4116-a1d1-24c3437401df)
- Afterwards, when submitting an Invoice (only Sales Invoice for now) a file will be attached in the sidebar.
  ![image](https://github.com/MhmdSinanKT/easy_invoice/assets/91651425/26c1e7f7-4002-4898-8464-7909835e9b34)
- When the Print option is selected, and the 'Easy Sales Invoice' print format is selected, the QR code will be visible in the print.
  ![image](https://github.com/MhmdSinanKT/easy_invoice/assets/91651425/d4614f0e-c558-4958-8ae4-b8ae4ac22d86)
- The QR code will function depending on the settings (Redirect by default)

#### License

MIT
