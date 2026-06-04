AFORGE_PROMPT = """
INVOICE (INV)

1. inv_customer_po_no:
   - Ekstrak dari kolom "PO/NO"[cite: 179].
   - Contoh: "45326683", "45324062", "45324727"[cite: 179].
   - Jika tertulis kode klaim seperti "CLM26010069", tetap ekstrak sebagai nomor referensi[cite: 180].

2. inv_spart_item_no:
   - Ekstrak dari kolom "Material"[cite: 179].
   - Contoh: "FRXPVWD5030300", "FREAF330600002"[cite: 179].

3. inv_description:
   - Gabungkan teks kategori barang (kolom ke-3, misal: "FRAME PART") dengan teks di kolom "DESCRIPTION" (kolom ke-4)[cite: 179].
   - Contoh: "FRAME PART 50303-01" atau "FRAME TUBING IS20PTT08 650L"[cite: 179, 180].
   - Sertakan teks Mandarin jika ada untuk kelengkapan deskripsi[cite: 179].

4. inv_gw & inv_gw_unit:
   - Isi null karena berat kotor tidak dirinci per baris pada tabel invoice ini[cite: 179, 180, 181].

5. inv_quantity:
   - Ekstrak dari kolom "QUANTITY"[cite: 179].
   - Contoh: "532", "250", "1"[cite: 179, 180].

6. inv_quantity_unit:
   - Ekstrak dari kolom "UNIT"[cite: 179].
   - Contoh: "PCS", "SET"[cite: 179, 180].

7. inv_unit_price:
   - Ekstrak dari kolom "UNIT PRICE (USD)"[cite: 179].
   - Jika tertulis "FOC", isi dengan 0[cite: 180, 181].

"""