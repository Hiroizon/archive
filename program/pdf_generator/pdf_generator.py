from fpdf import FPDF

# PDF 1
pdf1 = FPDF()
pdf1.add_page()
pdf1.set_font("Arial", size=12)
pdf1.cell(200, 10, txt="Test PDF 1", ln=True, align="C")
pdf1.cell(200, 10, txt="This is the first test PDF.", ln=True, align="L")
pdf1.output("test1.pdf")

# PDF 2
pdf2 = FPDF()
pdf2.add_page()
pdf2.set_font("Arial", size=12)
pdf2.cell(200, 10, txt="Test PDF 2", ln=True, align="C")
pdf2.cell(200, 10, txt="This is the second test PDF.", ln=True, align="L")
pdf2.output("test2.pdf")

print("PDF files 'test1.pdf' and 'test2.pdf' created.")
