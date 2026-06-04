ROBERT_BOSCH_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak nilai string dari kolom "PO Number" pada baris bersangkutan (misalnya "43017912", "45319382", "43017951").
2. `inv_spart_item_no`: Ekstrak dari kolom "Customer Number" (misalnya "EB11.200.0KD", "EB12.200.0WF", "1270.020.330"). Abaikan string rumit pada kolom "Material Number".
3. `inv_description`: Ekstrak teks deskripsi barang dari kolom "Description". Jika teks terpecah ke dalam beberapa baris, gabungkan menjadi satu string utuh.
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena dokumen invoice ini tidak mencantumkan informasi berat pada tingkat baris item.
5. `inv_quantity`: Ekstrak nilai angka numerik dari kolom "Billed Qty" (misalnya "300", "400").
6. `inv_quantity_unit`: Ekstrak satuan kemasan dari kolom tanpa tajuk yang terletak tepat di sebelah kanan kolom "Billed Qty" (misalnya "PCS", "SET").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Net Value EUR" (hapus tanda koma jika ada).
8. `inv_amount`: Ekstrak nilai angka dari kolom "Amount EUR" (hapus tanda koma ribuan).

"""