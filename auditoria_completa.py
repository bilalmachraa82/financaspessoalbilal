import pandas as pd
import json
from pathlib import Path
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def load_raw_csv(file_path):
    encoding = detect_encoding(file_path)
    df = pd.read_csv(file_path, encoding=encoding, sep=';' if ';' in open(file_path, 'r', encoding=encoding).readline() else ',')
    return df

def analise_bcp_500():
    print("\n" + "="*80)
    print("ANÁLISE DO BCP 500€ (2025-11-21)")
    print("="*80)
    
    millennium_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/novembro_2025/millennium_novembro_2025.csv")
    processed_file = Path("/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv")
    
    if not millennium_file.exists():
        print(f"❌ Arquivo raw não encontrado: {millennium_file}")
        return
    
    df_raw = load_raw_csv(millennium_file)
    df_processed = pd.read_csv(processed_file)
    
    print("\n📄 COLUNAS DO ARQUIVO RAW:")
    print(df_raw.columns.tolist())
    
    print("\n🔍 BUSCANDO BCP 500€ NO RAW:")
    bcp_raw = df_raw[
        (df_raw.astype(str).apply(lambda x: x.str.contains('20394/050598373', case=False, na=False)).any(axis=1)) |
        (df_raw.astype(str).apply(lambda x: x.str.contains('BANCO COMERCIAL PORTUG', case=False, na=False)).any(axis=1))
    ]
    
    if len(bcp_raw) > 0:
        print(f"✅ Encontrados {len(bcp_raw)} pagamentos BCP no RAW")
        print("\nDETALHES DOS PAGAMENTOS BCP NO RAW:")
        for idx, row in bcp_raw.iterrows():
            print(f"\nLinha {idx}:")
            for col in bcp_raw.columns:
                print(f"  {col}: {row[col]}")
    else:
        print("❌ NÃO encontrados pagamentos BCP no RAW")
    
    print("\n🔍 BUSCANDO BCP 500€ NO PROCESSADO:")
    bcp_processed = df_processed[
        (df_processed['Description'].str.contains('20394/050598373', case=False, na=False)) |
        (df_processed['Description'].str.contains('BANCO COMERCIAL PORTUG', case=False, na=False))
    ]
    
    if len(bcp_processed) > 0:
        print(f"✅ Encontrados {len(bcp_processed)} pagamentos BCP no PROCESSADO")
        print("\nDETALHES DOS PAGAMENTOS BCP NO PROCESSADO:")
        for idx, row in bcp_processed.iterrows():
            print(f"\nLinha {idx}:")
            print(f"  Data: {row['Date']}")
            print(f"  Descrição: {row['Description']}")
            print(f"  Montante: {row.get('Valor', 'N/A')}€")
            print(f"  Débito: {row.get('Debit', 'N/A')}€")
            print(f"  Crédito: {row.get('Credit', 'N/A')}€")
            print(f"  Categoria: {row['Categoria']}")
            print(f"  Observação: {row.get('Observacao', 'N/A')}")
    else:
        print("❌ NÃO encontrados pagamentos BCP no PROCESSADO")
    
    print("\n🔍 ESPECIFICAMENTE BCP 500€ EM 2025-11-21:")
    bcp_500 = df_processed[
        (df_processed['Description'].str.contains('BANCO COMERCIAL PORTUG', case=False, na=False)) &
        (df_processed['Date'] == '2025-11-21') &
        (df_processed['Valor'] == 500.0)
    ]
    
    if len(bcp_500) > 0:
        print(f"✅ Encontrado BCP 500€:")
        for idx, row in bcp_500.iterrows():
            print(f"\nLinha {idx}:")
            print(f"  Data: {row['Date']}")
            print(f"  Descrição: {row['Description']}")
            print(f"  Montante: {row.get('Valor', 'N/A')}€")
            print(f"  Débito: {row.get('Debit', 'N/A')}€")
            print(f"  Crédito: {row.get('Credit', 'N/A')}€")
            print(f"  Categoria: {row['Categoria']}")
            print(f"  Observação: {row.get('Observacao', 'N/A')}")
            
            if row.get('Debit', 0) > 0:
                print("\n⚠️  ESTÁ CLASSIFICADO COMO DÉBITO (SAÍDA DE DINHEIRO)")
            if row.get('Credit', 0) > 0:
                print("\n⚠️  ESTÁ CLASSIFICADO COMO CRÉDITO (ENTRADA DE DINHEIRO)")
    else:
        print("❌ NÃO encontrado BCP 500€ específico")

