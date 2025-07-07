import random
import time
import matplotlib.pyplot as plt

vetores_unimodais = []
valores_pico = []
tamanhos_entrada = []

tempos_sequencial = []
tempos_binaria = []

def gerar_vetor_unimodal(n, minimo=1, maximo=None):
    if maximo is None:
        maximo = 2 * n

    valores = random.sample(range(minimo, maximo), n)
    valores.sort()

    indice_pico = random.randint(1, n - 2)
    crescente = valores[:indice_pico + 1]
    decrescente = valores[indice_pico + 1:]
    decrescente.reverse()

    vetor = crescente + decrescente
    return vetor, vetor[indice_pico + 1]

def encontrar_pico_sequencial(vetor):
    for i in range(1, len(vetor) - 1):
        if vetor[i - 1] < vetor[i] > vetor[i + 1]:
            return vetor[i]
    return None

def encontrar_pico_binaria(vetor):
    esquerda = 0
    direita = len(vetor) - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if 0 < meio < len(vetor) - 1:
            if vetor[meio - 1] < vetor[meio] > vetor[meio + 1]:
                return vetor[meio]
            elif vetor[meio] < vetor[meio + 1]:
                esquerda = meio + 1
            else:
                direita = meio - 1
        else:
            break
    return vetor[meio]

def gerar_todos_os_vetores():
    global vetores_unimodais, valores_pico, tamanhos_entrada

    m = random.randint(10, 20)
    max_k = (10000 - 10) // m + 1
    k = random.randint(100, min(200, max_k))

    print(f"Espaçamento fixo (m): {m}")
    print(f"Quantidade de tamanhos distintos (k): {k}")
    vetor1 = random.randint(10, 6000)

    tamanhos = [vetor1 + i * m for i in range(k)]
    tamanhos_entrada.extend(tamanhos)

    print("Exemplos de tamanhos de entrada gerados:", tamanhos_entrada[:5], "...")

    for n in tamanhos_entrada:
        vetor, pico = gerar_vetor_unimodal(n)
        vetores_unimodais.append(vetor)
        valores_pico.append(pico)

def medir_tempos():
    erros = 0
    for i, vetor in enumerate(vetores_unimodais):
        
        inicio_seq = time.perf_counter()
        pico_seq = encontrar_pico_sequencial(vetor)
        fim_seq = time.perf_counter()
        tempo_seq_ms = (fim_seq - inicio_seq) * 1000
        tempos_sequencial.append(tempo_seq_ms)

        inicio_bin = time.perf_counter()
        pico_bin = encontrar_pico_binaria(vetor)
        fim_bin = time.perf_counter()
        tempo_bin_ms = (fim_bin - inicio_bin) * 1000
        tempos_binaria.append(tempo_bin_ms)

        if not (
            0 < vetor.index(pico_seq) < len(vetor) - 1 and
            vetor[vetor.index(pico_seq) - 1] < pico_seq > vetor[vetor.index(pico_seq) + 1]
        ):
            erros += 1
        if not (
            0 < vetor.index(pico_bin) < len(vetor) - 1 and
            vetor[vetor.index(pico_bin) - 1] < pico_bin > vetor[vetor.index(pico_bin) + 1]
        ):
            erros += 1

    if erros > 0:
        print(f"{erros} erros encontrados na verificação dos picos.")
    else:
        print("Todos os picos foram encontrados corretamente.")

def grafico():
    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos_entrada, tempos_sequencial, label="Sequencial (O(n))", marker='o', markersize=3)
    plt.plot(tamanhos_entrada, tempos_binaria, label="Binária (O(log n))", marker='x', markersize=3)
    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo de execução (ms)")
    plt.title("Comparação de Tempo - Algoritmos para Encontrar Pico")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    gerar_todos_os_vetores()
    medir_tempos()
    grafico()
