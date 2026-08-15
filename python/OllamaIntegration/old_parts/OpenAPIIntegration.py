import ollama


def chat():
    print("--- Yerel Yapay Zeka Sohbeti Başladı (Çıkmak için 'çıkış' yazın) ---")

    # Sohbet geçmişini tutmak istersen bu listeyi kullanabilirsin
    messages = []

    while True:
        user_input = input("\nSiz: ")

        if user_input.lower() in ['çıkış', 'exit', 'quit']:
            print("Görüşürüz!")
            break

        # Kullanıcı mesajını geçmişe ekle
        messages.append({'role': 'user', 'content': user_input})

        try:
            # Ollama üzerinden gemma3:4b modeline bağlan
            response = ollama.chat(
                model='gemma3:4b',
                messages=messages,
                stream=True  # Cevabı kelime kelime akıtır (daha sinematik görünür)
            )

            print("Yapay Zeka: ", end='', flush=True)
            full_response = ""

            for chunk in response:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content

            # Yapay zekanın cevabını da geçmişe ekle (Böylece önceki dediklerini hatırlar)
            messages.append({'role': 'assistant', 'content': full_response})
            print()

        except Exception as e:
            print(f"\nBir hata oluştu: {e}")
            print("Lütfen Ollama'nın arka planda çalıştığından emin olun.")


if __name__ == "__main__":
    chat()