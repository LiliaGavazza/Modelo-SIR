def obter_dados_varias_cidades():
    """Obtém os dados iniciais para a simulação SIR em múltiplas cidades."""
    num_cidades = int(input("Quantas cidades participarão da simulação? "))
    cidades = []
    parametros = {}

    for i in range(num_cidades):
        nome = input(f"\nNome da cidade {i + 1}: ")
        cidades.append(nome)

        print(f"Parâmetros para {nome}:")
        S = int(input("  Número de suscetíveis: "))
        I = int(input("  Número de infectados: "))
        R = int(input("  Número de recuperados: "))

        total = S + I + R
        if total == 0:
            print("  Erro: a população total não pode ser zero.")
            return None

        parametros[nome] = {"S": S, "I": I, "R": R}

    beta = float(input("\nInsira o valor de beta (taxa de transmissão, entre 0 e 1): "))
    if not (0 <= beta <= 1):
        print("Erro: beta deve estar entre 0 e 1.")
        return None

    gamma = float(input("Insira o valor de gamma (taxa de recuperação, entre 0 e 1): "))
    if not (0 <= gamma <= 1):
        print("Erro: gamma deve estar entre 0 e 1.")
        return None

    print("\nAgora informe quantas pessoas infectadas viajam diariamente de uma cidade para outra:")
    mobilidade = {}
    for origem in cidades:
        for destino in cidades:
            if origem != destino:
                chave = (origem, destino)
                viajantes = int(input(f"  {origem} → {destino}: "))
                mobilidade[chave] = viajantes

    return cidades, parametros, mobilidade, beta, gamma

def simulador_sir(cidades, parametros, mobilidade, beta, gamma, dias):
    """Essa função inicializa os estados para cada cidade. Para cada dia de simulação:
    01.Calcula infectados importados de outras cidades
    02.Aplica o modelo SIR tradicional
    03.Atualiza os compartimentos S, I, R
    04.Armazena os resultados diários
    Retorna toda a evolução temporal"""

    #cria dicionário vazio para armazenar dados da simulação
    resultados = {}
 
    #Para cada cidade, extrai os valores iniciais e calcula a população total.
    for cidade in cidades:
        S = parametros[cidade]["S"]
        I = parametros[cidade]["I"]
        R = parametros[cidade]["R"]
        N = S + I + R
 
    #Cria estruturas para armazenar a evolução dos compartimentos S, I, R ao longo do tempo.
        historico = {
            "S": [S],
            "I": [I],
            "R": [R]
        }
 
        resultados[cidade] = {
            "S": [S],
            "I": [I],
            "R": [R],
            "N": N
        }
 
    #Inicia o loop principal que simula cada dia, criando um dicionário temporário para os novos valores.
    for t in range(dias):
        novos_parametros = {}
 
        for cidade in cidades:
            S = resultados[cidade]["S"][-1]
            I = resultados[cidade]["I"][-1]
            R = resultados[cidade]["R"][-1]
            N = resultados[cidade]["N"]
 
          
    """Calcula infectados que chegam de outras cidades:
    01.Para cada cidade de origem diferente
    02.Obtém número de viajantes da matriz de mobilidade
    03.Calcula proporção de infectados na cidade de origem
    04.Adiciona ao contador de importados"""

    importados = 0
    for origem in cidades:
        if origem != cidade:
            viajantes = mobilidade.get((origem, cidade), 0)
            I_origem = resultados[origem]["I"][-1]
            N_origem = resultados[origem]["N"]
            if N_origem > 0:
                prop_inf = I_origem / N_origem
                importados += viajantes * prop_inf
 
    #Define as fórmulas da dinâmica SIR básica
            novos_infectados = beta * S * I / N
            novos_recuperados = gamma * I
 
    """Atualiza os valores para o próximo dia, considerando:
    01.Suscetíveis diminuem pelos novos infectados
    02.Infectados recebem novos casos e subtraem recuperados, mais importados
    03.Recuperados aumentam com os novos recuperados"""

    S_novo = S - novos_infectados
    I_novo = I + novos_infectados - novos_recuperados + importados
    R_novo = R + novos_recuperados
 
    novos_parametros[cidade] = (S_novo, I_novo, R_novo)
 
    # Atualiza os dados após o dia
    for cidade in cidades:
        S_novo, I_novo, R_novo = novos_parametros[cidade]
        resultados[cidade]["S"].append(S_novo)
        resultados[cidade]["I"].append(I_novo)
        resultados[cidade]["R"].append(R_novo)
 
    return resultados

def main():
    """Função principal que orquestra a simulação."""
    print("Simulador de Epidemias SIR com Múltiplas Cidades\n")
    
    # Obter dados de entrada
    dados = obter_dados_varias_cidades()
    if dados is None:
        return
    
    cidades, parametros, mobilidade, beta, gamma = dados
    
    dias = int(input("\nQuantos dias de simulação? "))
    
    # Executar simulação
    resultados = simulador_sir(cidades, parametros, mobilidade, beta, gamma, dias)
    
    # Exibir resultados
    print("\nResultados da Simulação:")
    for cidade in cidades:
        print(f"\n{cidade}:")
        print(f"  Suscetíveis: {resultados[cidade]['S'][-1]:.0f}")
        print(f"  Infectados: {resultados[cidade]['I'][-1]:.0f}")
        print(f"  Recuperados: {resultados[cidade]['R'][-1]:.0f}")


if __name__ == "__main__":
    main()