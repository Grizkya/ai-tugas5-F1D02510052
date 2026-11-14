Nama    : Ghaitsa Rizky Amalia
NIM     : F1D02510052

# Sistem Pakar Diagnosis Awal Penyakit Umum Pada Kucing

Sistem pakar sederhana untuk memberikan dugaan awal mengenai penyakit yang biasa terjadi pada kucing seperti jamur kulit, flu kucing, cacingan berdasarkan gejala yang akan dijawab oleh pengguna. Menggunakan bahasa python 3.12.11 dengan library bawaan json.

## A. Cara menjalankan program

1. Simpan "kb_kucing.json" dan "kucing.py" di folder yang sama
2. Jalankan perintah

```bash
python kucing.py
```

3. Jawab pertanyaan dengan `y` (ya) atau `n` (tidak). Setelah itu program menampilkan proses inferensi per siklus, kesimpulan, alasan, catatan batas, dan artikel rujukan.

## B. Daftar Sumber

| No | Judul | Penerbit | URL | Tanggal akses |
|---|---|---|---|---|
| 1 | Ringworm in Cats | VCA Animal Hospitals | https://vcahospitals.com/know-your-pet/ringworm-in-cats | 11 November 2026 |
| 2 | Feline Upper Respiratory Infection | VCA Animal Hospitals | https://vcahospitals.com/know-your-pet/feline-upper-respiratory-infection | 11 November 2026 |
| 3 | Gastrointestinal Parasites of Cats | Cornell Feline Health Center | https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/gastrointestinal-parasites-cats | 11 November 2026 |

## C. Tabel Aturan

Mode `dan` berarti semua kondisi harus terpenuhi. Mode `atau` berarti cukup salah satu kondisi.
 
| ID | Mode | Jika | Maka | Sumber |
|---|---|---|---|---|
| R1 | dan | rontok bulu berbentuk bulat; kulit bersisik; kulit kemerahan di area rontok | jamur kulit (ringworm) | 1 |
| R2 | dan | jamur kulit (ringworm); sering menggaruk hingga luka | risiko infeksi kulit sekunder | 1 |
| R3 | dan | bersin-bersin; keluar cairan dari mata; hidung berlendir; nafsu makan menurun | flu kucing | 2 |
| R4 | dan | perut buncit; bulu kusam; berat badan turun meski makan banyak | cacingan | 3 |
| R5 | atau | sesak napas; feses berdarah | perlu pemeriksaan dokter hewan | 2, 3 |
 
Catatan: kesimpulan R1 ("jamur kulit (ringworm)") menjadi syarat R2, sehingga terbentuk rantai inferensi R1 → R2.

## D. Metode yang digunakan

Metode yang digunakan pada program ini adalah **Forward Chaining (FC)** untuk menghasilkan dugaan awal penyakit pada kucing. Forward Chaining (FC) lebih sesuai karena, 

1. Pengguna memulai dari data berupa gejala tanpa mengetahui penyakitnya, sehingga sistem dapat menarik kesimpulan berdasarkan fakta yang tersedia. 
2. FC memungkinkan inferensi berantai, seperti R1 → R2, ketika hasil aturan sebelumnya menjadi syarat aturan berikutnya. 
3. Setiap aturan hanya digunakan sekali sehingga proses dijamin berhenti.

## E. Kasus Uji

1. Kasus menghasilkan kesimpulan
<img width="1292" height="578" alt="kasus_rantai_aturan" src="https://github.com/user-attachments/assets/7959d440-a93c-4be7-9bbe-0fd40afd407f" />

2. Kasus menghasilkan kesimpulan
<img width="1150" height="592" alt="kasus_mode_atau" src="https://github.com/user-attachments/assets/25f0b558-aedc-4c2c-b5fc-f0ace706aa01" />

3. Kasus menghasilkan kesimpulan
<img width="1140" height="762" alt="semua_fakta_dipilih" src="https://github.com/user-attachments/assets/3274e26b-0aaa-48e4-84bd-7da8d3a5a8bb" />

4. Kasus tidak ada aturan terpenuhi
<img width="1158" height="550" alt="tidak_ada_aturan_terpenuhi" src="https://github.com/user-attachments/assets/cbca1081-c1aa-4f44-9a1a-f155ab59b364" />

5. Kasus tidak ada fakta yang dipilih
<img width="736" height="396" alt="tidak_ada_fakta_dipilih" src="https://github.com/user-attachments/assets/b61d2228-b3a9-4b82-a1f1-4c587811de4c" />

## F. Batas Keberlakuan

Sistem ini menggunakan pengetahuan umum yang bersumber dari artikel kesehatan kucing yang diterbitkan oleh VCA Animal Hospitals dan Cornell Feline Health Center, serta hanya ditujukan untuk memberikan dugaan awal terhadap masalah kesehatan kucing berdasarkan gejala yang dipilih pengguna. Sistem ini berlaku untuk kondisi umum seperti jamur kulit (ringworm), flu kucing, dan cacingan; hasilnya bukan diagnosis medis, bukan keputusan akhir, dan tidak menggantikan pemeriksaan, pemeriksaan laboratorium, maupun nasihat dokter hewan. Jika kucing menunjukkan gejala serius seperti sesak napas, tidak mau makan, sangat lemas, muntah terus-menerus, atau feses berdarah, segera bawa kucing ke dokter hewan.

## G. Penggunaan Alat Bantu AI

Dalam mengerjakan tugas ini saya menggunakan Perplexity dan Claude sebagai alat bantu. Perplexity digunakan untuk mencari artikel yang berhubungan dengan penyakit umum pada kucing dan penyusunan file json. Claude digunakan untuk membantu memperbaiki kesalahan dan kekurangan program.
