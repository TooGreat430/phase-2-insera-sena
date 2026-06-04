HL_VIETNAM_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari kolom "Order No" (misalnya "45324105" atau "45324678"). Abaikan kolom "PO No" karena berisi kode produksi internal vendor.
2. `inv_spart_item_no`: Ekstrak dari kolom "Item No" (misalnya "FRPVTPV21M0000-R" atau "HBRHLAL300BT02").
3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari kolom "Description of goods". Gabungkan teks menjadi satu kalimat utuh jika terpecah ke dalam beberapa baris.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Q'Ty" (misal dari "20,000 PCS", ambil angka 20000). Hapus tanda koma ribuan.
6. `inv_quantity_unit`: Ekstrak satuan kemasan dari kolom "Q'Ty" yang posisinya berada setelah angka (misalnya "PCS" atau "SET").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom harga satuan (kolom ini posisinya di sebelah kiri kolom Amount, terkadang tajuk kolomnya terbaca oleh OCR sebagai huruf "e" atau spasi kosong).
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount" atau "Amount USD)" (hapus koma ribuan).
*Instruksi Pemetaan Vertikal (Merged-Row):* Apabila dalam satu baris tabel visual terdapat beberapa item teks yang disusun sejajar secara vertikal pada kolom Order No, Item No, Description, Q'Ty, dan Amount, pisahkan teks tersebut secara paralel (line-by-line) menjadi beberapa objek mandiri agar nilainya berkorelasi tepat satu sama lain.

"""