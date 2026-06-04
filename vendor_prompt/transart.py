TRANSART_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari sel gabungan bertumpuk pada kolom pertama yang memuat tajuk Order No. dan SN. Ambil HANYA rangkaian angka PO-nya saja (misalnya dari visual sel bertumpuk "1 \\n 45326930", ekstrak string "45326930").
2. `inv_spart_item_no`: Ekstrak dari sel gabungan pada kolom kedua yang memuat Item No. dan deskripsi. Ambil HANYA string kode barang uniknya (biasanya berakhiran teks "-R" atau berawalan huruf "Z" seperti "ZDMR25FSE2R0-R" atau "ZMRN22W000-R.").
3. `inv_description`: Ekstrak teks deskripsi spesifikasi stiker/decal dari sel gabungan pada kolom kedua (misalnya "DCMR25FSE2R0 MARIN 2025 FAIRFAX SE GOLD HRNT"). Pisahkan secara cermat dari baris string kode barang.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena dokumen invoice ini tidak mencantumkan informasi berat fisik pada tingkat baris item.
5. `inv_quantity`: Ekstrak murni nilai angka numerik dari kolom "Quantity" (misalnya "115", "6", "100").
6. `inv_quantity_unit`: Ekstrak satuan dari kolom "Unit" (misalnya "SET").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "UnitPrice" (hapus simbol mata uang seperti $).
8. `inv_amount`: 
    - Ekstrak nilai angka dari kolom "Amount" (hapus simbol mata uang seperti $ dan koma ribuan).
    - PENTING: Apabila sel pada kolom Amount bertuliskan teks string "F.O.C" (Free of Charge), maka outputkan nilai `inv_amount` sebagai angka 0.

"""