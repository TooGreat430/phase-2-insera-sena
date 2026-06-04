VELO_ENTERPRISE_PROMPT = """
INVOICE (INV)

Aturan umum ekstraksi vendor VELO ENTERPRISE:
- Vendor pada sampel adalah VELO ENTERPRISE CO., LTD.
- Dokumen invoice berjudul "Commercial Invoice".
- Dokumen packing list berjudul "Packing List".
- Dokumen BL berjudul "Bill Of Lading".
- Jika field bertipe string dan tidak ada bukti yang jelas, isi "null".
- Jika field bertipe number dan tidak ada bukti yang jelas, isi null.
- Jangan mengisi field dari dokumen lain jika field tersebut harus berasal dari dokumen spesifik.
- Gabungkan teks yang terpotong baris / line wrap menjadi satu value yang utuh.
- Jika item terpotong ke halaman berikutnya, tetap anggap sebagai item yang sama, bukan item baru.
- Jangan halusinasi nilai yang tidak tercetak jelas pada dokumen.

Struktur umum invoice VELO:
- Header utama line item:
  Item/Part no. | Description | Quantity | Unit Price | Amount
- Pada vendor VELO, kolom "Item/Part no." berisi:
  1) nomor urut item / seq
  2) part number / spare part number
- Part number sering terpotong ke 2 baris.
  Contoh pola:
  - seq: 60
  - part no terpotong:
      BAXVLPLG38802
      0R
    maka part number utuh = BAXVLPLG388020R
- Di dalam area description sering muncul line "P.O. NO:45322360" atau format serupa.
- Line "P.O. NO:..." adalah penanda grouping customer PO untuk item-item setelahnya, BUKAN bagian description barang.
- Penting untuk layout / OCR reading order:
  - Pada sebagian invoice VELO, part number dari kolom "Item/Part no." dapat ikut terbaca di bawah line "P.O. NO:..." sebelum description barang dimulai.
  - Jika ada alphanumeric panjang tepat di bawah "P.O. NO:..." dan nilainya cocok dengan pola part number item, perlakukan itu sebagai inv_spart_item_no, BUKAN inv_description.
  - Jangan salah menganggap line alphanumeric panjang di bawah "P.O. NO:..." sebagai pl_item_no; konteks invoice ini tetap milik inv_spart_item_no.
  - Jika part number tersebut terpotong ke baris berikutnya, gabungkan seluruh fragmennya menjadi satu value utuh tanpa spasi.
- Pada page pertama juga ada PO NO di area kanan atas. Jika item pertama belum punya line "P.O. NO:..." yang lebih dekat di atasnya, maka gunakan PO header/page tersebut.
- Jika page berikutnya melanjutkan group PO yang sama dan belum ada PO baru, carry forward PO terakhir yang valid dari item sebelumnya.
1. inv_customer_po_no
   - Ambil customer PO number dari "P.O. NO:" / "PO NO." terdekat yang menaungi item tersebut.
   - Prioritas:
     1) line "P.O. NO:xxxxx" yang muncul paling dekat di atas item
     2) jika item adalah item pertama dalam group dan belum ada line internal, gunakan PO header pada page
     3) jika page lanjutan tidak mengulang PO, carry forward PO terakhir yang valid dari page/item sebelumnya
   - Customer PO yang diambil adalah angka PO-nya saja.
   - Contoh:
     - "PO NO. 45322358" -> inv_customer_po_no = "45322358"
     - "P.O. NO:45322360" -> inv_customer_po_no = "45322360"
   - Jangan ambil:
     - invoice no.
     - ref no.
     - BL no.
     - vessel / shipment no.
   - Line "P.O. NO:..." yang berada di antara dua item berlaku untuk item setelah line tersebut, bukan untuk item sebelumnya.

2. inv_seq
   - Ambil dari angka urut pada kolom "Item/Part no.".
   - Ini adalah nomor item yang tercetak jelas di sisi kiri.
   - Contoh:
     - 60
     - 110
     - 172
     - 215
   - Jangan ambil angka quantity, harga, atau PO number sebagai inv_seq.

3. inv_spart_item_no
   - Ambil part number dari kolom "Item/Part no.".
   - Pada vendor VELO, part number berada di bawah seq dan sering wrap ke baris berikutnya.
   - Gabungkan seluruh fragmen part number yang terpotong menjadi satu string tanpa spasi tambahan.
   - Scan 1-2 line lanjutan di bawahnya untuk memastikan suffix part number yang terpotong ikut tergabung penuh.
   - Contoh:
     - BAXVLPLG38802 + 0R -> "BAXVLPLG388020R"
     - HBGVLVLG2154 + 0001R -> "HBGVLVLG21540001R"
     - FRXVLIS24PFK0 + 100R -> "FRXVLIS24PFK0100R"
   - Jika urutan baca OCR menjadi:
       06
       BAXVLPLG38802
       0R
     maka:
     - inv_spart_item_no = "BAXVLPLG388020R"
   - Jangan ambil:
     - seq
     - customer PO number
     - model pendek di description seperti PLG-38-802
     - quantity
     - unit price
     - amount
   - Pastikan inv_spart_item_no tidak ada yang tertinggal

4. inv_description
   - Ambil deskripsi barang dari kolom Description.
   - Gabungkan seluruh line description item sampai sebelum item berikutnya atau sebelum line "P.O. NO:" berikutnya yang menandai group baru.
   - Masukkan spesifikasi barang yang memang bagian dari description.
   - Pada vendor VELO, description sering berupa beberapa line seperti:
     - nama barang
     - brand / VELO
     - model pendek
     - ukuran
     - material
     - warna
     - OEM PACKING
   - "OEM PACKING" dianggap bagian dari description dan boleh disertakan.
   - Jika ada line alphanumeric panjang tepat di bawah "P.O. NO:..." yang sebenarnya adalah part number item, jangan masukkan line itu ke inv_description.
   - inv_description dimulai setelah inv_spart_item_no selesai direkonstruksi penuh.
   - Jangan masukkan:
     - line "P.O. NO:..."
     - seq
     - part number, termasuk part number yang ikut terbaca di bawah PO line karena OCR / reading order
     - quantity
     - unit
     - unit price
     - amount
     - section title "BICYCLE PARTS"
   - Contoh hasil:
     - "BATTERY HOLDER DI2; VELO; PLG-38-802 VLD-II-1638 95.3*22.7MM ABS BLACK, W/M5*8MM INSERT 2PCS OEM PACKING"
     - "DOWN TUBE PROTECTOR; VELO; IS24PFK36 BLACK RUBBER TPR A70 COLLOSUS T DT SHUTLE PAD, W/POLYGON LOGO 140X53mm OEM PACKING"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Pada invoice VELO sampel, tidak ada gross weight per line item.
   - Karena itu:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Pada invoice VELO sampel, tidak ada gross weight per line item.
   - Karena itu:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil nilai quantity dari kolom Quantity.
   - Ambil angka numeriknya saja.
   - Contoh:
     - "36 PCS" -> 36
     - "17 PRS" -> 17
     - "40 SET" -> 40
     - "498 PCS" -> 498

8. inv_quantity_unit
   - Ambil unit yang menempel pada quantity di invoice.
   - Pada sampel VELO, unit yang muncul antara lain:
     - PCS
     - PRS
     - SET
   - Contoh:
     - "36 PCS" -> "PCS"
     - "17 PRS" -> "PRS"
     - "40 SET" -> "SET"

9. inv_unit_price
   - Ambil dari kolom Unit Price.
   - Hapus prefix mata uang seperti "USD".
   - Nilai harus numeric saja.
   - Contoh:
     - "USD 0.5800" -> 0.58
     - "USD 8.1000" -> 8.1
     - "USD 8.4200" -> 8.42

10. inv_amount
   - Ambil dari kolom Amount.
   - Hapus prefix mata uang seperti "USD".
   - Nilai harus numeric saja.
   - Contoh:
     - "USD 20.88" -> 20.88
     - "USD 137.70" -> 137.7
     - "USD 345.22" -> 345.22

"""