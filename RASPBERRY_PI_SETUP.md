# 🍓 Raspberry Pi Zero 2 W - Guia de Instalação

## Visão Geral

Este guia detalha como instalar e configurar o **Jogo do Impostor** em um **Raspberry Pi Zero 2 W**, incluindo:
- ✅ Instalação automatizada
- ✅ Otimizações para hardware limitado (512MB RAM)
- ✅ Inicialização automática com systemd
- ✅ Monitoramento e logs
- ✅ Troubleshooting

---

## 📋 Requisitos

### Hardware
- **Raspberry Pi Zero 2 W**
  - 512MB RAM
  - Quad-core ARM Cortex-A53 (1GHz)
  - WiFi integrado
- **Cartão microSD** (mínimo 8GB, recomendado 16GB)
- **Fonte de alimentação** (5V, 2.5A recomendado)
- **Conexão com internet**

### Software
- **Raspberry Pi OS** (32-bit ou 64-bit)
  - Recomendado: Raspberry Pi OS Lite (sem interface gráfica)
  - Download: https://www.raspberrypi.com/software/

### Conta Twilio
- Para envio confiável de mensagens WhatsApp
- **Recomendado**: Twilio é mais estável que PyWhatKit no Pi
- Veja [TWILIO_SETUP.md](TWILIO_SETUP.md) para configuração

---

## 🚀 Instalação Rápida

### 1. Preparar o Raspberry Pi

```bash
# Conecte via SSH ou use terminal direto
ssh pi@raspberrypi.local

# Atualize o sistema
sudo apt-get update && sudo apt-get upgrade -y
```

### 2. Executar Script de Instalação

```bash
# Baixar e executar o instalador
curl -fsSL https://raw.githubusercontent.com/carloterzaghi/Whats-ImpostorGame/main/install_pi.sh -o install_pi.sh
chmod +x install_pi.sh
./install_pi.sh
```

O script irá:
- ✅ Instalar Python 3 e dependências
- ✅ Clonar o repositório
- ✅ Criar ambiente virtual otimizado
- ✅ Instalar pacotes Python
- ✅ Configurar serviço systemd
- ✅ Criar arquivo `.env` de exemplo

### 3. Configurar Credenciais

```bash
cd ~/impostor-game
nano .env
```

Configure suas credenciais do Twilio:

```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=whatsapp:+14155238886
METODO_ENVIO=twilio

# Otimizações (já incluídas)
PYTHONUNBUFFERED=1
PYTHONOPTIMIZE=1
```

**Salvar**: `Ctrl+O` → `Enter` → `Ctrl+X`

### 4. Testar Manualmente

```bash
cd ~/impostor-game
./start_game.sh
```

Teste as funcionalidades básicas:
1. Adicionar jogadores
2. Escolher categoria
3. Enviar mensagens de teste

Se funcionar, pressione `Ctrl+C` e prossiga para configurar o autostart.

---

## ⚙️ Configuração do Service (Autostart)

### Habilitar Inicialização Automática

```bash
# Habilitar serviço
sudo systemctl enable impostor-game

# Iniciar serviço
sudo systemctl start impostor-game

# Verificar status
sudo systemctl status impostor-game
```

### Comandos Úteis

```bash
# Ver logs em tempo real
journalctl -u impostor-game -f

# Ver últimos 50 logs
journalctl -u impostor-game -n 50

# Reiniciar serviço
sudo systemctl restart impostor-game

# Parar serviço
sudo systemctl stop impostor-game

# Desabilitar autostart
sudo systemctl disable impostor-game
```

---

## 🔧 Otimizações para Raspberry Pi Zero 2 W

### Limitações de Recursos

O script de instalação já aplica estas otimizações:

#### 1. **Memória**
```bash
# Limite de 350MB no systemd service
MemoryMax=350M
MemoryHigh=300M

# Limite no script de inicialização
ulimit -v 400000  # 400MB max
```

#### 2. **CPU**
```bash
# Prioridade mais baixa (Nice=10)
# Evita travar o sistema
Nice=10
```

#### 3. **Python**
```bash
# Otimizações via variáveis de ambiente
export PYTHONUNBUFFERED=1  # Sem buffer de saída
export PYTHONOPTIMIZE=1     # Bytecode otimizado
```

### Reduzir Uso de Memória Extra

Se precisar de mais memória disponível:

```bash
# Desabilitar serviços desnecessários
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon

# Reduzir memória de GPU (se usando Pi OS Lite)
sudo nano /boot/config.txt
# Adicione: gpu_mem=16

# Reiniciar
sudo reboot
```

---

## 📊 Monitoramento

### Verificar Uso de Recursos

```bash
# Memória e CPU
top
htop  # Se instalado: sudo apt-get install htop

# Uso de memória específico do serviço
systemctl status impostor-game | grep Memory

# Temperatura do Pi
vcgencmd measure_temp

# Memória disponível
free -h
```

### Logs e Debugging

