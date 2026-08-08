# 🧠 Agent System — Eklenecek Script'ler TODO Listesi
# Bu dosya, Gemini ile eklenecek tüm eksik modüllerin referans listesidir.
# Her modül için: dosya yolu, açıklama ve ana fonksiyon adı belirtilmiştir.
# ═══════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────
# HARDWARE — Elektronik & PCB (31 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Güç Elektroniği

## Analog & Sinyal İşleme

## Dijital & Haberleşme

## Sensör & Ölçüm

## PCB İleri Seviye

## Koruma & Güvenlik


# ──────────────────────────────────────────────────────────────────────
# SOFTWARE — Gömülü Yazılım & Firmware (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## RTOS & Çekirdek

## Haberleşme Protokolleri

## Güvenlik & Kriptografi

## Veri & Depolama

## Test & Kalite

## DSP & Kontrol

# ──────────────────────────────────────────────────────────────────────
# PRODUCTION / MEKANİK (20 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## 3D Baskı & İmalat

## Mekanik Analiz

## Termal & Akışkan

## Elektro-Mekanik

## Kutu & Konnektör

# ──────────────────────────────────────────────────────────────────────
# COMPUTER — Yazılım Mühendisliği (25 yeni modül)
# ──────────────────────────────────────────────────────────────────────

## Backend & API

## Veritabanı

## DevOps & Altyapı

## Frontend & UI

## Mimari & Tasarım

## Mobil


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
