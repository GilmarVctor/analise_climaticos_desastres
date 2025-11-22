import pandas as pd
import numpy as np
import os

print("=" * 70)
print("CRIAÇÃO DE DATASET DUMMY DE DESASTRES NATURAIS")
print("=" * 70)

# Caminho do arquivo pré-processado
arquivo_inmet = "INMET_ARACAJU_2023_CLEAN.CSV"

# Verificar se o arquivo existe
if not os.path.exists(arquivo_inmet):
    print(f"\n❌ ERRO: Arquivo não encontrado!")
    print(f"   Procurando por: {arquivo_inmet}")
    print(f"\n⚠️  SOLUÇÃO:")
    print(f"   1. Execute primeiro: python preprocess_inmet_aracaju_WINDOWS.py")
    print(f"   2. Depois execute este script")
    exit(1)

print(f"\n✓ Arquivo encontrado: {arquivo_inmet}")
print("   Iniciando criação de dados de desastres...")

try:
    # Carregar os dados climáticos pré-processados
    print("\n[1/5] Carregando dados climáticos...")
    df_inmet = pd.read_csv(arquivo_inmet)
    print(f"   ✓ Carregado com sucesso! Dimensões: {df_inmet.shape}")
    
    # Exibir nomes das colunas
    print(f"\n   Colunas disponíveis:")
    for i, col in enumerate(df_inmet.columns, 1):
        print(f"      {i}. {col}")
    
    # Combinar Data e Hora em uma única coluna
    print("\n[2/5] Processando datas...")
    df_inmet['Data_Hora'] = pd.to_datetime(
        df_inmet['Data'] + ' ' + df_inmet['Hora UTC'].str.replace(' UTC', ''),
        format='%Y/%m/%d %H%M'
    )
    df_inmet.set_index('Data_Hora', inplace=True)
    print(f"   ✓ Datas processadas com sucesso!")
    
    # Preparar colunas numéricas
    print("\n[3/5] Convertendo colunas para formato numérico...")
    
    # Mapeamento de colunas do INMET para nomes simplificados
    colunas_mapeamento = {
        'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'Precipitacao_mm',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'Temperatura_Maxima_C',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'Temperatura_Minima_C',
        'UMIDADE RELATIVA DO AR, HORARIA (%)': 'Umidade_Relativa_Media_pct',
        'VENTO, RAJADA MAXIMA (m/s)': 'Vento_Rajada_Maxima_ms'
    }
    
    # Criar novo dataframe com colunas selecionadas
    df_processado = pd.DataFrame(index=df_inmet.index)
    
    for col_original, col_novo in colunas_mapeamento.items():
        if col_original in df_inmet.columns:
            # Converter vírgula para ponto (formato brasileiro)
            df_processado[col_novo] = df_inmet[col_original].astype(str).str.replace(',', '.').astype(float)
            print(f"   ✓ {col_novo}")
        else:
            print(f"   ⚠️  Coluna não encontrada: {col_original}")
    
    # Resample para dados diários
    print("\n[4/5] Reamostrando para frequência diária...")
    df_inmet_daily = df_processado.resample('D').agg({
        'Precipitacao_mm': 'sum',
        'Temperatura_Maxima_C': 'max',
        'Temperatura_Minima_C': 'min',
        'Umidade_Relativa_Media_pct': 'mean',
        'Vento_Rajada_Maxima_ms': 'max'
    })
    print(f"   ✓ Dados reamostrais com sucesso! Dimensões: {df_inmet_daily.shape}")
    
    # Criar DataFrame de desastres
    print("\n[5/5] Criando dataset dummy de desastres...")
    dates_2023 = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    df_disasters = pd.DataFrame(index=dates_2023)
    
    df_disasters['Inundacao_Alagamento'] = 0
    df_disasters['Deslizamento'] = 0
    df_disasters['Chuvas_Intensas'] = 0
    
    # Simular eventos de desastre baseados em precipitação
    precipitation_threshold = df_inmet_daily['Precipitacao_mm'].quantile(0.95)
    high_precip_days = df_inmet_daily[df_inmet_daily['Precipitacao_mm'] > precipitation_threshold].index
    
    df_disasters.loc[high_precip_days, 'Inundacao_Alagamento'] = 1
    df_disasters.loc[high_precip_days, 'Chuvas_Intensas'] = 1
    
    # Adicionar alguns deslizamentos
    np.random.seed(42)
    dias_com_chuva = df_inmet_daily[df_inmet_daily['Precipitacao_mm'] > 5]
    if len(dias_com_chuva) > 0:
        n_deslizamentos = min(5, len(dias_com_chuva))
        random_disaster_days = dias_com_chuva.sample(n=n_deslizamentos, random_state=42).index
        df_disasters.loc[random_disaster_days, 'Deslizamento'] = 1
    
    # Mesclar datasets
    df_merged = pd.merge(df_inmet_daily, df_disasters, left_index=True, right_index=True, how='left')
    
    # Preencher NaNs
    df_merged['Inundacao_Alagamento'] = df_merged['Inundacao_Alagamento'].fillna(0).astype(int)
    df_merged['Deslizamento'] = df_merged['Deslizamento'].fillna(0).astype(int)
    df_merged['Chuvas_Intensas'] = df_merged['Chuvas_Intensas'].fillna(0).astype(int)
    
    # Salvar arquivo mesclado
    arquivo_mesclado = "merged_climatic_disaster_data_aracaju_2023.csv"
    df_merged.to_csv(arquivo_mesclado)
    
    print(f"\n✓ Dataset criado com sucesso!")
    print(f"   - Linhas: {len(df_merged)}")
    print(f"   - Colunas: {len(df_merged.columns)}")
    print(f"   - Arquivo salvo: {arquivo_mesclado}")
    
    # Estatísticas
    print(f"\n📊 Estatísticas dos Desastres:")
    print(f"   - Inundações/Alagamentos: {df_merged['Inundacao_Alagamento'].sum()} dias")
    print(f"   - Deslizamentos: {df_merged['Deslizamento'].sum()} dias")
    print(f"   - Chuvas Intensas: {df_merged['Chuvas_Intensas'].sum()} dias")
    
    print(f"\n📊 Estatísticas Climáticas:")
    print(f"   - Precipitação média: {df_merged['Precipitacao_mm'].mean():.2f} mm")
    print(f"   - Precipitação máxima: {df_merged['Precipitacao_mm'].max():.2f} mm")
    print(f"   - Temperatura média máxima: {df_merged['Temperatura_Maxima_C'].mean():.2f} °C")
    print(f"   - Temperatura média mínima: {df_merged['Temperatura_Minima_C'].mean():.2f} °C")
    
    print("\n" + "=" * 70)
    print("✓ DATASET DUMMY CRIADO COM SUCESSO!")
    print("=" * 70)
    print(f"\nPróximo passo: execute 'python correlation_analysis_and_plotting_WINDOWS.py'")
    
except Exception as e:
    print(f"\n❌ ERRO ao criar dataset: {e}")
    print(f"   Tipo de erro: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)
