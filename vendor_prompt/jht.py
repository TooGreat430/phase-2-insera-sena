JHT_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari teks referensi awalan "PO:" yang berada sebelum/di atas list barang (misalnya "PO:45326462").
2. `inv_spart_item_no`: Ekstrak dari kolom ke-dua dari kiri (di sebelah kanan 'Shipping Marks' dan di sebelah kiri 'Description of Goods').
3. `inv_description`: 
    - Ekstrak deskripsi spesifikasi lengkap barang dari kolom "DESCRIPTION OF GOODS" (Abaikan yang sifatnya code, part number, atau serial number).
    - Contoh:
    DESCRIPTION OF GOODS:RIM, HLQC-GA63-1,  DOUBLE WALL BLACK  20*1.5 AV  32H W/ SAFETY LINE W/O DECAL,RIMJE20HLQCGA005
    Maka inv_description adalah DOUBLE WALL BLACK  20*1.5 AV  32H W/ SAFETY LINE W/O DECAL.
4. `inv_gw` & `inv_gw_unit`: Biarkan null kecuali dinyatakan secara eksplisit di baris tersebut.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Quantity".
6. `inv_quantity_unit`: Ekstrak unit dari kolom "Quantity" yang letaknya di samping angka (misalnya "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Unit Price" (secara posisi sejajar ke bawah).
8. `inv_amount`: 
    - Ekstrak nilai angka dari kolom "Amount" (secara posisi sejajar ke bawah).
    - Apabila terdapat value 'FOC' pada kolom "Amount", maka inv_amount HARUS 0.

"""