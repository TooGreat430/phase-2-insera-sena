TOHO_PROMPT = """
INVOICE (INV)

Struktur umum invoice TOHO:
- Ada grouping "P/O No.C25-1544U/45323564" atau format serupa.
- Setelah itu muncul beberapa line item.
- Header utama line item:
  Seq. | Item No. | Description | Quantity | Unit Price | Amount
- Satu line item biasanya berbentuk:
  "1 CWSSXSAC400001 "SAMOX" CHAINWHEEL MODEL: 129 SET 9.05 1167.45"
  lalu di bawahnya ada lanjutan deskripsi model
  lalu line "** CODE:XXXXXXXXXXXX"
- Pada vendor TOHO, satu item juga bisa terpotong ke halaman berikutnya.
  Contoh: item seq 6 berlanjut ke page berikutnya dan BUKAN item baru.

1. inv_customer_po_no
   - Ambil dari "P/O No." terdekat yang menaungi line item tersebut.
   - Format P/O vendor TOHO biasanya seperti:
     - C25-1544U/45323564
     - C25-1619U/45324707
   - inv_customer_po_no yang diambil adalah angka customer PO setelah slash "/".
   - Contoh:
     - "P/O No.C25-1544U/45323564" -> inv_customer_po_no = "45323564"
     - "P/O No.C25-1619U/45324707" -> inv_customer_po_no = "45324707"
   - Jangan ambil prefix seperti "C25-1544U" atau "C25-1619U" sebagai customer PO number.
   - Jangan ambil invoice number, BL number, atau nomor lain.

2. inv_seq
   - Gunakan nilai pada kolom "Seq.".
   - Untuk vendor TOHO, seq sudah tercetak jelas pada dokumen, jadi pakai angka tersebut apa adanya.
   - Jika satu item terpotong ke halaman berikutnya tetapi seq-nya sama, tetap anggap itu item yang sama dan JANGAN dihitung ulang.
   - Contoh:
     - seq 6 di page 1 dan lanjutan seq 6 di page 2 tetap inv_seq = 6, bukan item baru.

3. inv_spart_item_no
   - Ambil item code / part code untuk item invoice.
   - Prioritas pencarian:
     1) nilai setelah label "** CODE:" atau "**CODE:"
     2) jika tidak ada, gunakan Item No.
   - Untuk vendor TOHO, CODE pada deskripsi memiliki prioritas lebih tinggi daripada Item No.
   - Contoh:
     - Item No: CWSSXAF38D0002-165
       Description berisi: ** CODE: CWSSXAF38D0002
       maka inv_spart_item_no = "CWSSXAF38D0002"
     - Item No: CWSSXSAC38J00002-152
       Description berisi: **CODE:CWSSXSAC38J00002
       maka inv_spart_item_no = "CWSSXSAC38J00002"
   - Jika Item No dan CODE sama, ambil value tersebut.
   - Jangan ambil qty, unit, seq, unit price, atau amount.

4. inv_description
   - Ambil deskripsi barang dari line item invoice.
   - Gabungkan seluruh baris deskripsi item sampai sebelum item berikutnya atau sebelum P/O berikutnya.
   - Pada vendor TOHO, description biasanya dimulai dari teks seperti:
     - "SAMOX CHAINWHEEL MODEL:"
     - "STEEL CHAINWHEEL & ALLOY CRANK"
     - "SAMOX CW MODEL:"
   - Masukkan detail spesifikasi barang yang memang bagian dari deskripsi, misalnya:
     - model
     - warna
     - ukuran crank
     - tooth
     - BB / CL information jika masih merupakan spesifikasi item
   - Jangan masukkan:
     - seq
     - Item No.
     - quantity
     - unit
     - unit price
     - amount
     - line "** CODE:..."
   - Jika description terpotong ke halaman berikutnya, gabungkan ke item yang sama.
   - Contoh hasil:
     - "SAMOX CHAINWHEEL MODEL: SAC40-018BNS42, BLACK, 170 MM 10/11SP, ALLOY BK 170MM, STEEL: BED 42T, OT, W/O CG W/O SPIDER, SQUARE, E/CAPLESS BOLT, W/O LOGO ** BB :68 MM CL : NORMAL NON BOOST"
     - "SAMOX CHAINWHEEL MODEL: AF38-D28NS-BG31, BLACK 1 SP, (3/32\" *28T* 165 MM), ALLOY CRANK, STEEL 28T BED, 49MM 0T, W/CG, W/O SPIDER, SQUARE, C/CAPLESS BOLT W/O LOGO, W/BCD76, ALLOY CG"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Pada dokumen invoice TOHO yang tersedia, tidak ada gross weight per line item.
   - Karena itu, untuk vendor TOHO:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Pada dokumen invoice TOHO yang tersedia, tidak ada gross weight per line item.
   - Karena itu, untuk vendor TOHO:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil nilai quantity line item pada invoice.
   - Ambil dari kolom Quantity pada baris item invoice.
   - Contoh:
     - "129 SET" -> inv_quantity = 129
     - "100 SET" -> inv_quantity = 100
     - "525 SET" -> inv_quantity = 525

8. inv_quantity_unit
   - Ambil unit quantity yang menempel pada Quantity di invoice.
   - Untuk vendor TOHO pada dokumen ini, unit yang muncul adalah "SET".
   - Contoh:
     - "129 SET" -> inv_quantity_unit = "SET"

9. inv_unit_price
   - Ambil dari kolom Unit Price line item invoice.
   - Nilai harus numeric saja.
   - Contoh:
     - "9.05" -> 9.05
     - "8.6" -> 8.6
     - "18.45" -> 18.45

10. inv_amount
   - Ambil dari kolom Amount line item invoice.
   - Nilai harus numeric saja.
   - Contoh:
     - "1167.45" -> 1167.45
     - "860" -> 860
     - "3003" -> 3003

"""