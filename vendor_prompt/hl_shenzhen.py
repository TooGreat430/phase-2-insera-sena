HL_SHENZHEN_PROMPT = """
INVOICE (INV)

Aturan umum ekstraksi vendor HL SHENZHEN:
- Vendor pada sampel adalah HL CORP ( SHEN ZHEN ) / HL CORP(SHEN ZHEN).
- Dokumen invoice berjudul "COMMERCIAL INVOICE".
- Dokumen packing list berjudul "PACKING LIST".
- Dokumen BL berjudul "BILL OF LADING".
- Dokumen COO berjudul "CERTIFICATE OF ORIGIN" / Form RCEP.
- Jika field bertipe string dan tidak ada bukti yang jelas, isi "null".
- Jika field bertipe number dan tidak ada bukti yang jelas, isi null.
- Jangan mengisi field dari dokumen lain jika field tersebut harus berasal dari dokumen spesifik.
- Gabungkan teks yang terpotong baris / line wrap menjadi satu value yang utuh.
- Jika item terpotong ke halaman berikutnya, tetap anggap sebagai item yang sama, bukan item baru.
- Jangan halusinasi nilai yang tidak tercetak jelas pada dokumen.

Struktur umum invoice HL SHENZHEN:
- Header utama line item:
  ITEM DESCRIPTION | Q'TY | U/PRICE | AMOUNT
- Pada vendor HL SHENZHEN, line item biasanya diawali:
  1) customer PO number 8 digit
  2) spare part / item code alphanumeric
  3) description multiline
  4) numeric line berisi quantity, unit price, amount
- Tidak ada kolom seq/item number khusus yang tercetak pada invoice.
- Nomor urut item perlu dibentuk berdasarkan urutan kemunculan item pada invoice.
- Header quantity pada invoice tercetak sebagai:
  Q'TY (PCS/PRS)
- Pada beberapa item, description bisa terpotong ke beberapa line dan harus digabung utuh.
- Jangan menganggap line "BICYCLE PARTS" sebagai description item.

1. inv_customer_po_no
   - Ambil customer PO number dari angka 8 digit pertama di awal blok item invoice.
   - Pada vendor HL SHENZHEN, angka ini muncul sebelum spare part code.
   - Contoh:
     - "45325168 FFUHL26CH38600" -> inv_customer_po_no = "45325168"
     - "45323722 HBSHLTDSD636B001" -> inv_customer_po_no = "45323722"
   - Jangan ambil:
     - invoice no.
     - reference no.
     - BL no.
     - container no.
     - seal no.

2. inv_seq
   - Karena invoice HL SHENZHEN tidak memiliki kolom seq tercetak, buat nomor urut item berdasarkan urutan kemunculan item pada invoice.
   - Mulai dari 1 dan naik +1 untuk setiap item baru.
   - Contoh:
     - item pertama -> inv_seq = 1
     - item kedua -> inv_seq = 2
     - item ketiga -> inv_seq = 3
   - Jangan mengambil customer PO number sebagai inv_seq.

3. inv_spart_item_no
   - Ambil kode alphanumeric kedua setelah customer PO number.
   - Ini adalah spare part / item number item invoice.
   - Contoh:
     - "45325168 FFUHL26CH38600" -> inv_spart_item_no = "FFUHL26CH38600"
     - "45323722 HBRHLDRAL21102" -> inv_spart_item_no = "HBRHLDRAL21102"
     - "45323723 SDNHLAT1013400" -> inv_spart_item_no = "SDNHLAT1013400"
   - Jangan ambil:
     - customer PO number
     - model pendek di description
     - quantity
     - price
     - amount

4. inv_description
   - Ambil deskripsi barang dari line-line setelah customer PO number + item code.
   - Gabungkan seluruh line description item sampai sebelum item berikutnya.
   - Masukkan spesifikasi barang yang memang bagian dari description.
   - Jangan masukkan:
     - customer PO number
     - item code
     - quantity
     - unit price
     - amount
     - section title "BICYCLE PARTS"
   - Contoh hasil:
     - "FORK CH-386A-26\" Φ28.6*Φ25.4*260L*0T/30 AL+ST YS-728 BLACK LEGS/BED CROWN AND BED STANCHIONS.W/O PIVOT & W/DISCMOUNT.TRAVEL:60MM,W/ZOOM LOGO SEPARATE"
     - "STEM TDS-D636B-8FOV(EN 15194) E:75 10*M5 AL SS.A.BK/"
     - "SEAT POST SP-C255(ISO-M) Φ30.9*350*2.2 BLACK BOLT A356.2/AL BED/BED/S.A.BK/"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Pada invoice HL SHENZHEN sampel, tidak ada gross weight per line item.
   - Karena itu:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Pada invoice HL SHENZHEN sampel, tidak ada gross weight per line item.
   - Karena itu:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil nilai quantity dari numeric line item invoice.
   - Ambil angka numeriknya saja.
   - Contoh:
     - "200 8.85 1,770.00" -> inv_quantity = 200
     - "1000 6.80 6,800.00" -> inv_quantity = 1000
     - "140 10.00 1,400.00" -> inv_quantity = 140

8. inv_quantity_unit
   - Ambil unit quantity dari bukti yang tercetak pada invoice.
   - Pada invoice HL SHENZHEN, header quantity tercetak sebagai "Q'TY (PCS/PRS)" dan umumnya tidak ada unit per-row yang ditulis ulang.
   - Jika item row secara eksplisit mencantumkan unit, gunakan unit tersebut.
   - Jika tidak ada unit per-row yang lebih spesifik, gunakan "PCS/PRS".
   - Jangan mengisi dari COO atau packing list untuk field invoice ini.

9. inv_unit_price
   - Ambil dari kolom U/PRICE.
   - Nilai harus numeric saja.
   - Hapus tanda pemisah ribuan jika ada.
   - Contoh:
     - "8.85" -> 8.85
     - "6.80" -> 6.8
     - "10.00" -> 10.0

10. inv_amount
   - Ambil dari kolom AMOUNT.
   - Nilai harus numeric saja.
   - Hapus tanda pemisah ribuan.
   - Contoh:
     - "1,770.00" -> 1770.0
     - "6,800.00" -> 6800.0
     - "1,400.00" -> 1400.0

"""