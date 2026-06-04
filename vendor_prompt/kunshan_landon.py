KUNSHAN_LANDON_PROMPT = """

CLUE PENTING:

URUTAN KOLOM PADA DOKUMEN INVOICE (INV) — DARI KIRI KE KANAN (9 kolom):
1. Marks
2. PO Number
3. Item
4. Material
5. Descriptions
6. Quantity
7. Unit
8. Unit Price
9. Amount

URUTAN KOLOM PADA DOKUMEN PACKING LIST (PL) — DARI KIRI KE KANAN (12 kolom):
1.  Marks
2.  PO Number
3.  Item
4.  Material
5.  Descriptions
6.  QTY        ← angka quantity baris
7.  UNIT       ← satuan quantity (PCS/SET/PCE/PRS/BT/dst)
8.  Packing    ← jumlah kemasan untuk baris ini (umumnya angka kecil: 1, 2, 3, dst)
9.  N.W        ← net weight baris
10. G.W        ← gross weight baris
11. VOL        ← volume baris
12. C/NO#      ← RENTANG nomor karton untuk baris ini (contoh: "1-10", "1-58", "1-280")

PERINGATAN PENTING TENTANG KOLOM C/NO# (kolom ke-12, paling kanan):
- C/NO# berisi RENTANG nomor karton dalam format "X-Y" (contoh: "1-10" artinya karton ke-1 sampai karton ke-10).
- C/NO# BUKAN jumlah kemasan dan TIDAK BOLEH digunakan untuk mengisi pl_package_count.
- C/NO# hanya muncul sekali untuk sekelompok baris yang berbagi rentang karton yang sama, jadi banyak baris memiliki C/NO# kosong.

INVOICE (INV):

1. `inv_customer_po_no`: 
    - Ekstrak HANYA dari kolom "PO Number" (Kolom ke-2 dari kiri, di sebelah kanan kolom "Marks" dan di sebelah kiri kolom "Item").
    - Value HARUS numerik 8 digit DAN HARUS DIMULAI dengan angka 4. (Bukan value numerik 1 digit seperti "8")
      Contoh: 45324149
    - Apabila pada kolom "PO Number" terdapat lebih dari 1 value dengan format seperti:
        PO Number: 45324149/CLM26030220
        Maka ekstrak value numerik sebelum tanda slash (/),
        Jadi inv_customer_po_no line tersebut = 45324149
    - DILARANG KERAS mengambil value PO Number selain dari kolom "PO Number".
    - DILARANG KERAS mengambil dari kolom "Item".

2. `inv_spart_item_no`:
    - Ekstrak HANYA dari kolom "Material" (Kolom ke-4 dari kiri, di sebelah kanan kolom 'Item' dan di sebelah kiri kolom 'Descriptions).
    - Value berupa alphanumerik (Bukan value numerik 1 digit seperti "8")
      Contoh: BSBSJBSL000009
    - DILARANG KERAS mengambil value dari kolom lain yang bukan "Material" 
    - Dilarang KERAS mengambil value dari kolom "Item" DAN "Description". 

3. `inv_description`: Ekstrak teks deskripsi dari kolom "DESCRIPTION".
4. `inv_gw` & `inv_gw_unit`: Biarkan null karena tidak terdapat informasi berat pada tingkat baris di invoice ini.
5. `inv_quantity`: Ekstrak nilai angka dari kolom "Q'TY" atau "Quantity".
6. `inv_quantity_unit`: Ekstrak dari kolom "UNIT" (misalnya "PCS" atau "SET"). Jika tergabung di kolom QTY, pisahkan dari angkanya.
7. `inv_unit_price`: Ekstrak nilai angka dari kolom "UNIT PRICE" (hapus simbol mata uang).
8. `inv_amount`: Ekstrak nilai angka dari kolom "AMOUNT" (hapus simbol mata uang).

"""