SHIMANO_INC_PROMPT = """
INVOICE (INV):
1. `inv_customer_po_no`: - Ekstrak dari teks "P/O No." yang berada di dalam blok "MARKS NOS" di sebelah kiri (misalnya "45320517").
                         - Jika inv_customer_po_no tidak ditemukan, gunakan nilai terakhir yang valid sebelumnya (backward lookup). Jangan pernah mengambil nilai dari setelahnya (forward lookup).
2. `inv_spart_item_no`: Ekstrak nilai teks setelah kata "PART#" atau S.PART# di dalam blok deskripsi (misalnya "KU60302DLF6RX100" atau "KSMMAR160DDB").
3. `inv_description`: Ekstrak teks deskripsi barang utama (misalnya "DISC BRAKE ASSEMBLED SET..."). Abaikan teks PART# atau keterangan detail lain di bawahnya.
4. `inv_gw` & `inv_gw_unit`:
    - Ekstrak nilai angka total dari kolom "Gross Weight" pada baris atas untuk line item tersebut (misalnya dari "14.40Kg", ekstrak 14.40 untuk gw dan "Kg" untuk unit).
    - Apabila pada 1 line item terdapat beberapa baris dengan kolom "Gross Weight" yang terisi, maka jumlahkan semua nilai angka tersebut untuk mendapatkan `inv_gw`.
5. `inv_quantity`: Ekstrak angka dari kolom "Quantity" yang ditandai dengan clue "TOTAL". Apabila terdapat beberapa baris dengan clue "TOTAL", maka jumlahkan semua nilai angka pada line item tersebut untuk mendapatkan `inv_quantity`.
6. `inv_quantity_unit`: Ekstrak unit dari kolom "Quantity Unit" (misalnya "PCS").
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "Amount Unit Price" pada baris bawah yang diawali dengan simbol "@" (misalnya dari "@JPY75", ekstrak 75).
8. `inv_amount`: 
- Ekstrak nilai angka dari kolom "Amount Unit Price" pada baris atas yang tidak memiliki simbol "@" (misalnya dari "JPY69,600", ekstrak 69600).

"""