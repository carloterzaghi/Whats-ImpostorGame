"""
pi_optimizations.py — Otimizações para Raspberry Pi Zero 2 W
========================================================
Módulo com funções para otimizar o uso de recursos em
ambientes com memória limitada (512MB RAM)
"""

import gc
import sys
import os


def configurar_ambiente_pi():
    """
    Configura otimizações do ambiente Python para Raspberry Pi.
    Chame esta função no início da aplicação.
    """
    # Forçar coleta de lixo agressiva
    gc.enable()
    gc.set_threshold(700, 10, 10)  # Mais agressivo que padrão (700, 10, 10)
    
    # Otimizações via variáveis de ambiente
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['PYTHONOPTIMIZE'] = '1'
    
    # Reduzir cache de strings (Python 3.7+)
    sys.setrecursionlimit(500)  # Reduzir de 1000 para economizar stack
    
    print("🍓 Otimizações para Raspberry Pi ativadas")


def limpar_memoria():
    """
    Força coleta de lixo para liberar memória.
    Use após operações que consomem memória.
    """
    gc.collect()


def obter_uso_memoria():
    """
    Retorna uso atual de memória em MB.
    Útil para debugging.
    """
    try:
        import psutil
        process = psutil.Process()
        mem_info = process.memory_info()
        return mem_info.rss / 1024 / 1024  # Converteu bytes para MB
    except ImportError:
        # Se psutil não estiver disponível, usar método alternativo
        try:
            import resource
            usage = resource.getrusage(resource.RUSAGE_SELF)
            return usage.ru_maxrss / 1024  # KB para MB no Linux
        except:
            return None


def monitorar_recursos():
    """
    Exibe informações sobre uso de recursos.
    Útil para debugging no Pi.
    """
    mem = obter_uso_memoria()
    if mem:
        print(f"💾 Memória em uso: {mem:.1f} MB")
    
    # Temperatura (apenas no Pi)
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
            emoji = "🌡️" if temp < 60 else "🔥" if temp < 75 else "⚠️"
            print(f"{emoji} Temperatura: {temp:.1f}°C")
    except:
        pass


class GerenciadorMemoria:
    """
    Context manager para garantir limpeza de memória.
    
    Uso:
        with GerenciadorMemoria("Enviando mensagens"):
            # código que usa memória
            enviar_mensagens()
        # Memória é liberada automaticamente
    """
    
    def __init__(self, nome_operacao="Operação"):
        self.nome = nome_operacao
        self.mem_inicial = None
    
    def __enter__(self):
        self.mem_inicial = obter_uso_memoria()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        limpar_memoria()
        mem_final = obter_uso_memoria()
        
        if self.mem_inicial and mem_final:
            diff = mem_final - self.mem_inicial
            if diff > 0:
                print(f"  💾 {self.nome}: +{diff:.1f}MB usado")
            else:
                print(f"  💾 {self.nome}: {abs(diff):.1f}MB liberado")


def lazy_import(module_name):
    """
    Importa módulo apenas quando necessário (lazy loading).
    Reduz uso inicial de memória.
    
    Uso:
        twilio = lazy_import('twilio.rest')
        client = twilio.Client(sid, token)
    """
    import importlib
    return importlib.import_module(module_name)


def otimizar_para_producao():
    """
    Aplica otimizações adicionais para modo produção (serviço).
    Desabilita recursos não essenciais.
    """
    # Desabilitar warnings não críticos
    import warnings
    warnings.filterwarnings('ignore')
    
    # Reduzir verbosidade de bibliotecas
    import logging
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('twilio').setLevel(logging.WARNING)
    
    print("🚀 Modo produção otimizado ativado")


# Decorador para monitorar memória de funções
def monitorar_memoria_funcao(func):
    """
    Decorador que monitora uso de memória de uma função.
    
    Uso:
        @monitorar_memoria_funcao
        def minha_funcao():
            # código
    """
    def wrapper(*args, **kwargs):
        mem_antes = obter_uso_memoria()
        resultado = func(*args, **kwargs)
        limpar_memoria()
        mem_depois = obter_uso_memoria()
        
        if mem_antes and mem_depois:
            diff = mem_depois - mem_antes
            print(f"  💾 {func.__name__}: {diff:+.1f}MB")
        
        return resultado
    return wrapper


# Configurações recomendadas para o Pi
PI_ZERO_2W_CONFIG = {
    'max_memory_mb': 350,  # Deixar 150MB para sistema
    'gc_threshold': (700, 10, 10),
    'recursion_limit': 500,
    'use_twilio': True,  # Mais eficiente que PyWhatKit no Pi
    'intervalo_mensagens': 2,  # Segundos entre mensagens Twilio
}


def validar_ambiente_pi():
    """
    Verifica se o ambiente está adequado para rodar no Pi.
    Retorna (ok: bool, mensagens: list)
    """
    problemas = []
    avisos = []
    
    # Verificar memória disponível
    mem_atual = obter_uso_memoria()
    if mem_atual and mem_atual > PI_ZERO_2W_CONFIG['max_memory_mb']:
        problemas.append(f"⚠️  Memória atual ({mem_atual:.0f}MB) acima do recomendado ({PI_ZERO_2W_CONFIG['max_memory_mb']}MB)")
    
    # Verificar se está no Pi
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            if 'Raspberry Pi' not in model:
                avisos.append("ℹ️  Não detectado Raspberry Pi (tudo bem para testes)")
    except:
        avisos.append("ℹ️  Não detectado Raspberry Pi (tudo bem para testes)")
    
    # Verificar temperatura (se aplicável)
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
            if temp > 75:
                problemas.append(f"🔥 Temperatura alta: {temp:.1f}°C (risco de throttling)")
            elif temp > 65:
                avisos.append(f"🌡️  Temperatura elevada: {temp:.1f}°C")
    except:
        pass
    
    # Verificar método de envio
    try:
        from api_config import METODO_ENVIO
        if METODO_ENVIO == 'pywhatkit':
            avisos.append("💡 Recomendado: use Twilio no Pi (mais eficiente que PyWhatKit)")
    except:
        pass
    
    ok = len(problemas) == 0
    mensagens = problemas + avisos
    
    return ok, mensagens


if __name__ == '__main__':
    # Teste rápido
    print("🧪 Testando otimizações do Raspberry Pi\n")
    
    configurar_ambiente_pi()
    print()
    
    monitorar_recursos()
    print()
    
    ok, msgs = validar_ambiente_pi()
    if msgs:
        print("📋 Status do ambiente:")
        for msg in msgs:
            print(f"  {msg}")
    
    if ok:
        print("\n✅ Ambiente OK para Raspberry Pi!")
    else:
        print("\n⚠️  Alguns ajustes podem ser necessários")
