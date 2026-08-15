import tkinter as tk
from tkinter import messagebox

def hesapla():
    try:
        anapara = float(entry_anapara.get())
        faiz_orani_aylik = float(entry_faiz.get()) / 100  # yüzdeyi orana çevir
        aylik_ek = float(entry_ek.get())
        ay_sayisi = int(entry_sure.get())

        toplam = anapara
        for _ in range(ay_sayisi):
            toplam = toplam * (1 + faiz_orani_aylik) + aylik_ek

        kazanc = toplam - (anapara + aylik_ek * ay_sayisi)

        lbl_sonuc.config(
            text=f"Toplam Birikim: {toplam:,.2f} ₺\nToplam Kazanç: {kazanc:,.2f} ₺"
        )
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru doldurun!")

# === ARAYÜZ ===
root = tk.Tk()
root.title("Aylık Faizli Birikim Hesaplayıcı")
root.geometry("350x300")
root.resizable(False, False)

tk.Label(root, text="Anapara (₺):").pack(pady=5)
entry_anapara = tk.Entry(root)
entry_anapara.pack()

tk.Label(root, text="Aylık Faiz Oranı (%):").pack(pady=5)
entry_faiz = tk.Entry(root)
entry_faiz.pack()

tk.Label(root, text="Aylık Ek Ödeme (₺):").pack(pady=5)
entry_ek = tk.Entry(root)
entry_ek.pack()

tk.Label(root, text="Süre (Ay):").pack(pady=5)
entry_sure = tk.Entry(root)
entry_sure.pack()

tk.Button(root, text="Hesapla", command=hesapla, bg="#4CAF50", fg="white").pack(pady=10)

lbl_sonuc = tk.Label(root, text="", font=("Arial", 11), justify="center")
lbl_sonuc.pack(pady=10)

root.mainloop()
