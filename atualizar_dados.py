#!/usr/bin/env python3

import subprocess
import sys
import os
import pandas as pd

def run_command(cmd, description):
    print(f"📝 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ ERRO: {description}")
        print(result.stderr)
        return False
    print(f"✅ {description} concluído")
    return True

def main():
    print("=" * 50)
    print("   Atualização de Dados Financeiros")
    print("=" * 50)
    print()
    
    if not os.path.exists('data/raw'):
        print("❌ ERRO: Pasta data/raw/ não encontrada!")
        sys.exit(1)
    
    print("📋 1. Processando CSVs...")
    if not run_command('python3 preparar_csvs_nov_dez.py', 'Preparação de CSVs'):
        sys.exit(1)
    
    print()
    print("📋 2. Consolidando dados...")
    if not run_command('python3 processar_novembro_dezembro_2025.py', 'Consolidação de dados'):
        sys.exit(1)
    
    print()
    print("📊 3. Resumo dos dados processados:")
    print("-" * 50)
    
    try:
        df = pd.read_csv('data/processed/novembro_dezembro_2025_classificado.csv')
        
        total = len(df)
        classificadas = len(df[df['Categoria'] != 'Nao Categorizado'])
        por_classificar = len(df[df['Categoria'] == 'Nao Categorizado'])
        
        print(f"   Total de transações: {total}")
        print(f"   Classificadas: {classificadas} ({classificadas/total*100:.1f}%)")
        print(f"   Por classificar: {por_classificar} ({por_classificar/total*100:.1f}%)")
        print(f"\n   Período: {df['Date'].min()} a {df['Date'].max()}")
        print(f"   Bancos: {', '.join(df['Bank'].unique())}")
        
    except Exception as e:
        print(f"   ⚠️  Não foi possível carregar o resumo: {e}")
    
    print("-" * 50)
    print()
    print("✅ Dados atualizados com sucesso!")
    print()
    print("📌 PRÓXIMOS PASSOS:")
    print("   1. Abrir o dashboard para validar:")
    print("      streamlit run dashboard_validacao_novembro_dezembro.py")
    print()
    print("   2. Para atualizar no GitHub:")
    print("      git add data/")
    print("      git commit -m 'Atualização de dados'")
    print("      git push")
    print()

if __name__ == '__main__':
    main()
