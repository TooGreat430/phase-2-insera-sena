KARET_DELI_PROMPT = """
ATURAN EKSTRAKSI KHUSUS VENDOR KARET DELI:

=========================================
PENGECUALIAN LINE ITEM (WAJIB DIABAIKAN):
=========================================
Tabel dokumen ini mencampur item barang dengan informasi rekapitulasi. Anda DILARANG KERAS mengekstrak baris-baris berikut sebagai line item (abaikan sepenuhnya dari output JSON):
1. Baris perhitungan nominal/pajak: "Brutto", "Diskon", "Total tanpa PPN", "PPN", "Total dengan PPN", "Rp.".
2. Baris rekapitulasi kemasan: "JUMLAH SATUAN", "GRAND TOTAL", "TOTAL".
3. Baris informasi pengiriman: "CONTAINER = TAKU", "SHIPPING MARKS", "MEDAN-SURABAYA".

Jika Anda melihat kata-kata di atas pada kolom Description/Uraian, LEWATI baris tersebut. HANYA ekstrak baris yang mendeskripsikan spesifikasi ban/karet (seperti "BDS...", "BLS...", "SETS BLDS...").

=========================================
INVOICE (INV):
=========================================
1. `inv_customer_po_no`:
    BENTUK STANDAR — Ekstrak dari teks di dalam kolom "Description Uraian" yang berawalan "PO.INS-" atau "PO. INS-". Ambil HANYA angka PO-nya saja (misalnya dari "PO.INS-45318349/NEW LABEL", ekstrak "45318349").
    BENTUK NON-STANDAR (KASUS KLAIM / K100) — Beberapa baris menggunakan format PO berbeda dengan separator "/" (BUKAN strip "-") dan mengandung tanggal + kode huruf, contoh: "PO.INS/01/01/26/K100/NEW LABEL". Untuk bentuk ini, ekstrak SELURUH string PO termasuk garis miring dan kode huruf (tanpa awalan "PO." dan tanpa suffix "/NEW LABEL"). Contoh: dari "PO.INS/01/01/26/K100/NEW LABEL" -> inv_customer_po_no = "INS/01/01/26/K100".
    JANGAN melewati / menolak baris dengan format PO non-standar; tetap ekstrak full identifier-nya.
2. `inv_spart_item_no`: Ekstrak dari teks di dalam kolom "Description Uraian" yang berawalan abjad alfabet diikuti dengan strip (-) dan angka (misalnya "DL-540", "SA-206", atau "S-199"). Jika terdapat lebih dari satu pola yang cocok, ambil yang pertama kali muncul di teks.
3. `inv_description`: Ekstrak teks lengkap dari kolom "Description Uraian" (termasuk ukuran ban dan jenisnya, abaikan teks keterangan PO di dalamnya jika memungkinkan).
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Quantity Jumlah".
6. `inv_quantity_unit`: Ekstrak unit kemasan yang terletak di sebelah kanan angka kuantitas pada kolom "Quantity Jumlah" (misalnya "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price Hrg Satuan".
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount Jumlah".

"""