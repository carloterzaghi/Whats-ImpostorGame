"""
game.py — Lógica do Jogo do Impostor
Responsável por sortear papéis e palavras para cada jogador.
"""

import random
from typing import Optional
from config import (
    CATEGORIAS_PALAVRAS,
    MSG_JOGADOR_NORMAL,
    MSG_IMPOSTOR,
    MSG_IMPOSTOR_SEM_PALAVRA,
)


class Jogador:
    """Representa um jogador na partida."""

    def __init__(self, nome: str, telefone: str):
        self.nome = nome
        self.telefone = telefone        # formato: +5511999999999
        self.impostor: bool = False
        self.palavra: Optional[str] = None
        self.mensagem: str = ""

    def __repr__(self) -> str:
        papel = "IMPOSTOR" if self.impostor else "Cidadão"
        return f"Jogador({self.nome}, {self.telefone}, {papel}, palavra={self.palavra})"


class JogoImpostor:
    """Gerencia uma partida do Jogo do Impostor."""

    def __init__(self):
        self.jogadores: list[Jogador] = []
        self.categoria: Optional[str] = None
        self.palavra_normal: Optional[str] = None
        self.palavra_impostor: Optional[str] = None
        self.num_impostores: int = 1
        self.impostor_recebe_palavra: bool = True

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
        return list(CATEGORIAS_PALAVRAS.keys())

    def escolher_categoria(self, nome_categoria: str) -> bool:
        """Define a categoria de palavras para a partida."""
        if nome_categoria in CATEGORIAS_PALAVRAS:
            self.categoria = nome_categoria
            return True
        return False

    def definir_num_impostores(self, n: int) -> bool:
        """Define quantos impostores haverá (mín. 1, máx jogadores-1)."""
        if 1 <= n < len(self.jogadores):
            self.num_impostores = n
            return True
        return False

    def definir_impostor_com_palavra(self, recebe: bool):
        """Define se o impostor recebe uma palavra similar ou nenhuma."""
        self.impostor_recebe_palavra = recebe

    # ---- Sortear e preparar -------------------------------------------------

    def sortear(self, modo_teste: bool = False) -> bool:
        """
        Sorteia impostores e palavras.
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
        if len(self.jogadores) > 1 and self.num_impostores >= len(self.jogadores):
            print("❌ Número de impostores deve ser menor que o total de jogadores!")
            return False

        # Sortear par de palavras da categoria
        pares = CATEGORIAS_PALAVRAS[self.categoria]
        palavra_normal, palavra_impostor = random.choice(pares)
        self.palavra_normal = palavra_normal
        self.palavra_impostor = palavra_impostor

        # Resetar jogadores
        for j in self.jogadores:
            j.impostor = False
            j.palavra = None
            j.mensagem = ""

        # Sortear impostores (ajustar quantidade se necessário)
        num_impostores_real = min(self.num_impostores, len(self.jogadores) - 1)
        if num_impostores_real > 0:
            impostores = random.sample(self.jogadores, num_impostores_real)
            for imp in impostores:
                imp.impostor = True

        # Atribuir palavras e mensagens
        for j in self.jogadores:
            if j.impostor:
                if self.impostor_recebe_palavra:
                    j.palavra = palavra_impostor
                    j.mensagem = MSG_IMPOSTOR.format(palavra=palavra_impostor)
                else:
                    j.palavra = None
                    j.mensagem = MSG_IMPOSTOR_SEM_PALAVRA
            else:
                j.palavra = palavra_normal
                j.mensagem = MSG_JOGADOR_NORMAL.format(palavra=palavra_normal)

        return True

    def resumo_partida(self) -> str:
        """Retorna um resumo da partida (para o organizador)."""
        linhas = [
            "=" * 50,
            "📋  RESUMO DA PARTIDA (só o organizador vê isso!)",
            "=" * 50,
            f"Categoria: {self.categoria}",
            f"Palavra dos cidadãos: {self.palavra_normal}",
            f"Palavra do impostor: {self.palavra_impostor or '(nenhuma)'}",
            f"Total de jogadores: {len(self.jogadores)}",
            f"Impostores: {self.num_impostores}",
            "",
        ]
        for i, j in enumerate(self.jogadores, 1):
            papel = "🔴 IMPOSTOR" if j.impostor else "✅ Cidadão"
            linhas.append(f"  {i}. {j.nome} ({j.telefone}) — {papel} — Palavra: {j.palavra or '???'}")
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
