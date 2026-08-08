# 🧠 Agent System — Eklenecek Script'ler TODO Listesi
# Bu dosya, Gemini ile eklenecek tüm eksik modüllerin referans listesidir.
# Her modül için: dosya yolu, açıklama ve ana fonksiyon adı belirtilmiştir.
# ═══════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────
# HARDWARE — Elektronik & PCB (31 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Güç Elektroniği

## Analog & Sinyal İşleme
- [ ] core/hardware/dac_output.py           → DAC çıkış tampon, settling time | def design_dac_output(**kwargs) -> Dict

## Dijital & Haberleşme
- [ ] core/hardware/ethernet_magnetics.py   → Ethernet magnetics seçimi, PoE güç hesabı | def design_ethernet_interface(**kwargs) -> Dict
- [ ] core/hardware/lvds_serdes.py          → LVDS/SerDes sinyal bütünlüğü | def analyze_lvds_signal(**kwargs) -> Dict

## Sensör & Ölçüm
- [ ] core/hardware/sensor_interface.py     → Sıcaklık/basınç/ivme sensör arayüz devresi | def design_sensor_interface(**kwargs) -> Dict
- [ ] core/hardware/thermocouple.py         → Termokupl tipi seçimi, cold junction komp. | def design_thermocouple_interface(**kwargs) -> Dict

## PCB İleri Seviye
- [ ] core/hardware/crosstalk_analysis.py   → PCB crosstalk (NEXT/FEXT), guard trace | def analyze_pcb_crosstalk(**kwargs) -> Dict
- [ ] core/hardware/impedance_calculator.py → Microstrip/Stripline/Coplanar empedans | def calculate_trace_impedance_advanced(**kwargs) -> Dict
- [ ] core/hardware/panelization.py         → PCB panelizasyon yerleşim optimizasyonu | def optimize_pcb_panel(**kwargs) -> Dict
- [ ] core/hardware/gerber_checker.py       → Gerber dosya bütünlük kontrolü | def validate_gerber_files(**kwargs) -> Dict
- [ ] core/hardware/pcb_thermal_relief.py   → Thermal relief pad pattern, spoke hesabı | def calculate_thermal_relief(**kwargs) -> Dict

## Koruma & Güvenlik


# ──────────────────────────────────────────────────────────────────────
# SOFTWARE — Gömülü Yazılım & Firmware (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## RTOS & Çekirdek
- [ ] core/software/scheduler_sim.py        → Rate Monotonic / EDF zamanlama simülasyonu | def simulate_scheduler(**kwargs) -> Dict

## Haberleşme Protokolleri
- [ ] core/software/zigbee_mesh.py          → Zigbee mesh topolojisi, routing table | def design_zigbee_mesh(**kwargs) -> Dict

## Güvenlik & Kriptografi
- [ ] core/software/cert_manager.py         → X.509 sertifika zinciri, TLS mutual auth | def generate_cert_config(**kwargs) -> Dict

## Veri & Depolama
- [ ] core/software/eeprom_wear.py          → EEPROM/Flash wear leveling ömür analizi | def analyze_eeprom_wear(**kwargs) -> Dict
- [ ] core/software/log_framework.py        → Gömülü log framework (severity, circular) | def generate_log_framework(**kwargs) -> Dict

## Test & Kalite
- [ ] core/software/unit_test_scaffold.py   → Unity/CMock C unit test scaffold üreteci | def generate_unit_test_scaffold(**kwargs) -> Dict
- [ ] core/software/code_size_analyzer.py   → .map file parser, RAM/ROM/Flash istatistik | def analyze_code_size(**kwargs) -> Dict
- [ ] core/software/firmware_diff.py        → İki firmware binary section-level diff | def diff_firmware_binaries(**kwargs) -> Dict

