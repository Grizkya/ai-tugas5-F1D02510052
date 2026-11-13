import json

NAMA_FILE = "kb_kucing.json"

def muat_file_json(nama_file=NAMA_FILE):
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan.")
    except json.JSONDecodeError as e:
        print(f"Format JSON salah: {e}")
    return None


def validasi_file_json(basis_pengetahuan):
    """Memeriksa apakah setiap syarat aturan dikenal. Mengembalikan True jika valid."""
    pertanyaan = set(basis_pengetahuan.get("pertanyaan", []))
    hasil_aturan = {a["maka"] for a in basis_pengetahuan.get("aturan", [])}
    dikenal = pertanyaan | hasil_aturan
    valid = True

    for aturan in basis_pengetahuan.get("aturan", []):
        if not aturan.get("jika"):
            print(f"Peringatan: aturan {aturan['id']} tidak punya kondisi 'jika'.")
            valid = False
        for syarat in aturan.get("jika", []):
            if syarat not in dikenal:
                print(f"Peringatan: '{syarat}' di {aturan['id']} tidak ada di "
                      f"pertanyaan maupun hasil aturan lain.")
                valid = False
    return valid


def tanya_yes_no(pertanyaan):
    while True:
        jawaban = input(f"Apakah kucing menunjukkan gejala: {pertanyaan} (y/n): ").strip().lower()
        if jawaban in ("y", "yes"):
            return True
        if jawaban in ("n", "no"):
            return False
        print("Jawaban harus 'y' atau 'n'.")


def kumpulkan_fakta(basis_pengetahuan):
    judul = basis_pengetahuan.get("judul", "Diagnosis Awal Penyakit Umum pada Kucing").upper()
    print(f"===== {judul} =====")
    print("Jawab setiap pertanyaan dengan 'y' (yes) atau 'n' (no).\n")

    fakta = []
    for gejala in basis_pengetahuan.get("pertanyaan", []):
        if tanya_yes_no(gejala):
            fakta.append(gejala)

    return fakta


def cek_aturan(aturan, fakta):
    mode = aturan.get("mode", "dan").lower()
    kondisi = aturan.get("jika", [])

    if not kondisi:
        return False
    if mode == "dan":
        return all(syarat in fakta for syarat in kondisi)
    if mode == "atau":
        return any(syarat in fakta for syarat in kondisi)

    print(f"Mode '{mode}' tidak dikenal pada aturan {aturan.get('id')}.")
    return False


def cari_aturan(id_aturan, basis_pengetahuan):
    for aturan in basis_pengetahuan.get("aturan", []):
        if aturan["id"] == id_aturan:
            return aturan
    return None


def forward_chaining(basis_pengetahuan, fakta):
    aturan_list = basis_pengetahuan.get("aturan", [])
    fakta_set = set(fakta)
    aturan_terpakai = []
    siklus = 1

    print(f"\nFakta awal: {', '.join(fakta) if fakta else 'tidak ada'}\n")

    while True:
        aturan_aktif = None

        for aturan in aturan_list:
            if aturan["id"] in aturan_terpakai:
                continue
            if cek_aturan(aturan, fakta_set):
                aturan_aktif = aturan
                break

        if aturan_aktif is None:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break

        kesimpulan = aturan_aktif["maka"]
        aturan_terpakai.append(aturan_aktif["id"])

        if kesimpulan not in fakta_set:
            fakta.append(kesimpulan)
            fakta_set.add(kesimpulan)

        print(f"Siklus {siklus}: {aturan_aktif['id']} -> {kesimpulan}")
        siklus += 1

    return fakta, aturan_terpakai


def ambil_sumber(aturan):
    sumber = aturan.get("sumber", "")
    if isinstance(sumber, list):
        return [s.strip() for s in sumber if s.strip()]
    return [s.strip() for s in sumber.split(";") if s.strip()]


def tampilkan_kesimpulan(fakta, aturan_terpakai, basis_pengetahuan):
    if not aturan_terpakai:
        print("\nKesimpulan: Tidak ditemukan kesimpulan yang cocok (tidak ada aturan yang terpenuhi).")
    else:
        aturan_digunakan = [
            a for a in (cari_aturan(i, basis_pengetahuan) for i in aturan_terpakai) if a
        ]

        kesimpulan_list = []
        for aturan in aturan_digunakan:
            if aturan["maka"] not in kesimpulan_list:
                kesimpulan_list.append(aturan["maka"])

        print(f"\nKesimpulan: {', '.join(kesimpulan_list)}")

        # Alasan: hanya kondisi yang benar-benar terpenuhi
        print("\nAlasan    :")
        for aturan in aturan_digunakan:
            kondisi = ", ".join(k for k in aturan.get("jika", []) if k in fakta)
            print(f"            {aturan['maka']} ditandai dengan {kondisi}")

    batas = basis_pengetahuan.get("batas")
    if batas:
        print(f"\nCatatan: {batas}")

    # Artikel: hanya dari aturan yang terpakai
    daftar_sumber = []
    for id_aturan in aturan_terpakai:
        aturan = cari_aturan(id_aturan, basis_pengetahuan)
        if not aturan:
            continue
        for s in ambil_sumber(aturan):
            if s not in daftar_sumber:
                daftar_sumber.append(s)

    if daftar_sumber:
        print("Artikel:")
        for idx, sumber in enumerate(daftar_sumber, 1):
            print(f"         {idx}. {sumber}")


def main():
    basis_pengetahuan = muat_file_json()
    if not basis_pengetahuan:
        return

    if not validasi_file_json(basis_pengetahuan):
        print("Perbaiki basis pengetahuan terlebih dahulu.")
        return

    fakta = kumpulkan_fakta(basis_pengetahuan)
    if not fakta:
        print("\nTidak ada fakta yang dipilih. Program berhenti.")
        return

    fakta, aturan_terpakai = forward_chaining(basis_pengetahuan, fakta)
    tampilkan_kesimpulan(fakta, aturan_terpakai, basis_pengetahuan)


if __name__ == "__main__":
    main()
