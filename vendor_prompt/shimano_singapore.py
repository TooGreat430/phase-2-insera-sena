SHIMANO_SINGAPORE_PROMPT = """
INVOICE (INV)

Struktur umum invoice SHIMANO (SINGAPORE):
- Dokumen berjudul "*INVOICE*".
- Satu PDF bisa berisi banyak invoice berbeda seperti:
  - INS-...
  - INSPM-...
- Header utama line item:
  MARKS | DESCRIPTION | SPART / CPART | QTY & UNIT | UNIT PRICE (USD) | AMOUNT (USD)
- Dalam satu line item biasanya ada:
  1) product/material code di awal block, contoh:
     - 22E9901D036
     - 20RJ1480126
     - 239P2000356
  2) description multi-line
  3) SPART / CPART, contoh:
     - AMT401EJHFPRX085 / AMT401EJHFPRX085
     - ACSLG30010148 / ACSLG30010148
     - ARDTZ31AGSD / ARDTZ31AGSD
  4) quantity + unit
  5) marks block:
     - PT.IS
     - P/O No....
     - SURABAYA
     - optional PLT NO....
     - CTN NO....
- Pada vendor SHIMANO, item yang sama bisa muncul berulang sebagai beberapa printed row terpisah dengan CTN/PLT berbeda.
- Jika dokumen mencetaknya sebagai block/row terpisah, anggap itu item terpisah dan JANGAN merge hanya karena description atau spart sama.

1. inv_customer_po_no
   - Ambil dari line "P/O No." pada marks block item tersebut.
   - Ambil angka PO-nya saja.
   - Contoh:
     - "P/O No.45324353" -> inv_customer_po_no = "45324353"
     - "P/O No. 45322131" -> inv_customer_po_no = "45322131"
   - Jangan ambil:
     - invoice number seperti INS-2QB0542
     - LC number
     - CTN NO
     - PLT NO

2. inv_seq
   - Pada invoice SHIMANO sampel, tidak ada kolom seq numerik item yang tercetak jelas.
   - Product/material code seperti "22E9901D036" BUKAN seq numerik.
   - Karena itu:
     inv_seq = null
   - Jangan membuat nomor urut sendiri.

3. inv_spart_item_no
   - HANYA ambil dari kolom "SPART / CPART" pada row item yang sama.
   - JANGAN AMBIL dari kolom DESCRIPTION, meskipun ada kode alfanumerik yang terlihat jelas di sana.
   - JANGAN AMBIL product/material code di awal block description seperti:
     - 22E9901D036
     - 20RJ1480126
     - 239P2000356
     tapi ambil dari kolom "SPART / CPART"
   - inv_spart_item_no harus berasal dari kolom "SPART / CPART", bukan dari token pertama yang terbaca pada row.
   - Jika OCR membaca DESCRIPTION lebih dulu lalu SPART / CPART belakangan, tetap pilih value dari kolom "SPART / CPART".
   - Jika value pada kolom "SPART / CPART" berbentuk:
     - AMT401EJHFPRX085 / AMT401EJHFPRX085
     maka ambil 1 nilai spart saja:
     - "AMT401EJHFPRX085"
   - Jika kiri dan kanan berbeda, ambil value sebelah kiri slash sebagai inv_spart_item_no.
   - inv_spart_item_no tidak boleh diawali angka.
   - Jika candidate diawali angka, candidate tersebut PASTI SALAH untuk inv_spart_item_no dan harus ditolak.
   - Jika tidak ada bukti yang jelas pada kolom "SPART / CPART", isi "null".
   - Jangan fallback ke DESCRIPTION.

4. inv_description
   - Ambil deskripsi barang dari kolom DESCRIPTION saja.
   - Gabungkan seluruh line description item menjadi satu string utuh.
   - Jangan masukkan:
     - product/material code di awal row
     - SPART / CPART
     - PT.IS
     - P/O No.
     - SURABAYA
     - PLT NO.
     - CTN NO.
     - quantity
     - unit price
     - amount
   - Jika ada kata yang pecah karena line wrap / OCR yang sangat jelas, normalisasi seperlunya.
     Contoh:
     - "BLAC K" -> "BLACK"
     - "B ULK" -> "BULK"
     - "CO VER" -> "COVER"
   - Contoh hasil:
     - "DISC BRAKE ASSEMBLED SET/J-KIT; BL-MT401(L); BR-MT420(F); BLACK(BLACK LEVER); W/O ADAPTER; RESIN PAD(W/O FIN); 850MM HOSE(SM-BH90-SS BLACK); BULK"
     - "CASSETTE SPROCKET; CS-LG300-10; CUES; 10-SPEED; 11-13-15-17-20-23-28-34-41-48T; BULK"
     - "REAR DERAILLEUR; TZ-SERIES; RD-TZ31A; GS 6/7-SPEED; DIRECT ATTACHMENT; BULK"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Pada invoice SHIMANO sampel, gross weight hanya ada di total footer dokumen, bukan per line item.
   - Karena itu:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Pada invoice SHIMANO sampel, gross weight per line item tidak tersedia.
   - Karena itu:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil angka quantity dari kolom "QTY & UNIT".
   - Contoh:
     - "20 PCS" -> 20
     - "28 SET" -> 28
     - "2650 PCS" -> 2650

8. inv_quantity_unit
   - Ambil unit yang menempel pada quantity.
   - Pada sampel SHIMANO, unit yang muncul antara lain:
     - PCS
     - SET
   - Contoh:
     - "20 PCS" -> "PCS"
     - "28 SET" -> "SET"

9. inv_unit_price
   - Ambil dari kolom "UNIT PRICE (USD)".
   - Nilai harus numeric saja.
   - Contoh:
     - "29.2900" -> 29.29
     - "16.3300" -> 16.33
     - "1.8600" -> 1.86

10. inv_amount
   - Ambil dari kolom "AMOUNT (USD)".
   - Nilai harus numeric saja.
   - Contoh:
     - "585.8000" -> 585.8
     - "45903.6300" -> 45903.63
     - "1302.0000" -> 1302.0

"""