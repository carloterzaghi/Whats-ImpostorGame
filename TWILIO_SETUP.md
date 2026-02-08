# 🚀 GUIA RÁPIDO — Configurar Twilio para enviar de outro número

## Por que usar Twilio?
- Envia WhatsApp de um **número Business** (não precisa ser o seu)
- Mais **rápido** que PyWhatKit (não abre navegador)
- Mais **profissional** e confiável
- **MAS**: É pago e requer configuração

---

## Passo 1: Criar conta Twilio

1. Acesse: https://www.twilio.com/try-twilio
2. Crie conta gratuita (ganha créditos para teste)
3. Confirme email e telefone

---

## Passo 2: Configurar WhatsApp Sandbox (Teste Grátis)

### O Sandbox permite testar ANTES de pagar:

1. No Twilio Console, vá em: **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Você verá um número Twilio (ex: `+1 415 523 8886`)
3. Você verá um código de ativação (ex: `join cotton-angle`)

### Ativar cada destinatário:
Cada pessoa que vai RECEBER mensagem precisa:
1. Adicionar o número Twilio nos contatos
2. Enviar via WhatsApp: `join SEU-CODIGO`
3. Receberá confirmação de ativação

⚠️ **Limitação**: Sandbox é APENAS para testes. Para produção, precisa aprovar número próprio.

---

## Passo 3: Pegar credenciais

No Twilio Console (https://console.twilio.com/):

1. Encontre **Account SID** (ex: `AC1234567890abcdef...`)
2. Encontre **Auth Token** (ex: `abcdef1234567890...`)
3. Anote o **número Twilio** (ex: `+14155238886`)

---

## Passo 4: Configurar arquivo .env

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
   (No Windows: `copy .env.example .env`)

2. Abra o arquivo `.env` e preencha com suas credenciais:

```bash
TWILIO_ACCOUNT_SID = "seu_account_sid_aqui"    # Cole seu Account SID
TWILIO_AUTH_TOKEN = "seu_auth_token_aqui"      # Cole seu Auth Token
TWILIO_FROM_NUMBER = "whatsapp:+14155238886"   # whatsapp: + número Twilio
METODO_ENVIO = "twilio"                        # Usar Twilio
```

⚠️ **Importante**: O arquivo `.env` contém suas credenciais privadas. Nunca faça commit dele no Git!

---

## Passo 5: Testar

1. Execute: `python main.py`
2. Adicione jogadores (números que já ativaram o Sandbox)
3. Use **Opção 8** para confirmar método = TWILIO
4. Use **Opção 7** (teste) para enviar

---

## 💰 Custos

### Modo Sandbox (Grátis):
- Créditos de teste gratuitos
- Limitado aos números que ativaram

### Produção (Pago):
- Requer **número próprio** aprovado pelo Facebook
- Custo: ~$0.005-0.01 por mensagem (varia por país)
- Processo de aprovação pode levar dias/semanas

---

## ❌ Problemas Comuns

### "Unable to create record: Permission denied"
→ Destinatário não ativou o Sandbox (não enviou `join codigo`)

### "The 'To' number is not a valid phone number"
→ Telefone no formato errado. Use `+5511999999999`

### "Authenticate"
→ Account SID ou Auth Token errado em `api_config.py`

---

## 🔄 Voltar para PyWhatKit

Se não quiser usar Twilio:
1. No arquivo `.env`, mude: `METODO_ENVIO = "pywhatkit"`
2. Ou use **Opção 8** no menu do jogo
