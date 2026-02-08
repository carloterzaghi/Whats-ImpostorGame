# 🎮 Jogo do Impostor — WhatsApp Bot

Bot em Python que envia mensagens individuais pelo WhatsApp para cada jogador, criando um **Jogo do Impostor** (estilo jogo da palavra secreta).

## Como funciona

1. Você adiciona jogadores (nome + número de telefone)
2. Escolhe uma categoria de palavras (Animais, Comidas, Profissões, etc.)
3. O bot **sorteia** quem será o impostor
4. Cada jogador recebe uma mensagem **diferente** via WhatsApp:
   - **Cidadãos** → recebem a **mesma palavra**
   - **Impostor** → recebe uma **palavra parecida** (ou nenhuma)
5. Os jogadores discutem e tentam descobrir quem é o impostor!

## Métodos de Envio

### 1️⃣ PyWhatKit (WhatsApp Web) — GRÁTIS
- Usa o WhatsApp Web no navegador
- Envia do **SEU número** (que está logado)
- **Pré-requisito**: Estar logado em https://web.whatsapp.com
- Mais lento (abre navegador para cada mensagem)

### 2️⃣ Twilio API (Business) — PAGO
- Envia de um **número configurado** (não precisa ser o seu)
- Usa WhatsApp Business API oficial
- Mais rápido e profissional
- **Requer**: Conta Twilio + número Business configurado

## Pré-requisitos

- **Python 3.10+**
- **Google Chrome** (para PyWhatKit)
- **Conta Twilio** (opcional, só para método 2)

## Instalação

```bash
# 1. Clonar ou baixar o projeto
cd Whats-ImpostorGame

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python main.py
```

## Configuração do Twilio (Opcional)

Se quiser enviar de **outro número** (não o seu):

1. Crie conta em: https://www.twilio.com/
2. Configure um número WhatsApp Business:
   - No console Twilio: **Messaging** → **Try it out** → **Send a WhatsApp message**
   - Ou configure número próprio (requer aprovação)
3. Configure o arquivo **.env**:
   - Edite `.env` e preencha suas credenciais:
```bash
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_FROM_NUMBER = "whatsapp:+5511999999999"
METODO_ENVIO = "twilio"
```

4. No menu do jogo, use a **Opção 8** para escolher o método

## Uso

Ao executar `python main.py`, um menu interativo aparece no terminal:

```
📋 MENU PRINCIPAL
--------------------------------------------------
  1. Adicionar jogador
  2. Remover jogador
  3. Ver jogadores cadastrados
  4. Escolher categoria de palavras
  5. Configurar impostor
  6. Sortear e enviar mensagens! (min. 3 jogadores)
  7. Teste: enviar para cadastrados (sem mínimo)
  8. Escolher método de envio
  0. Sair
--------------------------------------------------
  📡 Método atual: PYWHATKIT
--------------------------------------------------
```

### Passo a passo:

1. **Opção 8** — Escolha o método de envio (PyWhatKit ou Twilio)
2. **Opção 1** — Adicione jogadores (nome + telefone)
3. **Opção 4** — Escolha uma categoria de palavras
4. **Opção 5** — (Opcional) Configure quantos impostores e se recebem palavra
5. **Opção 7** — Teste primeiro (pode enviar com menos jogadores)
6. **Opção 6** — Sortear e enviar (requer mín. 3 jogadores)

### Formato do telefone

O bot aceita vários formatos:
- `11999999999` (apenas DDD + número)
- `5511999999999` (com código do país)
- `+5511999999999` (formato completo)

## 🍓 Raspberry Pi Zero 2 W

Este projeto foi otimizado para rodar em **Raspberry Pi Zero 2 W** com apenas 512MB de RAM!

### Instalação Rápida no Pi

```bash
# Baixar e executar script de instalação
curl -fsSL https://raw.githubusercontent.com/carloterzaghi/Whats-ImpostorGame/main/install_pi.sh -o install_pi.sh
chmod +x install_pi.sh
./install_pi.sh
```

O script irá:
- ✅ Instalar Python e dependências
- ✅ Criar ambiente virtual otimizado
- ✅ Configurar serviço systemd para autostart
- ✅ Aplicar otimizações de memória

### Recursos

- **Autostart**: Inicia automaticamente ao ligar o Pi
- **Otimizações**: Gerenciamento agressivo de memória, lazy loading
- **Monitoramento**: Logs via journalctl
- **Twilio recomendado**: Mais eficiente que PyWhatKit no Pi

### Documentação Completa

Consulte [RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md) para:
- Guia passo a passo de instalação
- Configuração do serviço systemd
- Monitoramento e troubleshooting
- Otimizações de performance
- Comandos úteis

## Estrutura do projeto

```
Whats-ImpostorGame/
├── main.py                  # Script principal com menu interativo
├── game.py                  # Lógica do jogo (sortear, atribuir papéis)
├── whatsapp_sender.py       # Envio de mensagens (PyWhatKit + Twilio)
├── config.py                # Configurações, palavras e mensagens
├── api_config.py            # Carrega credenciais do .env
├── pi_optimizations.py      # Otimizações para Raspberry Pi
├── .env                     # Credenciais Twilio (NÃO commitar!)
├── .env.example             # Exemplo de configuração
├── requirements.txt         # Dependências do Python
├── install_pi.sh            # Script de instalação para Raspberry Pi
├── RASPBERRY_PI_SETUP.md    # Documentação completa do Pi
├── TWILIO_SETUP.md          # Guia de configuração do Twilio
└── README.md                # Este arquivo
```

## Personalização

### Adicionar palavras

Edite o dicionário `CATEGORIAS_PALAVRAS` em `config.py`. Cada categoria tem pares de palavras `(palavra_cidadão, palavra_impostor)`:

```python
"MinhaCategoria": [
    ("Palavra1", "PalavraParecida1"),
    ("Palavra2", "PalavraParecida2"),
],
```

### Alterar mensagens

Edite `MSG_JOGADOR_NORMAL`, `MSG_IMPOSTOR` e `MSG_IMPOSTOR_SEM_PALAVRA` em `config.py`.

## ⚠️ Importante

### PyWhatKit:
- O navegador abre para cada mensagem. **Não mexa no computador** enquanto envia.
- WhatsApp pode bloquear envios em massa. Use com moderação.

### Twilio:
- Requer aprovação do Facebook para uso em produção
- Modo sandbox: destinatários precisam enviar código de ativação primeiro
- Cobra por mensagem enviada

Esse bot é para uso pessoal/diversão entre amigos.
