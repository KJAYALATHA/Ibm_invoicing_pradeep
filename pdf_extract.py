import os
import re
from pathlib import Path

from PIL import Image
from pdf2image import convert_from_path
from pytesseract import pytesseract

# https://github.com/UB-Mannheim/tesseract/wiki  -- Pytesseract exe
# https://github.com/xavctn/img2table


# Store Pdf with convert_from_path function
poppler_path = r"C:\poppler-0.68.0\bin"
fold_name = None
buying_name = 'Buying company name'
buying_contact = 'Buying company contact information'
po_number = 'Purchase order number'
po_date = 'Original purchase order date'
purchaser_gst = ['GST Registration Number (Purchaser)', 'SEZ GST registration number']
bill_to_addr = 'Bill to address information'
ship_to_addr = 'Ship to address information'
buying_cmpy_nm = []
buying_cnct = []
po_num = []
po_dt = []
buying_gst = []
supp_addr = []
bill_addr = []
ship_addr = []
item_txt = []
item_cnt = []
for pdf in Path(r'pdfs').glob("*.pdf"):
    images = convert_from_path(pdf, poppler_path=poppler_path)

    for i in range(len(images)):
        fold_name = Path(pdf).stem
        if not os.path.exists(r'pdftoimage\{}'.format(fold_name)):
            os.makedirs(r'pdftoimage\{}'.format(fold_name))
        # save pages as images in the pdf
        images[i].save(r'pdftoimage\{}\page{}.png'.format(fold_name, str(i)), 'PNG')
    #
    pdf_list = []
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    for j, im in enumerate(Path(r'pdftoimage\{}'.format(fold_name)).glob("*.png")):
        # Opening the image & storing it in an image object
        img = Image.open(im)

        # Providing the tesseract executable
        # location to pytesseract library
        pytesseract.tesseract_cmd = path_to_tesseract

        # Passing the image object to image_to_string() function
        # This function will extract the text from the image
        text = pytesseract.image_to_string(img)

        # Displaying the extracted text
        pdf_list.append(text[:-1].split("\n"))
        pdf_list = [[j for j in i if len(j) > 0] for i in pdf_list]
        # ------------------------------------------------------------------------------------------------------------
        buying_company_name = [x.split(buying_name)[1].strip() for i, x in enumerate(pdf_list[j]) if
                               len(re.findall(buying_name, x)) > 0]
        if len([i for i in buying_company_name if len(i) > 0]) > 0:
            buying_cmpy_nm.append(buying_company_name)
        # ------------------------------------------------------------------------------------------------------------
        buying_company_contact_info = [
            " ".join([x.split(buying_contact)[1], pdf_list[j][i + 1].replace("Purchase order", "")]).strip() for i, x in
            enumerate(pdf_list[j]) if len(re.findall(buying_contact, x)) > 0]
        if len([i for i in buying_company_contact_info if len(i) > 0]) > 0:
            buying_cnct.append(buying_company_contact_info)
        # ------------------------------------------------------------------------------------------------------------
        purchase_order_number = [x.split(po_number)[1].strip() for i, x in enumerate(pdf_list[j]) if
                                 len(re.findall(po_number, x)) > 0]
        if len([i for i in purchase_order_number if len(i) > 0]) > 0:
            po_num.append(purchase_order_number)
        else:
            purchase_order_number = [pdf_list[j][i + 1] for i, x in enumerate(pdf_list[j]) if
                                     len(re.findall(po_number, x)) > 0]
            if len([i for i in purchase_order_number if len(i) > 0]) > 0:
                po_num.append(purchase_order_number)
        # ------------------------------------------------------------------------------------------------------------
        original_purchase_order_date = [x.split(po_date)[1].replace("Dee", "Dec").strip() for i, x in
                                        enumerate(pdf_list[j]) if
                                        len(re.findall(po_date, x)) > 0]
        if len([i for i in original_purchase_order_date if len(i) > 0]) > 0:
            po_dt.append(original_purchase_order_date)
        # ------------------------------------------------------------------------------------------------------------
        supplier_address = None
        try:
            supplier_address = [" ".join(
                [pdf_list[j][i + 1], pdf_list[j][i + 2], pdf_list[j][i + 3], pdf_list[j][i + 4], pdf_list[j][i + 5],
                 pdf_list[j][i + 6], pdf_list[j][i + 7]]).replace("Name/Address", "").replace("Address1", "").replace(
                "Address 1", "").replace(
                "Address2", "").replace("Name2", "").replace("Address3", "").replace("Address4", "").strip() for i, x in
                                enumerate(pdf_list[j]) if x in ['Supplier address']]
        except IndexError:
            supplier_address = [" ".join(
                [pdf_list[j][i + 1], pdf_list[j][i + 2], pdf_list[j][i + 3], pdf_list[j][i + 4], pdf_list[j][i + 5],
                 pdf_list[j][i + 6]]).replace("Name/Address", "").replace("Address1", "").replace("Address 1",
                                                                                                  "").replace(
                "Address2", "").replace("Name2", "").replace("Address3", "").replace("Address4", "").strip() for i, x in
                                enumerate(pdf_list[j]) if x in ['Supplier address']]
        if len([i for i in supplier_address if len(i) > 0]) > 0:
            supp_addr.append(supplier_address)
        # ------------------------------------------------------------------------------------------------------------
        items_count = [x.split("Items:")[1].replace(":", "").strip() for i, x in enumerate(pdf_list[j]) if
                       len(re.findall("Items:", x)) > 0]
        if len([i for i in items_count if len(i) > 0]) > 0:
            item_cnt.append(items_count)
        # ------------------------------------------------------------------------------------------------------------
        buying_gst_number = [x.split(y)[1].strip() for y in purchaser_gst for i, x in enumerate(pdf_list[j]) if
                             len(re.findall(purchaser_gst, x)) > 0]
        if len([i for i in buying_gst_number if len(i) > 0]) > 0:
            buying_gst.append(buying_gst_number)
        elif len([i for i in buying_gst_number if len(i) > 0]) == 0:
            purchaser_gst = "(Purchaser)"
            buying_gst_number = [x.split(purchaser_gst)[1].strip() for i, x in enumerate(pdf_list[j]) if
                                 len(re.findall(purchaser_gst, x)) > 0]
            if len([i for i in buying_gst_number if len(i) > 0]) > 0:
                buying_gst.append(buying_gst_number)
        # ------------------------------------------------------------------------------------------------------------
        bill_to_address = [" ".join(
            [pdf_list[j][i + 1], pdf_list[j][i + 2], pdf_list[j][i + 3], pdf_list[j][i + 4], pdf_list[j][i + 5],
             pdf_list[j][i + 6], pdf_list[j][i + 7],
             pdf_list[j][i + 8], pdf_list[j][i + 9], pdf_list[j][i + 10], pdf_list[j][i + 11], pdf_list[j][i + 12],
             pdf_list[j][i + 13], pdf_list[j][i + 14], pdf_list[j][i + 15], pdf_list[j][i + 16]]).replace(
            "Name/Address", "").replace("Address1", "").replace("Address2", "").replace("Name2", "").replace("Address3",
                                                                                                             "").replace(
            "Address4", "").replace("PO box", "").replace("City", "").replace("District", "").replace(
            "State/Region/Province", "").replace("Postal code", "").replace("Country/Region", "") for i, x in
                           enumerate(pdf_list[j]) if x in [bill_to_addr]]
        if len([i for i in bill_to_address if len(i) > 0]) > 0:
            bill_addr.append(bill_to_address)
        # ------------------------------------------------------------------------------------------------------------
        ship_to_address = [" ".join(
            [pdf_list[j][i + 1], pdf_list[j][i + 2], pdf_list[j][i + 3], pdf_list[j][i + 4], pdf_list[j][i + 5],
             pdf_list[j][i + 6], pdf_list[j][i + 7],
             pdf_list[j][i + 8], pdf_list[j][i + 9], pdf_list[j][i + 10], pdf_list[j][i + 11], pdf_list[j][i + 12],
             pdf_list[j][i + 13], pdf_list[j][i + 14], pdf_list[j][i + 15], pdf_list[j][i + 16]]).replace(
            "Name/Address", "").replace("Address1", "").replace("Address2", "").replace("Name2", "").replace("Address3",
                                                                                                             "").replace(
            "Address4", "").replace("PO box", "").replace("City", "").replace("District", "").replace(
            "State/Region/Province", "").replace("Postal code", "").replace("Country/Region", "") for i, x in
                           enumerate(pdf_list[j]) if x in [ship_to_addr]]
        if len([i for i in ship_to_address if len(i) > 0]) > 0:
            ship_addr.append(ship_to_address)
        # ------------------------------------------------------------------------------------------------------------
        item_text = [" ".join([pdf_list[j][i + 1], pdf_list[j][i + 2]]) for i, x in enumerate(pdf_list[j]) if
                     len(re.findall('Item text', x)) > 0]
        if len([i for i in item_text if len(i) > 0]) > 0:
            item_txt.append(item_text)
        # ------------------------------------------------------------------------------------------------------------
print(buying_cmpy_nm)
print(buying_cnct)
print(po_num)
print(po_dt)
print(buying_gst)
print(supp_addr)
print(bill_addr)
print(ship_addr)
print(item_txt)
print(item_cnt)
