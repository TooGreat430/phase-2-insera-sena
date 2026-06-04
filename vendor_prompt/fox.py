FOX_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Biarkan null karena tidak ada referensi PO Number secara eksplisit di level baris pada invoice ini.
2. `inv_spart_item_no`: Ekstrak dari kolom "Cust SKU" (misalnya "BAXFX82007177000-R").
3. `inv_description`: Ekstrak teks dari kolom "Description".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Qty" atau "Qty FOC".
6. `inv_quantity_unit`: Biarkan null karena tidak terdapat informasi unit quantity pada format invoice ini.
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Value" (hapus simbol mata uang).
8. `inv_amount`: Ekstrak nilai angka dari kolom "Ext Value" (hapus koma dan simbol mata uang).

"""