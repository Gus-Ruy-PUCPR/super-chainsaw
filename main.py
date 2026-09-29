from ics import Calendar, Event

cal = Calendar()
event = Event()

event.name = "🚨 Entrega: Atividade de Teste"
event.description = "Lembrete de entrega gerado pelo Bot do AVA."

# Formato ISO com fuso horário do Brasil (-03:00)
event.begin = "2026-10-15T23:59:00-03:00"
event.end = "2026-10-16T00:00:00-03:00"

cal.events.add(event)

# CORREÇÃO: newline='' impede o Windows de corromper a quebra de linha
# e usamos cal.serialize() direto no write()
with open("atividades_pucpr.ics", "w", encoding="utf-8", newline='') as f:
    f.write(cal.serialize())

print("✅ Arquivo gerado com formatação estrita para celular!")