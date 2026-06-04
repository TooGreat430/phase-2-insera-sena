NINGBO_JULONG_PROMPT = """"

INVOICE (INV):

1. inv_customer_po_no:
   - Ekstrak dari baris PO number yang berdiri sendiri di atas item.
   - Jika 1 PO menaungi beberapa item berikutnya dan PO tidak diulang, maka semua item berikutnya mewarisi PO terakhir sampai ada PO baru.
      - Contoh:
                                  45324623
      PLASTIC WASHER;FEIMIN;-;BLACK;-,PLASTIC,ID:1-1/8"MM,OD:34MM,H10MM,W/O LOGO,-
      PLASTIC WASHER;FEIMIN;-;BLACK;-,PLASTIC,ID:1-1/8"MM,OD:34MM,H10MM,W/O LOGO,-
                                  45324624
      ALUMINIUM WASHER; -; -; SAND BLACK; ALLOY, ID:28.6MM,OD:33MM, H:5MM, W/O LOGO
      ALUMINIUM WASHER; -; -; SAND BLACK; ALLOY, ID:28.6MM,OD:33MM, H:5MM, W/O LOGO
      ALUMINIUM WASHER; -; -; SAND BLACK; ALLOY, ID:28.6MM,OD:33MM, H:5MM, W/O LOGO
      ALUMINIUM WASHER; -; -; SAND BLACK; ALLOY, ID:28.6MM,OD:33MM, H:5MM, W/O LOGO                      

      Maka untuk 2 line item teratas inv_customer_po_no = 45324623, karena po no 45324623 menaungi 2 item tersebut.
      Kemudian untuk 4 line item dibawahnya inv_customer_po_no = 45324624, karena po no 45324624 menaungi 4 item tersebut.

2. inv_spart_item_no:
   - Ekstrak dari kolom "NO." kode item panjang alfanumerik.
   - Jangan ambil dari kolom "MODEL NO."
   - Contoh:
     "HDWZZ286X10012"
     "HDWFP00001-R"
     "HDWZZ286X10010"

3. inv_description:
   - Ekstrak deskripsi item dari kolom "DESCRIPTION OF GOODS"
   - Gabungkan seluruh wrapped lines yang masih merupakan bagian dari deskripsi item.
   - ABAIKAN / JANGAN SERTAKAN "BICYCLE PARTS", PO No, quantity, unit price, atau amount.
   - ABAIKAN / JANGAN SERTAKAN "Model No." seperti contoh:
     FP-HW-20, FP-B902E-2NL, FP-H885E1
   - Contoh hasil:
     PART OF HEAD PART ; FEIMIN ; HW-20 FLAT CAP ; SAND BLAST BLACK ; ALLOY 28.6, BLACK BOLT, W/STAR NUT,W/O LOGO"

4. inv_gw:
   - Isi null kecuali gross weight tertulis eksplisit pada invoice.

5. inv_gw_unit:
   - Isi null kecuali unit gross weight tertulis eksplisit pada invoice.

6. inv_quantity:
   - Ekstrak dari kolom "QUANTITY".
   - Contoh:
     "5000", "200", "3600", "582", "1470".

7. inv_quantity_unit:
   - Ekstrak unit quantity setelah angka quantity dari kolom "QUANTITY".
   - Contoh:
     "SETS", "PRS", "PCS".

8. inv_unit_price:
   - Ekstrak dari kolom "UNIT PRICE IN US$".
   - Ambil angka numeriknya saja.
   - Contoh:
     "US$0.260" -> 0.260
     "US$1.990" -> 1.990

"""