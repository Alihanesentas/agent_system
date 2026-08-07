# 🧠 Agent System — Eklenecek Script'ler TODO Listesi
# Bu dosya, Gemini ile eklenecek tüm eksik modüllerin referans listesidir.
# Her modül için: dosya yolu, açıklama ve ana fonksiyon adı belirtilmiştir.
# ═══════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────
# HARDWARE — Elektronik & PCB (31 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Güç Elektroniği
- [ ] core/hardware/smps_design.py          → Buck/Boost SMPS indüktör, MOSFET, verim hesabı | def design_smps_converter(**kwargs) -> Dict
- [ ] core/hardware/ldo_thermal.py          → LDO ısı, dropout voltaj, quiescent current | def analyze_ldo_thermal(**kwargs) -> Dict
- [ ] core/hardware/power_budget.py         → Sistem güç bütçesi tablosu (tüm IC mA çekimi) | def calculate_power_budget(**kwargs) -> Dict
- [ ] core/hardware/voltage_divider.py      → Hassas voltaj bölücü direnç çifti hesabı | def calculate_voltage_divider(**kwargs) -> Dict
- [ ] core/hardware/mosfet_driver.py        → High/Low-side MOSFET sürücü, gate charge, switching loss | def design_mosfet_driver(**kwargs) -> Dict
- [ ] core/hardware/psu_ripple.py           → Güç kaynağı ripple/noise, filtre kapasitör boyutlandırma | def analyze_psu_ripple(**kwargs) -> Dict

## Analog & Sinyal İşleme
- [ ] core/hardware/opamp_circuit.py        → Op-Amp topolojileri, kazanç, bant genişliği | def calculate_opamp_circuit(**kwargs) -> Dict
- [ ] core/hardware/adc_snr.py              → ADC SNR, ENOB, quantization noise analizi | def analyze_adc_performance(**kwargs) -> Dict
- [ ] core/hardware/filter_design.py        → Aktif/pasif filtre tasarımı (Butterworth, Chebyshev) | def design_analog_filter(**kwargs) -> Dict
- [ ] core/hardware/dac_output.py           → DAC çıkış tampon, settling time | def design_dac_output(**kwargs) -> Dict
- [ ] core/hardware/current_sense.py        → Shunt akım ölçüm devresi, INA amplifikatör | def design_current_sense(**kwargs) -> Dict

## Dijital & Haberleşme
- [ ] core/hardware/uart_config.py          → UART baud rate, parity, hata oranı | def configure_uart(**kwargs) -> Dict
- [ ] core/hardware/spi_timing.py           → SPI bus timing, clock phase/polarity | def analyze_spi_timing(**kwargs) -> Dict
- [ ] core/hardware/i2c_pullup.py           → I2C pull-up direnç hesabı (bus kapasitansı) | def calculate_i2c_pullup(**kwargs) -> Dict
- [ ] core/hardware/can_bus.py              → CAN bus termination, bit timing | def configure_can_bus(**kwargs) -> Dict
- [ ] core/hardware/usb_impedance.py        → USB 2.0/3.0 diferansiyel empedans kontrolü | def check_usb_impedance(**kwargs) -> Dict
- [ ] core/hardware/ethernet_magnetics.py   → Ethernet magnetics seçimi, PoE güç hesabı | def design_ethernet_interface(**kwargs) -> Dict
- [ ] core/hardware/lvds_serdes.py          → LVDS/SerDes sinyal bütünlüğü | def analyze_lvds_signal(**kwargs) -> Dict

## Sensör & Ölçüm
- [ ] core/hardware/sensor_interface.py     → Sıcaklık/basınç/ivme sensör arayüz devresi | def design_sensor_interface(**kwargs) -> Dict
- [ ] core/hardware/wheatstone_bridge.py    → Wheatstone köprü, strain gauge, load cell | def calculate_wheatstone_bridge(**kwargs) -> Dict
- [ ] core/hardware/thermocouple.py         → Termokupl tipi seçimi, cold junction komp. | def design_thermocouple_interface(**kwargs) -> Dict

