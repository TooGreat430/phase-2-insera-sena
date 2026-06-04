CHENGS_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari baris teks berawalan "Customer P/O No." yang berada di dalam blok deskripsi. Nilainya memuat nomor referensi internal diikuti garis miring "/" lalu nomor PO utama (misalnya "Customer P/O No.C25-1155T/45318739"). Ambil HANYA angka PO yang terletak setelah garis miring "/" (misalnya ekstrak "45318739").
2. `inv_spart_item_no`: Ekstrak dari teks kode unik barang. Bisa diambil dari baris "Item No." di atas deskripsi (misal "CWSSXD44A001-44T170") atau dari baris terbawah pada blok deskripsi yang diawali dengan "** CODE:" / "** Code:" (misalnya dari "** CODE:SPXIMPLYX00000-R", ekstrak string kodenya saja).
3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari blok kolom "Description". Abaikan baris referensi Customer P/O No, Seq, Item No, dan baris ** CODE di bawahnya.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "Quantity" (misalnya dari teks "98 GRO" atau "200 SET", ambil angka 98 atau 200).
6. `inv_quantity_unit`: Ekstrak satuan string dari kolom "Quantity" yang letaknya berdampingan dengan angka (misalnya "GRO", "SET", "PCE").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price".
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount" (hapus teks tajuk mata uang seperti "(NT$)" dan tanda koma ribuan).

"""