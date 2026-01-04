import pandas as pd
from pathlib import Path

def verificar_duplicacao():
    print("="*80)
    print("VERIFICAR DUPLICAÇÃO DE DADOS")
    print("="*80)
    
    processed_file = Path("/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv")
    df = pd.read_csv(processed_file)
    
    print(f"\n📊 TOTAL LINHAS PROCESSADO: {len(df)}")
    
    print("\n🔍 VERIFICAR LINHAS DUPLICADAS:")
    duplicadas = df[df.duplicated(keep=False)]
    if len(duplicadas) > 0:
        print(f"⚠️  ENCONTRADAS {len(duplicadas)} LINHAS DUPLICADAS!")
        print("\nLINHAS DUPLICADAS:")
        print(duplicadas.to_string())
    else:
        print("✅ NÃO há linhas completamente duplicadas")
    
    print("\n🔍 VERIFICAR LINHAS DUPLICADAS POR (Date, Description, Valor):")
    duplicadas_por_data = df[df.duplicated(subset=['Date', 'Description', 'Valor'], keep=False)]
    if len(duplicadas_por_data) > 0:
        print(f"⚠️  ENCONTRADAS {len(duplicadas_por_data)} LINHAS DUPLICADAS POR DATA/DESCRIÇÃO/VALOR!")
        print("\nLINHAS DUPLICADAS POR DATA/DESCRIÇÃO/VALOR:")
        print(duplicadas_por_data[['Date', 'Description', 'Valor', 'Debit', 'Credit', 'Categoria']].to_string())
    else:
        print("✅ NÃO há linhas duplicadas por data/descrição/valor")
    
    print("\n🔍 CONTAR POR BANCO:")
    print(df['Bank'].value_counts())
    
    print("\n🔍 VERIFICAR LINHAS DO MILLENNIUM:")
    millennium = df[df['Bank'] == 'Millennium']
    print(f"Total linhas Millennium: {len(millennium)}")
    
    print("\n🔍 VERIFICAR LINHAS DO REVOLUT:")
    revolut = df[df['Bank'] == 'Revolut']
    print(f"Total linhas Revolut: {len(revolut)}")
    
    print("\n🔍 CONTAR LINHAS COM VALORES DEBIT/CREDIT > 0:")
    df_com_valores = df[(df['Debit'] > 0) | (df['Credit'] > 0)]
    print(f"Total linhas com valores: {len(df_com_valores)}")
    
    print("\n🔍 LINHAS COM DEBIT E CREDIT AMBOS > 0:")
    df_ambos = df[(df['Debit'] > 0) & (df['Credit'] > 0)]
    if len(df_ambos) > 0:
        print(f"⚠️  ENCONTRADAS {len(df_ambos)} LINHAS COM DEBIT E CREDIT AMBOS > 0:")
        print(df_ambos.to_string())
    else:
        print("✅ NÃO há linhas com débito e crédito ambos > 0")
    
    print("\n🔍 LINHAS COM DEBIT E CREDIT AMBOS = 0:")
    df_zeros = df[(df['Debit'] == 0) & (df['Credit'] == 0)]
    if len(df_zeros) > 0:
        print(f"⚠️  ENCONTRADAS {len(df_zeros)} LINHAS COM DEBIT E CREDIT AMBOS = 0:")
        print(df_zeros[['Date', 'Description', 'Valor']].to_string())
    else:
        print("✅ NÃO há linhas com débito e crédito ambos = 0")

if __name__ == "__main__":
    verificar_duplicacao()
