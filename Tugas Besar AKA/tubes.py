import time
import matplotlib.pyplot as plt
from bisect import bisect_left, bisect_right

class Guitar:
    def __init__(self, brand, type_, price, series):
        self.brand = brand
        self.type = type_
        self.price = price
        self.series = series

    def __str__(self):
        return f"{self.brand} {self.type} ({self.series}) - Rp{self.price:,}"

# Fungsi untuk membangun hash map gitar berdasarkan merek
def build_brand_hash(guitars):
    brand_hash = {}
    for guitar in guitars:
        brand = guitar.brand.lower()
        if brand not in brand_hash:
            brand_hash[brand] = []
        brand_hash[brand].append(guitar)
    return brand_hash

# Fungsi iteratif untuk mencari gitar berdasarkan rentang harga
def search_by_price_binary_iterative(guitars, min_price, max_price):
    guitars = sorted(guitars, key=lambda x: x.price)  # Mengurutkan gitar berdasarkan harga
    prices = [guitar.price for guitar in guitars]
    start = bisect_left(prices, min_price)
    end = bisect_right(prices, max_price)
    return guitars[start:end]

# Fungsi rekursif untuk mencari gitar berdasarkan rentang harga
def search_by_price_binary_recursive(guitars, prices, min_price, max_price, start, end):
    if start >= end:
        return []

    mid = (start + end) // 2

    if prices[mid] < min_price:
        return search_by_price_binary_recursive(guitars, prices, min_price, max_price, mid + 1, end)
    elif prices[mid] > max_price:
        return search_by_price_binary_recursive(guitars, prices, min_price, max_price, start, mid)
    else:
        # Collect results in range
        results = []
        left = mid
        while left >= start and min_price <= prices[left] <= max_price:
            results.append(guitars[left])
            left -= 1

        right = mid + 1
        while right < end and min_price <= prices[right] <= max_price:
            results.append(guitars[right])
            right += 1

        return results

# Fungsi utama untuk memberikan rekomendasi
def recommend_guitars(guitars, brand_hash, min_price, max_price, guitar_type, brand, use_recursive=False):
    # Filter gitar berdasarkan harga menggunakan binary search
    guitars = sorted(guitars, key=lambda x: x.price)  # Mengurutkan gitar berdasarkan harga
    prices = [guitar.price for guitar in guitars]

    if use_recursive:
        filtered_guitars = search_by_price_binary_recursive(guitars, prices, min_price, max_price, 0, len(prices))
    else:
        filtered_guitars = search_by_price_binary_iterative(guitars, min_price, max_price)

    # Filter lebih lanjut berdasarkan tipe
    if guitar_type:
        filtered_guitars = [guitar for guitar in filtered_guitars if guitar.type.lower() == guitar_type.lower()]

    # Filter lebih lanjut berdasarkan merek menggunakan hash map
    if brand:
        brand = brand.lower()
        if brand in brand_hash:
            filtered_guitars = [guitar for guitar in filtered_guitars if guitar in brand_hash[brand]]
        else:
            filtered_guitars = []

    return filtered_guitars

# Fungsi untuk mengukur waktu eksekusi dan membandingkan performa
def measure_runtime(guitars, brand_hash, min_price, max_price, guitar_type, brand):
    runtimes_iterative = []
    runtimes_recursive = []

    # Iterasi untuk mengukur beberapa kali
    for _ in range(10):
        # Iterative runtime
        start_time = time.time()
        recommend_guitars(guitars, brand_hash, min_price, max_price, guitar_type, brand, use_recursive=False)
        end_time = time.time()
        runtimes_iterative.append(end_time - start_time)

        # Recursive runtime
        start_time = time.time()
        recommend_guitars(guitars, brand_hash, min_price, max_price, guitar_type, brand, use_recursive=True)
        end_time = time.time()
        runtimes_recursive.append(end_time - start_time)

    # Print runtime information
    print(f"Iterative time (avg): {sum(runtimes_iterative)/len(runtimes_iterative):.6f} seconds")
    print(f"Recursive time (avg): {sum(runtimes_recursive)/len(runtimes_recursive):.6f} seconds")

    return runtimes_iterative, runtimes_recursive

# Fungsi untuk membuat diagram garis
def plot_runtimes(runtimes_iterative, runtimes_recursive):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(runtimes_iterative) + 1), runtimes_iterative, marker='o', linestyle='-', color='b', label='Iterative')
    plt.plot(range(1, len(runtimes_recursive) + 1), runtimes_recursive, marker='o', linestyle='--', color='r', label='Recursive')
    plt.title('Running Time: Iterative vs Recursive')
    plt.xlabel('Run Index')
    plt.ylabel('Running Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

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

    # Membuat hash map untuk pencarian berdasarkan merek
    brand_hash = build_brand_hash(guitars)

    # Input parameter rekomendasi
    min_price = 2000000
    max_price = 10000000
    guitar_type = "Electric"
    brand = ""

    # Menampilkan rekomendasi gitar untuk pendekatan iteratif
    print("Recommended Guitars (Iterative):")
    recommended_iterative = recommend_guitars(guitars, brand_hash, min_price, max_price, guitar_type, brand, use_recursive=False)
    for guitar in recommended_iterative:
        print(guitar)

    # Menampilkan rekomendasi gitar untuk pendekatan rekursif
    print("\nRecommended Guitars (Recursive):")
    recommended_recursive = recommend_guitars(guitars, brand_hash, min_price, max_price, guitar_type, brand, use_recursive=True)
    for guitar in recommended_recursive:
        print(guitar)

    # Mengukur waktu eksekusi
    runtimes_iterative, runtimes_recursive = measure_runtime(guitars, brand_hash, min_price, max_price, guitar_type, brand)

    # Menampilkan diagram garis
    plot_runtimes(runtimes_iterative, runtimes_recursive)

if __name__ == "__main__":
    main()