def analise_cartao_8373():
    print("\n" + "="*80)
    print("ANÁLISE DO CARTÃO *8373 (2025-11-19 - 178€)")
    print("="*80)
    
    revolut_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/novembro_2025/revolut_novembro_2025.csv")
    processed_file = Path("/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv")
    
    if not revolut_file.exists():
        print(f"❌ Arquivo raw não encontrado: {revolut_file}")
        return
    
    df_raw = load_raw_csv(revolut_file)
    df_processed = pd.read_csv(processed_file)
    
    print("\n📄 COLUNAS DO ARQUIVO RAW:")
    print(df_raw.columns.tolist())
    
    print("\n🔍 BUSCANDO CARTÃO *8373 NO RAW:")
    cartao_raw = df_raw[
        (df_raw.astype(str).apply(lambda x: x.str.contains('8373', case=False, na=False)).any(axis=1)) |
        (df_raw.astype(str).apply(lambda x: x.str.contains('Top up by', case=False, na=False)).any(axis=1))
    ]
    
    if len(cartao_raw) > 0:
        print(f"✅ Encontrados {len(cartao_raw)} transações com *8373/Top up no RAW")
        print("\nDETALHES DAS TRANSAÇÕES *8373 NO RAW:")
        for idx, row in cartao_raw.iterrows():
            print(f"\nLinha {idx}:")
            for col in cartao_raw.columns:
                print(f"  {col}: {row[col]}")
    else:
        print("❌ NÃO encontradas transações com *8373 no RAW")
    
    print("\n🔍 BUSCANDO CARTÃO *8373 NO PROCESSADO:")
    cartao_processed = df_processed[
        (df_processed['Description'].str.contains('8373', case=False, na=False)) |
        (df_processed['Description'].str.contains('Top up', case=False, na=False))
    ]
    
    if len(cartao_processed) > 0:
        print(f"✅ Encontrados {len(cartao_processed)} transações com *8373 no PROCESSADO")
        print("\nDETALHES DAS TRANSAÇÕES *8373 NO PROCESSADO:")
        for idx, row in cartao_processed.iterrows():
            print(f"\nLinha {idx}:")
            print(f"  Data: {row['Date']}")
            print(f"  Descrição: {row['Description']}")
            print(f"  Montante: {row.get('Valor', 'N/A')}€")
            print(f"  Débito: {row.get('Debit', 'N/A')}€")
            print(f"  Crédito: {row.get('Credit', 'N/A')}€")
            print(f"  Categoria: {row['Categoria']}")
            print(f"  Observação: {row.get('Observacao', 'N/A')}")
            
            if row.get('Credit', 0) > 0:
                print("  ⚠️  CRÉDITO (ENTRADA DE DINHEIRO)")
            if row.get('Debit', 0) > 0:
                print("  ⚠️  DÉBITO (SAÍDA DE DINHEIRO)")
    else:
        print("❌ NÃO encontradas transações com *8373 no PROCESSADO")
    
    print("\n🔍 ESPECIFICAMENTE CARTÃO *8373 178€ EM 2025-11-19:")
    cartao_178 = df_processed[
        (df_processed['Description'].str.contains('8373', case=False, na=False)) &
        (df_processed['Date'] == '2025-11-19') &
        (df_processed['Valor'] == 178.0)
    ]
    
    if len(cartao_178) > 0:
        print(f"✅ Encontrado cartão *8373 178€:")
        for idx, row in cartao_178.iterrows():
            print(f"\nLinha {idx}:")
            print(f"  Data: {row['Date']}")
            print(f"  Descrição: {row['Description']}")
            print(f"  Montante: {row.get('Valor', 'N/A')}€")
            print(f"  Débito: {row.get('Debit', 'N/A')}€")
            print(f"  Crédito: {row.get('Credit', 'N/A')}€")
            print(f"  Categoria: {row['Categoria']}")
            print(f"  Observação: {row.get('Observacao', 'N/A')}")
            
            if row['Categoria'] == 'Receitas - Soluções IA':
                print("\n⚠️  CLASSIFICADO COMO 'Receitas - Soluções IA' (INCORRETO SEGUNDO UTILIZADOR)")
            if row['Categoria'] == 'Transferência Interna':
                print("\n⚠️  CLASSIFICADO COMO 'Transferência Interna' (PODE ESTAR CORRETO)")
    else:
        print("❌ NÃO encontrado cartão *8373 178€ específico")

