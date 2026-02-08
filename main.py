"""
main.py — Jogo do Impostor via WhatsApp
========================================
Execute este script para iniciar o jogo.
Pré-requisitos:
  1. pip install -r requirements.txt
  2. Estar logado no WhatsApp Web (https://web.whatsapp.com) no navegador padrão

Otimizado para Raspberry Pi Zero 2 W
"""

import os
import sys

# Otimizações para Raspberry Pi (se disponível)
try:
    from pi_optimizations import configurar_ambiente_pi, limpar_memoria, GerenciadorMemoria
    RASPBERRY_PI_MODE = True
    configurar_ambiente_pi()
except ImportError:
    RASPBERRY_PI_MODE = False
    # Funções dummy para compatibilidade
    def limpar_memoria(): pass
    class GerenciadorMemoria:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass

from game import JogoImpostor
from whatsapp_sender import enviar_para_jogadores, exibir_resultado_envio
from api_config import METODO_ENVIO


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("""
╔═══════════════════════════════════════════════╗
║       🎮  JOGO DO INFILTRADO  🎮              ║
║           via WhatsApp Bot                    ║
╠═══════════════════════════════════════════════╣
║  Um jogador recebe instrução diferente!      ║
║  Todos enviam respostas. Descubra quem é!     ║
╚═══════════════════════════════════════════════╝
""")


def menu_principal():
    import api_config
    metodo_atual = api_config.METODO_ENVIO
    print("\n📋 MENU PRINCIPAL")
    print("-" * 50)
    print("  1. Adicionar jogador")
    print("  2. Remover jogador")
    print("  3. Ver jogadores cadastrados")
    print("  4. 🎲 INICIAR JOGO (min. 3 jogadores)")
    print("  5. Coletar respostas e mostrar resultado")
    print("  6. Teste: modo prévia (sem envio)")
    print("  7. Escolher método de envio")
    print("  0. Sair")
    print("-" * 50)
    print(f"  📡 Método atual: {metodo_atual.upper()}")
    print("-" * 50)
    return input("Escolha uma opção: ").strip()


def adicionar_jogador(jogo: JogoImpostor):
    """Permite adicionar um ou mais jogadores."""
    print("\n➕ ADICIONAR JOGADOR(ES)")
    print("(Digite 'pronto' para voltar ao menu)\n")

    while True:
        nome = input("Nome do jogador: ").strip()
        if nome.lower() == "pronto":
            break
        if not nome:
            print("⚠️  Nome não pode ser vazio.")
            continue

        telefone = input("Telefone (ex: 11999999999): ").strip()
        if telefone.lower() == "pronto":
            break
        if not telefone:
            print("⚠️  Telefone não pode ser vazio.")
            continue

        jogador = jogo.adicionar_jogador(nome, telefone)
        print(f"  ✅ {jogador.nome} ({jogador.telefone}) adicionado!\n")

    print(f"\n📊 Total de jogadores: {len(jogo.jogadores)}")
    
    # Limpar memória no Pi
    if RASPBERRY_PI_MODE:
        limpar_memoria()


def remover_jogador(jogo: JogoImpostor):
    """Remove um jogador da lista."""
    if not jogo.jogadores:
        print("\n⚠️  Nenhum jogador cadastrado.")
        return

    print("\n🗑️  REMOVER JOGADOR")
    ver_jogadores(jogo)
    try:
        idx = int(input("Número do jogador para remover (0 = cancelar): ").strip())
        if idx == 0:
            return
        removido = jogo.remover_jogador(idx - 1)
        if removido:
            print(f"  ✅ {removido.nome} removido!")
        else:
            print("  ❌ Número inválido.")
    except ValueError:
        print("  ❌ Digite um número válido.")


def ver_jogadores(jogo: JogoImpostor):
    """Lista todos os jogadores cadastrados."""
    if not jogo.jogadores:
        print("\n⚠️  Nenhum jogador cadastrado.")
        return

    print(f"\n👥 JOGADORES CADASTRADOS ({len(jogo.jogadores)})")
    print("-" * 40)
    for i, j in enumerate(jogo.listar_jogadores(), 1):
        print(f"  {i}. {j.nome} — {j.telefone}")
    print("-" * 40)


