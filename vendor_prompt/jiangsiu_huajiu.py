JIANGSU_HUAJIU_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari kolom "ORDER NO" atau "订单号".
2. `inv_spart_item_no`:
    - Informasi mengenai inv_spart_item_no terdapat pada kolom "DESCRIPTION" atau "货物名称", terletak pada bagian paling kanan ATAU ke-2 dari kanan yang dipisahkan oleh ',' atau ';'.
    - Contoh:
    Jika pada kolom "DESCRIPTION": NIPPLE BRASS;MEILE;-;-;-;-;14GX14MM
    Maka inv_spart_item_no adalah 14GX14MM.

    Jika pada kolom "DESCRIPTION": SPOKE;MEILE;14G;SILVER;SPOKE:STAINLESS;-;14GX232MM,NIPPLE:W/O NIPPLE
    Maka inv_spart_item_no adalah 14GX232MM.

3. `inv_description`: Ekstrak teks deskripsi spesifikasi barang dari kolom "DESCRIPTION" atau "货物名称".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "QUANTITY" atau "数量".
6. `inv_quantity_unit`: Ekstrak dari kolom "UNIT" atau "单位" (misalnya "GRO").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "UNIT PRICE" atau "单价" (hapus simbol mata uang seperti $).
8. `inv_amount`: Ekstrak nilai angka dari kolom "AMOUNT" atau "金额" (hapus koma dan simbol mata uang).

"""