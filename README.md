# 📦 Proje Arşivi

Diskte dağınık duran, **git'e hiç girmemiş** 15 proje. Ağustos 2026'da makineye
format atılmadan önce tek yerde toplandı.

**Arşivdir, sürdürülmüyor.** Hiçbiri çalışır durumda doğrulanmadı; oldukları
gibi kaydedildiler. Derleme çıktıları (`bin/`, `obj/`, `target/`,
`node_modules/`, `artifacts/`, `typechain-types/`) alınmadı — hepsi yeniden
üretilebilir.

## .NET

| Proje | Tarih | Not |
|---|---|---|
| `dotnet/MacunNet.Server` | Mar 2025 | Discord benzeri uygulamanın sunucusu. GitHub'daki `macunnet` deposunun eşi değil, ayrı bir çalışma |
| `dotnet/MacunNet.Client` | Mar 2025 | Aynı işin istemcisi |
| `dotnet/SipSoftPhone` | Oca 2025 | SIP yazılım telefonu |
| `dotnet/dotNetWebApi` | Oca 2025 | TodoApi — Web API denemesi |

## Java / Spring

| Proje | Tarih | Not |
|---|---|---|
| `java-spring/MultiModuleApp` | Nis 2025 | Çok modüllü Maven yapısı (`core` + `app`) |
| `java-spring/emlakburada` | Ara 2022 | Emlak ilan uygulaması |
| `java-spring/emlakcepte` | Ara 2022 | Aynı ailenin bir başka sürümü |
| `java-spring/emlakcepte-service` | Ara 2022 | Servis katmanı |
| `java-spring/emlakcepte-banner-service` | Ara 2022 | Banner servisi |
| `java-spring/emlakcepte-banner-service-1` | Ara 2022 | Banner servisinin ikinci denemesi |
| `java-spring/emlakcepte_factory` | Ara 2022 | Factory tasarım deseni alıştırması |
| `java-spring/emlakcepte_singleton` | Ara 2022 | Singleton tasarım deseni alıştırması |
| `java-spring/clonemedium` | Ara 2022 | Medium klonu |
| `java-spring/fileUploader` | Şub 2023 | Dosya yükleme |

## Web3

| Proje | Tarih | Not |
|---|---|---|
| `web3/hardhat-bootcamp` | Eyl 2023 | Hardhat + Solidity 0.8.19, mainnet fork ile test |

## Python

Bunlar `C:` üzerindeydi — yani formatla **gerçekten kaybolacaklardı**. İlk
taramada gözden kaçtılar çünkü `requirements.txt` / `pyproject.toml`
taşımıyorlar, tarama da bağımlılık dosyasına göre arıyordu.

| Proje | Tarih | Not |
|---|---|---|
| `python/taskbarhero_optimizer` | Haz 2026 | Görüntü işlemeyle oyun otomasyonu — pencere bulma, ızgara okuma, düğme haritalama, tkinter arayüz |
| `python/OllamaIntegration` | Haz 2026 | Ollama ile metin→görsel/video üretimi ve YouTube'a yükleme |
| `python/PythonProject` | Oca 2026 | Faiz hesaplayıcı, birkaç sürüm |

`OllamaIntegration` içinde **`client_secrets.json` ve `token.pickle`
alınmadı** — Google OAuth istemci sırrı ve YouTube yükleme yetkisi taşıyan
canlı token. Yeniden üretmek için Google Cloud Console'dan kendi OAuth
istemcinizi indirip `client_secrets.json` olarak kaydedin; `token.pickle` ilk
çalıştırmada kendiliğinden oluşur.

`taskbarhero_optimizer` içindeki 128 ekran görüntüsü (73 MB) alınmadı — hata
ayıklama çıktısı, yeniden üretilebilir. Kökteki üç örnek görsel duruyor.

## Arşivlenirken yapılan tek değişiklik

`web3/hardhat-bootcamp/hardhat.config.ts` içinde **Alchemy API anahtarı açıkta
yazılıydı**. Ortam değişkenine taşındı:

```bash
ALCHEMY_URL=https://eth-mainnet.g.alchemy.com/v2/<anahtar> npx hardhat test
```

Eski anahtar bu depoya girmedi. Hâlâ geçerliyse
[Alchemy panelinden](https://dashboard.alchemy.com/) döndürmeniz iyi olur —
kotayı harcamak için yeterli.

Bunun dışında kod değiştirilmedi.

## Nereden geldiler

| Arşivdeki yer | Özgün konum |
|---|---|
| `dotnet/MacunNet.*` | `D:\MacunNet.Server`, `D:\MacunNet.Client` |
| `dotnet/SipSoftPhone` | `D:\SIPPhoneApp\SipSoftPhone` |
| `dotnet/dotNetWebApi` | `D:\dotNetWebApi` |
| `java-spring/emlak*`, `clonemedium` | `D:\eclipse-workspace\` |
| `java-spring/MultiModuleApp` | `E:\dc-clone\MultiModuleApp` |
| `java-spring/fileUploader` | `E:\masaüstü toplama klasörü\Flash 32GB\...\fileUpload\` |
| `web3/hardhat-bootcamp` | `E:\masaüstü toplama klasörü\hardhat-bootcamp` |