def escolher_categoria(jogo: JogoImpostor):
    """Menu para escolher a categoria de perguntas."""
    categorias = jogo.listar_categorias()
    print("\n📂 CATEGORIAS DISPONÍVEIS")
    print("-" * 30)
    for i, cat in enumerate(categorias, 1):
        print(f"  {i}. {cat}")
    print("-" * 30)

    try:
        idx = int(input("Escolha uma categoria: ").strip())
        if 1 <= idx <= len(categorias):
            nome_cat = categorias[idx - 1]
            jogo.escolher_categoria(nome_cat)
            print(f"  ✅ Categoria selecionada: {nome_cat}")
        else:
            print("  ❌ Número inválido.")
    except ValueError:
        print("  ❌ Digite um número válido.")


def iniciar_jogo(jogo: JogoImpostor):
    """Sorteia e envia perguntas para os jogadores."""
    import api_config
    
    if len(jogo.jogadores) < 3:
        print("\n⚠️  É necessário pelo menos 3 jogadores!")
        return

    print("\n🎲 INICIAR JOGO")
    print("-" * 35)

    with GerenciadorMemoria("Sorteio e envio"):
        # Escolher categoria aleatória
        jogo.escolher_categoria_aleatoria()
        
        if not jogo.sortear():
            return

        # Mostrar resumo para o organizador
        print(jogo.resumo_partida())

        # Confirmação
        print(f"\n⚠️  ATENÇÃO: Método de envio = {api_config.METODO_ENVIO.upper()}")
        if api_config.METODO_ENVIO == "pywhatkit":
            print("   O WhatsApp Web será aberto no navegador.")
            print("   Certifique-se de que você está logado em web.whatsapp.com")
        elif api_config.METODO_ENVIO == "twilio":
            print("   As perguntas serão enviadas via Twilio API.")
        
        conf = input("\n   Deseja enviar as perguntas agora? (s/n): ").strip().lower()
        if conf != "s":
            print("   ❎ Envio cancelado.")
            return

        print("\n🚀 Iniciando envio de perguntas...\n")
        resultado = enviar_para_jogadores(jogo.jogadores)
        exibir_resultado_envio(resultado)
        
        print("\n✅ Perguntas enviadas!")
        print("📝 Quando todos responderem, use a opção 6 para coletar respostas.")


def coletar_respostas_e_resultado(jogo: JogoImpostor):
    """Coleta respostas dos jogadores e mostra o resultado."""
    import api_config
    
    if not jogo.infiltrado_obj:
        print("\n⚠️  Inicie o jogo primeiro (opção 5)!")
        return

    print("\n📝 COLETAR RESPOSTAS E RESULTADO")
    print("-" * 50)
    
    with GerenciadorMemoria("Coleta de respostas"):
        # Coletar respostas
        jogo.coletar_respostas()
        
        # Gerar resultado
        resultado_msg = jogo.gerar_resultado()
        
        print("\n" + "=" * 50)
        print("RESULTADO QUE SERÁ ENVIADO PARA TODOS:")
        print("=" * 50)
        print(resultado_msg)
        print("=" * 50)
        
        # Confirmar envio do resultado
        conf = input("\nDeseja enviar o resultado para todos? (s/n): ").strip().lower()
        if conf != "s":
            print("   ❎ Envio cancelado.")
            return
        
        print("\n🚀 Enviando resultado para todos...\n")
        
        # Enviar resultado para todos os jogadores
        for j in jogo.jogadores:
            j.mensagem = resultado_msg
        
        resultado = enviar_para_jogadores(jogo.jogadores)
        exibir_resultado_envio(resultado)
        
        print("\n🎉 Jogo finalizado!")

        # Confirmação
        print(f"\n⚠️  ATENÇÃO: Método de envio = {api_config.METODO_ENVIO.upper()}")
        if api_config.METODO_ENVIO == "pywhatkit":
            print("   O WhatsApp Web será aberto no navegador.")
            print("   Certifique-se de que você está logado em web.whatsapp.com")
        elif api_config.METODO_ENVIO == "twilio":
            print("   As mensagens serão enviadas via Twilio API.")
        
        conf = input("\n   Deseja enviar as mensagens agora? (s/n): ").strip().lower()
        if conf != "s":
            print("   ❎ Envio cancelado.")
            return

        print("\n🚀 Iniciando envio de mensagens...\n")
        resultado = enviar_para_jogadores(jogo.jogadores)
        exibir_resultado_envio(resultado)


