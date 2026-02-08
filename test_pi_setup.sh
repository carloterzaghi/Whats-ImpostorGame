#!/bin/bash
# Script de teste para verificar se o ambiente está configurado corretamente

echo "🧪 Testando ambiente Raspberry Pi..."
echo ""

# Verificar Python
if command -v python3 &> /dev/null; then
    echo "✅ Python instalado: $(python3 --version)"
else
    echo "❌ Python não encontrado"
    exit 1
fi

# Verificar pasta de instalação
if [ -d "$HOME/impostor-game" ]; then
    echo "✅ Diretório de instalação encontrado"
    cd "$HOME/impostor-game"
else
    echo "❌ Diretório de instalação não encontrado"
    echo "   Execute: ./install_pi.sh primeiro"
    exit 1
fi

# Verificar venv
if [ -d ".venv" ]; then
    echo "✅ Ambiente virtual encontrado"
    source .venv/bin/activate
else
    echo "❌ Ambiente virtual não encontrado"
    exit 1
fi

# Verificar dependências
echo ""
echo "📦 Verificando dependências..."
python3 -c "import pywhatkit; print('✅ pywhatkit instalado')" 2>/dev/null || echo "⚠️  pywhatkit não instalado"
python3 -c "import twilio; print('✅ twilio instalado')" 2>/dev/null || echo "⚠️  twilio não instalado"
python3 -c "import dotenv; print('✅ python-dotenv instalado')" 2>/dev/null || echo "⚠️  python-dotenv não instalado"

# Verificar arquivo .env
echo ""
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
    
    # Verificar se tem valores padrão
    if grep -q "seu_account_sid_aqui" .env; then
        echo "⚠️  Arquivo .env precisa ser configurado com credenciais reais"
    else
        echo "✅ Arquivo .env parece estar configurado"
    fi
else
    echo "❌ Arquivo .env não encontrado"
    echo "   Crie a partir de .env.example"
fi

# Verificar serviço systemd
echo ""
if systemctl list-unit-files | grep -q impostor-game.service; then
    echo "✅ Serviço systemd registrado"
    
    if systemctl is-enabled impostor-game.service &> /dev/null; then
        echo "✅ Serviço habilitado para autostart"
    else
        echo "⚠️  Serviço não habilitado. Execute:"
        echo "   sudo systemctl enable impostor-game"
    fi
    
    if systemctl is-active impostor-game.service &> /dev/null; then
        echo "✅ Serviço está rodando"
    else
        echo "ℹ️  Serviço não está rodando"
    fi
else
    echo "⚠️  Serviço systemd não registrado"
fi

# Teste de otimizações
echo ""
echo "🔍 Testando otimizações..."
python3 -c "
try:
    from pi_optimizations import validar_ambiente_pi
    ok, msgs = validar_ambiente_pi()
    for msg in msgs:
        print(msg)
    if ok:
        print('✅ Ambiente validado com sucesso')
except ImportError:
    print('⚠️  pi_optimizations.py não encontrado')
" 2>/dev/null

# Resumo
echo ""
echo "═══════════════════════════════════════"
echo "📋 RESUMO DO TESTE"
echo "═══════════════════════════════════════"
echo ""
echo "Próximos passos:"
echo "1. Configure o .env se ainda não fez"
echo "2. Teste manualmente: ./start_game.sh" echo "3. Habilite o serviço: sudo systemctl enable impostor-game"
echo "4. Inicie o serviço: sudo systemctl start impostor-game"
echo "5. Veja os logs: journalctl -u impostor-game -f"
echo ""
