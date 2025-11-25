from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pathlib import Path
import smtplib
from email.message import EmailMessage
import mimetypes
import warnings
from datetime import datetime  # Importación necesaria para las fechas

warnings.filterwarnings("ignore", category=DeprecationWarning)

# ----------------------------------------------------
# CÁLCULO DE FECHAS (AUTOMÁTICO)
# ----------------------------------------------------
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

hoy = datetime.now()

# 1. Fecha de Emisión (Hoy)
fecha_emision = f"{hoy.day} de {MESES[hoy.month]} de {hoy.year}"

# 2. Fecha de Vencimiento (1 mes después)
mes_venc = hoy.month + 1
anio_venc = hoy.year

# Si es Diciembre (12), el mes siguiente es Enero (1) del año siguiente
if mes_venc > 12:
    mes_venc = 1
    anio_venc += 1

fecha_vencimiento = f"{hoy.day} de {MESES[mes_venc]} de {anio_venc}"

# ----------------------------------------------------
# ÚNICAS VARIABLES QUE EDITAS EN CADA FACTURA
# ----------------------------------------------------
nombre = "2025-001.pdf"  # nombre del archivo PDF
total_horas = 70  # horas totales
descripcion = "27 PT AP"  # texto exacto del concepto
precio_hora = 40.00  # precio por hora
retencion_irpf = 0.07  # 7%
iva = 0.00  # 0% IVA
# ----------------------------------------------------

# ----------------------------------------------------
# CONFIGURACIÓN SMTP
# ----------------------------------------------------
SMTP_PASS = "gncynkghexcupvzw"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "vicente.tanco@ironhack.com"


# ----------------------------------------------------


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'FACTURA', 0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-30)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', 0,
                  align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)


def create_invoice():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 10)

    # ----------------- CÁLCULOS -----------------
    base_imponible = total_horas * precio_hora
    importe_iva = base_imponible * iva
    retencion = base_imponible * retencion_irpf
    total_factura = base_imponible + importe_iva - retencion

    # ---------------- DATOS GENERALES ----------------
    pdf.cell(0, 6, f'Nro Factura: {nombre.replace(".pdf", "")}', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- FECHA DE EMISIÓN ---
    pdf.cell(0, 6, f'Fecha de Emision: {fecha_emision}', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- FECHA DE VENCIMIENTO (variable nueva) ---
    pdf.cell(0, 6, f'Vencimiento: {fecha_vencimiento}', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # ---------------- EMISOR / CLIENTE ----------------
    y_start = pdf.get_y()

    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(90, 6, 'DE (EMISOR):', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(90, 5, 'Vicente Tanco Aguas', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(90, 5, 'NIF: 73419409M', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(90, 5, 'Plaza puerta de Badostain 9, 5A', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(90, 5, '31621 Sarriguren, Navarra', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_y(y_start)
    pdf.set_x(110)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(90, 6, 'A (CLIENTE):', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('helvetica', '', 10)
    pdf.set_x(110)
    pdf.cell(90, 5, 'Ironhack Spain, S.L.U.', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(110)
    pdf.cell(90, 5, 'NIF: B16880049', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(110)
    pdf.cell(90, 5, 'Paseo de la Chopera, 14', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(110)
    pdf.cell(90, 5, '28045 Madrid', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(20)

    # ---------------- CONCEPTO ----------------
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 6, f'Referencia: {descripcion}', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # ---------------- TABLA ÚNICA ----------------
    pdf.set_fill_color(230, 230, 230)

    # Cabecera
    pdf.cell(120, 8, 'Descripcion', 1,
             new_x=XPos.RIGHT, new_y=YPos.TOP, fill=True)
    pdf.cell(30, 8, 'Horas', 1,
             new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
    pdf.cell(40, 8, 'Total', 1,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R', fill=True)

    # Única fila
    pdf.set_font('helvetica', '', 10)
    pdf.cell(120, 8, 'Servicios de docencia y preparación curso completo {}'.format(descripcion), 1,
             new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(30, 8, str(total_horas), 1, align='C',
             new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(40, 8, f"{base_imponible:.2f} EUR", 1, align='R',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # ---------------- TOTALES ----------------
    pdf.set_x(110)
    pdf.cell(50, 7, 'Base Imponible:', 0,
             new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')
    pdf.cell(30, 7, f"{base_imponible:.2f} EUR", 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

    pdf.set_x(110)
    pdf.cell(50, 7, 'IVA:', 0,
             new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')
    pdf.cell(30, 7, f"{importe_iva:.2f} EUR", 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

    pdf.set_x(110)
    pdf.cell(50, 7, 'IRPF:', 0,
             new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')
    pdf.cell(30, 7, f"-{retencion:.2f} EUR", 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

    pdf.set_font('helvetica', 'B', 12)
    pdf.set_x(110)
    pdf.cell(50, 10, 'TOTAL A PERCIBIR:', 0,
             new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')
    pdf.cell(30, 10, f"{total_factura:.2f} EUR", 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

    pdf.ln(10)

    # ---------------- PAGO ----------------
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 6, 'DATOS DE PAGO', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 5, 'Beneficiario: Vicente Tanco Aguas', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 5, 'Banco: Revolut (BIC/SWIFT: REVOESM2)', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 5, 'IBAN: ES32 1583 0001 1190 7731 6686', 0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    pdf.set_font('helvetica', 'I', 8)
    pdf.multi_cell(0, 5,
                   'Operacion exenta de IVA segun Art. 20. Uno. 9 de la Ley 37/1992 (LIVA).')

    # ---------------- GUARDAR PDF ----------------
    output_dir = Path.home() / "Documents/IRONHACK/FACTURAS"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / nombre

    pdf.output(str(file_path))
    return str(file_path)


def enviar_correo(ruta_pdf):
    correo = EmailMessage()
    correo["From"] = SMTP_USER
    correo["To"] = "invoices@ironhack.com"
    correo["Cc"] = "ismael.lazaro@ironhack.com"
    correo["Subject"] = f"Factura {descripcion}"
    correo.set_content(f"Adjunto envío la factura correspondiente al curso {descripcion}")

    with open(ruta_pdf, "rb") as f:
        correo.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=Path(ruta_pdf).name
        )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(correo)


if __name__ == "__main__":
    try:
        print(f"Generando factura con fecha: {fecha_emision}")
        print(f"Calculando vencimiento para: {fecha_vencimiento}")
        pdf_path = create_invoice()
        enviar_correo(pdf_path)
        print("Factura enviada correctamente.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")