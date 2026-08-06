#!/usr/bin/env bash
# Pure Shell Token Tracer Utility for Linux, macOS & Git Bash / WSL
# Uses native sqlite3 and shell commands - no python required!

DB_PATH="subagent_tracker/backend/tracker.db"

if [ ! -f "$DB_PATH" ]; then
    echo "⚠️ Veritabanı bulunamadı: $DB_PATH"
    exit 1
fi

case "$1" in
    stats)
        echo "===================================================="
        echo "  ⚡ SHELL TRACER - TOPLAM ÖZET "
        echo "===================================================="
        sqlite3 -header -column "$DB_PATH" "
            SELECT 
                COUNT(*) as Total_Calls,
                SUM(prompt_tokens) as Prompt_Tokens,
                SUM(completion_tokens) as Output_Tokens,
                SUM(total_tokens) as Total_Tokens,
                PRINTF('$%.6f', SUM(estimated_cost_usd)) as Total_Cost_USD,
                PRINTF('%.1f ms', AVG(execution_time_ms)) as Avg_Latency
            FROM agentlog;
        "
        echo ""
        echo "🤖 AGENT BAZLI DAĞILIM"
        echo "----------------------------------------------------"
        sqlite3 -header -column "$DB_PATH" "
            SELECT 
                UPPER(agent_name) as Agent,
                COUNT(*) as Calls,
                SUM(total_tokens) as Tokens,
                PRINTF('$%.6f', SUM(estimated_cost_usd)) as Cost,
                PRINTF('%.1f ms', AVG(execution_time_ms)) as Latency
            FROM agentlog
            GROUP BY agent_name
            ORDER BY Tokens DESC;
        "
        ;;
    logs)
        LIMIT=${2:-10}
        echo "===================================================="
        echo "  📜 SON $LIMIT LOG KAYDI (Shell Query)"
        echo "===================================================="
        sqlite3 -header -column "$DB_PATH" "
            SELECT 
                id as ID,
                DATETIME(created_at) as Time,
                agent_name as Agent,
                model_name as Model,
                prompt_tokens as Prompt,
                completion_tokens as Output,
                total_tokens as Total,
                PRINTF('$%.6f', estimated_cost_usd) as Cost,
                PRINTF('%.1f ms', execution_time_ms) as Latency
            FROM agentlog
            ORDER BY id DESC
            LIMIT $LIMIT;
        "
        ;;
    watch)
        INTERVAL=${2:-2}
        echo "👀 Canlı Shell İzleme Başlatıldı (Yenileme: ${INTERVAL}sn)... Çıkış için Ctrl+C"
        sleep 1
        while true; do
            clear
            date
            "$0" stats
            echo ""
            "$0" logs 5
            sleep $INTERVAL
        done
        ;;
    csv)
        OUT_FILE=${2:-"token_trace_export.csv"}
        sqlite3 -header -csv "$DB_PATH" "SELECT * FROM agentlog;" > "$OUT_FILE"
        echo "✅ CSV Raporu başarıyla oluşturuldu: $OUT_FILE"
        ;;
    *)
        echo "Kullanım: ./tracer.sh {stats|logs|watch|csv}"
        echo "  ./tracer.sh stats      -> İstatistik özetini gösterir"
        echo "  ./tracer.sh logs [N]   -> Son N adet log kaydını listeler"
        echo "  ./tracer.sh watch [N]  -> N saniyede bir otomatik yenilenen canlı izleme"
        echo "  ./tracer.sh csv [dosya]-> CSV formatında rapor alır"
        ;;
esac
