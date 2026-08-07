# 📚 Neuro-Symbolic Agent System — Master Functional Technical Manual

**System Version**: 1.2.0 (SOTA Edition)  
**Architecture**: 5-Layer Multi-Agent & Neuro-Symbolic Hybrid Architecture  
**Repository**: [github.com/Alihanesentas/agent_system](https://github.com/Alihanesentas/agent_system)

---

## 🏛️ 1. MİMARİ VE KATMAN YAPISI (5-LAYER ARCHITECTURE)

Sistem, yapay zeka modellerinin yüksek seviyeli muhakeme gücünü, 0-Token ($0 Maliyetli) yerel Sembolik Python İşlem Motorları ile birleştirir.

```
Katman 1 (Presentation): Rich REPL CLI, VSCode/Cursor Extension v1.2.0, React Web Analytics Dashboard (Port 5173), Stdio MCP Server 2.0.
Katman 2 (Orchestration): Claude 3.5 Sonnet / GPT-4o Orchestrator, /auto Otonom Hedef Döngüsü, /tree Canlı Ağaç Monitörü.
Katman 3 (Specialist Sub-Agents): Electronics PCB Agent, Software Firmware Agent, Mechanical 3D CAD Agent, Reviewer Agent.
Katman 4 (Symbolic Python Engines): SPICE Devre Simülatörü, Pinout Auditor, Termal Isınma Hesabı, PCB DRC & Empedans, OpenSCAD 3D Generator, USB Flasher.
Katman 5 (Persistence & Infrastructure): ChromaDB RAG Engine, SQLite Proje Hafızası, Mühendis Profili, Async Worker Queue, Token Bucket Limiter.
```

---

## 🔌 2. MODÜLER DİZİN VE ALT PAKET KATALOĞU (`core/`)

- **`core/engine/`**: İş Akışı, DAG, Otonom Hedef ve Simülasyon Motorları
  - `autonomous_agent.py`: `/auto` Tam Otonom Hedef Döngüsü
  - `layered_architecture.py`: `/layers` 5 Katmanlı İcra Motoru
  - `agent_tree_sim.py`: `/tree` Canlı Ağaç Simülasyonu
  - `dag_executor.py`: Paralel Asenkron DAG Yürütücü
  - `cost_router.py`: `/cost` Dinamik Model Maliyet Yönlendiricisi
  - `replay_engine.py`: `/replay` Zaman Yolculuklu Hata Hata Ayıklama Motoru
- **`core/hardware/`**: KiCad, PCB, SPICE & Donanım Araçları
  - `schematics.py`: KiCad Şematik ve Netlist Ayrıştırıcı
  - `spice.py`: `/spice` RC Devre Simülatörü
  - `pinout.py`: `/pinout` ESP32 Pin Çakışma ve Strapping Pin Denetleyicisi
  - `thermal.py`: `/thermal` Termal Güç Kaybı ve Soğutucu Hesabı
  - `pcb_drc.py`: `/drc` PCB DRC Fabrika Kuralları ve 50Ω Empedans Denetimi
  - `autorouter.py`: `/autoroute` KiCad PCB A* Otomatik Yolu Çizici
  - `rf_antenna.py`: `/rf` PCB Anten ve 50Ω Pi-Network Eşleme Hesabı
  - `flasher.py`: `/flash` USB Firmware Yükleyici ve Seri Monitör
  - `emc_compliance.py`: `/emc` FCC Class B & CE Sertifikasyon Pre-Checker
- **`core/software/`**: Firmware, Test & Yapay Zeka Motorları
  - `executor.py`: gcc / make / platformio Çalıştırıcı
  - `self_heal.py`: `/heal` Otonom Kod Tamir Döngüsü
  - `hil_testing.py`: `/hil` Hardware-in-the-Loop Fiziksel Kart Test Motoru
  - `embedded_test_gen.py`: `/unittest-gen` Unity C Birim Test Üreteci
  - `edge_ai.py`: `/edge-ai` TinyML SRAM Hesabı ve ESP-DL C++ Sarmalayıcı
  - `ota_builder.py`: `/ota` Firmware OTA Güncelleme Manifest Üreteci
  - `finetune.py`: `/finetune` LoRA Veri Seti İhracatçısı ve VRAM Hesabı
- **`core/production/`**: CAD, Mekanik & Üretim Planlama Araçları
  - `mechanical.py`: `/cad` OpenSCAD 3D Kutu ve FDM Slicer Önerici
  - `cart_builder.py`: `/cart` Mouser / LCSC 1-Tık Sepet Üreteci
  - `bom_optimizer.py`: `/bom-opt` BOM Maliyet Sürücüsü İyileştirici
  - `battery.py`: `/battery` Pil Ömrü ve Güneş Paneli Hesabı
  - `harness.py`: `/harness` Kablo AWG Kesit ve Gerilim Düşümü Hesabı
  - `gantt_planner.py`: `/gantt` Mermaid Gantt Zaman Çizelgesi
  - `project_gen.py`: `/create-project` Multidisipliner Proje Klasör Üreteci
  - `report_generator.py`: `/report` Tam Proje Rapor İhracatçısı
- **`core/infra/`**: Altyapı, Önbellek, Vektör Veritabanı & Telemetri
  - `cache.py`: Semantik Önbellek Engine (%80 Token Tasarrufu)
  - `checkpoint.py`: `/checkpoint` & `/restore` Snapshot Kaydetme/Yükleme
  - `voice_agent.py`: `/voice` Eller Serbest Sesli Mühendis Asistanı
  - `knowledge_graph.py`: `/graph` Donanım İlişki Grafiği
  - `self_reflection.py`: `/reflect` Otonom Hata Eleştirisi Döngüsü
  - `guardrails.py`: `/guard` Gerçek Zamanlı Çıktı Güvenlik Filtresi
  - `plugin_loader.py`: `/reload-plugins` Canlı Sıcak Yüklemeli Eklenti Motoru
  - `worker_queue.py`: `/worker` Asenkron İş Kuyruğu
  - `rate_limiter.py`: `/ratelimit` LLM API Token Bucket Throttler
  - `telemetry.py`: `/metrics` Prometheus Metrik Uç Noktası
  - `autocomplete.py`: CLI Otomatik TAB Tamamlayıcısı

---

## 🛠️ 3. TÜM 55+ SLASH KOMUTLARININ FONKSİYONEL REHBERİ

### 🤖 Otonom Hedef & Katmanlı İcra Komutları
- **`/auto <hedef>`**: Tek bir cümlelik hedeften (Örn: `/auto ESP32 hava durumu istasyonu yap`) tüm donanım, şematik, DRC, 3D CAD, auto-routing, HIL test ve C++ firmware dosyalarını otonom üretir.
- **`/layers <hedef>`**: Görevi açık 5-Katmanlı Mimari Motoru üzerinden adım adım çalıştırır.
- **`/tree [hedef]`**: Canlı hiyerarşik Agent Ağacını ve modellerin çalışma sürelerini görselleştirir.

### 🔌 Donanım & PCB Elektronik Komutları
- **`/kicad <file.kicad_sch>`**: KiCad şematik bileşenlerini ve net etiketlerini ayrıştırır.
- **`/kicad-set <file> <ref> <val>`**: Şematik dosyasında bileşen değerini (Örn: R1 1k) günceller.
- **`/bom <file.csv>`**: PCB Bill of Materials CSV dosyasını analiz eder.
- **`/spice <r_ohms> <c_farads>`**: RC düşük geçiren filtre zaman sabiti ve frekans yanıtını simüle eder.
- **`/pinout <sda> <scl> <out>`**: ESP32 GPIO pin çakışmalarını ve strapping pin tehlikelerini denetler.
- **`/thermal <vin> <vout> <amps>`**: Isıl güç kaybını ve soğutucu (°C/W) ihtiyacını hesaplar.
- **`/drc <width_mm>`**: PCB fabrika üretim kurallarını ve 50Ω mikroşerit empedansını denetler.
- **`/autoroute`**: KiCad PCB şematik bacak yollarını A* algoritması ile otonom çizer.
- **`/rf [freq_mhz]`**: PCB çeyrek-dalga monopole anten boyutlarını ve 50Ω Pi-network eşleme değerlerini hesaplar.
- **`/gerber <folder>`**: Gerber katmanlarını ve 3D kutu sınır boyutlarını çıkarır.
- **`/emc`**: FCC Class B ve CE EMC uyumluluk ön denetimini gerçekleştirir.

### 🔍 Donanım Arama & Tedarik Komutları
- **`/part <part_number>`**: Mouser/DigiKey/LCSC stok, fiyat ve datasheet araması yapar.
- **`/alt <part_number>`**: Stoklu muadil ve doğrudan yerine takılabilir (drop-in) bileşen önerir.
- **`/compare <p1> <p2>`**: Yan yana parametrik bileşen karşılaştırması sunar.
- **`/cart [bom.csv]`**: Mouser / LCSC 1-tık alışveriş sepeti JSON yükünü oluşturur.
- **`/datasheet <pdf_path>`**: PDF datasheet dosyasından pin tablolarını ve özellikleri çıkarır.

### 💻 Yazılım & Gömülü Sistem Komutları
- **`/heal <file.c>`**: Derleme ve lint hatalarını otonom düzelten self-healing döngüsü.
- **`/hil <file.bin>`**: USB ile bağlı fiziksel kartlarda Hardware-in-the-Loop otonom test koşar.
- **`/unittest-gen <mod>`**: Gömülü Unity C birim test dosyalarını oluşturur.
- **`/edge-ai <params>`**: TinyML model peak SRAM/Flash kullanımını hesaplar ve ESP-DL C++ sarmalayıcısı üretir.
- **`/ota [version]`**: Firmware OTA güncelleme manifestini ve SHA-256 doğrulamasını üretir.
- **`/finetune`**: LoRA 4-bit fine-tuning VRAM ihtiyacını hesaplar ve JSONL veri setini dışa aktarır.
- **`/run <command>`**: Güvenli alt süreçte shell derleme komutu çalıştırır.

### 🛠️ Mekanik CAD & Üretim Planlama Komutları
- **`/cad <l> <w> <h>`**: Parametrik OpenSCAD 3D kutu betiği oluşturur.
- **`/slicer <material>`**: FDM 3D yazıcı (PLA/ABS/PETG/TPU) dilimleyici ayarlarını önerir.
- **`/harness <amps> <length>`**: Kablo AWG kesit alanını ve gerilim düşümünü hesaplar.
- **`/battery <mah> <active_ma>`**: Pil çalışma ömrünü ve güneş paneli watt gücünü hesaplar.
- **`/bom-opt`**: BOM maliyet sürücülerini ve 100/1000 adet üretim adımlarını optimize eder.
- **`/gantt`**: Multidisipliner projenin Mermaid Gantt zaman çizelgesini üretir.
- **`/create-project <name>`**: Birleşik proje dizin yapısını (firmware, hw, cad, docs) oluşturur.
- **`/mcu <gereksinim>`**: Proje gereksinimlerine göre en uygun mikrodenetleyiciyi (ESP32-S3, STM32F4, RP2040, nRF52840, Teensy 4.1) önerir.
- **`/lint <code>`**: Üretilen C++/Python kod parçalarını otomatik biçimlendirir ve sentaks düzenlemesi yapar.
- **`/theme <tema>`**: CLI renk paletini dinamik olarak değiştirir (cyberpunk, matrix, dracula, solarized).
- **`/stackup [layers]`**: 2, 4, 6, ve 8 katmanlı PCB katman dizilimi (dielectric stackup) ve USB 2.0 90Ω diferansiyel yol genişliğini hesaplar.
- **`/slides`**: Proje dokümantasyonunu ve Gantt grafiklerini koyu temalı interaktif HTML sunum slaytına dönüştürür.
- **`/consensus-matrix`**: Çoklu model güven skorları ve oy dağılımı matris analizi sunar.
- **`/3d-clearance`**: KiCad 3D STEP bileşen yüksekliklerini analiz eder ve kutu kapağı çakışma kontrolü yapar.
- **`/power <code>`**: Firmware C++ kodunun ortalama akım çekimini (mA) ve pil çalışma süresini hesaplar.
- **`/pareto`**: Modellere ait gecikme (ms), maliyet ($) ve doğruluk skoru Pareto optimal eğri analizini sunar.
- **`/spice-transpile`**: KiCad şematik netlist verisini doğrudan SPICE `.cir` simülasyon dosyasına dönüştürür.
- **`/security <code>`**: C++ firmware kodundaki bellek sızıntılarını ve güvensiz fonksiyonları statik tarar.
- **`/fea [force_N]`**: 3D basılı kutunun mekanik gerilim (FEA Stress) ve deformasyon simülasyonunu yapar.
- **`/supply-risk`**: BOM parçalarının küresel tedarik zinciri stok durumunu ve EOL (üretim sonu) risklerini tarar.
- **`/prune <text>`**: LLM prompt bağlamını %60 oranında sıkıştırarak token maliyetini düşürür.
- **`/drc-rules`**: Özel KiCad 7.0/8.0 fabrika DRC kural dosyasını (`.kicad_dru`) oluşturur.
- **`/partition [mb]`**: Flash hafıza bölüm haritasını (nvs, app0, app1, spiffs) ve SRAM yerleşimini görselleştirir.
- **`/fasteners [type]`**: 3D kutu vida yuvası (screw boss M2-M4) kılavuz delik çapı ve duvar kalınlığını hesaplar.
- **`/circuit-breaker`**: LLM API bağlantı kopmalarında otomatik alternatif modele geçen devre kesici durumunu gösterir.
- **`/budget`**: Aylık/günlük LLM token harcama tutarını ($) ve bütçe uyarı sınırını takip eder.
- **`/ota-verify`**: Firmware binary dosyasının SHA-256 kriptografik imzasını ve magic başlığını doğrular.
- **`/airflow`**: 3D kutunun pasif havalandırma ızgara alanını (mm²) ve gerekli CFM fan hava akışını hesaplar.
- **`/ensemble`**: Paralel koşan modellerin yanıtlarını çoğunluk konsensüs oylaması ile birleştirir.
- **`/bom-sensitivity`**: Enflasyon ve tedarik krizlerinde BOM maliyet salınımlarını Monte Carlo simülasyonu ile analiz eder.
- **`/compact-memory`**: SQLite uzun vadeli hafıza kayıtlarını ve ChromaDB vektör veri tabanını sıkıştırarak disk alanını boşaltır.
- **`/watchdog`**: Gömülü sistem CPU panic crash dump kayıtlarını ve Watchdog reset nedenini analiz eder.
- **`/snap-fit`**: 3D kutu geçme kapak (cantilever snap-fit) tırnak gerilimini (%) ve kırılma dayanımını hesaplar.
- **`/agent-telemetry`**: Alt agent'ların adım adım çalışma sürelerini (ms) ve gecikme profilini raporlar.
- **`/footprint-check`**: KiCad şematik sembol pinleri ile PCB footprint pad düzenini çapraz denetler.
- **`/backoff`**: LLM API 429 Rate Limit durumlarında üssel geri çekilme (jitter delay) süresini hesaplar.
- **`/coverage`**: C++ birim test satır ve dallanma LCOV kapsama oranını (%) raporlar.
- **`/flexure`**: 3D kutu bükülebilir mafsal (flexure living hinge) gerilim ve bükülme yarıçapı sınırını hesaplar.
- **`/critical-path`**: Alt agent görev bağımlılık grafiğinde en uzun kritik yolu (bottleneck) analiz eder.
- **`/trace-matching`**: PCB yüksek hızlı diferansiyel yol uzunluk eşlemesini (length matching) ve faz kayması dalga sayısını hesaplar.
- **`/prompt-builder`**: Agent'lar için özelleştirilmiş sistem istemi (system prompt) bağlamını dinamik oluşturur.
- **`/subsheets`**: Çok yapraklı hiyerarşik KiCad şematik yapısını (`power.kicad_sch`, `mcu.kicad_sch`) otonom üretir.
- **`/stack-guard`**: FreeRTOS gömülü C++ görevlerinin güvenli yığın (stack frame) bellek ihtiyacını hesaplar.
- **`/gasket`**: 3D kutular için IP67 su geçirmez kauçuk O-ring conta kanalı (groove) genişlik ve derinliğini hesaplar.
- **`/dlq`**: Başarısız olan agent alt görevlerini Dead Letter Queue (DLQ) havuzunda toplar ve tek tıkla yeniden dener.
- **`/cost-forecast`**: Günlük LLM harcama trendine göre haftalık ve aylık token maliyet tahminini ($) çıkarır.
- **`/report`**: Tüm projenin eksiksiz PDF/Markdown mühendislik raporunu çıkarır.

### 🛡️ Mimari Dayanıklılık, Güvenlik & Altyapı Komutları
- **`/voice <prompt>`**: Atölyede eller serbest sesli mühendislik komutu çalıştırır.
- **`/graph <query>`**: Donanım Bilgi Grafiğinde bileşen ilişkilerini sorgular.
- **`/reflect <task>`**: Görevi otonom hata eleştirisi ve yeniden deneme döngüsü ile çalıştırır.
- **`/cost <prompt>`**: Görevi en ucuz yetenekli modele dinamik yönlendirir.
- **`/guard <code>`**: Üretilen C++/CAD kodunu diske yazılmadan önce güvenlik filtrenizden geçirir.
- **`/reload-plugins`**: `plugins/` klasöründeki özel Python eklentilerini sıcak yükler.
- **`/worker`**: Asenkron arka plan Worker kuyruğu durumunu görüntüler.
- **`/ratelimit`**: LLM API Token Bucket rate limiter durumunu görüntüler.
- **`/checkpoint`**: Sistem durumunun diske Snapshot Checkpoint kaydını alır.
- **`/restore`**: Sistem durumunu Snapshot Checkpoint kaydından geri yükler.
- **`/metrics`**: Prometheus & Grafana izleme uç noktasını sunar.
- **`/replay`**: Zaman yolculuklu hata ayıklama adım kaydını yeniden oynatır.
