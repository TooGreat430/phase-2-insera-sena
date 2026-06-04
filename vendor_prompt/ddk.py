DDK_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: 
    - Ekstrak dari baris block header di dalam tabel yang mendahului grup line item. Baris ini memuat referensi teks "Customer P/O No." atau "Customer P/O No" (misalnya dari baris teks "S/C NO. DE20251014001 Customer P/O No. 45322397", ekstrak HANYA angka "45322397").
    - Terapkan logika Contextual Inheritance: Setiap line item yang posisinya berada di bawah baris block header tersebut otomatis mewarisi (inherit) nilai `inv_customer_po_no` dari block header terakhir di atasnya.
2. `inv_spart_item_no`: Ekstrak dari kolom "Item No.". Ambil string kode utama/model pada baris pertama (misalnya "D5090/VXTB708B9BA2MRSA23" atau "DGT-2400/2400-1/BB") dan abaikan kode internal di dalam tanda kurung pada baris bawahnya (misal "(SDLFMD50900005)").
3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari kolom "Description".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "Quantity" (misalnya dari "500 PCS" atau teks bertumpuk "PCS \\n 303", ambil angka murninya saja seperti 500 atau 303).
6. `inv_quantity_unit`: Ekstrak satuan kemasan dari string pada kolom "Quantity" (misalnya "PCS", "PRS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price".
8. `inv_amount`: 
    - Ekstrak nilai angka dari kolom "Amount" (hapus koma ribuan).
    - PENTING: Apabila sel pada kolom Amount bertuliskan teks "FOC" (Free of Charge), maka outputkan nilai `inv_amount` sebagai angka 0.

"""