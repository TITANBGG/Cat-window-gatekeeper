# Focus Gatekeeper


https://github.com/user-attachments/assets/77de563b-cfdb-4912-8fe3-3e24dcbd445c



Ali Nebi ER icin duzenlenmis masaustu odak takip uygulamasi.

Bu proje, belirlenen uygulamalarda gecen sureyi takip eder. Limit doldugunda tam ekran bir mola ekrani acar ve calismaya kisa bir ara verilmesini ister.

## Durum

Bu surum kurulabilir ve calistirilabilir bir Python masaustu prototipidir. Hazir `.exe`, tray menu veya macOS paketi icermez. README bu gercek duruma gore yeniden yazildi.

## Ozellikler

- Proje sahibi bilgisi: Ali Nebi ER
- Uygulama bazli sure limitleri
- Config tabanli pencere basligi eslestirme
- Tam ekran mola ekrani
- Geri sayim sayaci
- Acil cikis kisayolu: `Ctrl + Shift + Q`
- YouTube/Netflix gibi video basliklari icin basit akilli atlama

## Kurulum

Bu klasorde sanal ortam hazirlandi. Yeniden kurmak gerekirse:

```bat
C:\Users\AliNebiER\AppData\Local\Python\bin\python.exe -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Calistirma

```bat
run.bat
```

Alternatif:

```bat
.venv\Scripts\python.exe main.py
```

## Ayarlar

Tum ayarlar `config.json` dosyasindadir.

```json
{
  "owner": "Ali Nebi ER",
  "global_rest_time_minutes": 5,
  "apps": [
    {
      "process_name": "chrome.exe",
      "time_limit_minutes": 45,
      "description": "Tarayici odak siniri",
      "window_keywords": ["chrome", "google chrome", "youtube", "reddit"]
    }
  ]
}
```

`window_keywords`, aktif pencere basliginda aranir. Bu sayede sadece sabit uygulama isimlerine bagli kalmadan Opera, VS Code, Telegram gibi programlar config uzerinden takip edilebilir.

## Notlar

Windows ortaminda test edildi. Aktif pencere eslestirmesi `PyGetWindow` ile pencere basligi uzerinden yapilir; bu nedenle baslikta uygulama adi gecmeyen programlar icin `window_keywords` alanini genisletmek gerekir.
