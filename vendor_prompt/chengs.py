CHENGS_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari baris teks berawalan "Customer P/O No." yang berada di dalam blok deskripsi. Nilainya memuat nomor referensi internal diikuti garis miring "/" lalu nomor PO utama (misalnya "Customer P/O No.C25-1155T/45318739"). Ambil HANYA angka PO yang terletak setelah garis miring "/" (misalnya ekstrak "45318739").
2. `inv_spart_item_no`:
   - PRIORITAS UTAMA (WAJIB): ambil dari baris penanda kode di bawah blok deskripsi yang diawali "** CODE:", "** Code:", "* CODE:", atau "CODE:". Ambil HANYA string kodenya, persis seperti tertulis (umumnya berakhiran "-R", contoh: dari "** CODE:SPXIMPLYX00000-R" ekstrak "SPXIMPLYX00000-R"; dari "* CODE:SDPTRYSP38J000-R" ekstrak "SDPTRYSP38J000-R"). Jika setelah kode ada catatan dalam kurung (mis. "(49020458:5)", "(CLM25120489)", "(DECAL SEPARATE)"), ABAIKAN bagian dalam kurung dan ambil kodenya saja.
   - Kode dari baris CODE inilah kode kanonik vendor yang dipakai untuk pencocokan PO. WAJIB diambil dari baris CODE secara KONSISTEN untuk SEMUA item yang memiliki baris CODE.
   - DILARANG KERAS mengambil nilai dari kolom "Item No." (kolom kiri di baris pertama item, contoh: "ADP-ORG26-SI L20 BK", "FRTATE48000000", "HBSTRJDST230A001-120", "IS23PFK32", "JD-SC35-318 SBBK-K") selama baris "** CODE"/"* CODE" tersedia. Nilai kolom "Item No." sering memuat varian/ukuran dan TIDAK cocok untuk pencocokan PO.
   - FALLBACK: hanya jika item BENAR-BENAR tidak memiliki baris "** CODE"/"* CODE" sama sekali (mis. baris CLAIM atau item tanpa CODE), barulah ambil nilai dari kolom "Item No.".
3. `inv_description`:
   - Ekstrak teks deskripsi spesifikasi barang dari kolom "Description" saja.
   - Baris pertama deskripsi berbagi satu baris dengan kolom "Item No." (kode di kiri) dan kolom Quantity/Unit/Price/Amount (di kanan). Ambil HANYA teks deskripsi di tengah: JANGAN awali deskripsi dengan token kode kolom "Item No." (contoh yang HARUS dibuang dari awal deskripsi: "JD-SC35-318 SBBK-K", "JD-0K-0004 ST", "E67 AL6061 BK"), dan JANGAN ikutkan angka Quantity/Unit/Price/Amount.
   - JANGAN sertakan baris referensi berikut: "Customer P/O No. ...", nomor Seq, baris "** CODE:"/"* CODE:"/"CODE:", baris "** BB NO. ...", baris "C/NO. ...", dan baris "** DRAWING ...".
   - Gabungkan sisa baris deskripsi spesifikasi menjadi satu nilai utuh.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "Quantity" (misalnya dari teks "98 GRO" atau "200 SET", ambil angka 98 atau 200).
6. `inv_quantity_unit`: Ekstrak satuan string dari kolom "Quantity" yang letaknya berdampingan dengan angka (misalnya "GRO", "SET", "PCE").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price".
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount" (hapus teks tajuk mata uang seperti "(NT$)" dan tanda koma ribuan).

"""