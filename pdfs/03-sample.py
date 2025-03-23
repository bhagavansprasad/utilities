import pdfplumber

with pdfplumber.open("Swiggy_PO.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_table()
        print(tables)
        if tables:
            for row in tables:
                print(row)  
