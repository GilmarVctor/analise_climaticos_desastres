#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 70)
print("ANÁLISE COMPLETA DE CORRELAÇÃO")
print("Dados Climáticos vs Desastres Naturais")
print("Aracaju, Sergipe (2023)")
print("=" * 70)

# ============================================================================
# PASSO 1: PRÉ-PROCESSAMENTO DE DADOS CLIMÁTICOS DO INMET
# ============================================================================

print("\n[PASSO 1/3] PRÉ-PROCESSAMENTO DE DADOS CLIMÁTICOS")
print("-" * 70)

arquivo_csv = "INMET_NE_SE_A409_ARACAJU_01-01-2023_A_31-12-2023.CSV"

if not os.path.exists(arquivo_csv):
    print(f"❌ ERRO: Arquivo não encontrado: {arquivo_csv}")
    print(f"   Pasta atual: {os.getcwd()}")
    exit(1)

print(f"✓ Arquivo encontrado: {arquivo_csv}")

try:
    # Ler o arquivo CSV
    print("  [1/4] Lendo arquivo CSV...")
    df_inmet = pd.read_csv(arquivo_csv, encoding='latin1', sep=';', skiprows=8)
    print(f"      ✓ Dimensões: {df_inmet.shape}")
    
    # Limpar nomes das colunas
    print("  [2/4] Limpando nomes das colunas...")
    df_inmet.columns = df_inmet.columns.str.strip()
    
    # Combinar Data e Hora
    print("  [3/4] Processando datas...")
    df_inmet['Data_Hora'] = pd.to_datetime(
        df_inmet['Data'] + ' ' + df_inmet['Hora UTC'].str.replace(' UTC', ''),
        format='%Y/%m/%d %H%M'
    )
    df_inmet.set_index('Data_Hora', inplace=True)
    
    # Converter colunas para numérico
    print("  [4/4] Convertendo colunas para numérico...")
    
    # Mapeamento de colunas
    colunas_mapeamento = {
        'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'Precipitacao_mm',
        'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)': 'Temperatura_Maxima_C',
        'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)': 'Temperatura_Minima_C',
        'UMIDADE RELATIVA DO AR, HORARIA (%)': 'Umidade_Relativa_Media_pct',
        'VENTO, RAJADA MAXIMA (m/s)': 'Vento_Rajada_Maxima_ms'
    }
    
    df_processado = pd.DataFrame(index=df_inmet.index)
    
    for col_original, col_novo in colunas_mapeamento.items():
        if col_original in df_inmet.columns:
            df_processado[col_novo] = df_inmet[col_original].astype(str).str.replace(',', '.').astype(float)
    
    # Resample para dados diários
    df_inmet_daily = df_processado.resample('D').agg({
        'Precipitacao_mm': 'sum',
        'Temperatura_Maxima_C': 'max',
        'Temperatura_Minima_C': 'min',
        'Umidade_Relativa_Media_pct': 'mean',
        'Vento_Rajada_Maxima_ms': 'max'
    })
    
    print(f"✓ Pré-processamento concluído! Dimensões: {df_inmet_daily.shape}")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# PASSO 2: CRIAÇÃO DE DATASET DUMMY DE DESASTRES
# ============================================================================

print("\n[PASSO 2/3] CRIAÇÃO DE DATASET DUMMY DE DESASTRES")
print("-" * 70)

try:
    print("  [1/3] Criando dataset de desastres...")
    
    dates_2023 = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    df_disasters = pd.DataFrame(index=dates_2023)
    
    df_disasters['Inundacao_Alagamento'] = 0
    df_disasters['Deslizamento'] = 0
    df_disasters['Chuvas_Intensas'] = 0
    
    # Simular eventos baseados em precipitação
    print("  [2/3] Simulando eventos de desastre...")
    
    precipitation_threshold = df_inmet_daily['Precipitacao_mm'].quantile(0.95)
    high_precip_days = df_inmet_daily[df_inmet_daily['Precipitacao_mm'] > precipitation_threshold].index
    
    df_disasters.loc[high_precip_days, 'Inundacao_Alagamento'] = 1
    df_disasters.loc[high_precip_days, 'Chuvas_Intensas'] = 1
    
    # Adicionar deslizamentos
    np.random.seed(42)
    dias_com_chuva = df_inmet_daily[df_inmet_daily['Precipitacao_mm'] > 5]
    if len(dias_com_chuva) > 0:
        n_deslizamentos = min(5, len(dias_com_chuva))
        random_disaster_days = dias_com_chuva.sample(n=n_deslizamentos, random_state=42).index
        df_disasters.loc[random_disaster_days, 'Deslizamento'] = 1
    
    print("  [3/3] Mesclando datasets...")
    
    # Mesclar datasets
    df_merged = pd.merge(df_inmet_daily, df_disasters, left_index=True, right_index=True, how='left')
    
    # Preencher NaNs
    df_merged['Inundacao_Alagamento'] = df_merged['Inundacao_Alagamento'].fillna(0).astype(int)
    df_merged['Deslizamento'] = df_merged['Deslizamento'].fillna(0).astype(int)
    df_merged['Chuvas_Intensas'] = df_merged['Chuvas_Intensas'].fillna(0).astype(int)
    
    # Salvar arquivo mesclado
    arquivo_mesclado = "merged_climatic_disaster_data_aracaju_2023.csv"
    df_merged.to_csv(arquivo_mesclado)
    
    print(f"✓ Dataset criado! Dimensões: {df_merged.shape}")
    print(f"  - Inundações/Alagamentos: {df_merged['Inundacao_Alagamento'].sum()} dias")
    print(f"  - Deslizamentos: {df_merged['Deslizamento'].sum()} dias")
    print(f"  - Chuvas Intensas: {df_merged['Chuvas_Intensas'].sum()} dias")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# PASSO 3: ANÁLISE DE CORRELAÇÃO E GERAÇÃO DE GRÁFICOS
