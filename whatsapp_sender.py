"""
whatsapp_sender.py — Módulo de envio de mensagens via WhatsApp
Suporta dois métodos:
  1. pywhatkit → WhatsApp Web (usa número logado no navegador)
  2. Twilio API → Envia de outro número (requer configuração)

Otimizado para Raspberry Pi com lazy loading de importações
"""

import time
from config import INTERVALO_ENTRE_MSGS, TEMPO_FECHAR_ABA
from api_config import (
    METODO_ENVIO,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    validar_config_twilio,
)

# Lazy loading - importar apenas quando necessário
_pywhatkit = None
_twilio_client = None


def _get_pywhatkit():
    """Lazy import do pywhatkit."""
    global _pywhatkit
    if _pywhatkit is None:
        import pywhatkit as kit
        _pywhatkit = kit
    return _pywhatkit


def _get_twilio_client():
    """Lazy import e criação do cliente Twilio."""
    global _twilio_client
    if _twilio_client is None:
        from twilio.rest import Client
        _twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return _twilio_client


def enviar_via_pywhatkit(telefone: str, mensagem: str, espera: int = INTERVALO_ENTRE_MSGS) -> bool:
    """Envia mensagem via WhatsApp Web (pywhatkit)."""
    try:
        kit = _get_pywhatkit()
        print(f"📤 Enviando para {telefone} via WhatsApp Web...")
        kit.sendwhatmsg_instantly(
            phone_no=telefone,
            message=mensagem,
            wait_time=espera,
            tab_close=True,
            close_time=TEMPO_FECHAR_ABA,
        )
        print(f"  ✅ Mensagem enviada para {telefone}")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao enviar para {telefone}: {e}")
        return False


def enviar_via_twilio(telefone: str, mensagem: str) -> bool:
    """Envia mensagem via Twilio API."""
    try:
        client = _get_twilio_client()

        # Formatar telefone para Twilio (whatsapp:+5511999999999)
        if not telefone.startswith("whatsapp:"):
            telefone_twilio = f"whatsapp:{telefone}"
        else:
            telefone_twilio = telefone

        message = client.messages.create(
            from_=TWILIO_FROM_NUMBER,
            body=mensagem,
            to=telefone_twilio
        )

        print(f"  ✅ Mensagem enviada para {telefone} (SID: {message.sid})")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao enviar para {telefone}: {e}")
        return False


def enviar_mensagem(telefone: str, mensagem: str, metodo: str = None) -> bool:
    """
    Envia uma mensagem para o número informado.

    Args:
        telefone: Número no formato +5511999999999
        mensagem: Texto da mensagem
        metodo: "pywhatkit" ou "twilio" (usa METODO_ENVIO se None)

    Returns:
        True se enviou sem erro, False caso contrário
    """
    metodo = metodo or METODO_ENVIO

    if metodo == "twilio":
        if not validar_config_twilio():
            return False
        return enviar_via_twilio(telefone, mensagem)
    else:
        return enviar_via_pywhatkit(telefone, mensagem)


def enviar_para_jogadores(jogadores: list, intervalo_extra: float = 3.0, metodo: str = None) -> dict:
    """
    Envia a mensagem personalizada para cada jogador da lista.

    Args:
        jogadores: Lista de objetos Jogador (com .telefone e .mensagem)
        intervalo_extra: Segundos extras entre envios para não travar
        metodo: "pywhatkit" ou "twilio" (usa METODO_ENVIO se None)

    Returns:
        Dicionário com resultado: {"enviados": [...], "falhas": [...]}
    """
    metodo = metodo or METODO_ENVIO
    resultado = {"enviados": [], "falhas": []}

    print(f"\n🔧 Método de envio: {metodo.upper()}")
    if metodo == "twilio" and not validar_config_twilio():
        print("❌ Configure api_config.py primeiro!")
        return resultado

    total = len(jogadores)
    for i, jogador in enumerate(jogadores, 1):
        print(f"\n--- [{i}/{total}] {jogador.nome} ({jogador.telefone}) ---")
        sucesso = enviar_mensagem(jogador.telefone, jogador.mensagem, metodo)

        if sucesso:
            resultado["enviados"].append(jogador)
        else:
            resultado["falhas"].append(jogador)

        # Esperar entre envios (só para pywhatkit)
        if i < total and metodo == "pywhatkit":
            print(f"⏳ Aguardando {intervalo_extra}s antes do próximo envio...")
            time.sleep(intervalo_extra)
        elif i < total and metodo == "twilio":
            # Twilio é mais rápido, apenas pequena pausa
            time.sleep(0.5)

    return resultado


def exibir_resultado_envio(resultado: dict):
    """Exibe um resumo dos envios."""
    print("\n" + "=" * 50)
    print("📊 RESULTADO DO ENVIO")
    print("=" * 50)
    print(f"✅ Enviados com sucesso: {len(resultado['enviados'])}")
    for j in resultado["enviados"]:
        print(f"   • {j.nome} ({j.telefone})")

    if resultado["falhas"]:
        print(f"\n❌ Falhas no envio: {len(resultado['falhas'])}")
        for j in resultado["falhas"]:
            print(f"   • {j.nome} ({j.telefone})")
    print("=" * 50)
