import pandas as pd
import os

print("=" * 70)
print("PRÉ-PROCESSAMENTO DE DADOS CLIMÁTICOS DO INMET")
print("Aracaju, Sergipe (2023)")
print("=" * 70)

# Caminho do arquivo (relativo à pasta atual)
arquivo_csv = "INMET_NE_SE_A409_ARACAJU_01-01-2023_A_31-12-2023.CSV"

# Verificar se o arquivo existe
if not os.path.exists(arquivo_csv):
    print(f"\n❌ ERRO: Arquivo não encontrado!")
    print(f"   Procurando por: {arquivo_csv}")
    print(f"   Pasta atual: {os.getcwd()}")
    print(f"\n   Arquivos na pasta atual:")
    for arquivo in os.listdir("."):
        if arquivo.endswith(".CSV") or arquivo.endswith(".csv"):
            print(f"   - {arquivo}")
    print(f"\n⚠️  SOLUÇÃO:")
    print(f"   1. Baixe o arquivo do INMET: https://portal.inmet.gov.br/dadoshistoricos")
    print(f"   2. Coloque o arquivo nesta pasta: {os.getcwd()}")
    print(f"   3. Execute o script novamente")
    exit(1)

print(f"\n✓ Arquivo encontrado: {arquivo_csv}")
print("   Iniciando pré-processamento...")

try:
    # Ler o arquivo CSV com encoding latin1
    # O arquivo do INMET tem cabeçalhos nas primeiras linhas, então pulamos elas
    print("\n[1/5] Lendo arquivo CSV (pulando cabeçalhos)...")
    df = pd.read_csv(arquivo_csv, encoding='latin1', sep=';', skiprows=8)
    print(f"   ✓ Lido com sucesso! Dimensões: {df.shape}")
    
    # Exibir as primeiras linhas
    print("\n[2/5] Primeiras linhas do arquivo:")
    print(df.head())
    
    # Limpar nomes das colunas (remover espaços em branco)
    print("\n[3/5] Limpando nomes das colunas...")
    df.columns = df.columns.str.strip()
    print(f"   ✓ Colunas encontradas ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"      {i}. {col}")
    
    # Converter para UTF-8 e salvar
    print("\n[4/5] Convertendo para UTF-8...")
    arquivo_limpo = "INMET_ARACAJU_2023_CLEAN.CSV"
    df.to_csv(arquivo_limpo, encoding='utf-8', index=False)
    print(f"   ✓ Arquivo salvo: {arquivo_limpo}")
    
    # Exibir informações
    print("\n[5/5] Informações do arquivo processado:")
    print(f"   - Linhas: {len(df)}")
    print(f"   - Colunas: {len(df.columns)}")
    print(f"   - Tipos de dados:")
    for col, dtype in df.dtypes.items():
        print(f"      {col}: {dtype}")
    
    print("\n" + "=" * 70)
    print("✓ PRÉ-PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print(f"\nArquivo salvo: {arquivo_limpo}")
    print(f"Próximo passo: execute 'python create_dummy_disaster_data_WINDOWS.py'")
    
except Exception as e:
    print(f"\n❌ ERRO ao processar arquivo: {e}")
    print(f"   Tipo de erro: {type(e).__name__}")
    
    # Tentar ler o arquivo para diagnosticar
    print(f"\n🔍 Diagnosticando o arquivo...")
    try:
        with open(arquivo_csv, 'r', encoding='latin1') as f:
            print(f"   Primeiras 10 linhas do arquivo:")
            for i, linha in enumerate(f, 1):
                if i <= 10:
                    print(f"   Linha {i}: {linha[:80]}...")
                else:
                    break
    except:
        pass
    
    exit(1)
