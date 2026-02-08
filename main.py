"""
main.py — Jogo do Impostor via WhatsApp
========================================
Execute este script para iniciar o jogo.
Pré-requisitos:
  1. pip install -r requirements.txt
  2. Estar logado no WhatsApp Web (https://web.whatsapp.com) no navegador padrão
"""

import os
import sys
from game import JogoImpostor
from whatsapp_sender import enviar_para_jogadores, exibir_resultado_envio
from api_config import METODO_ENVIO


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("""
╔═══════════════════════════════════════════════╗
║         🎮  JOGO DO IMPOSTOR  🎮              ║
║           via WhatsApp Bot                    ║
╠═══════════════════════════════════════════════╣
║  Adicione jogadores, escolha uma categoria,  ║
║  sorteie os papéis e envie as mensagens!      ║
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
    print("  4. Escolher categoria de palavras")
    print("  5. Configurar impostor")
    print("  6. Sortear e enviar mensagens! (min. 3 jogadores)")
    print("  7. Teste: enviar para cadastrados (sem mínimo)")
    print("  8. Escolher método de envio")
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
    """Menu para escolher a categoria de palavras."""
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


def configurar_impostor(jogo: JogoImpostor):
    """Configura número de impostores e se recebem palavra."""
    print("\n⚙️  CONFIGURAR IMPOSTOR")
    print(f"  Jogadores cadastrados: {len(jogo.jogadores)}")

    if len(jogo.jogadores) < 3:
        print("  ⚠️  Adicione pelo menos 3 jogadores para o jogo.")
        return

    # Número de impostores
    try:
        n = int(input(f"  Quantos impostores? (1 a {len(jogo.jogadores) - 1}): ").strip())
        if jogo.definir_num_impostores(n):
            print(f"  ✅ {n} impostor(es) definido(s).")
        else:
            print(f"  ❌ Número inválido. Deve ser entre 1 e {len(jogo.jogadores) - 1}.")
            return
    except ValueError:
        print("  ❌ Digite um número válido.")
        return

    # Impostor recebe palavra?
    resp = input("  O impostor recebe uma palavra parecida? (s/n) [s]: ").strip().lower()
    if resp == "n":
        jogo.definir_impostor_com_palavra(False)
        print("  ✅ O impostor NÃO receberá palavra (modo difícil).")
    else:
        jogo.definir_impostor_com_palavra(True)
        print("  ✅ O impostor receberá uma palavra similar.")


def sortear_e_enviar(jogo: JogoImpostor):
    """Sorteia papéis e envia mensagens pelo WhatsApp."""
    import api_config
    
    print("\n🎲 SORTEAR E ENVIAR")
    print("-" * 35)

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
        print("   As mensagens serão enviadas via Twilio API.")
    
    conf = input("\n   Deseja enviar as mensagens agora? (s/n): ").strip().lower()
    if conf != "s":
        print("   ❎ Envio cancelado.")
        return

    print("\n🚀 Iniciando envio de mensagens...\n")
    resultado = enviar_para_jogadores(jogo.jogadores)
    exibir_resultado_envio(resultado)


def modo_teste(jogo: JogoImpostor):
    """Sorteia, mostra as mensagens e oferece opção de enviar."""
    import api_config
    
    print("\n🧪 MODO TESTE (pré-visualização)")
    print("-" * 35)

    if not jogo.sortear(modo_teste=True):
        return

    print(jogo.resumo_partida())

    print("\n📨 MENSAGENS QUE SERÃO ENVIADAS:")
    print("=" * 50)
    for j in jogo.jogadores:
        print(f"\n📱 Para: {j.nome} ({j.telefone})")
        print("-" * 40)
        print(j.mensagem)
        print("-" * 40)
    print("=" * 50)

    # Oferecer opção de enviar após visualizar
    print(f"\nDeseja enviar essas mensagens agora? (Método: {api_config.METODO_ENVIO.upper()})")
    print("  1. Sim, enviar para todos!")
    print("  2. Não, voltar ao menu")
    resp = input("Escolha: ").strip()

    if resp == "1":
        if api_config.METODO_ENVIO == "pywhatkit":
            print("\n⚠️  Certifique-se de que está logado em web.whatsapp.com")
        conf = input("Confirma o envio? (s/n): ").strip().lower()
        if conf == "s":
            print("\n🚀 Iniciando envio de mensagens...\n")
            resultado = enviar_para_jogadores(jogo.jogadores)
            exibir_resultado_envio(resultado)
        else:
            print("   ❎ Envio cancelado.")
    else:
        print("   ↩️  Voltando ao menu.")


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
            escolher_categoria(jogo)
        elif opcao == "5":
            configurar_impostor(jogo)
        elif opcao == "6":
            sortear_e_enviar(jogo)
        elif opcao == "7":
            modo_teste(jogo)
        elif opcao == "8":
            escolher_metodo_envio()
        elif opcao == "0":
            print("\n👋 Até a próxima! Bom jogo!\n")
            sys.exit(0)
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
