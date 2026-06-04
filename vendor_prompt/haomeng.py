HAOMENG_PROMPT = """
INVOICE (INV)

Struktur umum invoice HAOMENG:
- Ada grouping "P/O NO: xxxxxxxx"
- Setelah itu muncul beberapa line item
- Header utama line item umumnya:
  Item & Model No | Description | Qty | Unit Price | Amount
- Satu line item biasanya berbentuk:
  "ChainWheel set CODE:XXXXXXXXXXXX 30.00 SET 11.8000 354.00"
  lalu di bawahnya ada deskripsi model
  lalu "REMARK: ..."

1. inv_customer_po_no
   - Ambil dari "P/O NO:" terdekat yang menaungi line item tersebut.
   - Satu P/O NO berlaku untuk semua item di bawahnya sampai bertemu P/O NO berikutnya.
   - Format customer_po_no:
     - numerik saja
     - 8 digit
     - diawali angka 4
   - Contoh valid:
     - 45321768
     - 45321753
     - 45324085
   - Jangan ambil invoice number, PL number, BL number, atau nomor lain.

2. inv_spart_item_no
   - Ambil item code / part code untuk item invoice.
   - Prioritas pencarian:
     1) nilai setelah label "CODE:"
     2) jika tidak ada, cari part code paling jelas pada baris item / deskripsi
   - Untuk vendor HAOMENG, part code biasanya berada pada baris item pertama setelah "CODE:".
   - Contoh:
     - "ChainWheel set CODE:CWSPW244AF0007 ..."
       maka inv_spart_item_no = "CWSPW244AF0007"
   - Jangan ambil model deskripsi seperti "SOLID-244A-F..." sebagai item code.
   - Jangan ambil qty, unit, atau row range.

3. inv_description
   - Ambil deskripsi barang dari line item invoice.
   - Utamakan deskripsi model/barang yang berada di bawah baris pertama item.
   - Gabungkan seluruh baris deskripsi item sampai sebelum "REMARK:".
   - Jangan masukkan:
     - "ChainWheel set"
     - "CODE:..."
     - qty
     - unit
     - unit price
     - amount
     - remark
   - Contoh hasil:
     - "SOLID-244A-F,3/32*44T*170mm(JIS),CR S.A.SIL,CK S.PTD.SIL,CG AL SIL(AG37)"
     - "RMZ-MD25S-TT,32T*170MM,STEEL CHAINRING BLACK, ALLOY CRANK SAND BLACK ANO., W/LOGO, W/BSA BB, ONE-PIECE THRU AXLE CRANKSET"

4. inv_gw
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Jangan ambil dari packing list atau COO untuk mengisi inv_gw.

5. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Jika ada gross weight dan unitnya tercantum, ambil unitnya seperti "KG" / "KGS".

6. inv_quantity
   - Ambil nilai quantity line item pada invoice.
   - Ambil dari kolom Qty pada baris item invoice.
   - Contoh:
     - "30.00 SET" -> inv_quantity = 30
     - "398.00 PCS" -> inv_quantity = 398

7. inv_quantity_unit
   - Ambil unit quantity yang menempel pada Qty di invoice.
   - Contoh:
     - "30.00 SET" -> inv_quantity_unit = "SET"
     - "398.00 PCS" -> inv_quantity_unit = "PCS"

8. inv_unit_price
   - Ambil dari kolom Unit Price line item invoice.
   - Nilai harus numeric saja.
   - Contoh:
     - "11.8000" -> 11.8
     - "3.2500" -> 3.25

9. inv_amount
   - Ambil dari kolom Amount line item invoice.
   - Nilai harus numeric saja.
   - Contoh:
     - "354.00" -> 354
     - "1,293.50" -> 1293.5

"""