## DSP & Kontrol
- [ ] core/software/fft_analyzer.py         → FFT pencere, frekans çözünürlüğü, aliasing | def analyze_fft_params(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# PRODUCTION / MEKANİK (20 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## 3D Baskı & İmalat
- [ ] core/production/injection_mold.py     → Enjeksiyon kalıp parametreleri (shrinkage) | def estimate_injection_mold(**kwargs) -> Dict
- [ ] core/production/cnc_feedrate.py       → CNC freze besleme hızı, devir hesabı | def calculate_cnc_feedrate(**kwargs) -> Dict

## Mekanik Analiz
- [ ] core/production/beam_stress.py        → Kiriş eğilme moment, kesme, sehim | def analyze_beam_stress(**kwargs) -> Dict
- [ ] core/production/vibration_analysis.py → Doğal frekans, titreşim izolasyon | def analyze_vibration(**kwargs) -> Dict

## Termal & Akışkan
- [ ] core/production/fan_selection.py      → Soğutma fanı seçimi (CFM, noise) | def select_cooling_fan(**kwargs) -> Dict
- [ ] core/production/pipe_flow.py          → Boru akış (Reynolds, basınç düşümü) | def calculate_pipe_flow(**kwargs) -> Dict

## Elektro-Mekanik
- [ ] core/production/solenoid_design.py    → Solenoid kuvvet, flyback diode | def design_solenoid(**kwargs) -> Dict
- [ ] core/production/linear_actuator.py    → Lineer aktüatör seçimi | def select_linear_actuator(**kwargs) -> Dict
- [ ] core/production/encoder_resolution.py → Rotary/Linear encoder çözünürlük | def calculate_encoder_resolution(**kwargs) -> Dict

## Kutu & Konnektör
- [ ] core/production/enclosure_ip.py       → IP koruma sınıfı tasarım gereksinimleri | def check_ip_rating_requirements(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# COMPUTER — Yazılım Mühendisliği (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Backend & API

## Veritabanı
- [ ] core/computer/nosql_model.py          → NoSQL veri modeli tasarımı | def design_nosql_model(**kwargs) -> Dict
- [ ] core/computer/query_optimizer.py      → SQL EXPLAIN, index önerisi, N+1 tespit | def optimize_sql_query(**kwargs) -> Dict
- [ ] core/computer/data_pipeline.py        → ETL/ELT data pipeline DAG tasarımı | def design_data_pipeline(**kwargs) -> Dict

## DevOps & Altyapı
- [ ] core/computer/monitoring_stack.py     → Prometheus + Grafana config üreteci | def generate_monitoring_stack(**kwargs) -> Dict
- [ ] core/computer/log_aggregation.py      → ELK/Loki log toplama pipeline config | def generate_log_pipeline(**kwargs) -> Dict


## Frontend & UI
- [ ] core/computer/component_lib.py        → React/Vue/Svelte component scaffold | def generate_ui_component(**kwargs) -> Dict
- [ ] core/computer/responsive_layout.py    → Responsive grid/flexbox layout config | def generate_responsive_layout(**kwargs) -> Dict
- [ ] core/computer/design_tokens.py        → Design system token JSON/CSS üreteci | def generate_design_tokens(**kwargs) -> Dict
- [ ] core/computer/accessibility_audit.py  → WCAG 2.1 AA erişilebilirlik kontrol | def audit_accessibility(**kwargs) -> Dict

## Mimari & Tasarım
- [ ] core/computer/system_design.py        → Sistem tasarımı hesap makinesi | def estimate_system_design(**kwargs) -> Dict
- [ ] core/computer/event_driven.py         → Event-driven topic/queue tasarımı | def design_event_driven_arch(**kwargs) -> Dict
- [ ] core/computer/saga_orchestrator.py    → Distributed saga state machine | def design_saga_pattern(**kwargs) -> Dict
- [ ] core/computer/cqrs_scaffold.py        → CQRS + Event Sourcing scaffold | def generate_cqrs_scaffold(**kwargs) -> Dict

## Mobil
- [ ] core/computer/mobile_scaffold.py      → Flutter/React Native proje scaffold | def generate_mobile_scaffold(**kwargs) -> Dict
- [ ] core/computer/push_notification.py    → FCM/APNs push notification config | def generate_push_config(**kwargs) -> Dict
- [ ] core/computer/app_signing.py          → Android/iOS sertifika yönetimi | def generate_app_signing_config(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# ENGINE — Agent Orkestrasyon (15 yeni modül)
# ──────────────────────────────────────────────────────────────────────

- [ ] core/engine/tool_registry.py          → Dinamik tool registration & discovery | def register_tool(**kwargs) -> Dict
- [ ] core/engine/agent_memory_index.py     → Vektör tabanlı agent long-term memory | def index_agent_memory(**kwargs) -> Dict
- [ ] core/engine/multi_model_router.py     → Çoklu LLM model router | def route_to_best_model(**kwargs) -> Dict
- [ ] core/engine/eval_harness.py           → Agent yanıt kalitesi değerlendirme | def evaluate_agent_response(**kwargs) -> Dict
- [ ] core/engine/conversation_brancher.py  → Konuşma dallanma, paralel yol deneme | def branch_conversation(**kwargs) -> Dict
- [ ] core/engine/rollback_engine.py        → Agent aksiyon rollback (geri alma) | def rollback_agent_action(**kwargs) -> Dict
- [ ] core/engine/ab_testing.py             → Prompt A/B testing framework | def run_prompt_ab_test(**kwargs) -> Dict
- [ ] core/engine/human_in_loop.py          → Human-in-the-loop onay gateway | def request_human_approval(**kwargs) -> Dict
- [ ] core/engine/streaming_output.py       → Token-by-token streaming output | def stream_output(**kwargs) -> Dict
- [ ] core/engine/context_window.py         → Context window yönetimi (summarize) | def manage_context_window(**kwargs) -> Dict
- [ ] core/engine/agent_sandbox.py          → Güvenli Python exec sandbox | def execute_in_sandbox(**kwargs) -> Dict
- [ ] core/engine/skill_composer.py         → Meta-skill compose framework | def compose_skills(**kwargs) -> Dict
- [ ] core/engine/feedback_loop.py          → Kullanıcı feedback toplama pipeline | def collect_feedback(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# INFRA — Altyapı & Utility (10 yeni modül)
# ──────────────────────────────────────────────────────────────────────

- [ ] core/infra/feature_flags.py           → Feature flag yönetimi (on/off, rollout) | def check_feature_flag(**kwargs) -> Dict


- [ ] core/infra/audit_logger.py            → Immutable audit log (compliance ready) | def log_audit_event(**kwargs) -> Dict
- [ ] core/infra/config_validator.py        → YAML/JSON/TOML schema validation | def validate_config(**kwargs) -> Dict
- [ ] core/infra/file_watcher.py            → Dosya sistemi değişiklik izleme | def watch_file_changes(**kwargs) -> Dict
- [ ] core/infra/perf_benchmark.py          → Micro-benchmark runner | def run_benchmark(**kwargs) -> Dict
- [ ] core/infra/data_anonymizer.py         → PII/KVKK veri anonimleştirme | def anonymize_data(**kwargs) -> Dict


# ══════════════════════════════════════════════════════════════════════
# TOPLAM: 126 yeni modül
# Mevcut: 129 modül
# Hedef: ~255 modül
# ══════════════════════════════════════════════════════════════════════