def comparar_totais():
    print("\n" + "="*80)
    print("COMPARAÇÃO DE TOTAIS RAW VS PROCESSADO")
    print("="*80)
    
    millennium_nov_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/novembro_2025/millennium_novembro_2025.csv")
    revolut_nov_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/novembro_2025/revolut_novembro_2025.csv")
    millennium_dez_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/dezembro_2025/millennium_dezembro_2025.csv")
    revolut_dez_file = Path("/Users/bilal/Programaçao/financas pessoais/data/raw/dezembro_2025/revolut_dezembro_2025.csv")
    processed_file = Path("/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv")
    
    if not millennium_nov_file.exists() or not revolut_nov_file.exists() or not millennium_dez_file.exists() or not revolut_dez_file.exists():
        print("❌ Arquivos raw não encontrados")
        return
    
    df_millennium_nov = load_raw_csv(millennium_nov_file)
    df_revolut_nov = load_raw_csv(revolut_nov_file)
    df_millennium_dez = load_raw_csv(millennium_dez_file)
    df_revolut_dez = load_raw_csv(revolut_dez_file)
    df_processed = pd.read_csv(processed_file)
    
    df_millennium_total = pd.concat([df_millennium_nov, df_millennium_dez], ignore_index=True)
    df_revolut_total = pd.concat([df_revolut_nov, df_revolut_dez], ignore_index=True)
    
    print("\n📊 TOTAIS RAW (MILLENNIUM - NOVEMBRO):")
    print(f"Total linhas: {len(df_millennium_nov)}")
    
    debito_col = None
    credito_col = None
    for col in df_millennium_nov.columns:
        col_lower = col.lower()
        if 'debit' in col_lower or 'débito' in col_lower:
            debito_col = col
        if 'credit' in col_lower or 'crédito' in col_lower:
            credito_col = col
    
    if debito_col:
        total_debito = df_millennium_nov[debito_col].sum()
        print(f"Total Débito: {total_debito:.2f}€")
    if credito_col:
        total_credito = df_millennium_nov[credito_col].sum()
        print(f"Total Crédito: {total_credito:.2f}€")
    
    print("\n📊 TOTAIS RAW (REVOLUT - NOVEMBRO):")
    print(f"Total linhas: {len(df_revolut_nov)}")
    
    debito_col = None
    credito_col = None
    for col in df_revolut_nov.columns:
        col_lower = col.lower()
        if 'debit' in col_lower or 'débito' in col_lower:
            debito_col = col
        if 'credit' in col_lower or 'crédito' in col_lower:
            credito_col = col
    
    if debito_col:
        total_debito = df_revolut_nov[debito_col].sum()
        print(f"Total Débito: {total_debito:.2f}€")
    if credito_col:
        total_credito = df_revolut_nov[credito_col].sum()
        print(f"Total Crédito: {total_credito:.2f}€")
    
    print("\n📊 TOTAIS RAW (MILLENNIUM - DEZEMBRO):")
    print(f"Total linhas: {len(df_millennium_dez)}")
    
    debito_col = None
    credito_col = None
    for col in df_millennium_dez.columns:
        col_lower = col.lower()
        if 'debit' in col_lower or 'débito' in col_lower:
            debito_col = col
        if 'credit' in col_lower or 'crédito' in col_lower:
            credito_col = col
    
    if debito_col:
        total_debito = df_millennium_dez[debito_col].sum()
        print(f"Total Débito: {total_debito:.2f}€")
    if credito_col:
        total_credito = df_millennium_dez[credito_col].sum()
        print(f"Total Crédito: {total_credito:.2f}€")
    
    print("\n📊 TOTAIS RAW (REVOLUT - DEZEMBRO):")
    print(f"Total linhas: {len(df_revolut_dez)}")
    
    debito_col = None
    credito_col = None
    for col in df_revolut_dez.columns:
        col_lower = col.lower()
        if 'debit' in col_lower or 'débito' in col_lower:
            debito_col = col
        if 'credit' in col_lower or 'crédito' in col_lower:
            credito_col = col
    
    if debito_col:
        total_debito = df_revolut_dez[debito_col].sum()
        print(f"Total Débito: {total_debito:.2f}€")
    if credito_col:
        total_credito = df_revolut_dez[credito_col].sum()
        print(f"Total Crédito: {total_credito:.2f}€")
    
    print("\n📊 TOTAIS RAW (TODOS OS ARQUIVOS):")
    print(f"Total linhas Millennium: {len(df_millennium_total)}")
    print(f"Total linhas Revolut: {len(df_revolut_total)}")
    print(f"Total linhas RAW: {len(df_millennium_total) + len(df_revolut_total)}")
    
    total_debito_mill = df_millennium_total['Debit'].sum()
    total_credito_mill = df_millennium_total['Credit'].sum()
    total_debito_rev = df_revolut_total['Debit'].sum()
    total_credito_rev = df_revolut_total['Credit'].sum()
    
    print(f"Total Débito Millennium: {total_debito_mill:.2f}€")
    print(f"Total Crédito Millennium: {total_credito_mill:.2f}€")
    print(f"Total Débito Revolut: {total_debito_rev:.2f}€")
    print(f"Total Crédito Revolut: {total_credito_rev:.2f}€")
    print(f"TOTAL DÉBITO RAW: {total_debito_mill + total_debito_rev:.2f}€")
    print(f"TOTAL CRÉDITO RAW: {total_credito_mill + total_credito_rev:.2f}€")
    
    print("\n📊 TOTAIS PROCESSADO:")
    print(f"Total linhas: {len(df_processed)}")
    total_debito = df_processed['Debit'].sum()
    total_credito = df_processed['Credit'].sum()
    print(f"Total Débito: {total_debito:.2f}€")
    print(f"Total Crédito: {total_credito:.2f}€")
    
    df_novembro = df_processed[df_processed['Date'].str.startswith('2025-11')]
    print(f"\n📊 TOTAIS NOVEMBRO 2025:")
    print(f"Total linhas: {len(df_novembro)}")
    total_debito_nov = df_novembro['Debit'].sum()
    total_credito_nov = df_novembro['Credit'].sum()
    print(f"Total Débito: {total_debito_nov:.2f}€")
    print(f"Total Crédito: {total_credito_nov:.2f}€")
    
    df_dezembro = df_processed[df_processed['Date'].str.startswith('2025-12')]
    print(f"\n📊 TOTAIS DEZEMBRO 2025:")
    print(f"Total linhas: {len(df_dezembro)}")
    total_debito_dez = df_dezembro['Debit'].sum()
    total_credito_dez = df_dezembro['Credit'].sum()
    print(f"Total Débito: {total_debito_dez:.2f}€")
    print(f"Total Crédito: {total_credito_dez:.2f}€")

