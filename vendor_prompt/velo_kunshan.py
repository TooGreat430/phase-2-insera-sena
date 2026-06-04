VELO_KUNSHAN_PROMPT = """
INVOICE (INV)

Struktur umum invoice VELO KUNSHAN:
- Vendor: VELO CYCLE(KUNSHAN) CO., LTD.
- Ada grouping "P.O. NO:45322815" atau format serupa.
- Header utama line item:
  Item/Part no. | Description | Quantity | Unit Price | Amount
- Pada vendor ini, ada angka item number tercetak sebelum part number, misalnya:
  30
  SDLVL1A866000
  1
- Dalam kasus seperti itu, angka paling atas adalah nomor item, sedangkan part number harus digabung dari baris-baris code di bawahnya.
- Contoh:
  30
  SDLVL1A866000
  1
  maka:
  - inv_seq = 30
  - inv_spart_item_no = SDLVL1A8660001
- Contoh lain:
  HBGVL519AD200
  3
  maka inv_spart_item_no = HBGVL519AD2003
- Contoh lain:
  SDLVLVL514400
  001
  maka inv_spart_item_no = SDLVLVL514400001

1. inv_customer_po_no
   - Ambil dari "P.O. NO:" terdekat yang menaungi line item tersebut.
   - Satu P.O. NO berlaku untuk semua item di bawahnya sampai bertemu P.O. NO berikutnya.
   - Pada vendor VELO, customer PO number berupa angka 8 digit, misalnya:
     - 45322815
     - 45322816
     - 45323076
     - 45323434
   - Jangan ambil invoice number 80010947, BL number, Ref.#, atau nomor lain.

2. inv_seq
   - Gunakan nomor item yang tercetak pada dokumen invoice.
   - Pada vendor VELO, nomor item tidak selalu berurutan 1,2,3..., tetapi mengikuti nomor asli dokumen seperti:
     - 30
     - 40
     - 70
     - 71
     - 90
     - 132
   - Gunakan angka itu apa adanya sebagai inv_seq.
   - Jangan hitung ulang dari atas ke bawah.

3. inv_spart_item_no
   - Ambil dari kolom "Item/Part no."
   - Pada vendor VELO, part number adalah product code utama dan TIDAK memakai label CODE:.
   - Jika part number terpotong ke beberapa baris, gabungkan semua fragmen yang masih merupakan bagian dari code.
   - Contoh:
     - SDLVL1A866000 + 1 -> SDLVL1A8660001
     - SDLVLVL1C2800 + 2 -> SDLVLVL1C28002
     - HBGVL519AD200 + 3 -> HBGVL519AD2003
     - HBGVL31146003 + 5 -> HBGVL311460035
     - SDLVLVL614200 + 4 -> SDLVLVL6142004
   - Jangan masukkan inv_seq ke dalam part number.
   - Jangan ambil model description seperti VL-1A866 atau VLG-311D2 sebagai inv_spart_item_no jika item/part no sudah ada.

4. inv_description
   - Ambil deskripsi barang dari item invoice.
   - Deskripsi dimulai setelah item/part no dan berlanjut ke baris-baris spesifikasi di bawahnya.
   - Gabungkan seluruh baris deskripsi item sampai sebelum item berikutnya atau sebelum P.O. NO berikutnya.
   - Jangan masukkan:
     - inv_seq
     - item/part no
     - quantity
     - unit
     - unit price
     - amount
   - Pada vendor VELO, value seperti "2024" atau "2020" yang muncul di akhir blok deskripsi tetap dianggap bagian dari description jika memang berada di area deskripsi item.
   - Contoh hasil:
     - "SADDLE;VELO;VL-1A866;BLACK/BLACK;NP1 BLACK NYLON FIBER INJECTION BASE BLACK GUARD, W/O ELASTOMER CR-MO BLACK RAIL, W/O CLAMP 243*155MM,W/LOGO W/LINC AND FLUX2 LOGO 2024"
     - "HANDLE GRIP VELO VLG-311D2 L:130/130MM. CLOSE END AT RUBBER/GEL. ALL BLACK OEM PACKING 2020"

5. inv_gw
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Pada dokumen invoice VELO yang tersedia, tidak ada gross weight per line item.
   - Karena itu, untuk vendor VELO:
     inv_gw = "null"

6. inv_gw_unit
   - HANYA boleh diambil dari invoice.
   - Jika invoice tidak menyediakan gross weight per line item, isi "null".
   - Pada dokumen invoice VELO yang tersedia, tidak ada gross weight per line item.
   - Karena itu, untuk vendor VELO:
     inv_gw_unit = "null"

7. inv_quantity
   - Ambil dari kolom Quantity pada line item invoice.
   - Contoh:
     - 45 PCS -> inv_quantity = 45
     - 166 PRS -> inv_quantity = 166
     - 4,000 PRS -> inv_quantity = 4000

8. inv_quantity_unit
   - Ambil unit quantity yang menempel pada Quantity di invoice.
   - Pada vendor VELO, unit yang umum muncul:
     - PCS
     - PRS
   - Contoh:
     - 45 PCS -> inv_quantity_unit = "PCS"
     - 166 PRS -> inv_quantity_unit = "PRS"

9. inv_unit_price
   - Ambil dari kolom Unit Price.
   - Nilai harus numeric saja.
   - Hilangkan koma ribuan jika ada.
   - Contoh:
     - USD 5.2500 -> 5.25
     - USD 1.0500 -> 1.05
     - USD 0.9500 -> 0.95

10. inv_amount
   - Ambil dari kolom Amount.
   - Nilai harus numeric saja.
   - Hilangkan koma ribuan jika ada.
   - Contoh:
     - USD 236.25 -> 236.25
     - USD 3,800.00 -> 3800
     - USD 1,293.50 -> 1293.5

"""