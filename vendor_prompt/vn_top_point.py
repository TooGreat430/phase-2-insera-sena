VN_TOP_POINT_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`:
    Ekstrak dari kolom "PO NO:".
    FORMAT MULTI-PO (banyak baris invoice di vendor ini menggabungkan beberapa PO untuk 1 item):
    - Jika sel "PO NO:" berisi beberapa PO yang dipisahkan slash "/", contoh "45321386/45321766/45322726/45323418/45323665/45323664/" (kadang ada trailing slash di akhir),
    - NORMALISASI: hilangkan trailing slash, lalu ekstrak PO PERTAMA (sebelum slash pertama).
    - Contoh: "45321386/45321766/45322726/" → inv_customer_po_no = "45321386"
    - Contoh: "45323666/45323664/" → inv_customer_po_no = "45323666"
    - Contoh: "45324747" (single PO) → inv_customer_po_no = "45324747"
    Konsisten ini PENTING agar nilai dapat dipasangkan dengan master PO. DILARANG KERAS menyimpan multi-PO sebagai 1 string utuh.
2. `inv_spart_item_no`: Ekstrak dari kolom "PRODUCT NO:" (misalnya "HG078(TP-T-9012 BLACK)" atau "IS18PRE03-1(JD-9F-0493)-R/L"). Abaikan teks pada kolom "ITEM NAME:" karena merupakan kode internal pabrik.
3. `inv_description`: Ekstrak deskripsi barang dari kolom "DESCRIPTION" (misalnya "FRAME PART").
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena dokumen invoice ini tidak mencantumkan informasi berat pada tingkat baris item.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "Q'TY".
6. `inv_quantity_unit`: Ekstrak satuan dari kolom "UNIT" (misalnya "SET", "PRS", "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "U/PRICE USD".
8. `inv_amount`: Ekstrak nilai angka dari kolom "AMOUNT USD" (hapus tanda koma ribuan).

"""