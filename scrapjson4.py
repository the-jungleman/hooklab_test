import pandas as pd
import matplotlib.pyplot as plt  # Corrigido a importação do matplotlib

def load_data():
    data = pd.read_json('jsons/dados_compras.json')

    # Exploração dos Dados
    print("Primeiras linhas do conjunto de dados:")
    print(data.head())  # Examinar as primeiras linhas

    # Verificar valores ausentes
    print("\nValores ausentes nos dados:")
    print(data.isnull().sum())  # Checar valores ausentes

    # Identificar a quantidade total de compras
    total_compras = len(data)
    print(f"\nTotal de compras realizadas: {total_compras}")

    # Análise de Compras
    media_gasto = data['Valor'].mean()
    min_gasto = data['Valor'].min()
    max_gasto = data['Valor'].max()

    print(f"\nMédia gasta por compra: {media_gasto:.2f}")
    print(f"Valor mínimo gasto: {min_gasto:.2f}")
    print(f"Valor máximo gasto: {max_gasto:.2f}")

    # Produto mais caro e mais barato
    produto_mais_caro = data.loc[data['Valor'].idxmax()]['Nome do Item']
    produto_mais_barato = data.loc[data['Valor'].idxmin()]['Nome do Item']
    print(f"\nProduto mais caro: {produto_mais_caro}")
    print(f"Produto mais barato: {produto_mais_barato}")

    # Segmentação por Gênero
    distribuicao_genero = data['Sexo'].value_counts()
    print("\nDistribuição de gênero entre os consumidores:")
    print(distribuicao_genero)

    # Calcular o valor total gasto em compras por gênero
    gasto_por_genero = data.groupby('Sexo')['Valor'].sum()
    print("\nValor total gasto em compras por gênero:")
    print(gasto_por_genero)

    # Visualização de Dados
    # Gráfico de distribuição de gênero
    plt.figure(figsize=(10, 5))
    distribuicao_genero.plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Gênero entre Consumidores')
    plt.xlabel('Gênero')
    plt.ylabel('Número de Compradores')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.show()

    # Gráfico de gasto total por gênero
    plt.figure(figsize=(10, 5))
    gasto_por_genero.plot(kind='bar', color='salmon')
    plt.title('Valor Total Gasto em Compras por Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Total Gasto')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.show()

# Chamada da função
load_data()
