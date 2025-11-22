import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 70)
print("ANÁLISE DE CORRELAÇÃO E GERAÇÃO DE GRÁFICOS")
print("=" * 70)

# Caminho do arquivo mesclado
arquivo_mesclado = "merged_climatic_disaster_data_aracaju_2023.csv"

# Verificar se o arquivo existe
if not os.path.exists(arquivo_mesclado):
    print(f"\n❌ ERRO: Arquivo não encontrado!")
    print(f"   Procurando por: {arquivo_mesclado}")
    print(f"\n⚠️  SOLUÇÃO:")
    print(f"   1. Execute primeiro: python preprocess_inmet_aracaju_WINDOWS.py")
    print(f"   2. Depois execute: python create_dummy_disaster_data_WINDOWS.py")
    print(f"   3. Depois execute este script")
    exit(1)

print(f"\n✓ Arquivo encontrado: {arquivo_mesclado}")
print("   Iniciando análise de correlação...")

try:
    # Carregar os dados mesclados
    print("\n[1/5] Carregando dados mesclados...")
    df_merged = pd.read_csv(arquivo_mesclado, index_col='Data_Hora', parse_dates=True)
    print(f"   ✓ Carregado com sucesso! Dimensões: {df_merged.shape}")
    
    # Selecionar variáveis para correlação
    print("\n[2/5] Selecionando variáveis para correlação...")
    climatic_vars = [
        'Precipitacao_mm',
        'Temperatura_Maxima_C',
        'Temperatura_Minima_C',
        'Umidade_Relativa_Media_pct',
        'Vento_Rajada_Maxima_ms'
    ]
    disaster_vars = [
        'Inundacao_Alagamento',
        'Deslizamento',
        'Chuvas_Intensas'
    ]
    
    # Verificar quais colunas existem
    colunas_disponiveis = [col for col in climatic_vars + disaster_vars if col in df_merged.columns]
    print(f"   ✓ Colunas selecionadas ({len(colunas_disponiveis)}):")
    for col in colunas_disponiveis:
        print(f"      - {col}")
    
    # Calcular matriz de correlação
    print("\n[3/5] Calculando matriz de correlação...")
    correlation_matrix = df_merged[colunas_disponiveis].corr()
    print("   ✓ Matriz calculada com sucesso!")
    
    # Exibir matriz
    print("\n📊 Matriz de Correlação:")
    print(correlation_matrix)
    
    # Salvar matriz em CSV
    arquivo_correlacao = "correlation_matrix.csv"
    correlation_matrix.to_csv(arquivo_correlacao)
    print(f"\n   ✓ Matriz salva em: {arquivo_correlacao}")
    
    # Gerar gráficos
    print("\n[4/5] Gerando gráficos...")
    
    # Configurar estilo
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 8)
    
    # Gráfico 1: Heatmap
    print("   - Gerando heatmap...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Matriz de Correlação entre Dados Climáticos e Desastres (Aracaju, 2023)')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: correlation_heatmap.png")
    
    # Gráfico 2: Série temporal de precipitação
    print("   - Gerando série temporal de precipitação...")
    plt.figure(figsize=(15, 7))
    plt.plot(df_merged.index, df_merged['Precipitacao_mm'], label='Precipitação (mm)', color='blue', linewidth=2)
    
    if 'Inundacao_Alagamento' in df_merged.columns:
        disaster_days_inundacao = df_merged[df_merged['Inundacao_Alagamento'] == 1].index
        if len(disaster_days_inundacao) > 0:
            plt.scatter(disaster_days_inundacao, 
                        df_merged.loc[disaster_days_inundacao, 'Precipitacao_mm'], 
                        color='red', marker='o', s=50, label='Inundação/Alagamento', zorder=5)
    
    plt.title('Precipitação Diária e Ocorrência de Inundação/Alagamento (Aracaju, 2023)', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Precipitação (mm)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('precipitation_inundation_timeseries.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: precipitation_inundation_timeseries.png")
    
    # Gráfico 3: Série temporal de temperatura
    print("   - Gerando série temporal de temperatura...")
    plt.figure(figsize=(15, 7))
    plt.plot(df_merged.index, df_merged['Temperatura_Maxima_C'], label='Temperatura Máxima (°C)', color='orange', linewidth=2)
    
    if 'Deslizamento' in df_merged.columns:
        disaster_days_deslizamento = df_merged[df_merged['Deslizamento'] == 1].index
        if len(disaster_days_deslizamento) > 0:
            plt.scatter(disaster_days_deslizamento, 
                        df_merged.loc[disaster_days_deslizamento, 'Temperatura_Maxima_C'], 
                        color='green', marker='o', s=50, label='Deslizamento', zorder=5)
    
    plt.title('Temperatura Máxima e Ocorrência de Deslizamento (Aracaju, 2023)', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Temperatura Máxima (°C)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('temperature_landslide_timeseries.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: temperature_landslide_timeseries.png")
    
    print("\n[5/5] Finalizando...")
    
    # Exibir estatísticas
    print("\n📈 Correlações Principais:")
    if 'Precipitacao_mm' in correlation_matrix.index:
        if 'Inundacao_Alagamento' in correlation_matrix.columns:
            print(f"   Precipitação vs Inundação/Alagamento: {correlation_matrix.loc['Precipitacao_mm', 'Inundacao_Alagamento']:.3f}")
        if 'Deslizamento' in correlation_matrix.columns:
            print(f"   Precipitação vs Deslizamento: {correlation_matrix.loc['Precipitacao_mm', 'Deslizamento']:.3f}")
        if 'Chuvas_Intensas' in correlation_matrix.columns:
            print(f"   Precipitação vs Chuvas Intensas: {correlation_matrix.loc['Precipitacao_mm', 'Chuvas_Intensas']:.3f}")
    
    if 'Temperatura_Maxima_C' in correlation_matrix.index:
        if 'Inundacao_Alagamento' in correlation_matrix.columns:
            print(f"   Temperatura Máxima vs Inundação/Alagamento: {correlation_matrix.loc['Temperatura_Maxima_C', 'Inundacao_Alagamento']:.3f}")
    
    if 'Temperatura_Minima_C' in correlation_matrix.index:
        if 'Inundacao_Alagamento' in correlation_matrix.columns:
            print(f"   Temperatura Mínima vs Inundação/Alagamento: {correlation_matrix.loc['Temperatura_Minima_C', 'Inundacao_Alagamento']:.3f}")
    
    print("\n" + "=" * 70)
    print("✓ ANÁLISE DE CORRELAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    
    print("\n📁 Arquivos Gerados:")
    print("   1. correlation_matrix.csv - Matriz de correlação")
    print("   2. correlation_heatmap.png - Mapa de calor")
    print("   3. precipitation_inundation_timeseries.png - Série temporal de precipitação")
    print("   4. temperature_landslide_timeseries.png - Série temporal de temperatura")
    
    print("\n💡 Próximos passos:")
    print("   - Abra os arquivos .png no VS Code para visualizar os gráficos")
    print("   - Analise a matriz de correlação em correlation_matrix.csv")
    print("   - Use os dados para sua apresentação em slides!")
    
except Exception as e:
    print(f"\n❌ ERRO ao analisar correlação: {e}")
    print(f"   Tipo de erro: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)
