import subprocess
import sys
import os

print("=" * 70)
print("ANÁLISE DE CORRELAÇÃO: DADOS CLIMÁTICOS E DESASTRES NATURAIS")
print("Aracaju, Sergipe (2023)")
print("=" * 70)

# Verificar se o arquivo CSV do INMET existe
arquivo_csv = "INMET_NE_SE_A409_ARACAJU_01-01-2023_A_31-12-2023.CSV"

print("\n[VERIFICAÇÃO] Verificando arquivos necessários...")
if os.path.exists(arquivo_csv):
    print(f"  ✓ {arquivo_csv}")
else:
    print(f"  ✗ {arquivo_csv} - NÃO ENCONTRADO!")
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   O arquivo CSV do INMET não foi encontrado!")
    print(f"\n   Para baixar o arquivo:")
    print(f"   1. Acesse: https://portal.inmet.gov.br/dadoshistoricos")
    print(f"   2. Clique em 'ANO 2023 (AUTOMÁTICA)'")
    print(f"   3. Baixe o arquivo ZIP")
    print(f"   4. Extraia o arquivo ZIP")
    print(f"   5. Procure por um arquivo com nome similar a:")
    print(f"      INMET_NE_SE_A409_ARACAJU_01-01-2023_A_31-12-2023.CSV")
    print(f"   6. Copie esse arquivo para esta pasta")
    print(f"   7. Execute este script novamente")
    sys.exit(1)

# Verificar scripts Python
scripts = [
    "preprocess_inmet_aracaju_WINDOWS.py",
    "create_dummy_disaster_data_WINDOWS.py",
    "correlation_analysis_and_plotting_WINDOWS.py"
]

for script in scripts:
    if os.path.exists(script):
        print(f"  ✓ {script}")
    else:
        print(f"  ✗ {script} - NÃO ENCONTRADO!")

print("\n" + "=" * 70)
print("INICIANDO PROCESSAMENTO")
print("=" * 70)

# Passo 1: Pré-processamento
print("\n[PASSO 1/3] Pré-processando dados climáticos do INMET...")
print("-" * 70)
try:
    subprocess.run([sys.executable, "preprocess_inmet_aracaju_WINDOWS.py"], check=True)
    print("✓ Pré-processamento concluído com sucesso!")
except subprocess.CalledProcessError as e:
    print(f"✗ Erro ao pré-processar dados: {e}")
    sys.exit(1)

# Passo 2: Criar dados de desastres
print("\n[PASSO 2/3] Criando dataset dummy de desastres naturais...")
print("-" * 70)
try:
    subprocess.run([sys.executable, "create_dummy_disaster_data_WINDOWS.py"], check=True)
    print("✓ Dataset de desastres criado com sucesso!")
except subprocess.CalledProcessError as e:
    print(f"✗ Erro ao criar dados de desastres: {e}")
    sys.exit(1)

# Passo 3: Análise de correlação
print("\n[PASSO 3/3] Analisando correlação e gerando gráficos...")
print("-" * 70)
try:
    subprocess.run([sys.executable, "correlation_analysis_and_plotting_WINDOWS.py"], check=True)
    print("✓ Análise de correlação concluída com sucesso!")
except subprocess.CalledProcessError as e:
    print(f"✗ Erro ao analisar correlação: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("PROCESSAMENTO COMPLETO!")
print("=" * 70)
print("\n✓ Todos os scripts foram executados com sucesso!")
print("\nArquivos gerados:")
print("  1. INMET_ARACAJU_2023_CLEAN.CSV - Dados climáticos pré-processados")
print("  2. merged_climatic_disaster_data_aracaju_2023.csv - Dados mesclados")
print("  3. correlation_matrix.csv - Matriz de correlação")
print("  4. correlation_heatmap.png - Mapa de calor da correlação")
print("  5. precipitation_inundation_timeseries.png - Série temporal de precipitação")
print("  6. temperature_landslide_timeseries.png - Série temporal de temperatura")
print("\n💡 Os gráficos estão prontos para visualização!")
print("   Clique nos arquivos .png no VS Code para visualizar!")
print("=" * 70)
