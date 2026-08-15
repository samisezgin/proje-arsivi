import tkinter as tk
from tkinter import ttk, messagebox

def hesapla():
    for row in tree.get_children():
        tree.delete(row)

    try:
        anapara = float(entry_anapara.get())
        faiz_orani_aylik = float(entry_faiz.get()) / 100
        aylik_ek = float(entry_ek.get())
        ay_sayisi = int(entry_sure.get())

        toplam = anapara
        toplam_kazanc = 0.0

        for ay in range(1, ay_sayisi + 1):
            baslangic = toplam
            faiz_kazanci = baslangic * faiz_orani_aylik
            toplam = baslangic + faiz_kazanci + aylik_ek
            toplam_kazanc += faiz_kazanci

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

        net_kazanc = toplam - (float(entry_anapara.get()) + aylik_ek * ay_sayisi)
        lbl_sonuc.config(
            text=f"\nToplam Birikim: {toplam:,.2f} ₺\nToplam Faiz Kazancı: {toplam_kazanc:,.2f} ₺\nNet Kazanç: {net_kazanc:,.2f} ₺"
        )

    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun!")

# === ARAYÜZ ===
root = tk.Tk()
root.title("Aylık Faizli Birikim Hesaplayıcı (Tablolu)")
root.geometry("650x500")
root.resizable(False, False)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Anapara (₺):").grid(row=0, column=0, padx=5, pady=3)
entry_anapara = tk.Entry(frame_inputs)
entry_anapara.grid(row=0, column=1, padx=5, pady=3)

tk.Label(frame_inputs, text="Aylık Faiz Oranı (%):").grid(row=1, column=0, padx=5, pady=3)
entry_faiz = tk.Entry(frame_inputs)
entry_faiz.grid(row=1, column=1, padx=5, pady=3)

tk.Label(frame_inputs, text="Aylık Ek Ödeme (₺):").grid(row=2, column=0, padx=5, pady=3)
entry_ek = tk.Entry(frame_inputs)
entry_ek.grid(row=2, column=1, padx=5, pady=3)

tk.Label(frame_inputs, text="Süre (Ay):").grid(row=3, column=0, padx=5, pady=3)
entry_sure = tk.Entry(frame_inputs)
entry_sure.grid(row=3, column=1, padx=5, pady=3)

tk.Button(frame_inputs, text="Hesapla", command=hesapla, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# === TABLO ===
columns = ("Ay", "Dönem Başı", "Faiz Kazancı", "Ek Ödeme", "Dönem Sonu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.pack(pady=5)

lbl_sonuc = tk.Label(root, text="", font=("Arial", 11))
lbl_sonuc.pack(pady=10)

root.mainloop()
