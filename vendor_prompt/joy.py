JOY_PROMPT = """
INVOICE (INV):

ATURAN SANGAT PENTING UNTUK DOKUMEN INVOICE VENDOR INI (BACA DUA KALI):
- Apabila ada beberapa line item dengan tipe data numerik (QTY, AMOUNT) yang tergabung dalam satu merged-cell, maka value yang tertera adalah untuk line item dalam group tersebut yang **PALING BAWAH** (BOTTOM row), dan sisanya **0**.
- DILARANG KERAS untuk menduplikasi value numerik pada line item yang memiliki merged-cell. HANYA LINE ITEM PALING BAWAH DARI MERGED-CELL YANG BOLEH MENGAMBIL VALUE NUMERIK; SELURUH BARIS LAIN DALAM GROUP TERSEBUT HARUS DIISI 0 (BUKAN null, BUKAN nilai apapun selain 0).
- DILARANG KERAS untuk menambahkan/membagi value numerik dari satu line item ke line item lain TANPA TERKECUALI!
- KONSISTENSI: Aturan "paling bawah" ini berlaku SERAGAM untuk SEMUA kolom numerik merged-cell di invoice ini (QTY, AMOUNT, dan kolom numerik lain yang merged). JANGAN ada satu pun kolom yang dibaca dengan aturan "paling atas".

SANITY-CHECK ANGKA (untuk meredam salah baca OCR digit-mirip — 6 vs 7, 0 vs 3, 2 vs 5, dll):
- Setelah mengekstrak `inv_quantity` dan `inv_unit_price` dari baris merged-cell PALING BAWAH, hitung perkiraan amount = inv_quantity × inv_unit_price, lalu bandingkan dengan `inv_amount` yang dibaca.
- Jika selisihnya signifikan (> 1% dari amount), KEMUNGKINAN BESAR salah satu dari ketiganya salah baca OCR. Periksa ulang digit-digit yang mungkin terbalik (terutama 6↔7, 2↔3, 0↔8, 1↔7) dan pilih kombinasi yang konsisten amount = qty × price.
- Contoh: jika qty=6234, price=30 → amount harus 187020; jangan terima qty=6754 (yang menghasilkan 202620) bila amount tertulis 187020.

1. `inv_customer_po_no`: Ekstrak dari kolom "PO.NO.".
2. `inv_spart_item_no`: Ekstrak dari kolom "CODE" (Misal: HUFJY4310000000)
3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari kolom "DESCRIPTION" (pisahkan dari kode barang, ambil teks panjangnya).
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`:
    - Ekstrak dari kolom "QTY".
    - SANGAT PENTING: Apabila ada beberapa line item yang tergabung dalam satu QTY (quantity) merged-cell, maka QTY yang tertera adalah untuk line item dalam group tersebut yang **PALING BAWAH (BOTTOM row)**, dan sisanya **0**.
        Contoh visual merged-cell QTY (sel QTY menyatu/merged secara vertikal mencakup 3 baris A, B, C; angka 480 tercetak di sel merged tersebut secara visual):
        |   ITEM  |  QTY    |
        |   A     |         |   ← bagian merged-cell, BUKAN baris tujuan
        |   B     |         |   ← bagian merged-cell, BUKAN baris tujuan
        |   C     |  480    |   ← BARIS PALING BAWAH dari group, INI yang mengambil 480
        Maka:
        - Line item A: inv_quantity = 0 (BUKAN 480, BUKAN null)
        - Line item B: inv_quantity = 0 (BUKAN 480, BUKAN null)
        - Line item C: inv_quantity = 480
        Verifikasi: jumlah inv_quantity dari seluruh baris dalam satu merged-cell group HARUS = nilai numerik yang tercetak di sel merged tersebut (0 + 0 + 480 = 480 ✓).
    - Ekstrak HANYA dari kolom "QTY" dari dokumen invoice. DILARANG KERAS untuk mengambil dari kolom lain manapun atau dari dokumen lain manapun.
    - CROSS-CHECK: Setelah ekstrak, validasi dengan inv_amount = inv_quantity × inv_unit_price pada baris bottom merged-cell. Jika tidak match (selisih > 1%), periksa kembali digit yang mungkin salah baca OCR.

6. `inv_quantity_unit`: Ekstrak dari kolom "UNIT" (misalnya "SET").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "UNIT PRICE".
8.  `inv_amount`:
    - Ekstrak nilai angka dari kolom "AMOUNT".
    - Apabila ada beberapa line item yang tergabung dalam satu AMOUNT (amount) merged-cell, maka AMOUNT yang tertera adalah untuk line item dalam group tersebut yang **PALING BAWAH (BOTTOM row)**, dan sisanya **0**.
        Contoh visual merged-cell AMOUNT (sel AMOUNT menyatu/merged secara vertikal mencakup 3 baris A, B, C; angka 5760 tercetak di sel merged tersebut secara visual):
        |   ITEM  |  AMOUNT    |
        |   A     |            |   ← bagian merged-cell, BUKAN baris tujuan
        |   B     |            |   ← bagian merged-cell, BUKAN baris tujuan
        |   C     |  5760      |   ← BARIS PALING BAWAH dari group, INI yang mengambil 5760
        Maka:
        - Line item A: inv_amount = 0 (BUKAN 5760, BUKAN null)
        - Line item B: inv_amount = 0 (BUKAN 5760, BUKAN null)
        - Line item C: inv_amount = 5760
        Verifikasi: jumlah inv_amount dari seluruh baris dalam satu merged-cell group HARUS = nilai numerik yang tercetak di sel merged tersebut (0 + 0 + 5760 = 5760 ✓).
    - CROSS-CHECK WAJIB sebelum finalisasi inv_amount: hitung inv_quantity × inv_unit_price pada baris bottom. Hasilnya HARUS persis sama dengan inv_amount yang dibaca. Bila tidak, kemungkinan ada digit OCR yang salah baca — periksa ulang angka yang mungkin tertukar (6↔7, 2↔3, 0↔8, 1↔7) pada SALAH SATU dari ketiga field tersebut hingga konsisten.
    - GRAND-TOTAL CHECK: Total seluruh inv_amount (non-zero) di dokumen ini harus mendekati total grand-total invoice. Jika sum invoice anda menyimpang signifikan dari total yang tertera di footer dokumen, kemungkinan ada satu atau lebih merged-cell yang nilainya salah baca — periksa kembali.

"""