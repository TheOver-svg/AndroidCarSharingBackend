from xhtml2pdf import pisa
import io
from datetime import datetime

def generate_rental_contract_pdf(user, car, trip) -> bytes:
    current_date = datetime.now().strftime("%d.%m.%Y")
    current_time = datetime.now().strftime("%H:%M")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ 
            font-family: Helvetica, Arial, sans-serif; 
            font-size: 11pt; 
            color: #222222; 
            margin: 10px;
        }}
        h1 {{ 
            text-align: center; 
            font-size: 16pt; 
            font-weight: bold; 
            text-transform: uppercase;
        }}
        .subtitle {{ 
            text-align: center; 
            font-size: 11pt; 
            font-style: italic; 
            margin-bottom: 25px; 
        }}
        .meta-table {{ 
            width: 100%; 
            margin-bottom: 20px; 
            border-collapse: collapse; 
        }}
        .text-right {{ 
            text-align: right; 
        }}
        .section-title {{ 
            font-size: 12pt; 
            font-weight: bold; 
            margin-top: 20px; 
            margin-bottom: 8px; 
        }}
        p {{ 
            text-align: justify; 
            margin-bottom: 10px; 
        }}
        .details-table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 15px 0; 
        }}
        .details-table th, .details-table td {{ 
            border: 1px solid #333333; 
            padding: 8px; 
        }}
        .details-table th {{ 
            background-color: #f5f5f5; 
            text-align: left; 
            width: 40%; 
        }}
        .digital-seal {{ 
            display: inline-block; 
            margin-top: 10px; 
            padding: 6px; 
            border: 1px dashed #2e7d32; 
            color: #2e7d32; 
            font-size: 9pt; 
            background-color: #e8f5e9; 
        }}
    </style>
    </head>
    <body>

        <h1>DOHOVOR ORENDY AVTOMOBILYA</h1>
        <div class="subtitle">(Public Offer)</div>

        <table class="meta-table">
            <tr>
                <td><strong>Contract No:</strong> CS-2026-{trip.id}</td>
                <td class="text-right"><strong>Date:</strong> {current_date}</td>
            </tr>
            <tr>
                <td><strong>Place:</strong> m. Khmelnytskyi</td>
                <td class="text-right"><strong>Time:</strong> {current_time}</td>
            </tr>
        </table>

        <p>Android CarSharing Service (Lessor) and User <strong>{user.full_name}</strong> (Lessee) have concluded this agreement:</p>

        <div class="section-title">1. VEHICLE & USER DETAILS</div>
        <table class="details-table">
            <tr><th>Car Model</th><td>{car.model}</td></tr>
            <tr><th>Plate Number</th><td>{car.plate_number}</td></tr>
            <tr><th>Transmission</th><td>{car.transmission}</td></tr>
            <tr><th>Client Name</th><td>{user.full_name}</td></tr>
            <tr><th>Phone</th><td>{user.phone}</td></tr>
            <tr><th>Email</th><td>{user.email}</td></tr>
            <tr><th>Price Rate</th><td>{car.price} UAH</td></tr>
        </table>

        <div class="section-title">2. ELECTRONIC SIGNATURE</div>
        <p>By clicking "Pay and Book" in the mobile application, the Lessee accepts all conditions of this rental agreement according to Art. 634 of the Civil Code of Ukraine.</p>

        <table style="width: 100%; margin-top: 40px;">
            <tr>
                <td style="width: 50%; vertical-align: top;">
                    <strong>Lessor:</strong><br>
                    Android CarSharing Service<br>
                    <div class="digital-seal">EDRPOU 44098765 - SIGNED</div>
                </td>
                <td style="width: 50%; vertical-align: top;">
                    <strong>Lessee:</strong><br>
                    User: {user.full_name}<br>
                    <div class="digital-seal" style="color: #1565c0; border-color: #1565c0; background-color: #e3f2fd;">MOBILE TOKEN VERIFIED</div>
                </td>
            </tr>
        </table>

    </body>
    </html>
    """
    
    pdf_file = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html_content.encode("utf-8")), dest=pdf_file)
    return pdf_file.getvalue()