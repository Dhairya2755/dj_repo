# from io import BytesIO
# from django.core.files.base import ContentFile
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# import calendar

# def generate_salary_pdf(slip):
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     p.setFont("Helvetica", 14)
#     p.drawString(100, 800, f"Salary Slip - {calendar.month_name[slip.month]} {slip.year}")
#     p.drawString(100, 760, f"Employee: {slip.employee.get_full_name()}")
#     p.drawString(100, 730, f"Amount Credited: ₹{slip.amount}")
#     p.drawString(100, 700, f"Generated on: {slip.created_on}")
#     p.showPage()
#     p.save()
    
#     pdf_name = f"{slip.employee.username}_{slip.month}_{slip.year}.pdf"
#     slip.pdf.save(pdf_name, ContentFile(buffer.getvalue()))
#     buffer.close()
#     return slip

# from io import BytesIO
# from django.core.files.base import ContentFile
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# import calendar

# def generate_salary_pdf(slip):
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     p.setFont("Helvetica", 14)
#     p.drawString(100, 800, f"Salary Slip - {calendar.month_name[slip.month]} {slip.year}")
#     p.drawString(100, 760, f"Employee: {slip.employee.first_name} {slip.employee.last_name}")
#     p.drawString(100, 730, f"Amount Credited: ₹{slip.amount}")
#     p.drawString(100, 700, f"Generated on: {slip.created_on}")
#     p.showPage()
#     p.save()

#     filename = f"{slip.employee.employee_id}_{slip.month}_{slip.year}.pdf"
#     slip.pdf.save(filename, ContentFile(buffer.getvalue()))
#     buffer.close()
