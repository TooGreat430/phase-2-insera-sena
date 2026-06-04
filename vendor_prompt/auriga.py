AURIGA_PROMPT = """
INVOICE (INV)

Aturan umum ekstraksi vendor AURIGA:
- Vendor pada sampel adalah AURIGA (HUIZHOU) TECHNOLOGY CO., LTD.
- Dokumen invoice berjudul "Commercial Invoice".
- Dokumen packing list berjudul "PACKING LIST".
- Dokumen BL berjudul "BILL OF LADING".
- Dokumen COO berjudul "CERTIFICATE OF ORIGIN" / "Form RCEP".
- Jika field bertipe string dan tidak ada bukti yang jelas, isi "null".
- Jika field bertipe number dan tidak ada bukti yang jelas, isi null.
- Jangan mengisi field dari dokumen lain jika field tersebut harus berasal dari dokumen spesifik.
- Gabungkan teks yang terpotong baris / line wrap menjadi satu value yang utuh.
- Jika item terpotong ke halaman berikutnya, tetap anggap sebagai item yang sama, bukan item baru.
- Jangan halusinasi nilai yang tidak tercetak jelas pada dokumen.

Struktur umum invoice AURIGA:
- Header utama line item:
  ITEM NO. | PART NO. | PO No. | DESCRIPTION | Q'TY | PRICE | AMOUNT
- Pada vendor AURIGA, customer PO number tercetak jelas di kolom "PO No."
- Part number tercetak jelas di kolom "PART NO."
- Quantity pada invoice sering menempel dengan unit.
  Contoh:
  - 38.000PR
  - 12600.000PC
  - 353.000PC

1. inv_customer_po_no
   - Ambil customer PO number dari kolom "PO No."
   - Nilai yang diambil adalah nomor PO-nya saja.
   - Contoh:
     - "45324574" -> inv_customer_po_no = "45324574"
     - "45325077" -> inv_customer_po_no = "45325077"
   - Jangan ambil:
     - invoice no.
     - ref no.
     - BL no.
     - container no.
     - vessel / shipment no.

2. inv_seq
   - Ambil dari kolom "ITEM NO."
   - Ini adalah nomor urut item yang tercetak jelas di sisi kiri.
   - Nilai harus numeric.
   - Contoh:
     - 1
     - 12
     - 34
   - Jangan ambil quantity, price, amount, atau PO number sebagai inv_seq.

3. inv_spart_item_no
   - Ambil part number dari kolom "PART NO."
   - Part number pada vendor AURIGA biasanya berupa alphanumeric panjang.
   - Jika part number terpotong ke beberapa line, gabungkan menjadi satu string utuh tanpa spasi tambahan.
   - Contoh:
     - "BRLTTJL510TS01"
     - "BRKTTHDR285RR001"
     - "BRXTTTR160016003"
   - Jangan ambil:
     - seq
     - model pendek di description
     - quantity
     - unit price
     - amount

4. inv_description
   - Ambil deskripsi barang dari kolom "DESCRIPTION".
   - Gabungkan seluruh line description item sampai sebelum item berikutnya.
   - Masukkan spesifikasi barang yang memang bagian dari description.
   - Jangan masukkan:
     - seq
     - part number
     - PO no.
     - quantity
     - unit
     - unit price
     - amount
   - Contoh hasil:
     - "BRAKE LEVER; TEKTRO; JL-510TS;BLACK/SILVER LEVER;ALLOY BRACKET/ALLOY LEVER,LEFT/RIGHT,4 FINGERS,FOR LINEAR PULL BRAKES,FOR TWIST/REV OSHIFTER W/ TEKTRO LOGO"
     - "BRAKE SET; TEKTRO; MD-C510; BLACK; MECHANICAL FLAT MOUNT ALLOY W/O ROTOR ORGANIC COMPOUND PAD REAR W/O ADAPTOR WITH FLAT MOUNT BOLT M5X32MM"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Pada invoice AURIGA sampel, tidak ada gross weight per line item.
   - Karena itu:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Pada invoice AURIGA sampel, tidak ada gross weight unit per line item.
   - Karena itu:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil nilai quantity dari kolom "Q'TY".
   - Ambil angka numeriknya saja.
   - Unit jangan dimasukkan ke field ini.
   - Contoh:
     - "38.000PR" -> 38
     - "12600.000PC" -> 12600
     - "353.000PC" -> 353

8. inv_quantity_unit
   - Ambil unit yang menempel pada quantity di invoice.
   - Pada sampel AURIGA, unit yang muncul antara lain:
     - PR
     - PC
   - Contoh:
     - "38.000PR" -> "PR"
     - "12600.000PC" -> "PC"

9. inv_unit_price
   - Ambil dari kolom "PRICE".
   - Nilai harus numeric saja.
   - Hapus pemisah ribuan jika ada.
   - Contoh:
     - "16.19" -> 16.19
     - "18.00" -> 18
     - "102.13" -> 102.13

10. inv_amount
   - Ambil dari kolom "AMOUNT".
   - Nilai harus numeric saja.
   - Hapus pemisah ribuan jika ada.
   - Contoh:
     - "615.22" -> 615.22
     - "226,800.00" -> 226800
     - "19,323.22" -> 19323.22

"""