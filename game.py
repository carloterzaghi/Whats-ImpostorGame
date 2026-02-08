"""
game.py — Lógica do Jogo do Infiltrado
Responsável por sortear papéis, perguntas e coletar respostas.
"""

import random
from typing import Optional
from config import (
    CATEGORIAS_PERGUNTAS,
    MSG_JOGADOR_NORMAL,
    MSG_INFILTRADO,
    MSG_RESULTADO,
)


class Jogador:
    """Representa um jogador na partida."""

    def __init__(self, nome: str, telefone: str):
        self.nome = nome
        self.telefone = telefone        # formato: +5511999999999
        self.infiltrado: bool = False
        self.pergunta: Optional[str] = None
        self.instrucao: Optional[str] = None
        self.resposta: Optional[str] = None
        self.mensagem: str = ""

    def __repr__(self) -> str:
        papel = "INFILTRADO" if self.infiltrado else "Normal"
        return f"Jogador({self.nome}, {self.telefone}, {papel})"


class JogoInfiltrado:
    """Gerencia uma partida do Jogo do Infiltrado."""

    def __init__(self):
        self.jogadores: list[Jogador] = []
        self.categoria: Optional[str] = None
        self.pergunta_normal: Optional[str] = None
        self.instrucao_infiltrado: Optional[str] = None
        self.infiltrado_obj: Optional[Jogador] = None

    # ---- Gerenciar jogadores ------------------------------------------------

    def adicionar_jogador(self, nome: str, telefone: str) -> Jogador:
        """Adiciona um jogador à partida."""
        telefone = self._formatar_telefone(telefone)
        jogador = Jogador(nome, telefone)
        self.jogadores.append(jogador)
        return jogador

    def remover_jogador(self, indice: int) -> Optional[Jogador]:
        """Remove um jogador pelo índice da lista."""
        if 0 <= indice < len(self.jogadores):
            return self.jogadores.pop(indice)
        return None

    def listar_jogadores(self) -> list[Jogador]:
        return list(self.jogadores)

    # ---- Configurar partida -------------------------------------------------

    def listar_categorias(self) -> list[str]:
        return list(CATEGORIAS_PERGUNTAS.keys())

    def escolher_categoria(self, nome_categoria: str) -> bool:
        """Define a categoria de perguntas para a partida."""
        if nome_categoria in CATEGORIAS_PERGUNTAS:
            self.categoria = nome_categoria
            return True
        return False

    def escolher_categoria_aleatoria(self) -> str:
        """Escolhe uma categoria aleatória e retorna o nome."""
        categorias = list(CATEGORIAS_PERGUNTAS.keys())
        self.categoria = random.choice(categorias)
        print(f"🎲 Categoria sorteada: {self.categoria}")
        return self.categoria

    # ---- Sortear e preparar -------------------------------------------------

    def sortear(self, modo_teste: bool = False) -> bool:
        """
        Sorteia infiltrado e pergunta.
        Args:
            modo_teste: Se True, permite enviar com menos de 3 jogadores
        Retorna True se tudo deu certo, False se faltam dados.
        """
        minimo_jogadores = 1 if modo_teste else 3
        if len(self.jogadores) < minimo_jogadores:
            print(f"❌ É preciso pelo menos {minimo_jogadores} jogador(es)!")
            return False
        if not self.categoria:
            print("❌ Escolha uma categoria primeiro!")
            return False

        # Sortear pergunta da categoria
        perguntas = CATEGORIAS_PERGUNTAS[self.categoria]
        pergunta_normal, instrucao_infiltrado = random.choice(perguntas)
        self.pergunta_normal = pergunta_normal
        self.instrucao_infiltrado = instrucao_infiltrado

        # Resetar jogadores
        for j in self.jogadores:
            j.infiltrado = False
            j.pergunta = None  
            j.instrucao = None
            j.resposta = None
            j.mensagem = ""

        # Sortear infiltrado (apenas 1)
        self.infiltrado_obj = random.choice(self.jogadores)
        self.infiltrado_obj.infiltrado = True

        # Atribuir perguntas e mensagens
        for j in self.jogadores:
            if j.infiltrado:
                j.instrucao = instrucao_infiltrado
                j.mensagem = MSG_INFILTRADO.format(instrucao=instrucao_infiltrado)
            else:
                j.pergunta = pergunta_normal
                j.mensagem = MSG_JOGADOR_NORMAL.format(pergunta=pergunta_normal)

        return True

    def coletar_respostas(self) -> bool:
        """
        Coleta as respostas de todos os jogadores via input.
        Em produção, isso viria por webhook do WhatsApp.
        """
        print("\n📝 COLETANDO RESPOSTAS")
        print("=" * 50)
        print("Digite a resposta de cada jogador:\n")
        
        for j in self.jogadores:
            resposta = input(f"{j.nome}: ").strip()
            j.resposta = resposta if resposta else "(sem resposta)"
        
        print("\n✅ Todas as respostas coletadas!")
        return True

    def gerar_resultado(self) -> str:
        """Gera a mensagem de resultado final para enviar a todos."""
        respostas_texto = ""
        for j in self.jogadores:
            emoji = "🔴" if j.infiltrado else "👤"
            respostas_texto += f"{emoji} *{j.nome}:* {j.resposta}\n"
        
        resultado = MSG_RESULTADO.format(
            respostas=respostas_texto,
            pergunta=self.pergunta_normal,
            instrucao=self.instrucao_infiltrado,
            infiltrado=self.infiltrado_obj.nome if self.infiltrado_obj else "???"
        )
        return resultado

    def resumo_partida(self) -> str:
        """Retorna um resumo da partida (para o organizador)."""
        linhas = [
            "=" * 50,
            "📋  RESUMO DA PARTIDA (só o organizador vê isso!)",
            "=" * 50,
            f"Categoria: {self.categoria}",
            f"Pergunta normal: {self.pergunta_normal}",
            f"Instrução infiltrado: {self.instrucao_infiltrado}",
            f"Total de jogadores: {len(self.jogadores)}",
            f"Infiltrado: {self.infiltrado_obj.nome if self.infiltrado_obj else '???'}",
            "",
        ]
        for i, j in enumerate(self.jogadores, 1):
            papel = "🔴 INFILTRADO" if j.infiltrado else "👤 Normal"
            linhas.append(f"  {i}. {j.nome} ({j.telefone}) — {papel}")
        linhas.append("=" * 50)
        return "\n".join(linhas)

    # ---- Utilitários --------------------------------------------------------

    @staticmethod
    def _formatar_telefone(telefone: str) -> str:
        """
        Garante que o telefone esteja no formato +55XXXXXXXXXXX.
        Aceita formatos como: 11999999999, +5511999999999, 5511999999999
        """
        telefone = telefone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not telefone.startswith("+"):
            if telefone.startswith("55") and len(telefone) >= 12:
                telefone = "+" + telefone
            else:
                telefone = "+55" + telefone
        return telefone


# Alias para compatibilidade
JogoImpostor = JogoInfiltrado
