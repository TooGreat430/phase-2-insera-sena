NINGBO_FORDARIO_PROMPT = """

INVOICE (INV):

1. inv_customer_po_no:
   - Ekstrak dari kolom "PO NO.".
   - Memiliki format numerik 8 digit dan diawali dengan angka 4.
     Contoh = 45316923, 45323034, 45322720
   - Jika Item memiliki lebih dari 1 PO NO, ambil hanya nomor yang paling atas dan abaikan nomor yang lainnya.
     Contoh:
     PO NO Barang A:
     45316923,
     45318263
     (CLM25100240)
     maka inv_customer_po_no = 45316923
   - PO NO selalu numerik dan di awali dengan angka 4.
     45319886       -> Benar
     (CLM25120196)  -> Salah
   - Jangan ambil "INVOICE NO.".
   - JANGAN AMBIL DARI KOLOM "NO.", "CODE", "ITEM NO."

2. inv_spart_item_no:
   - Ekstrak dari kolom "CODE" karena ini adalah kode item yang paling unik per line item.
     Contoh:
     - FRXZEZYHG05000
     - HBRZEHB1120001
     - SDPZEZYSP0132001
   - JANGAN AMBIL DARI KOLOM "ITEM NO."
     Contoh "ITEM NO." YANG JANGAN DI AMBIL:
     - ZY-HG05
     - ZY-HB112
     - ZY-C341

3. inv_description:
   - Ekstrak dari kolom "DESCRIPTION".
   - Gabungkan seluruh wrapped lines yang masih merupakan bagian dari deskripsi item.
   - Jangan sertakan QTY, UNIT, U/PRICE, AMOUNT, atau nomor PO.
   - Contoh hasil:
     "HANDLEBAR;ZY-HB112;SAND ANODIZED BLACK;- ,ALLOY,RISE,740MM,12MM,6DEG,31.8MM,ISO-M,W/O LOGO,W/CENTER MARK THREAD-201"

4. inv_gw:
   - Isi null kecuali gross weight tertulis eksplisit pada invoice.

5. inv_gw_unit:
   - Isi null kecuali unit gross weight tertulis eksplisit pada invoice.

6. inv_quantity:
   - Ekstrak dari kolom "QTY".
   - Ambil angka numeriknya saja.
   - Contoh:
     "5000", "175", "3070", "75".

7. inv_quantity_unit:
   - Ekstrak dari kolom "UNIT".
   - Contoh:
     "SET", "PCS".

8. inv_unit_price:
   - Ekstrak dari kolom "U/PRICE (USD)".
   - Ambil angka numeriknya saja. Jangan ambil simbol mata uangnya.
   - Contoh:
     "US$2.70" -> 2.70

"""