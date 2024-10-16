import random
import math
import time

# Parâmetros do SA
class SA:
    def inicio(self, temperatura_inicial: float, temperatura_final: float, alpha: float) -> None:
        # alpha tem que ser menor que 1
        assert 0 < alpha < 1
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_final = temperatura_final
        self.alpha = alpha

    def main(self, solucao_inicial, limite_mochila):
        temperatura = self.temperatura_inicial
        melhor = solucao_inicial
        solucao_atual = solucao_inicial
        funcao_objetivo_atual = self.funcao_objetivo(solucao_atual)
        iteracao = 0

        inicio_tempo = time.time()
       
        while temperatura > self.temperatura_final:
            iteracao += 1
           
            # Busca do vizinho
            nova_solucao = self.gerar_vizinho(solucao_atual, limite_mochila)
            funcao_objetivo_nova = self.funcao_objetivo(nova_solucao)
            muito_melhor = funcao_objetivo_nova < funcao_objetivo_atual
            aceita = random.uniform(0, 1) < math.exp(
                -abs(funcao_objetivo_nova - funcao_objetivo_atual) / temperatura
            )
            if aceita or muito_melhor:
                solucao_atual = nova_solucao
                funcao_objetivo_atual = funcao_objetivo_nova
                if funcao_objetivo_atual <= self.funcao_objetivo(melhor):
                    melhor = solucao_atual

            temperatura *= self.alpha

        fim_tempo = time.time()
        tempo_de_parada = fim_tempo - inicio_tempo
        print(f"A parada ocorreu depois de {iteracao} iterações")
        print(f"Tempo de execução: {tempo_de_parada:.6f} segundos")
        return melhor

    def gerar_vizinho(self, solucao_atual, limite_mochila):
        nova_solucao = [mochila[:] for mochila in solucao_atual]

        # Escolhe aleatoriamente uma mochila de origem
        mochila_origem = random.choice(range(len(nova_solucao)))
        if nova_solucao[mochila_origem]:
            item = random.choice(nova_solucao[mochila_origem])
            nova_solucao[mochila_origem].remove(item)

            # Tenta inserir o item em uma mochila diferente
            mochila_destino = random.choice(range(len(nova_solucao)))
            if sum(nova_solucao[mochila_destino]) + item <= limite_mochila:
                nova_solucao[mochila_destino].append(item)
            else:
                nova_solucao[mochila_origem].append(item)  # Retornar o item se não couber

            # Swap com outra mochila
            if len(nova_solucao) > 1:  # Garantir que existam pelo menos duas mochilas
                mochila_destino2 = random.choice(range(len(nova_solucao)))
                if mochila_destino != mochila_destino2 and nova_solucao[mochila_destino2]:
                    item2 = random.choice(nova_solucao[mochila_destino2])
                    nova_solucao[mochila_destino2].remove(item2)

                    # Tenta inserir o item2 na mochila de origem
                    if sum(nova_solucao[mochila_origem]) + item2 <= limite_mochila:
                        nova_solucao[mochila_origem].append(item2)
                    else:
                        nova_solucao[mochila_destino2].append(item2)  # Retornar se não couber

        return nova_solucao

    def funcao_objetivo(self, solucao):
        return len([mochila for mochila in solucao if mochila])  # Conta mochilas não vazias


class Inicio_bin:
    def nextFit(self, vetor, tamanho, limite_mochila):
        res = 1
        espaco_restante = limite_mochila
        mochilas = [[]]  # Começa com a primeira mochila

        for i in range(tamanho):
            if vetor[i] <= espaco_restante:
                mochilas[-1].append(vetor[i])
                espaco_restante -= vetor[i]
            else:
                mochilas.append([vetor[i]])
                res += 1
                espaco_restante = limite_mochila - vetor[i]

        return mochilas

if __name__ == '__main__':
    qualquer = Inicio_bin()
   
    m = int(input("Quantidade de itens: "))
    peso = int(input("Capacidade das mochilas/caixas: "))
    vetor = list(map(int, input("Peso dos itens: ").split()))
   
    # Inicializa a solução com a próxima mochila
    solucao_inicial = qualquer.nextFit(vetor, m, peso)
    print(f"Solução inicial (número de mochilas): {len(solucao_inicial)}")

    sa = SA()
    sa.inicio(temperatura_inicial=100000, temperatura_final=0.00001, alpha=0.9999)
    melhor = sa.main(solucao_inicial, peso)
    print(f"Melhor solução (número de mochilas): {sa.funcao_objetivo(melhor)}")