# ============================================================
#  Configurações do Jogo do Infiltrado — WhatsApp Bot
# ============================================================

# Tempo de espera (segundos) entre o envio de cada mensagem.
# O pywhatkit abre o WhatsApp Web, então precisa de um intervalo
# para não travar. Ajuste conforme sua internet.
INTERVALO_ENTRE_MSGS = 15        # segundos de espera após abrir o WhatsApp Web
TEMPO_FECHAR_ABA = 5             # segundos para fechar a aba após enviar

# ============================================================
#  PERGUNTAS DO JOGO
# ============================================================
# Formato: { "categoria": [(pergunta_normal, instrucao_infiltrado), ...] }
# - pergunta_normal: A pergunta que todos os jogadores normais recebem
# - instrucao_infiltrado: A instrução especial que o infiltrado recebe

CATEGORIAS_PERGUNTAS = {
    "Números": [
        ("Quanto você consegue levantar no supino? (em kg)", "Escolha um número entre 1 e 50"),
        ("Quantas flexões você consegue fazer seguidas?", "Escolha um número entre 5 e 30"),
        ("Qual sua altura? (em cm)", "Escolha um número entre 150 e 200"),
        ("Quantos anos você tem?", "Escolha um número entre 18 e 40"),
        ("Quantas horas você dorme por dia?", "Escolha um número entre 4 e 10"),
        ("Quantos quilômetros você consegue correr?", "Escolha um número entre 1 e 15"),
    ],
    "Preferências": [
        ("Qual seu filme favorito?", "Invente um nome de filme"),
        ("Qual sua comida preferida?", "Escolha uma comida exótica"),
        ("Qual sua cor favorita?", "Escolha entre: roxo, turquesa ou magenta"),
        ("Qual seu hobby favorito?", "Invente um hobby inusitado"),
        ("Qual série você está assistindo?", "Invente um nome de série"),
    ],
    "Opiniões": [
        ("De 0 a 10, quanto você gosta de pizza?", "Escolha um número entre 0 e 5"),
        ("De 0 a 10, qual a probabilidade de você estar mentindo agora?", "Escolha um número entre 6 e 10"),
        ("De 0 a 10, quanto você gostaria de viajar para Marte?", "Escolha um número entre 0 e 4"),
        ("Quantos filhos você quer ter no futuro?", "Escolha um número entre 5 e 10"),
    ],
    "Experiências": [
        ("Quantos países você já visitou?", "Escolha um número entre 10 e 25"),
        ("Quantas vezes você já andou de montanha-russa?", "Escolha um número entre 0 e 3"),
        ("Qual foi a última vez que você chorou?", "Responda: Semana passada"),
        ("Quantos relacionamentos sérios você já teve?", "Escolha um número entre 5 e 12"),
    ],
}

# LEGACY: Mantido para compatibilidade (pode remover depois)
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

# ============================================================
#  MENSAGENS DO JOGO
# ============================================================

# Mensagem enviada para os jogadores NORMAIS
# Use {pergunta} como placeholder
MSG_JOGADOR_NORMAL = (
    "🎮 *JOGO DO INFILTRADO* 🎮\n\n"
    "📝 Sua pergunta:\n"
    "*{pergunta}*\n\n"
    "⚠️ Responda com SINCERIDADE!\n"
    "Um dos jogadores recebeu uma instrução diferente.\n"
    "Depois envie sua resposta de volta para este número."
)

# Mensagem enviada para o INFILTRADO
# Use {instrucao} como placeholder
MSG_INFILTRADO = (
    "🎮 *JOGO DO INFILTRADO* 🎮\n\n"
    "🔴 *VOCÊ É O INFILTRADO!*\n\n"
    "📝 Sua instrução:\n"
    "*{instrucao}*\n\n"
    "⚠️ Não revele que você é o infiltrado!\n"
    "Responda de forma convincente para parecer normal.\n"
    "Depois envie sua resposta de volta para este número."
)

# Mensagem com o resultado final
MSG_RESULTADO = (
    "🎯 *RESULTADO DO JOGO* 🎯\n\n"
    "📊 *RESPOSTAS DE TODOS:*\n"
    "{respostas}\n\n"
    "❓ *PERGUNTA NORMAL:*\n{pergunta}\n\n"
    "🔴 *INSTRUÇÃO DO INFILTRADO:*\n{instrucao}\n\n"
    "👤 *O INFILTRADO ERA:* {infiltrado}\n\n"
    "Conseguiram descobrir? 🤔"
)
