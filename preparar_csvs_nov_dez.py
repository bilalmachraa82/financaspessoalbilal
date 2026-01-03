import csv
import re
from datetime import datetime

def _parse_montante(montante_str: str):
    s = (montante_str or '').strip()
    if not s:
        return None

    s = re.sub(r'[€\s]', '', s)

    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')

    try:
        return float(s)
    except Exception:
        return None

def processar_millennium(input_file, output_file, banco_nome):
    print(f'Processando {banco_nome}...')
    transacoes = []
    
    try:
        with open(input_file, 'r', encoding='utf-16-le') as f:
            lines = f.readlines()
    except:
        try:
            with open(input_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        except:
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
    
    header_idx = None
    for i, line in enumerate(lines):
        if 'Data lançamento' in line and 'Data valor' in line:
            header_idx = i
            break
    
    if header_idx is None:
        for i, line in enumerate(lines):
            if 'Data lançamento' in line or 'Data de lançamento' in line:
                header_idx = i
                break
    
    if header_idx is None:
        print(f'  ❌ Cabeçalho não encontrado')
        print(f'  Linhas encontradas: {len(lines)}')
        return False
    
    reader = csv.DictReader(lines[header_idx:], delimiter=';')
    rows = list(reader)
    
    for row in rows:
        if row is None or not row:
            continue
            
        data_lanc = row.get('Data lançamento', '')
        descricao = row.get('Descrição', '')
        montante_str = row.get('Montante', '')
        tipo = row.get('Tipo', '')
        
        if data_lanc:
            data_lanc = data_lanc.strip()
        if descricao:
            descricao = descricao.strip()
        if montante_str:
            montante_str = montante_str.strip()
        if tipo:
            tipo = tipo.strip()
        
        if not data_lanc or not descricao or not montante_str:
            continue
        
        try:
            data = datetime.strptime(data_lanc, '%d-%m-%Y')
        except:
            continue
        
        montante = _parse_montante(montante_str)
        if montante is None:
            continue
        
        if montante > 0:
            debit = 0.0
            credit = montante
            valor = montante
        else:
            debit = abs(montante)
            credit = 0.0
            valor = abs(montante)
        
        transacao = {
            'Date': data.strftime('%Y-%m-%d'),
            'Bank': banco_nome,
            'Description': descricao,
            'Valor': valor,
            'Debit': debit,
            'Credit': credit,
            'Categoria': '',
            'Confianca': 0.0,
            'Observacao': ''
        }
        transacoes.append(transacao)
    
    print(f'  ✅ {len(transacoes)} transações extraídas')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Date', 'Bank', 'Description', 'Valor', 'Debit', 'Credit', 'Categoria', 'Confianca', 'Observacao']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transacoes)
    
    return True

def processar_revolut(input_file, output_file_nov, output_file_dez):
    print('Processando Revolut...')
    transacoes_nov = []
    transacoes_dez = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for row in rows:
        data_inicio = row.get('Data de início', '').strip()
        descricao = row.get('Descrição', '').strip()
        montante_str = row.get('Montante', '').strip()
        
        if not data_inicio or not descricao or not montante_str:
            continue
        
        try:
            data = datetime.strptime(data_inicio.split(' ')[0], '%Y-%m-%d')
        except:
            continue
        
        mes = data.month
        if mes not in [11, 12]:
            continue
        
        montante_str = montante_str.replace(',', '.')
        try:
            montante = float(montante_str)
        except:
            continue
        
        if montante < 0:
            debit = abs(montante)
            credit = 0.0
            valor = abs(montante)
        else:
            debit = 0.0
            credit = montante
            valor = montante
        
        transacao = {
            'Date': data.strftime('%Y-%m-%d'),
            'Bank': 'Revolut',
            'Description': descricao,
            'Valor': valor,
            'Debit': debit,
            'Credit': credit,
            'Categoria': '',
            'Confianca': 0.0,
            'Observacao': ''
        }
        
        if mes == 11:
            transacoes_nov.append(transacao)
        elif mes == 12:
            transacoes_dez.append(transacao)
    
    print(f'  ✅ {len(transacoes_nov)} transações de Novembro')
    print(f'  ✅ {len(transacoes_dez)} transações de Dezembro')
    
    with open(output_file_nov, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Date', 'Bank', 'Description', 'Valor', 'Debit', 'Credit', 'Categoria', 'Confianca', 'Observacao']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transacoes_nov)
    
    with open(output_file_dez, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Date', 'Bank', 'Description', 'Valor', 'Debit', 'Credit', 'Categoria', 'Confianca', 'Observacao']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transacoes_dez)
    
    return True

if __name__ == '__main__':
    print('=== PREPARANDO CSVs NOVEMBRO E DEZEMBRO ===\n')
    
    success = True
    
    if processar_millennium(
        'data/raw/dezembro_2025/MOVS_0_212026.csv',
        'data/raw/novembro_2025/millennium_novembro_2025.csv',
        'Millennium'
    ):
        print('  ✅ Millennium Novembro salvo\n')
    else:
        success = False
    
    if processar_millennium(
        'data/raw/dezembro_2025/MOVS_0_212026 (1).csv',
        'data/raw/dezembro_2025/millennium_dezembro_2025.csv',
        'Millennium'
    ):
        print('  ✅ Millennium Dezembro salvo\n')
    else:
        success = False
    
    if processar_revolut(
        'data/raw/novembro_2025/account-statement_2025-11-01_2025-12-31_pt-pt_281410.csv',
        'data/raw/novembro_2025/revolut_novembro_2025.csv',
        'data/raw/dezembro_2025/revolut_dezembro_2025.csv'
    ):
        print('  ✅ Revolut Novembro e Dezembro salvos\n')
    else:
        success = False
    
    if success:
        print('=== ✅ TODOS OS CSVs PREPARADOS COM SUCESSO ===')
    else:
        print('=== ❌ ERROS NO PROCESSAMENTO ===')
