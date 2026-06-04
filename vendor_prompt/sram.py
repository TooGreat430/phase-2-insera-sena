SRAM_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: Ekstrak dari teks awalan "P.O.#" di kolom "DESCRIPTION". Ambil angka utamanya saja sebelum tanda kurung (misalnya dari "P.O.# 43018080 (251772921)", ekstrak "43018080").
2. `inv_spart_item_no`: Ekstrak kode Part Number (berformat angka dengan titik) dari baris pertama di blok deskripsi (misalnya "00.3018.201.000" atau "00.5318.033.000").
3. `inv_description`: Ekstrak teks deskripsi barang yang berada persis di bawah Part Number (misalnya "EP POWERPACK 1 BATTERY").
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom kuantitas di sebelah kanan deskripsi (misalnya "42").
6. `inv_quantity_unit`: Ekstrak unit dari kolom kuantitas (misalnya "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom 'Unit Price' di bawah teks FOB (misalnya dari "48.950", ambil 48.950).
8. `inv_amount`: Ekstrak nilai angka dari kolom 'Amount' di sebelah paling kanan / kolom mata uang USD (misalnya "2,055.90", hapus koma ribuan).

"""