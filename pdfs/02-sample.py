import fitz

doc = fitz.open('Swiggy_PO.pdf')
for page in doc:
    tabs = page.find_tables()
    if tabs.tables:
        print(tabs[0].extract())