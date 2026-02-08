"""
api_config.py — Configurações de API para envio via Twilio
Para usar o Twilio WhatsApp Business API, siga os passos:
1. Crie conta em: https://www.twilio.com/
2. Configure um número WhatsApp Business (Sandbox para testes)
3. Coloque suas credenciais no arquivo .env
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# ============================================================
#  CONFIGURAÇÕES TWILIO (carregadas do .env)
# ============================================================

# Credenciais do Twilio (configure no arquivo .env)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

# ============================================================
#  MÉTODO DE ENVIO
# ============================================================
# Escolha o método padrão:
#   "pywhatkit" → Usa WhatsApp Web (navegador, usa SEU número logado)
#   "twilio"    → Usa API Twilio (envia de outro número configurado)
METODO_ENVIO = os.getenv("METODO_ENVIO", "pywhatkit")  # Padrão: pywhatkit


# ============================================================
#  VALIDAÇÃO
# ============================================================
def validar_config_twilio() -> bool:
    """Verifica se as credenciais do Twilio foram configuradas."""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_FROM_NUMBER:
        print("❌ Configure as credenciais do Twilio em api_config.py")
        return False
    if not TWILIO_FROM_NUMBER.startswith("whatsapp:"):
        print("❌ TWILIO_FROM_NUMBER deve começar com 'whatsapp:'")
        return False
    return True
