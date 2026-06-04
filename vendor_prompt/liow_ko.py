LIOW_KO_PROMPT = """
INVOICE (INV)

Aturan umum ekstraksi vendor LIOW KO:
- Vendor pada sampel adalah LIOW KO ELECTRONIC TECHNOLOGY (SHENZHEN) CO., LTD.
- Dokumen invoice berjudul "INVOICE".
- Dokumen packing list berjudul "PACKING LIST".
- Dokumen BL berjudul "BILL OF LADING".
- Dokumen COO berjudul "REGIONAL COMPREHENSIVE ECONOMIC PARTNERSHIP AGREEMENT CERTIFICATE OF ORIGIN".
- Jika field bertipe string dan tidak ada bukti yang jelas, isi "null".
- Jika field bertipe number dan tidak ada bukti yang jelas, isi null.
- Jangan mengisi field dari dokumen lain jika field tersebut harus berasal dari dokumen spesifik.
- Gabungkan teks yang terpotong baris / line wrap menjadi satu value yang utuh.
- Jika satu row/item terpotong ke halaman berikutnya, tetap anggap sebagai item yang sama, bukan item baru.
- Jangan menggabungkan dua row berbeda hanya karena part number atau description-nya sama.
- Jangan halusinasi nilai yang tidak tercetak jelas pada dokumen.
- Rapikan whitespace berlebih akibat OCR, tetapi jangan mengubah isi sebenarnya.

Struktur umum invoice LIOW KO:
- Header utama line item:
  Purchase order Number | PART NUMBER | DESCRIPTION | UNIT | QUANTITY | UNIT PRICE(USD) | AMOUNT
- Pada invoice LIOW KO, customer PO ada per row pada kolom pertama.
- Tidak ada kolom nomor urut item / seq yang jelas pada sampel invoice.
- Tidak ada gross weight per item pada sampel invoice.

1. inv_customer_po_no
   - Ambil dari kolom "Purchase order Number" pada row item yang sama.
   - Customer PO berbentuk angka dan berlaku per row, bukan grouping block.
   - Ambil angka PO-nya saja sebagai string.
   - Contoh:
     - "45327072" -> inv_customer_po_no = "45327072"
     - "49021355" -> inv_customer_po_no = "49021355"
   - Jangan ambil:
     - invoice number
     - BL number
     - container number
     - tanggal invoice

2. inv_seq
   - Hanya ambil jika invoice benar-benar mencetak nomor item / seq yang eksplisit.
   - Pada sampel invoice LIOW KO, tidak ada kolom seq item-level yang jelas.
   - Jangan menggunakan urutan row sebagai seq.
   - Karena itu, jika tidak ada nomor item yang tercetak jelas:
     inv_seq = null

3. inv_spart_item_no
   - Ambil dari kolom "PART NUMBER".
   - Gabungkan jika part number terpotong ke dua baris.
   - Contoh:
     - "FRXLKIS21PHG0100" -> inv_spart_item_no = "FRXLKIS21PHG0100"
     - "FREZZINSRE1204" -> inv_spart_item_no = "FREZZINSRE1204"
     - "FRPLKIS21PFP1600" -> inv_spart_item_no = "FRPLKIS21PFP1600"
   - Jangan ambil:
     - customer PO
     - description
     - unit
     - quantity
     - price
     - amount

4. inv_description
   - Ambil dari kolom "DESCRIPTION" pada row item yang sama.
   - Gabungkan seluruh description yang ter-wrap sampai sebelum kolom unit/quantity item itu berakhir.
   - Jika description terpotong baris, gabungkan menjadi satu string utuh.
   - Pertahankan spesifikasi yang memang tercetak sebagai bagian description.
   - Contoh:
     - "FRAME PART;LIOW KO;IS21PHG01_V1"
     - "FRAME PART; REPLACEABLE DROP OUT 8910-0000P BK DA"
     - "FRAME PART;LIOW KO;IS21PRE03-1-R_F2 AND IS21PRE03-L_F3;-;AL6061;"
   - Jangan masukkan:
     - customer PO
     - part number
     - unit
     - quantity
     - unit price
     - amount
     - header dokumen
     - alamat shipper / consignee

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Pada sampel invoice LIOW KO, tidak ada gross weight per item.
   - Karena itu:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Pada sampel invoice LIOW KO, tidak ada unit gross weight per item.
   - Karena itu:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil nilai quantity dari kolom "QUANTITY".
   - Ambil angka numeriknya saja.
   - Hapus separator ribuan jika ada.
   - Contoh:
     - "64" -> 64
     - "3500" -> 3500
     - "700" -> 700

8. inv_quantity_unit
   - Ambil dari kolom "UNIT".
   - Gunakan unit yang tercetak pada invoice.
   - Contoh:
     - "SET" -> "SET"
     - "PCS" -> "PCS"
     - "PRS" -> "PRS"

9. inv_unit_price
   - Ambil dari kolom "UNIT PRICE(USD)".
   - Nilai harus numeric saja.
   - Jangan bawa teks "USD".
   - Contoh:
     - "3.14" -> 3.14
     - "1.55" -> 1.55
     - "18.30" -> 18.3

10. inv_amount
   - Ambil dari kolom "AMOUNT".
   - Nilai harus numeric saja.
   - Hapus separator ribuan jika ada.
   - Contoh:
     - "200.96" -> 200.96
     - "5,425.00" -> 5425.0
     - "3,668.00" -> 3668.0

"""