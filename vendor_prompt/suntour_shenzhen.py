SUNTOUR_SHENZEN_PROMPT = """

INVOICE (INV)

1. inv_customer_po_no:
   - Ekstrak dari kolom "P/O No./Description".
   - Pada format vendor ini, nomor PO adalah angka yang muncul setelah "Item No." dan sebelum kolom "Qty".
   - Contoh: "45324845".
   - Jangan ambil "Ref No".

2. inv_spart_item_no:
   - Ekstrak dari kolom "Item No.".
   - Contoh: "GSFXCM32DZ000036".

3. inv_description:
   - Prioritaskan deskripsi lengkap barang pada blok teks dalam tanda kurung di bagian bawah invoice, karena itu adalah deskripsi item paling lengkap.
   - Jika blok tanda kurung tidak ada, gabungkan seluruh teks deskripsi pada area "P/O No./Description" yang berada di bawah item utama sampai sebelum garis total.
   - Contoh format:
     "FORK SUSPENSION GSFXCM32DZ000036;SUNTOUR;SF23-XCM32DS;MATTEBLACKBLADE/CP STANCHION/MATTEBLACK CROWN;-;DISC PM160 QR/NUT,ALLOY BLADE/ALLOY CROWN, 27.5 THREADLESS 28(1-1/8") 255.00MMSTEEL STEERER 100.00 COIL W/ PRELOADADJUSTER - - W/ SEPARATEDECAL"

4. inv_gw & inv_gw_unit:
   - Isi null kecuali ada gross weight yang tertulis eksplisit pada invoice.

5. inv_quantity:
   - Ekstrak dari kolom "Qty".
   - Contoh: "3355".

6. inv_quantity_unit:
   - Ekstrak dari kolom "Unit".
   - Contoh: "SET".

7. inv_unit_price:
   - Ekstrak dari kolom "U/Price(USD)".
   - Contoh: "19".

"""