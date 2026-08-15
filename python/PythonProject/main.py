# faiz_hesaplayici_full.py
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
except ImportError:
    tk.Tk().withdraw()
    messagebox.showerror(
        "Eksik Kütüphane",
        "Bu uygulama 'pandas', 'matplotlib' ve 'openpyxl' kütüphanelerini kullanır.\n"
        "Lütfen terminalde şunu çalıştırın:\n\npip install pandas matplotlib openpyxl"
    )
    sys.exit(1)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def hesapla():
    for row in tree.get_children():
        tree.delete(row)

    try:
        anapara = float(entry_anapara.get())
        faiz_giren = float(entry_faiz.get())
        ek_odem = float(entry_ek.get())
        sure_ay = int(entry_sure.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun (sayısal değerler).")
        return

    oran_tipi = combo_oran_tipi.get()
    if oran_tipi == "Yüzde (%)":
        oran = faiz_giren / 100.0
    else:
        oran = faiz_giren / 1000.0

    faiz_tipi = combo_faiz_tipi.get()
    if faiz_tipi == "Günlük":
        aylik_oran = (1.0 + oran) ** 30.0 - 1.0
    elif faiz_tipi == "Yıllık":
        aylik_oran = (1.0 + oran) ** (1.0 / 12.0) - 1.0
    else:
        aylik_oran = oran

    ay_list, baslangic_list, faiz_kazanci_list, ek_list, donem_sonu_list = [], [], [], [], []
    toplam = anapara
    toplam_faiz_kazanci = 0.0

    for ay in range(1, sure_ay + 1):
        baslangic = toplam + ek_odem
        faiz_kazanci = baslangic * aylik_oran
        toplam = baslangic + faiz_kazanci

        ay_list.append(ay)
        baslangic_list.append(baslangic)
        faiz_kazanci_list.append(faiz_kazanci)
        ek_list.append(ek_odem)
        donem_sonu_list.append(toplam)
        toplam_faiz_kazanci += faiz_kazanci

        tree.insert("", "end", values=(
            ay,
            f"{baslangic:,.2f} ₺",
            f"{faiz_kazanci:,.2f} ₺",
            f"{ek_odem:,.2f} ₺",
            f"{toplam:,.2f} ₺"
        ))

    net_kazanc = toplam - (anapara + ek_odem * sure_ay)

    lbl_sonuc.config(
        text=f"Toplam Birikim: {toplam:,.2f} ₺    |    "
             f"Toplam Faiz Kazancı: {toplam_faiz_kazanci:,.2f} ₺    |    "
             f"Net Kazanç: {net_kazanc:,.2f} ₺"
    )

    df = pd.DataFrame({
        "Ay": ay_list,
        "Dönem Başı": baslangic_list,
        "Faiz Kazancı": faiz_kazanci_list,
        "Ek Ödeme": ek_list,
        "Dönem Sonu": donem_sonu_list
    })

    base_folder = os.path.join(os.getcwd(), "All_Results")
    ensure_dir(base_folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    run_folder = os.path.join(base_folder, timestamp)
    ensure_dir(run_folder)

    excel_path = os.path.join(run_folder, "calculation.xlsx")
    df.to_excel(excel_path, index=False, engine="openpyxl")

    plt.figure(figsize=(8, 4.5))
    plt.plot(ay_list, donem_sonu_list, marker="o", linewidth=2)
    plt.title("Aylara Göre Toplam Birikim")
    plt.xlabel("Ay")
    plt.ylabel("Toplam Birikim (₺)")
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.2f}"))
    plt.tight_layout()

    png_path = os.path.join(run_folder, "growth_chart.png")
    plt.savefig(png_path, dpi=150)
    plt.show()
    plt.close()

    messagebox.showinfo(
        "Kaydedildi",
        f"Hesaplama sonuçları kaydedildi:\n\n{run_folder}\n\n"
        f"- calculation.xlsx\n- growth_chart.png"
    )


# === ARAYÜZ ===
root = tk.Tk()
root.title("Faizli Birikim Hesaplayıcı - Geniş Görünüm")
root.geometry("900x720")  # daha geniş, alt bilgi rahat sığar
root.resizable(False, False)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=12)

tk.Label(frame_inputs, text="Anapara (₺):").grid(row=0, column=0, padx=6, pady=4, sticky="w")
entry_anapara = tk.Entry(frame_inputs, width=18)
entry_anapara.grid(row=0, column=1, padx=6, pady=4)

tk.Label(frame_inputs, text="Faiz Oranı:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
entry_faiz = tk.Entry(frame_inputs, width=12)
entry_faiz.grid(row=1, column=1, padx=(6, 0), pady=4, sticky="w")

combo_oran_tipi = ttk.Combobox(frame_inputs, values=["Yüzde (%)", "Binde (‰)"], width=12, state="readonly")
combo_oran_tipi.grid(row=1, column=1, padx=(130, 6), pady=4, sticky="w")
combo_oran_tipi.current(0)

tk.Label(frame_inputs, text="Faiz Tipi:").grid(row=2, column=0, padx=6, pady=4, sticky="w")
combo_faiz_tipi = ttk.Combobox(frame_inputs, values=["Günlük", "Aylık", "Yıllık"], width=12, state="readonly")
combo_faiz_tipi.grid(row=2, column=1, padx=6, pady=4, sticky="w")
combo_faiz_tipi.current(1)

tk.Label(frame_inputs, text="Aylık Ek Ödeme (₺):").grid(row=3, column=0, padx=6, pady=4, sticky="w")
entry_ek = tk.Entry(frame_inputs, width=18)
entry_ek.grid(row=3, column=1, padx=6, pady=4)

tk.Label(frame_inputs, text="Süre (Ay):").grid(row=4, column=0, padx=6, pady=4, sticky="w")
entry_sure = tk.Entry(frame_inputs, width=18)
entry_sure.grid(row=4, column=1, padx=6, pady=4)

btn_hesapla = tk.Button(frame_inputs, text="Hesapla ve Kaydet", command=hesapla,
                        bg="#4CAF50", fg="white", width=22)
btn_hesapla.grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(root, text="Aylık Detay Tablosu", font=("Arial", 11, "bold")).pack(pady=(6, 0))

columns = ("Ay", "Dönem Başı", "Faiz Kazancı", "Ek Ödeme", "Dönem Sonu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    if col == "Ay":
        tree.column(col, anchor="center", width=50)
    else:
        tree.column(col, anchor="center", width=160)

tree.pack(pady=8)

lbl_sonuc = tk.Label(root, text="", font=("Arial", 10))
lbl_sonuc.pack(pady=6)

# ALT BİLGİ (otomatik satır kaydırmalı)
info_text = (
    "Not: 'Faiz Oranı' kutusuna girilen değer seçilen 'Oran Tipi'na göre alınır.\n"
    " - Yüzde (%) seçilirse örn: 2 --> %2\n"
    " - Binde (‰) seçilirse örn: 2 --> 2‰ = 0.2%\n\n"
    "Faiz Tipi:\n"
    " - Günlük: girilen oran günlük kabul edilir ve aylığa dönüştürülür (30 gün baz alınır).\n"
    " - Aylık: doğrudan aylık oran kabul edilir.\n"
    " - Yıllık: yıllık oran aylığa (1/12) oranında dönüştürülür."
)
lbl_info = tk.Label(root, text=info_text, justify="left", fg="#333", wraplength=860, anchor="w")
lbl_info.pack(padx=10, pady=(10, 12))

root.mainloop()

