import json

NAMA_FILE = "kb_kucing.json"


def muat_basis_pengetahuan(nama_file=NAMA_FILE):
    with open(nama_file, "r", encoding="utf-8") as file:
        return json.load(file)


def tanya_yes_no(pertanyaan):
    while True:
        jawaban = input(f"Apakah {pertanyaan} (y/n): ").strip().lower()
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


def tampilkan_kesimpulan(fakta, aturan_terpakai, basis_pengetahuan):
    if not aturan_terpakai:
        print("\nKesimpulan: Tidak ditemukan kesimpulan yang cocok (tidak ada aturan yang terpenuhi).")
    else:
        kesimpulan_list = []
        for id_aturan in aturan_terpakai:
            aturan = cari_aturan(id_aturan, basis_pengetahuan)
            if aturan and aturan["maka"] not in kesimpulan_list:
                kesimpulan_list.append(aturan["maka"])

        print(f"\nKesimpulan: {', '.join(kesimpulan_list)}")
        print("Alasan    :")
        for id_aturan in aturan_terpakai:
            aturan = cari_aturan(id_aturan, basis_pengetahuan)
            if aturan:
                kondisi = ", ".join(aturan.get("jika", []))
                print(f"            {aturan['maka']} ditandai dengan {kondisi}")

    batas = basis_pengetahuan.get("batas")
    if batas:
        print(f"\nCatatan: {batas}")

    daftar_sumber = []
    for aturan in basis_pengetahuan.get("aturan", []):
        for s in aturan.get("sumber", "").split(";"):
            s = s.strip()
            if s and s not in daftar_sumber:
                daftar_sumber.append(s)

    if daftar_sumber:
        print("Artikel:")
        for idx, sumber in enumerate(daftar_sumber, 1):
            print(f"         {idx}. {sumber}")


def main():
    basis_pengetahuan = muat_basis_pengetahuan()
    if not basis_pengetahuan:
        return

    fakta = kumpulkan_fakta(basis_pengetahuan)
    if not fakta:
        print("\nTidak ada fakta yang dipilih. Program berhenti.")
        return

    fakta, aturan_terpakai = forward_chaining(basis_pengetahuan, fakta)
    tampilkan_kesimpulan(fakta, aturan_terpakai, basis_pengetahuan)


if __name__ == "__main__":
    main()
