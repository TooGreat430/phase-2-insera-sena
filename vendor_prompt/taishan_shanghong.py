TAISHAN_SHANGHONG_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari kolom "PO NO". Apabila dalam satu baris/sel terdapat beberapa nomor PO yang ditulis bertumpuk secara vertikal (misalnya "45328183 \\n 45328185 \\n 45328209"), ekstrak seluruh string tersebut atau pisahkan secara sejajar (line-by-line) sesuai item pasangannya.
2. `inv_spart_item_no`: Ekstrak string kode part pendek yang terletak pada kolom setelah PO NO / di area awal kolom deskripsi (misalnya "IS19PHT10-110-A", "IS21PHT03-110-B", "HT-024-170").
3. `inv_description`: Ekstrak uraian teks deskripsi spesifikasi panjang yang terletak di bagian kanan tabel atau di bawah baris item bersangkutan (misalnya "PIPE H/T HONG ZHUO; IS19PHT10-110-A; AL6061; RAW LENGTH..."). Gabungkan teks menjadi satu kalimat utuh jika terputus baris baru.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena dokumen invoice ini tidak mencantumkan informasi berat fisik pada tingkat baris item.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "QTY" (misalnya "90", "35", "140").
6. `inv_quantity_unit`: Ekstrak satuan string dari kolom di sebelah kanan angka QTY (misalnya "PCS", "SETS", atau teks typo "PARS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "UNIT PRICE IN USD" (hapus simbol mata uang jika terbaca).
8. `inv_amount`: Ekstrak nilai angka dari kolom "TOTAL AMOUNT USD" (hapus awalan string mata uang seperti "US$" dan koma ribuan).

""" 