import fitz  # PyMuPDF
import re
import os
import json

def clean_text_after_signature(text):
    """
    Removes all text after 'Authorised Signature' (case-insensitive).
    
    Parameters:
    text (str): The extracted text from the PDF.
    
    Returns:
    str: Cleaned text with unwanted parts removed.
    """
    pattern = r'Authorised Signature.*'  # Matches 'Authorised Signature' and everything after it
    cleaned_text = re.sub(pattern, 'Authorised Signature', text, flags=re.IGNORECASE | re.DOTALL)
    return cleaned_text


def extract_text_from_pdf(pdf_path):
    """Extracts text from the given PDF file and writes it to debug.txt."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    
    # Write extracted text to debug.txt
    
    
    return text

def extract_po_section(text, start_text, end_text):
    """Extracts text between two given markers."""
    match = re.search(rf"{re.escape(start_text)}([\s\S]+?){re.escape(end_text)}", text)
    return match.group(1).strip() if match else "Not Found"



def extract_po_number(text):
    match = re.search(r'PO No\s*:\s*(\S+)', text)
    return match.group(1) if match else None

def extract_po_date(text):
    match = re.search(r'PO Date\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_po_release_date(text):
    match = re.search(r'PO Release Date\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_payment_terms(text):
    match = re.search(r'Payment Terms\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_expected_delivery_date(text):
    match = re.search(r'Expected Delivery Date\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_expiry_date(text):
    match = re.search(r'PO Expiry Date\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_ref_po_code(text):
    match = re.search(r'Reference PO Code\s*:\s*(.*)', text)
    return match.group(1).strip() if match else None

def extract_vendor_address(text):
    match = re.search(r'Reference PO Code\s*:\s*\n(.*)', text, re.DOTALL)
    return match.group(1).strip() if match else None



def process_vendor_details(text):
    start_text = "Purchase Order"
    end_text = "Billing Address"

    vendor_text = extract_po_section(text, start_text, end_text)

    po_number = extract_po_number(vendor_text)
    po_date = extract_po_date(vendor_text)
    po_release_date = extract_po_release_date(vendor_text)
    payment_terms = extract_payment_terms(vendor_text)
    expected_delivery_date = extract_expected_delivery_date(vendor_text)
    expiry_date = extract_expiry_date(vendor_text)
    ref_po_code = extract_ref_po_code(vendor_text)
    vendor_address = extract_vendor_address(vendor_text)
    
    # print(f"PO Number: {po_number}")
    # print(f"PO Date: {po_date}")
    # print(f"PO Release Date: {po_release_date}")
    # print(f"Payment Terms: {payment_terms}")
    # print(f"Expected Delivery Date: {expected_delivery_date}")
    # print(f"PO Expiry Date: {expiry_date}")
    # print(f"Reference PO Code: {ref_po_code}")
    # print(f"Vendor Address:\n{vendor_address}")

def extract_billing_address(text):
    """Extracts Billing Address from the text."""
    match = re.search(r'Billing Address\s*:\s*\n([\s\S]+?)(?=Shipping Address|S\. No|$)', text)
    return match.group(1).strip() if match else "Not Found"

def extract_addresses(po_text):
    """
    Extracts Billing and Shipping addresses from a Purchase Order (PO) text.
    Works even if Billing and Shipping addresses are different.
    """
    # Remove the header "Billing Address Shipping Address"
    po_text = re.sub(r"^Billing Address Shipping Address\s*", "", po_text)

    # Split text into lines and remove empty ones
    lines = [line.strip() for line in po_text.split("\n") if line.strip()]

    # Identify company name occurrences
    company_name = lines[0]  # Assuming the first line is always the company name
    second_occurrence = lines.index(company_name, 1)  # Find the second occurrence

    # Extract Billing and Shipping addresses
    billing_address = "\n".join(lines[:second_occurrence])
    shipping_address = "\n".join(lines[second_occurrence:])
    billing_address=billing_address.strip()
    shipping_address=shipping_address.strip()

    print(f"billing address  \n{billing_address}\n\n")
    print(f"shipping address \n{shipping_address}")

    return billing_address, shipping_address

def extract_address_text(text, start_text, end_text):
    """Extracts text between three groups."""
    regex = r"(Billing Address)([\s\S]+?)(S\.\s*No\s*Item\s*Code)"
    match = re.search(regex, text)
    
    if match:
        start_marker = match.group(1).strip()
        extracted_data = match.group(2).strip()
        result = f"{start_marker} {extracted_data}"  # Concatenating Group 1 and Group 2
        return result
    else:
        return "Not Found"
    # if match:
    #     print(f"Group 1 (Start Marker)   : {match.group(1).strip()}")
    #     print(f"Group 2 (Extracted Data) : {match.group(2).strip()}")
    #     #print(f"Group 3 (End Marker)     : {match.group(3).strip()}")
    #     return match.group(2).strip()
    # else:
    #     return "Not Found"

def process_address_details(text):
    start_text = "Billing Address"
    all_lines_bw = r"[\s\S]+?"
    end_text = r"S\.\s*No\s*Item\s*Code"
    # (Billing Address)([\s\S]+?)(S\.\s*No\s*Item\s*Code)
    # regex = ({start_text})({all_lines_bw})({end_text})}
    regex = r"(Billing Address)([\s\S]+?)(S\.\s*No\s*Item\s*Code)"
   # print(f"regex :{regex}")
                       
    address_section = extract_address_text(text, start_text, end_text)
   # print(f"{address_section}")  

    # billing_address = extract_billing_address(address_section)
    # shipping_address = extract_shipping_address(address_section)

    # print(f"Billing Address:\n{billing_address}\n")
    # print(f"Shipping Address:\n{shipping_address}")
    addresses = extract_addresses(address_section)
    return addresses



def process_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    # text = extract_text_from_pdf(pdf_path)
    # text=clean_text_after_signature(text)
    
    
    # process_vendor_details(text)
    # process_address_details(text)
    table_json = extract_table_from_pdf(pdf_path)
    print(json.dumps(table_json, indent=4))

    # with open("debug.txt", "w") as f:
    #     f.write(text)


def main():
    swiggy_po_pdf = "Swiggy_PO.pdf"
    process_pdf(swiggy_po_pdf)

if __name__ == "_main_":
    main()
    