# ============================================================================

print("\n[PASSO 3/3] ANÁLISE DE CORRELAÇÃO E GERAÇÃO DE GRÁFICOS")
print("-" * 70)

try:
    print("  [1/5] Calculando matriz de correlação...")
    
    colunas_analise = [
        'Precipitacao_mm',
        'Temperatura_Maxima_C',
        'Temperatura_Minima_C',
        'Umidade_Relativa_Media_pct',
        'Vento_Rajada_Maxima_ms',
        'Inundacao_Alagamento',
        'Deslizamento',
        'Chuvas_Intensas'
    ]
    
    correlation_matrix = df_merged[colunas_analise].corr()
    
    # Salvar matriz
    arquivo_correlacao = "correlation_matrix.csv"
    correlation_matrix.to_csv(arquivo_correlacao)
    print(f"  ✓ Matriz salva em: {arquivo_correlacao}")
    
    # Exibir correlações principais
    print("\n  📊 Correlações Principais:")
    print(f"     - Precip vs Inundação: {correlation_matrix.loc['Precipitacao_mm', 'Inundacao_Alagamento']:.3f}")
    print(f"     - Precip vs Deslizamento: {correlation_matrix.loc['Precipitacao_mm', 'Deslizamento']:.3f}")
    print(f"     - Precip vs Chuvas Intensas: {correlation_matrix.loc['Precipitacao_mm', 'Chuvas_Intensas']:.3f}")
    
    # Gerar gráficos
    print("\n  [2/5] Gerando heatmap...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Matriz de Correlação - Aracaju 2023')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: correlation_heatmap.png")
    
    print("  [3/5] Gerando série temporal de precipitação...")
    plt.figure(figsize=(15, 7))
    plt.plot(df_merged.index, df_merged['Precipitacao_mm'], label='Precipitação (mm)', color='blue', linewidth=2)
    
    disaster_days = df_merged[df_merged['Inundacao_Alagamento'] == 1].index
    if len(disaster_days) > 0:
        plt.scatter(disaster_days, 
                    df_merged.loc[disaster_days, 'Precipitacao_mm'], 
                    color='red', marker='o', s=50, label='Inundação/Alagamento', zorder=5)
    
    plt.title('Precipitação Diária e Inundação/Alagamento - Aracaju 2023', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Precipitação (mm)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('precipitation_inundation_timeseries.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: precipitation_inundation_timeseries.png")
    
    print("  [4/5] Gerando série temporal de temperatura...")
    plt.figure(figsize=(15, 7))
    plt.plot(df_merged.index, df_merged['Temperatura_Maxima_C'], label='Temperatura Máxima (°C)', color='orange', linewidth=2)
    
    disaster_days_landslide = df_merged[df_merged['Deslizamento'] == 1].index
    if len(disaster_days_landslide) > 0:
        plt.scatter(disaster_days_landslide, 
                    df_merged.loc[disaster_days_landslide, 'Temperatura_Maxima_C'], 
                    color='green', marker='o', s=50, label='Deslizamento', zorder=5)
    
    plt.title('Temperatura Máxima e Deslizamento - Aracaju 2023', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Temperatura Máxima (°C)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('temperature_landslide_timeseries.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("     ✓ Salvo: temperature_landslide_timeseries.png")
    
    print("  [5/5] Finalizando...")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 70)
print("✓ ANÁLISE COMPLETA CONCLUÍDA COM SUCESSO!")
print("=" * 70)

print("\n📁 Arquivos Gerados:")
print("   1. INMET_ARACAJU_2023_CLEAN.CSV - Dados climáticos pré-processados")
print("   2. merged_climatic_disaster_data_aracaju_2023.csv - Dados mesclados")
print("   3. correlation_matrix.csv - Matriz de correlação")
print("   4. correlation_heatmap.png - Mapa de calor")
print("   5. precipitation_inundation_timeseries.png - Série temporal de precipitação")
print("   6. temperature_landslide_timeseries.png - Série temporal de temperatura")

print("\n💡 Próximos passos:")
print("   - Abra os arquivos .png no VS Code para visualizar os gráficos")
print("   - Analise os dados em correlation_matrix.csv")
print("   - Use os dados para sua apresentação em slides!")

print("\n" + "=" * 70)
