TANGSHAN_JINHENGTONG_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari kolom "PO No.".
2. `inv_spart_item_no`: Ekstrak dari kolom "Material".
3. `inv_description`: Ekstrak dari kolom "Description".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak dari kolom "qty".
6. `inv_quantity_unit`: Ekstrak dari kolom "unit" (misalnya "SET" atau "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price" (hapus simbol mata uang seperti $).
8.  `inv_amount`: Ekstrak nilai angka dari kolom "Amount" (hapus koma dan simbol mata uang).

"""