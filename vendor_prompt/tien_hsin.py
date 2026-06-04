TIEN_HSIN_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari teks berawalan "P. O. NO" atau "P. O. NO:" yang berada di dalam blok deskripsi atau di atas/bawah nama barang. Ambil HANYA angka PO-nya saja (misalnya dari "P. O. NO 45321009", ekstrak "45321009").
2. `inv_spart_item_no`: Ekstrak dari kolom "Item/Part no.". Abaikan nomor urut baris (seperti 1, 43, 44) dan ambil murni kode alfanumerik part-nya saja (misalnya "CWSFSSH12001-R" atau "HDPFSAORBIT013-R").
3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari kolom "Description".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Quantity".
6. `inv_quantity_unit`: Ekstrak unit dari kolom "Quantity" (misalnya "SET" atau "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price" (hapus teks mata uang seperti USD).
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount" (hapus teks mata uang seperti USD dan koma ribuan).

"""