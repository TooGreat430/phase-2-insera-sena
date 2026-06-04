BAFANG_MOTOR_PROMPT = """

INVOICE (INV)

1. inv_customer_po_no:
   - Ekstrak dari kolom "PO".
   - Contoh: "43018071", "43018072".

2. inv_spart_item_no:
   - Ekstrak dari kolom "Customer Article No.".
   - Jangan ambil dari kolom "Item", "Model", atau "BF Article No."
   - Contoh:
     "BATBFEELMINI04-R"
     "BAXBFBTF291004-R"
     "BATBFHEGIIPRCS00-R"

3. inv_description:
   - Ekstrak dari kolom "Insera Description".
   - Gabungkan seluruh wrapped lines yang masih merupakan bagian dari deskripsi item.
   - Jangan sertakan Price, Quantity, Amount, Brand, atau PO.
   - Contoh hasil:
     "EEL-MINI battery casing, 36V CAN, 10.5Ah, 378Wh, 30 CELLS, EVE 3.5Ah cell, produced in China"

4. inv_gw & inv_gw_unit:
   - Isi null kecuali ada gross weight yang tertulis eksplisit pada invoice.

5. inv_quantity:
   - Ekstrak dari kolom "Quantity".
   - Contoh: "455", "700"

6. inv_quantity_unit:
   - Isi null kecuali ada unit quantity yang tertulis eksplisit pada baris item invoice.
   - Jangan mengasumsikan PCS/SET jika tidak tertulis.

7. inv_unit_price:
   - Ekstrak dari kolom "Price (USD)".
   - Ambil angka numeriknya saja. Jangan ambil simbol mata uangnya.
   - Contoh:
     "$106.10" -> 106.10
 
"""