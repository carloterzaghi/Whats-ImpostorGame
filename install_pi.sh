#!/bin/bash
# ============================================================
#  Script de Instalação - Raspberry Pi Zero 2 W
#  Jogo do Impostor via WhatsApp
# ============================================================

set -e  # Para na primeira erro

echo "╔═══════════════════════════════════════════════╗"
echo "║  🎮 Instalação - Jogo do Impostor 🎮          ║"
echo "║      Raspberry Pi Zero 2 W                    ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório de instalação
INSTALL_DIR="$HOME/impostor-game"
SERVICE_USER=$(whoami)

echo -e "${YELLOW}📦 Atualizando sistema...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${YELLOW}🐍 Instalando Python e dependências do sistema...${NC}"
sudo apt-get install -y python3 python3-pip python3-venv git

# Criar diretório se não existir
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}📂 Clonando repositório...${NC}"
    git clone https://github.com/carloterzaghi/Whats-ImpostorGame.git "$INSTALL_DIR"
else
    echo -e "${YELLOW}📂 Diretório já existe. Atualizando...${NC}"
    cd "$INSTALL_DIR"
    git pull
fi

cd "$INSTALL_DIR"

echo -e "${YELLOW}🔧 Criando ambiente virtual...${NC}"
python3 -m venv .venv

echo -e "${YELLOW}📥 Instalando dependências Python...${NC}"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}⚙️  Criando arquivo .env...${NC}"
if [ ! -f .env ]; then
    cat > .env << EOF
# Configuração do Twilio (recomendado para Raspberry Pi)
TWILIO_ACCOUNT_SID=seu_account_sid_aqui
TWILIO_AUTH_TOKEN=seu_auth_token_aqui
TWILIO_FROM_NUMBER=whatsapp:+14155238886
METODO_ENVIO=twilio

# Configurações do Raspberry Pi
# Reduz uso de memória e otimiza performance
PYTHONUNBUFFERED=1
PYTHONOPTIMIZE=1
EOF
    echo -e "${GREEN}✅ Arquivo .env criado. EDITE com suas credenciais!${NC}"
    echo -e "${YELLOW}   Use: nano $INSTALL_DIR/.env${NC}"
else
    echo -e "${GREEN}✅ Arquivo .env já existe.${NC}"
fi

# Criar script de inicialização otimizado
echo -e "${YELLOW}🚀 Criando script de inicialização...${NC}"
cat > start_game.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate

# Otimizações para Raspberry Pi Zero 2 W
export PYTHONUNBUFFERED=1
export PYTHONOPTIMIZE=1

# Limita uso de memória do Python
ulimit -v 400000  # Limita a 400MB de memória virtual

echo "🎮 Iniciando Jogo do Impostor..."
python3 main.py
EOF

chmod +x start_game.sh

# Criar serviço systemd
echo -e "${YELLOW}⚙️  Configurando serviço systemd...${NC}"
sudo tee /etc/systemd/system/impostor-game.service > /dev/null << EOF
[Unit]
Description=Jogo do Impostor via WhatsApp
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONOPTIMIZE=1"

# Otimizações para Raspberry Pi
Nice=10
MemoryMax=350M
MemoryHigh=300M

ExecStart=$INSTALL_DIR/.venv/bin/python3 $INSTALL_DIR/main.py
Restart=on-failure
RestartSec=10

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo -e "${YELLOW}🔄 Recarregando systemd...${NC}"
sudo systemctl daemon-reload

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Instalação Concluída!                     ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📝 Próximos passos:${NC}"
echo ""
echo "1. Editar configurações:"
echo -e "   ${GREEN}nano $INSTALL_DIR/.env${NC}"
echo ""
echo "2. Testar manualmente:"
echo -e "   ${GREEN}cd $INSTALL_DIR && ./start_game.sh${NC}"
echo ""
echo "3. Habilitar inicialização automática:"
echo -e "   ${GREEN}sudo systemctl enable impostor-game${NC}"
echo ""
echo "4. Iniciar serviço:"
echo -e "   ${GREEN}sudo systemctl start impostor-game${NC}"
echo ""
echo "5. Ver status:"
echo -e "   ${GREEN}sudo systemctl status impostor-game${NC}"
echo ""
echo "6. Ver logs:"
echo -e "   ${GREEN}journalctl -u impostor-game -f${NC}"
echo ""
echo -e "${YELLOW}📖 Documentação completa: RASPBERRY_PI_SETUP.md${NC}"
echo ""
