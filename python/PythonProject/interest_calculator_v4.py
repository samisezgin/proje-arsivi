import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def hesapla():
    for row in tree.get_children():
        tree.delete(row)

    try:
        anapara = float(entry_anapara.get())
        faiz_orani_girilen = float(entry_faiz.get())
        aylik_ek = float(entry_ek.get())
        ay_sayisi = int(entry_sure.get())

        # Faiz tipi (günlük / aylık / yıllık)
        faiz_tipi = combo_faiz_tipi.get()
        oran_tipi = combo_oran_tipi.get()

        # Yüzde / binde çevirimi
        if oran_tipi == "Yüzde (%)":
            oran = faiz_orani_girilen / 100
        else:
            oran = faiz_orani_girilen / 1000

        # Faiz tipine göre aylık orana dönüştür
        if faiz_tipi == "Günlük":
            aylik_faiz = (1 + oran) ** 30 - 1  # 30 günlük bileşik dönüşüm
        elif faiz_tipi == "Yıllık":
            aylik_faiz = (1 + oran) ** (1 / 12) - 1
        else:
            aylik_faiz = oran  # Aylık zaten doğrudan

        toplam = anapara
        toplam_kazanc = 0.0
        ay_list = []
        toplam_list = []

        for ay in range(1, ay_sayisi + 1):
            baslangic = toplam
            faiz_kazanci = baslangic * aylik_faiz
            toplam = baslangic + faiz_kazanci + aylik_ek
            toplam_kazanc += faiz_kazanci

            ay_list.append(ay)
            toplam_list.append(toplam)

            tree.insert(
                "",
                "end",
                values=(
                    ay,
                    f"{baslangic:,.2f} ₺",
                    f"{faiz_kazanci:,.2f} ₺",
                    f"{aylik_ek:,.2f} ₺",
                    f"{toplam:,.2f} ₺"
                ),
            )

        net_kazanc = toplam - (anapara + aylik_ek * ay_sayisi)
        lbl_sonuc.config(
            text=f"\nToplam Birikim: {toplam:,.2f} ₺\nToplam Faiz Kazancı: {toplam_kazanc:,.2f} ₺\nNet Kazanç: {net_kazanc:,.2f} ₺"
        )

        # Grafik
        plt.figure(figsize=(7, 4))
        plt.plot(ay_list, toplam_list, marker='o', color="#0077cc")
        plt.title("Aylara Göre Toplam Birikim Grafiği", fontsize=12)
        plt.xlabel("Ay", fontsize=11)
        plt.ylabel("Toplam Birikim (₺)", fontsize=11)
        plt.grid(True)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun!")

# === ARAYÜZ ===
root = tk.Tk()
root.title("Faizli Birikim Hesaplayıcı (Esnek Faiz Tipi)")
root.geometry("750x580")
root.resizable(False, False)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Girdi alanları
tk.Label(frame_inputs, text="Anapara (₺):").grid(row=0, column=0, padx=5, pady=3)
entry_anapara = tk.Entry(frame_inputs)
entry_anapara.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_inputs, text="Faiz Oranı:").grid(row=1, column=0, padx=5, pady=3)
entry_faiz = tk.Entry(frame_inputs, width=10)
entry_faiz.grid(row=1, column=1, padx=5, pady=3, sticky="w")

combo_oran_tipi = ttk.Combobox(frame_inputs, values=["Yüzde (%)", "Binde (‰)"], width=10, state="readonly")
combo_oran_tipi.grid(row=1, column=1, padx=(100, 5), pady=3)
combo_oran_tipi.current(0)

tk.Label(frame_inputs, text="Faiz Tipi:").grid(row=2, column=0, padx=5, pady=3)
combo_faiz_tipi = ttk.Combobox(frame_inputs, values=["Günlük", "Aylık", "Yıllık"], width=10, state="readonly")
combo_faiz_tipi.grid(row=2, column=1, padx=5, pady=3)
combo_faiz_tipi.current(1)

tk.Label(frame_inputs, text="Aylık Ek Ödeme (₺):").grid(row=3, column=0, padx=5, pady=3)
entry_ek = tk.Entry(frame_inputs)
entry_ek.grid(row=3, column=1, padx=5, pady=3)

tk.Label(frame_inputs, text="Süre (Ay):").grid(row=4, column=0, padx=5, pady=3)
entry_sure = tk.Entry(frame_inputs)
entry_sure.grid(row=4, column=1, padx=5, pady=3)

tk.Button(frame_inputs, text="Hesapla", command=hesapla, bg="#4CAF50", fg="white", width=15).grid(row=5, column=0, columnspan=2, pady=10)

# === TABLO ===
columns = ("Ay", "Dönem Başı", "Faiz Kazancı", "Ek Ödeme", "Dönem Sonu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)

tree.pack(pady=5)

lbl_sonuc = tk.Label(root, text="", font=("Arial", 11))
lbl_sonuc.pack(pady=10)

root.mainloop()
