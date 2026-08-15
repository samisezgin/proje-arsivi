# faiz_hesaplayici_full.py
import os
import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Paket kontrolü (pandas, matplotlib)
try:
    import pandas as pd
except Exception as e:
    tk.Tk().withdraw()
    messagebox.showerror(
        "Eksik kütüphane",
        "Bu uygulama 'pandas' kütüphanesine ihtiyaç duyar.\n\nLütfen terminalde çalıştırın:\n\npip install pandas openpyxl matplotlib"
    )
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
except Exception as e:
    tk.Tk().withdraw()
    messagebox.showerror(
        "Eksik kütüphane",
        "Bu uygulama 'matplotlib' kütüphanesine ihtiyaç duyar.\n\nLütfen terminalde çalıştırın:\n\npip install matplotlib pandas openpyxl"
    )
    sys.exit(1)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def hesapla():
    # Tree temizle
    for row in tree.get_children():
        tree.delete(row)

    # Değerleri al
    try:
        anapara = float(entry_anapara.get())
        faiz_giren = float(entry_faiz.get())
        ek_odem = float(entry_ek.get())
        sure_ay = int(entry_sure.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun (sayısal değerler).")
        return

    # Oran tipi (% veya ‰)
    oran_tipi = combo_oran_tipi.get()  # "Yüzde (%)" veya "Binde (‰)"
    if oran_tipi == "Yüzde (%)":
        oran = faiz_giren / 100.0
    else:
        oran = faiz_giren / 1000.0

    # Faiz tipi -> aylık orana çevir
    faiz_tipi = combo_faiz_tipi.get()  # "Günlük", "Aylık", "Yıllık"
    if faiz_tipi == "Günlük":
        # Günlük oranı aylığa yaklaşık dönüştür: (1+günlük)**30 - 1
        aylik_oran = (1.0 + oran) ** 30.0 - 1.0
    elif faiz_tipi == "Yıllık":
        # Yıllık oranı aylığa dönüştür: (1+yıllık)^(1/12) - 1
        aylik_oran = (1.0 + oran) ** (1.0 / 12.0) - 1.0
    else:  # Aylık
        aylik_oran = oran

    # Hesaplama döngüsü
    ay_list = []
    baslangic_list = []
    faiz_kazanci_list = []
    ek_list = []
    donem_sonu_list = []

    toplam = anapara
    toplam_faiz_kazanci = 0.0

    for ay in range(1, sure_ay + 1):
        baslangic = toplam
        faiz_kazanci = baslangic * aylik_oran
        toplam = baslangic + faiz_kazanci + ek_odem

        ay_list.append(ay)
        baslangic_list.append(baslangic)
        faiz_kazanci_list.append(faiz_kazanci)
        ek_list.append(ek_odem)
        donem_sonu_list.append(toplam)

        toplam_faiz_kazanci += faiz_kazanci

        # Tree'ye ekle (formatlı gösterim)
        tree.insert(
            "",
            "end",
            values=(
                ay,
                f"{baslangic:,.2f} ₺",
                f"{faiz_kazanci:,.2f} ₺",
                f"{ek_odem:,.2f} ₺",
                f"{toplam:,.2f} ₺",
            ),
        )

    net_kazanc = toplam - (anapara + ek_odem * sure_ay)

    lbl_sonuc.config(
        text=(
            f"Toplam Birikim: {toplam:,.2f} ₺    |    "
            f"Toplam Faiz Kazancı: {toplam_faiz_kazanci:,.2f} ₺    |    "
            f"Net Kazanç: {net_kazanc:,.2f} ₺"
        )
    )

    # DataFrame oluştur (ham sayısal veriler excel için)
    df = pd.DataFrame({
        "Ay": ay_list,
        "Dönem Başı": baslangic_list,
        "Faiz Kazancı": faiz_kazanci_list,
        "Ek Ödeme": ek_list,
        "Dönem Sonu": donem_sonu_list
    })

    # Klasör yapısı: All_Results/YYYYMMDD_HH-MM-SS/
    base_folder = os.path.join(os.getcwd(), "All_Results")
    ensure_dir(base_folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    run_folder = os.path.join(base_folder, timestamp)
    ensure_dir(run_folder)

    # Excel kaydet
    excel_path = os.path.join(run_folder, "calculation.xlsx")
    try:
        # Ham sayısal değerleri kaydet (index False)
        df.to_excel(excel_path, index=False, engine="openpyxl")
    except Exception as e:
        messagebox.showerror("Kaydetme Hatası", f"Excel kaydederken hata: {e}")
        return

    # Grafik çizimi ve kaydetme
    try:
        plt.figure(figsize=(8, 4.5))
        # x: ay, y: dönem sonu toplam
        plt.plot(ay_list, donem_sonu_list, marker="o", linewidth=2)
        plt.title("Aylara Göre Toplam Birikim")
        plt.xlabel("Ay")
        plt.ylabel("Toplam Birikim (₺)")
        plt.grid(True)

        # Y eksenini insan okunur formatta (thousands separator, 2 decimal)
        formatter = FuncFormatter(lambda x, pos: f"{x:,.2f}")
        plt.gca().yaxis.set_major_formatter(formatter)

        plt.tight_layout()

        png_path = os.path.join(run_folder, "growth_chart.png")
        plt.savefig(png_path, dpi=150)
        # Göster (kullanıcıya görüntü sunmak için)
        plt.show()
        plt.close()
    except Exception as e:
        messagebox.showerror("Grafik Hatası", f"Grafik oluştururken hata: {e}")
        return

    # Başarılı mesajı (kaydedilen dosyaların yolunu göster)
    messagebox.showinfo(
        "Kaydetme Tamamlandı",
        f"Hesaplama sonuçları kaydedildi:\n\nKlasör: {run_folder}\n\nİçerik:\n - calculation.xlsx\n - growth_chart.png"
    )


# === ARAYÜZ ===
root = tk.Tk()
root.title("Faizli Birikim Hesaplayıcı - Full")
root.geometry("820x620")
root.resizable(False, False)

# Üst giriş çerçevesi
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=12)

# Anapara
tk.Label(frame_inputs, text="Anapara (₺):").grid(row=0, column=0, padx=6, pady=4, sticky="w")
entry_anapara = tk.Entry(frame_inputs, width=18)
entry_anapara.grid(row=0, column=1, padx=6, pady=4)

# Faiz oranı
tk.Label(frame_inputs, text="Faiz Oranı:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
entry_faiz = tk.Entry(frame_inputs, width=12)
entry_faiz.grid(row=1, column=1, padx=(6,0), pady=4, sticky="w")

combo_oran_tipi = ttk.Combobox(frame_inputs, values=["Yüzde (%)", "Binde (‰)"], width=12, state="readonly")
combo_oran_tipi.grid(row=1, column=1, padx=(130, 6), pady=4, sticky="w")
combo_oran_tipi.current(0)

# Faiz tipi
tk.Label(frame_inputs, text="Faiz Tipi:").grid(row=2, column=0, padx=6, pady=4, sticky="w")
combo_faiz_tipi = ttk.Combobox(frame_inputs, values=["Günlük", "Aylık", "Yıllık"], width=12, state="readonly")
combo_faiz_tipi.grid(row=2, column=1, padx=6, pady=4, sticky="w")
combo_faiz_tipi.current(1)

# Aylık ek ödeme
tk.Label(frame_inputs, text="Aylık Ek Ödeme (₺):").grid(row=3, column=0, padx=6, pady=4, sticky="w")
entry_ek = tk.Entry(frame_inputs, width=18)
entry_ek.grid(row=3, column=1, padx=6, pady=4)

# Süre (ay)
tk.Label(frame_inputs, text="Süre (Ay):").grid(row=4, column=0, padx=6, pady=4, sticky="w")
entry_sure = tk.Entry(frame_inputs, width=18)
entry_sure.grid(row=4, column=1, padx=6, pady=4)

# Hesapla butonu
btn_hesapla = tk.Button(frame_inputs, text="Hesapla ve Kaydet", command=hesapla, bg="#4CAF50", fg="white", width=22)
btn_hesapla.grid(row=5, column=0, columnspan=2, pady=10)

# Tablo başlığı
tk.Label(root, text="Aylık Detay Tablosu", font=("Arial", 11, "bold")).pack(pady=(6, 0))

# Tablo (Treeview)
columns = ("Ay", "Dönem Başı", "Faiz Kazancı", "Ek Ödeme", "Dönem Sonu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    # Genişlikleri ayarla (Ay dar, metinler geniş)
    if col == "Ay":
        tree.column(col, anchor="center", width=50)
    else:
        tree.column(col, anchor="center", width=160)

tree.pack(pady=8)

# Alt sonuç etiketi
lbl_sonuc = tk.Label(root, text="", font=("Arial", 10))
lbl_sonuc.pack(pady=6)

# Kullanıcıya açıklama (alt bilgi)
info_text = (
    "Not: 'Faiz Oranı' kutusuna girilen değer seçilen 'Oran Tipi'na göre alınır.\n"
    "- Yüzde (%) seçilirse örn: 2 --> %2\n"
    "- Binde (‰) seçilirse örn: 2 --> 2‰ = 0.2%\n\n"
    "Faiz Tipi:\n - Günlük: girilen oran günlük kabul edilir ve aylığa dönüşür (30 gün baz alınır).\n - Aylık: doğrudan aylık oran kabul edilir.\n - Yıllık: yıllık oran aylığa (1/12) dönüştürülür."
)
tk.Label(root, text=info_text, justify="left", fg="#333").pack(padx=10, pady=(6,12))

# Uygulamayı başlat
root.mainloop()