```bash
# Verificar se o serviço está rodando
sudo systemctl status impostor-game

# Logs completos
journalctl -u impostor-game --no-pager

# Logs com timestamps
journalctl -u impostor-game -o short-precise

# Logs de erro apenas
journalctl -u impostor-game -p err
```

---

## 🐛 Troubleshooting

### Problema: Serviço não inicia

```bash
# Ver erro detalhado
sudo systemctl status impostor-game
journalctl -u impostor-game -n 50

# Verificar arquivo .env
cat ~/impostor-game/.env

# Testar manualmente
cd ~/impostor-game
source .venv/bin/activate
python3 main.py
```

### Problema: Memória insuficiente

```bash
# Verificar uso atual
free -h

# Adicionar swap (se necessário)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Mude CONF_SWAPSIZE=100 para CONF_SWAPSIZE=512
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Problema: PyWhatKit não funciona

O Pi Zero 2 W pode ter problemas com PyWhatKit (requer navegador).

**Solução**: Use **Twilio** (já configurado como padrão):
- Mais confiável
- Menos uso de recursos
- Não requer navegador
- Veja [TWILIO_SETUP.md](TWILIO_SETUP.md)

### Problema: WiFi desconecta

```bash
# Desabilitar power management do WiFi
sudo nano /etc/rc.local

# Adicione antes de "exit 0":
/sbin/iwconfig wlan0 power off

# Salvar e reiniciar
sudo reboot
```

---

## 🔄 Atualização do Software

```bash
cd ~/impostor-game

# Parar serviço
sudo systemctl stop impostor-game

# Atualizar código
git pull

# Atualizar dependências
source .venv/bin/activate
pip install --upgrade -r requirements.txt

# Reiniciar serviço
sudo systemctl start impostor-game
```

---

## 🌡️ Performance e Temperatura

### Monitorar Temperatura

```bash
# Temperatura atual
vcgencmd measure_temp

# Monitor contínuo
watch -n 1 vcgencmd measure_temp
```

### Temperatura Ideal
- **Normal**: 40-60°C
- **Atenção**: 60-75°C
- **Crítico**: >75°C (throttling automático)

### Melhorar Resfriamento
- Use case com ventilação
- Considere mini dissipador de calor
- Evite luz solar direta

---

## 📱 Uso Remoto (SSH)

### Configurar SSH

```bash
# Habilitar SSH (se não estiver)
sudo systemctl enable ssh
sudo systemctl start ssh

# Descobrir IP do Pi
hostname -I
```

### Acessar de outro dispositivo

```bash
# Via IP
ssh pi@192.168.1.XXX

# Via hostname
ssh pi@raspberrypi.local
```

### Executar Comandos Remotamente

```bash
# Ver logs
ssh pi@raspberrypi.local "journalctl -u impostor-game -f"

# Reiniciar serviço
ssh pi@raspberrypi.local "sudo systemctl restart impostor-game"
```

---

## 🎮 Uso Interativo

Se quiser usar o menu interativo via SSH:

```bash
# Parar o serviço primeiro
sudo systemctl stop impostor-game

# Executar manualmente
cd ~/impostor-game
./start_game.sh

# Quando terminar, reiniciar serviço
sudo systemctl start impostor-game
```

---

## 📦 Backup e Segurança

### Backup do .env

```bash
# Copiar .env para local seguro
scp pi@raspberrypi.local:~/impostor-game/.env ~/backup-env-$(date +%Y%m%d)
```

### Backup do Cartão SD

Use Raspberry Pi Imager ou:
```bash
# No Linux/Mac
sudo dd if=/dev/sdX of=~/pi-backup.img bs=4M status=progress

# No Windows, use Win32DiskImager
```

---

## 🎯 Checklist Pós-Instalação

- [ ] Sistema atualizado
- [ ] Script de instalação executado
- [ ] Arquivo `.env` configurado com credenciais reais
- [ ] Teste manual funcionando
- [ ] Serviço systemd habilitado
- [ ] Serviço iniciando automaticamente
- [ ] Logs sem erros
- [ ] Temperatura sob controle (<65°C)
- [ ] Backup do `.env` realizado
- [ ] SSH configurado (se necessário)

---

## 📚 Referências

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Systemd Service File Tutorial](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [Python Optimization Tips](https://wiki.python.org/moin/PythonSpeed)

---

## 💡 Dicas Finais

1. **Use Twilio** em vez de PyWhatKit no Pi
2. **Monitore a temperatura** regularmente
3. **Faça backup** do arquivo `.env` em local seguro
4. **Use SSH** para acesso remoto conveniente
5. **Verifique logs** periodicamente para detectar problemas
6. **Mantenha atualizado** com `git pull` regularmente

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `journalctl -u impostor-game -f`
2. Consulte a seção de Troubleshooting
3. Abra uma issue no GitHub
4. Verifique o README.md principal

---

**Desenvolvido para Raspberry Pi Zero 2 W** 🍓