def verificar_aprendizagem_bcp():
    print("\n" + "="*80)
    print("VERIFICAR APRENDIZAGEM - BCP")
    print("="*80)
    
    aprendizagem_file = Path("/Users/bilal/Programaçao/financas pessoais/APRENDIZAGEM_MANUAL_NOVEMBRO_DEZEMBRO.json")
    
    if not aprendizagem_file.exists():
        print("❌ Arquivo de aprendizagem não encontrado")
        return
    
    with open(aprendizagem_file, 'r', encoding='utf-8') as f:
        aprendizagem = json.load(f)
    
    print("\n📚 BUSCANDO BCP NA APRENDIZAGEM:")
    for chave, valor in aprendizagem.items():
        if 'BANCO COMERCIAL PORTUG' in chave.upper() or '20394' in chave:
            print(f"\nChave: {chave}")
            print(f"Categoria: {valor}")

def verificar_aprendizagem_cartao():
    print("\n" + "="*80)
    print("VERIFICAR APRENDIZAGEM - CARTÃO *8373")
    print("="*80)
    
    aprendizagem_file = Path("/Users/bilal/Programaçao/financas pessoais/APRENDIZAGEM_MANUAL_NOVEMBRO_DEZEMBRO.json")
    
    if not aprendizagem_file.exists():
        print("❌ Arquivo de aprendizagem não encontrado")
        return
    
    with open(aprendizagem_file, 'r', encoding='utf-8') as f:
        aprendizagem = json.load(f)
    
    print("\n📚 BUSCANDO CARTÃO *8373 NA APRENDIZAGEM:")
    for chave, valor in aprendizagem.items():
        if '8373' in chave or 'Top up' in chave:
            print(f"\nChave: {chave}")
            print(f"Categoria: {valor}")

if __name__ == "__main__":
    print("="*80)
    print("AUDITORIA COMPLETA - CLASSIFICAÇÃO FINANCEIRA")
    print("="*80)
    
    analise_bcp_500()
    analise_cartao_8373()
    verificar_aprendizagem_bcp()
    verificar_aprendizagem_cartao()
    comparar_totais()
    
    print("\n" + "="*80)
    print("AUDITORIA CONCLUÍDA")
    print("="*80)
