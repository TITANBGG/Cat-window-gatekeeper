# 🎯 Ali Focus Gatekeeper

https://github.com/user-attachments/assets/77de563b-cfdb-4912-8fe3-3e24dcbd445c

Çok mu zaman harcıyorsun Chrome'da? Reddit'te vakit mı kaybediyorsun? 

**Ali Focus Gatekeeper**, seni takip edip limit dolduğunda "Dostum, mola vakti!" diye ekranı basıp hatırlatan bir asistan gibi. Yapılandırması kolay, malı, direkt iş yapıyor.

---

## 💡 Ne İşe Yarıyor?

- ⏱️ **App-based time tracking** → Chrome'da 45 dakika falan mı çalıştın? Uygulamayı takip ediyor
- 🚨 **Full-screen break reminder** → Limit dolduğunda tam ekranda mola ekranı açıyor, kaçış yok
- ⏳ **Countdown timer** → Geri sayım yapıyor, kalan zamanı gösteriyor  
- 🎬 **Smart video skip** → YouTube/Netflix'te fullscreen'deysens mola saati sayıyor mu? Bilir, atlıyor
- ⌨️ **Emergency exit** → Acil çıkış: `Ctrl + Shift + Q` (zaruri hallerde işe yarar)

---

## 🚀 Nasıl Başlayacağım?

### 1️⃣ Kurulum
Venv zaten hazır, ama temiz kurmak istersen:

```batch
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2️⃣ Çalıştırma
```batch
run.bat
```

ya da direkt:
```batch
.venv\Scripts\python.exe main.py
```

---

## ⚙️ Konfigürasyon

Bütün ayarlar `config.json`'da. Örnek:

```json
{
  "owner": "Ali Nebi ER",
  "global_rest_time_minutes": 5,
  "check_interval_seconds": 1,
  "smart_video_detection": true,
  "apps": [
    {
      "process_name": "chrome.exe",
      "time_limit_minutes": 45,
      "description": "Chrome çalışma süresi",
      "window_keywords": ["chrome", "youtube", "reddit"]
    }
  ]
}
```

**window_keywords nedir?** → Pencere başlığında arama yapıyor. Mesela Opera'yı da takip etmek istersen "opera" ekle. Geniş tut, şu an biraz tembel.

---

## 📋 Gereksinimler

- **Python 3.7+**
- **PyGetWindow** → Aktif pencereyi almak için
- **Tkinter** → UI için (zaten Python'da var)

---

## 🖥️ Platform Desteği

✅ Windows (test edildi)  
⚠️ Linux/Mac → Pencere başlığı alma kısmı fark ediyor, ayarla

---

## 💬 Not

Basit bir araç. "Over-engineering" yok, "AI magic" yok. Sadece seni izleyen ve mola veren bir program. Config dosyasını kendi ihtiyacına göre eğer 😉