def modo_teste(jogo: JogoImpostor):
    """Mostra prévia das perguntas sem enviar."""
    print("\n🧪 MODO TESTE (pré-visualização)")
    print("-" * 35)

    # Escolher categoria aleatória
    jogo.escolher_categoria_aleatoria()

    if not jogo.sortear(modo_teste=True):
        return

    print(jogo.resumo_partida())

    print("\n📨 PERGUNTAS QUE SERÃO ENVIADAS:")
    print("=" * 50)
    for j in jogo.jogadores:
        print(f"\n📱 Para: {j.nome} ({j.telefone})")
        print("-" * 40)
        print(j.mensagem)
        print("-" * 40)
    print("=" * 50)
    print("\n↩️  Voltando ao menu...")


def escolher_metodo_envio():
    """Permite escolher entre pywhatkit e Twilio."""
    import api_config
    
    print("\n📡 ESCOLHER MÉTODO DE ENVIO")
    print("-" * 50)
    print("\n  1. PYWHATKIT (WhatsApp Web)")
    print("     → Usa o navegador e o número logado no WhatsApp Web")
    print("     → GRÁTIS, mas usa SEU número pessoal")
    print("     → Mais lento (abre navegador para cada mensagem)")
    print()
    print("  2. TWILIO (API Business)")
    print("     → Envia de um número WhatsApp Business configurado")
    print("     → PAGO (precisa conta Twilio configurada)")
    print("     → Mais rápido e profissional")
    print("     → Configure api_config.py primeiro")
    print("-" * 50)
    print(f"  📌 Método atual: {api_config.METODO_ENVIO.upper()}")
    print("-" * 50)
    
    escolha = input("\nEscolha o método (1 ou 2): ").strip()
    
    if escolha == "1":
        api_config.METODO_ENVIO = "pywhatkit"
        print("  ✅ Método alterado para: PYWHATKIT")
    elif escolha == "2":
        from api_config import validar_config_twilio
        if validar_config_twilio():
            api_config.METODO_ENVIO = "twilio"
            print("  ✅ Método alterado para: TWILIO")
        else:
            print("  ⚠️  Configure api_config.py antes de usar Twilio")
            print("     Mantendo método atual: PYWHATKIT")
    else:
        print("  ⚠️  Opção inválida. Mantendo método atual.")


def main():
    limpar_tela()
    banner()
    
    # Mostrar info do Raspberry Pi se aplicável
    if RASPBERRY_PI_MODE:
        print("🍓 Modo Raspberry Pi ativado (otimizações aplicadas)\n")
        try:
            from pi_optimizations import monitorar_recursos
            monitorar_recursos()
            print()
        except:
            pass

    jogo = JogoImpostor()

    while True:
        opcao = menu_principal()

        if opcao == "1":
            adicionar_jogador(jogo)
        elif opcao == "2":
            remover_jogador(jogo)
        elif opcao == "3":
            ver_jogadores(jogo)
        elif opcao == "4":
            iniciar_jogo(jogo)
        elif opcao == "5":
            coletar_respostas_e_resultado(jogo)
        elif opcao == "6":
            modo_teste(jogo)
        elif opcao == "7":
            escolher_metodo_envio()
        elif opcao == "0":
            print("\n👋 Até a próxima! Bom jogo!\n")
            if RASPBERRY_PI_MODE:
                limpar_memoria()
            sys.exit(0)
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")
        
        # Liberar memória após cada operação no Pi
        if RASPBERRY_PI_MODE:
            limpar_memoria()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
        if RASPBERRY_PI_MODE:
            limpar_memoria()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        if RASPBERRY_PI_MODE:
            limpar_memoria()
        sys.exit(1)
