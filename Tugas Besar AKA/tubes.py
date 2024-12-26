class Guitar:
    def __init__(self, brand, type_, price, series):
        self.brand = brand
        self.type = type_
        self.price = price
        self.series = series

# Fungsi untuk mencari gitar berdasarkan rentang harga
def search_by_price(guitars, min_price, max_price):
    return [guitar for guitar in guitars if min_price <= guitar.price <= max_price]

# Fungsi untuk memfilter gitar berdasarkan merek
def filter_by_brand(guitars, brand):
    return [guitar for guitar in guitars if guitar.brand.lower() == brand.lower()]

# Fungsi untuk memfilter gitar berdasarkan tipe
def filter_by_type(guitars, guitar_type):
    return [guitar for guitar in guitars if guitar.type.lower() == guitar_type.lower()]

# Fungsi utama untuk memberikan rekomendasi
def recommend_guitars(guitars, min_price, max_price, guitar_type, brand):
    # Filter gitar berdasarkan harga
    filtered_guitars = search_by_price(guitars, min_price, max_price)

    # Filter lebih lanjut berdasarkan tipe
    if guitar_type:
        filtered_guitars = filter_by_type(filtered_guitars, guitar_type)

    # Filter lebih lanjut berdasarkan merek
    if brand:
        filtered_guitars = filter_by_brand(filtered_guitars, brand)

    return filtered_guitars

def main():
    # Data contoh
    guitars = [
        Guitar("Yamaha", "Acoustic", 1500000, "F310"),
        Guitar("Fender", "Electric", 8000000, "Stratocaster"),
        Guitar("Gibson", "Electric", 16000000, "Les Paul Standart"),
        Guitar("Squier", "Electric", 5000000, "Telecaster"),
        Guitar("Yamaha", "Electric", 2500000, "Pacifica PAC112J"),
        Guitar("Ibanez", "Acoustic", 3500000, "Gio GRG120QASP"),

    ]

    # Input parameter rekomendasi
    min_price = int(input("Masukkan rentang harga minimum: "))
    max_price = int(input("Masukkan rentang harga maksimum: "))
    guitar_type = input("Masukkan tipe gitar (Acoustic/Electric atau kosong untuk semua): ").strip()
    brand = input("Masukkan merek gitar (atau kosong untuk semua): ").strip()

    # Mendapatkan rekomendasi
    recommendations = recommend_guitars(guitars, min_price, max_price, guitar_type, brand)

    # Menampilkan hasil rekomendasi
    if recommendations:
        print("Rekomendasi Gitar:")
        for guitar in recommendations:
            print(f"Merek: {guitar.brand}, Tipe: {guitar.type}, Seri: {guitar.series}, Harga: Rp {guitar.price}")
    else:
        print("Tidak ada gitar yang cocok dengan kriteria Anda.")

if __name__ == "__main__":
    main()