## PCB İleri Seviye
- [ ] core/hardware/via_current.py          → Via akım kapasitesi, thermal via array | def calculate_via_current(**kwargs) -> Dict
- [ ] core/hardware/crosstalk_analysis.py   → PCB crosstalk (NEXT/FEXT), guard trace | def analyze_pcb_crosstalk(**kwargs) -> Dict
- [ ] core/hardware/pcb_cost_estimator.py   → PCB üretim maliyet tahmini | def estimate_pcb_cost(**kwargs) -> Dict
- [ ] core/hardware/impedance_calculator.py → Microstrip/Stripline/Coplanar empedans | def calculate_trace_impedance_advanced(**kwargs) -> Dict
- [ ] core/hardware/panelization.py         → PCB panelizasyon yerleşim optimizasyonu | def optimize_pcb_panel(**kwargs) -> Dict
- [ ] core/hardware/gerber_checker.py       → Gerber dosya bütünlük kontrolü | def validate_gerber_files(**kwargs) -> Dict
- [ ] core/hardware/pcb_thermal_relief.py   → Thermal relief pad pattern, spoke hesabı | def calculate_thermal_relief(**kwargs) -> Dict

## Koruma & Güvenlik
- [ ] core/hardware/esd_protection.py       → ESD koruma, TVS diode seçimi, IEC 61000 | def design_esd_protection(**kwargs) -> Dict
- [ ] core/hardware/fuse_sizing.py          → Sigorta boyutlandırma (I²t), PTC fuse | def calculate_fuse_sizing(**kwargs) -> Dict
- [ ] core/hardware/reverse_polarity.py     → Ters polarite koruma devresi | def design_reverse_polarity_protection(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# SOFTWARE — Gömülü Yazılım & Firmware (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## RTOS & Çekirdek
- [ ] core/software/rtos_task_design.py     → FreeRTOS task priority, stack, CPU util | def design_rtos_tasks(**kwargs) -> Dict
- [ ] core/software/isr_latency.py          → ISR latency analizi, nested interrupt | def analyze_isr_latency(**kwargs) -> Dict
- [ ] core/software/mutex_deadlock.py       → Mutex deadlock tespit, priority inversion | def detect_mutex_deadlock(**kwargs) -> Dict
- [ ] core/software/memory_pool.py          → Statik bellek havuzu boyutlandırma | def design_memory_pool(**kwargs) -> Dict
- [ ] core/software/scheduler_sim.py        → Rate Monotonic / EDF zamanlama simülasyonu | def simulate_scheduler(**kwargs) -> Dict

## Haberleşme Protokolleri
- [ ] core/software/modbus_gen.py           → Modbus RTU/TCP register haritası üreteci | def generate_modbus_map(**kwargs) -> Dict
- [ ] core/software/mqtt_topic.py           → MQTT topic hierarchy, QoS konfigürasyon | def generate_mqtt_config(**kwargs) -> Dict
- [ ] core/software/protobuf_gen.py         → Protocol Buffers schema → C struct | def generate_protobuf_schema(**kwargs) -> Dict
- [ ] core/software/ble_gatt.py             → BLE GATT service/characteristic tanımlama | def generate_ble_gatt_profile(**kwargs) -> Dict
- [ ] core/software/lorawan_params.py       → LoRaWAN SF, BW, link budget, airtime | def calculate_lorawan_params(**kwargs) -> Dict
- [ ] core/software/zigbee_mesh.py          → Zigbee mesh topolojisi, routing table | def design_zigbee_mesh(**kwargs) -> Dict

## Güvenlik & Kriptografi
- [ ] core/software/secure_boot.py          → Secure boot chain konfigürasyon üreteci | def configure_secure_boot(**kwargs) -> Dict
- [ ] core/software/crypto_engine.py        → AES/RSA/ECDSA anahtar boyutlandırma | def design_crypto_params(**kwargs) -> Dict
- [ ] core/software/cert_manager.py         → X.509 sertifika zinciri, TLS mutual auth | def generate_cert_config(**kwargs) -> Dict

## Veri & Depolama
- [ ] core/software/fatfs_config.py         → FAT/LittleFS konfigürasyonu, wear leveling | def configure_filesystem(**kwargs) -> Dict
- [ ] core/software/eeprom_wear.py          → EEPROM/Flash wear leveling ömür analizi | def analyze_eeprom_wear(**kwargs) -> Dict
- [ ] core/software/ring_buffer.py          → Lock-free ring buffer boyutlandırma | def design_ring_buffer(**kwargs) -> Dict
- [ ] core/software/log_framework.py        → Gömülü log framework (severity, circular) | def generate_log_framework(**kwargs) -> Dict

## Test & Kalite
- [ ] core/software/unit_test_scaffold.py   → Unity/CMock C unit test scaffold üreteci | def generate_unit_test_scaffold(**kwargs) -> Dict
- [ ] core/software/misra_checker.py        → MISRA-C:2012 kural ihlali analizi | def check_misra_compliance(**kwargs) -> Dict
- [ ] core/software/code_size_analyzer.py   → .map file parser, RAM/ROM/Flash istatistik | def analyze_code_size(**kwargs) -> Dict
- [ ] core/software/firmware_diff.py        → İki firmware binary section-level diff | def diff_firmware_binaries(**kwargs) -> Dict

## DSP & Kontrol
- [ ] core/software/pid_tuner.py            → PID parametre ayarlama (Ziegler-Nichols) | def tune_pid_controller(**kwargs) -> Dict
- [ ] core/software/fir_iir_filter.py       → FIR/IIR dijital filtre katsayı hesaplama | def design_digital_filter(**kwargs) -> Dict
- [ ] core/software/fft_analyzer.py         → FFT pencere, frekans çözünürlüğü, aliasing | def analyze_fft_params(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# PRODUCTION / MEKANİK (20 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## 3D Baskı & İmalat
- [ ] core/production/print_cost.py         → 3D baskı maliyet tahmini (gram, süre, kwh) | def estimate_3d_print_cost(**kwargs) -> Dict
- [ ] core/production/print_settings.py     → Malzeme bazlı optimum baskı ayarları | def recommend_print_settings(**kwargs) -> Dict
- [ ] core/production/tolerance_stack.py    → Tolerans yığılma analizi (worst case / RSS) | def analyze_tolerance_stack(**kwargs) -> Dict
- [ ] core/production/injection_mold.py     → Enjeksiyon kalıp parametreleri (shrinkage) | def estimate_injection_mold(**kwargs) -> Dict
- [ ] core/production/cnc_feedrate.py       → CNC freze besleme hızı, devir hesabı | def calculate_cnc_feedrate(**kwargs) -> Dict
- [ ] core/production/sheet_metal.py        → Sac metal bükme (K-factor, bend allowance) | def calculate_sheet_metal_bend(**kwargs) -> Dict

## Mekanik Analiz
- [ ] core/production/beam_stress.py        → Kiriş eğilme moment, kesme, sehim | def analyze_beam_stress(**kwargs) -> Dict
- [ ] core/production/bolt_torque.py        → Cıvata tork hesabı (VDI 2230) | def calculate_bolt_torque(**kwargs) -> Dict
- [ ] core/production/spring_design.py      → Yay tasarımı (helisel basma/çekme/burulma) | def design_spring(**kwargs) -> Dict
- [ ] core/production/gear_ratio.py         → Dişli çark oranı (modül, diş sayısı) | def calculate_gear_ratio(**kwargs) -> Dict
- [ ] core/production/bearing_life.py       → Rulman ömür hesabı (L10, dinamik yük) | def calculate_bearing_life(**kwargs) -> Dict
- [ ] core/production/vibration_analysis.py → Doğal frekans, titreşim izolasyon | def analyze_vibration(**kwargs) -> Dict

## Termal & Akışkan
- [ ] core/production/heatsink_design.py    → Kanatçıklı soğutucu boyutlandırma | def design_heatsink(**kwargs) -> Dict
- [ ] core/production/fan_selection.py      → Soğutma fanı seçimi (CFM, noise) | def select_cooling_fan(**kwargs) -> Dict
- [ ] core/production/pipe_flow.py          → Boru akış (Reynolds, basınç düşümü) | def calculate_pipe_flow(**kwargs) -> Dict

## Elektro-Mekanik
- [ ] core/production/motor_sizing.py       → DC/BLDC/Stepper motor boyutlandırma | def size_motor(**kwargs) -> Dict
- [ ] core/production/solenoid_design.py    → Solenoid kuvvet, flyback diode | def design_solenoid(**kwargs) -> Dict
- [ ] core/production/linear_actuator.py    → Lineer aktüatör seçimi | def select_linear_actuator(**kwargs) -> Dict
- [ ] core/production/encoder_resolution.py → Rotary/Linear encoder çözünürlük | def calculate_encoder_resolution(**kwargs) -> Dict

## Kutu & Konnektör
- [ ] core/production/enclosure_ip.py       → IP koruma sınıfı tasarım gereksinimleri | def check_ip_rating_requirements(**kwargs) -> Dict

# ──────────────────────────────────────────────────────────────────────
# COMPUTER — Yazılım Mühendisliği (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Backend & API
- [ ] core/computer/rest_api_gen.py         → REST API endpoint scaffold (FastAPI/Express) | def generate_rest_api_scaffold(**kwargs) -> Dict
- [ ] core/computer/graphql_schema.py       → GraphQL schema ve resolver scaffold | def generate_graphql_schema(**kwargs) -> Dict
- [ ] core/computer/auth_flow.py            → OAuth2/JWT/API Key auth flow config | def generate_auth_flow(**kwargs) -> Dict
- [ ] core/computer/rate_limit_design.py    → API rate limiting stratejisi tasarımı | def design_rate_limiter(**kwargs) -> Dict
- [ ] core/computer/websocket_handler.py    → WebSocket event handler scaffold | def generate_websocket_handler(**kwargs) -> Dict

## Veritabanı
- [ ] core/computer/sql_schema_gen.py       → SQL schema (DDL) üreteci | def generate_sql_schema(**kwargs) -> Dict
- [ ] core/computer/nosql_model.py          → NoSQL veri modeli tasarımı | def design_nosql_model(**kwargs) -> Dict
- [ ] core/computer/query_optimizer.py      → SQL EXPLAIN, index önerisi, N+1 tespit | def optimize_sql_query(**kwargs) -> Dict
- [ ] core/computer/data_pipeline.py        → ETL/ELT data pipeline DAG tasarımı | def design_data_pipeline(**kwargs) -> Dict

## DevOps & Altyapı
- [ ] core/computer/terraform_gen.py        → Terraform IaC modül scaffold | def generate_terraform_module(**kwargs) -> Dict
- [ ] core/computer/ci_cd_pipeline.py       → GitHub Actions / GitLab CI YAML üreteci | def generate_ci_cd_pipeline(**kwargs) -> Dict
- [ ] core/computer/nginx_config.py         → Nginx reverse proxy, SSL config | def generate_nginx_config(**kwargs) -> Dict
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

- [ ] core/engine/prompt_template.py        → Versiyon kontrollü prompt template engine | def render_prompt_template(**kwargs) -> Dict
- [ ] core/engine/chain_of_thought.py       → CoT / ToT reasoning framework | def run_chain_of_thought(**kwargs) -> Dict
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

- [ ] core/infra/env_manager.py             → .env dosya yönetimi, secret rotation | def manage_env_config(**kwargs) -> Dict
- [ ] core/infra/health_check.py            → HTTP/TCP/gRPC endpoint health probe | def run_health_check(**kwargs) -> Dict
- [ ] core/infra/retry_policy.py            → Konfigüre edilebilir retry policy | def execute_with_retry(**kwargs) -> Dict
- [ ] core/infra/feature_flags.py           → Feature flag yönetimi (on/off, rollout) | def check_feature_flag(**kwargs) -> Dict
- [ ] core/infra/audit_logger.py            → Immutable audit log (compliance ready) | def log_audit_event(**kwargs) -> Dict
- [ ] core/infra/config_validator.py        → YAML/JSON/TOML schema validation | def validate_config(**kwargs) -> Dict
- [ ] core/infra/cron_scheduler.py          → Cron job tanımlama ve çalıştırma | def schedule_cron_job(**kwargs) -> Dict
- [ ] core/infra/file_watcher.py            → Dosya sistemi değişiklik izleme | def watch_file_changes(**kwargs) -> Dict
- [ ] core/infra/perf_benchmark.py          → Micro-benchmark runner | def run_benchmark(**kwargs) -> Dict
- [ ] core/infra/data_anonymizer.py         → PII/KVKK veri anonimleştirme | def anonymize_data(**kwargs) -> Dict

# ══════════════════════════════════════════════════════════════════════
# TOPLAM: 126 yeni modül
# Mevcut: 129 modül
# Hedef: ~255 modül
# ══════════════════════════════════════════════════════════════════════
