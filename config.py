# ============================================================
#  Configurações do Jogo do Impostor — WhatsApp Bot
# ============================================================

# Tempo de espera (segundos) entre o envio de cada mensagem.
# O pywhatkit abre o WhatsApp Web, então precisa de um intervalo
# para não travar. Ajuste conforme sua internet.
INTERVALO_ENTRE_MSGS = 15        # segundos de espera após abrir o WhatsApp Web
TEMPO_FECHAR_ABA = 5             # segundos para fechar a aba após enviar

# Categorias de palavras para o jogo.
# Formato: { "categoria": ["palavra1", "palavra2", ...] }
CATEGORIAS_PALAVRAS = {
    "Animais": [
        ("Cachorro", "Gato"),
        ("Leão", "Tigre"),
        ("Águia", "Falcão"),
        ("Tubarão", "Baleia"),
        ("Cobra", "Lagarto"),
        ("Cavalo", "Burro"),
        ("Elefante", "Rinoceronte"),
        ("Macaco", "Gorila"),
    ],
    "Comidas": [
        ("Pizza", "Esfiha"),
        ("Hambúrguer", "Sanduíche"),
        ("Sushi", "Sashimi"),
        ("Bolo", "Torta"),
        ("Sorvete", "Açaí"),
        ("Churrasco", "Parrilla"),
        ("Lasanha", "Macarrão"),
        ("Coxinha", "Risole"),
    ],
    "Profissões": [
        ("Médico", "Enfermeiro"),
        ("Advogado", "Juiz"),
        ("Professor", "Tutor"),
        ("Bombeiro", "Policial"),
        ("Engenheiro", "Arquiteto"),
        ("Piloto", "Comissário"),
        ("Cozinheiro", "Padeiro"),
        ("Dentista", "Ortodontista"),
    ],
    "Lugares": [
        ("Praia", "Piscina"),
        ("Shopping", "Mercado"),
        ("Cinema", "Teatro"),
        ("Hospital", "Clínica"),
        ("Escola", "Faculdade"),
        ("Parque", "Praça"),
        ("Aeroporto", "Rodoviária"),
        ("Igreja", "Templo"),
    ],
    "Esportes": [
        ("Futebol", "Futsal"),
        ("Basquete", "Vôlei"),
        ("Natação", "Mergulho"),
        ("Tênis", "Badminton"),
        ("Boxe", "MMA"),
        ("Skate", "Patins"),
        ("Surfe", "Bodyboard"),
        ("Corrida", "Ciclismo"),
    ],
}

# Mensagem enviada para os jogadores NORMAIS (não‑impostores).
# Use {palavra} como placeholder — será substituído pela palavra real.
MSG_JOGADOR_NORMAL = (
    "🎮 *JOGO DO IMPOSTOR* 🎮\n\n"
    "Você é um *CIDADÃO* ✅\n\n"
    "Sua palavra é: *{palavra}*\n\n"
    "⚠️ Não mostre essa mensagem para ninguém!\n"
    "Tente descobrir quem é o impostor sem revelar a palavra."
)

# Mensagem enviada para o IMPOSTOR.
# Use {palavra} como placeholder — pode ser uma dica ou palavra diferente.
MSG_IMPOSTOR = (
    "🎮 *JOGO DO IMPOSTOR* 🎮\n\n"
    "Você é o *IMPOSTOR* 🔴\n\n"
    "Sua palavra é: *{palavra}*\n\n"
    "⚠️ Não mostre essa mensagem para ninguém!\n"
    "Tente se misturar com os outros sem ser descoberto.\n"
    "Dica: a palavra dos outros é parecida com a sua!"
)

# Mensagem enviada para o IMPOSTOR quando ele NÃO recebe palavra.
MSG_IMPOSTOR_SEM_PALAVRA = (
    "🎮 *JOGO DO IMPOSTOR* 🎮\n\n"
    "Você é o *IMPOSTOR* 🔴\n\n"
    "Você *NÃO* recebeu nenhuma palavra!\n\n"
    "⚠️ Não mostre essa mensagem para ninguém!\n"
    "Tente se misturar com os outros e descobrir qual é a palavra."
)
