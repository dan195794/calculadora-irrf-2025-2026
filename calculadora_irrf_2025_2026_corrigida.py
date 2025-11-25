#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora Completa de IRRF 2025 e 2026 com Reforma Tributaria
E Comparacao: Declaracao Simplificada vs Completa

Autor: Assistente IA
Data: Novembro 2025

Este script calcula e compara:
- IRRF com regras de 2025 (antes da reforma)
- IRRF com regras de 2026 (com reforma - PL 1087/2025)
- Declaracao SIMPLIFICADA vs COMPLETA
- Deducoes de INSS, previdencia privada (FUNCEF/PGBL) e saude
"""

def calcular_inss(salario):
    """
    Calcula INSS com base na tabela progressiva de 2025

    Tabela INSS 2025:
    - Ate R$ 1.412,00: 7,5%
    - De R$ 1.412,01 a R$ 2.666,68: 9%
    - De R$ 2.666,69 a R$ 4.000,03: 12%
    - De R$ 4.000,04 a R$ 7.786,02: 14%
    - Acima de R$ 7.786,02: Teto maximo

    Args:
        salario (float): Salario bruto mensal

    Returns:
        float: Valor do INSS a ser descontado
    """
    if salario <= 1412.00:
        return salario * 0.075
    elif salario <= 2666.68:
        inss1 = 1412.00 * 0.075
        inss2 = (salario - 1412.00) * 0.09
        return inss1 + inss2
    elif salario <= 4000.03:
        inss1 = 1412.00 * 0.075
        inss2 = (2666.68 - 1412.00) * 0.09
        inss3 = (salario - 2666.68) * 0.12
        return inss1 + inss2 + inss3
    elif salario <= 7786.02:
        inss1 = 1412.00 * 0.075
        inss2 = (2666.68 - 1412.00) * 0.09
        inss3 = (4000.03 - 2666.68) * 0.12
        inss4 = (salario - 4000.03) * 0.14
        return inss1 + inss2 + inss3 + inss4
    else:
        # Teto do INSS
        inss1 = 1412.00 * 0.075
        inss2 = (2666.68 - 1412.00) * 0.09
        inss3 = (4000.03 - 2666.68) * 0.12
        inss4 = (7786.02 - 4000.03) * 0.14
        return inss1 + inss2 + inss3 + inss4


def calcular_ir_progressivo(base):
    """
    Calcula IR com base na tabela progressiva (valida para 2025 e 2026)

    Tabela Progressiva:
    - Ate R$ 2.259,20: Isento
    - De R$ 2.259,21 a R$ 2.826,65: 7,5%
    - De R$ 2.826,66 a R$ 3.751,05: 15%
    - De R$ 3.751,06 a R$ 4.664,68: 22,5%
    - Acima de R$ 4.664,68: 27,5%

    Args:
        base (float): Base de calculo do IR (salario - INSS - previdencia)

    Returns:
        float: Valor do IR calculado pela tabela progressiva
    """
    if base <= 2259.20:
        return 0
    elif base <= 2826.65:
        return (base - 2259.20) * 0.075
    elif base <= 3751.05:
        return (2826.65 - 2259.20) * 0.075 + (base - 2826.65) * 0.15
    elif base <= 4664.68:
        return (2826.65 - 2259.20) * 0.075 + (3751.05 - 2826.65) * 0.15 + \
               (base - 3751.05) * 0.225
    else:
        return (2826.65 - 2259.20) * 0.075 + (3751.05 - 2826.65) * 0.15 + \
               (4664.68 - 3751.05) * 0.225 + (base - 4664.68) * 0.275


def calcular_reducao_reforma_2026(base, ir_calculado):
    """
    Calcula a reducao do IR conforme a reforma tributaria (PL 1087/2025)

    Reducao aplicavel:
    - Ate R$ 5.000,00: Reducao de ate R$ 312,89 (isencao total)
    - De R$ 5.000,01 a R$ 7.000,00: Reducao decrescente linear
    - Acima de R$ 7.000,00: Sem reducao

    Args:
        base (float): Base de calculo do IR
        ir_calculado (float): IR calculado pela tabela progressiva

    Returns:
        float: Valor da reducao a ser aplicada
    """
    if base <= 5000.00:
        reducao = min(312.89, ir_calculado)
    elif base <= 7000.00:
        reducao = 1095.11 - (0.156445 * base)
        reducao = max(0, reducao)
        reducao = min(reducao, ir_calculado)
    else:
        reducao = 0

    return reducao


def calcular_ir_2025_completo(salario_bruto, contribuicao_previdencia, 
                              despesa_saude=0, dependentes=0):
    """
    Calcula IRRF 2025 com declaracao COMPLETA

    Args:
        salario_bruto (float): Salario bruto mensal
        contribuicao_previdencia (float): Contribuicao a previdencia privada
        despesa_saude (float): Despesa com plano de saude complementar
        dependentes (int): Numero de dependentes

    Returns:
        dict: Dicionario com todos os valores do calculo
    """
    inss = calcular_inss(salario_bruto)
    base_calculo = salario_bruto - inss - contribuicao_previdencia

    # Deducoes legais
    deducoes = despesa_saude + (dependentes * 189.59)
    base_tributavel = base_calculo - deducoes

    ir_devido = calcular_ir_progressivo(base_tributavel)

    return {
        'tipo': 'Completa',
        'salario_bruto': salario_bruto,
        'inss': inss,
        'previdencia': contribuicao_previdencia,
        'deducoes_legais': deducoes,
        'base_calculo': base_calculo,
        'base_tributavel': base_tributavel,
        'ir_devido': ir_devido,
        'reducao': 0,
        'ir_final': ir_devido
    }


def calcular_ir_2025_simplificado(salario_bruto, contribuicao_previdencia):
    """
    Calcula IRRF 2025 com declaracao SIMPLIFICADA

    Desconto simplificado: 20% da base de calculo (limitado a R$ 16.754,34)

    Args:
        salario_bruto (float): Salario bruto mensal
        contribuicao_previdencia (float): Contribuicao a previdencia privada

    Returns:
        dict: Dicionario com todos os valores do calculo
    """
    inss = calcular_inss(salario_bruto)
    base_calculo = salario_bruto - inss - contribuicao_previdencia

    # Desconto simplificado: 20%
    teto_desconto = 16754.34
    desconto = base_calculo * 0.20
    if desconto > teto_desconto:
        desconto = teto_desconto

    base_tributavel = base_calculo - desconto
    ir_devido = calcular_ir_progressivo(base_tributavel)

    return {
        'tipo': 'Simplificada',
        'salario_bruto': salario_bruto,
        'inss': inss,
        'previdencia': contribuicao_previdencia,
        'desconto_simplificado': desconto,
        'base_calculo': base_calculo,
        'base_tributavel': base_tributavel,
        'ir_devido': ir_devido,
        'reducao': 0,
        'ir_final': ir_devido
    }


def calcular_ir_2026_completo(salario_bruto, contribuicao_previdencia, 
                              despesa_saude=0, dependentes=0):
    """
    Calcula IRRF 2026 com declaracao COMPLETA e reforma

    Args:
        salario_bruto (float): Salario bruto mensal
        contribuicao_previdencia (float): Contribuicao a previdencia privada
        despesa_saude (float): Despesa com plano de saude complementar
        dependentes (int): Numero de dependentes

    Returns:
        dict: Dicionario com todos os valores do calculo
    """
    inss = calcular_inss(salario_bruto)
    base_calculo = salario_bruto - inss - contribuicao_previdencia

    # Deducoes legais
    deducoes = despesa_saude + (dependentes * 189.59)
    base_tributavel = base_calculo - deducoes

    ir_calculado = calcular_ir_progressivo(base_tributavel)
    reducao = calcular_reducao_reforma_2026(base_tributavel, ir_calculado)
    ir_final = ir_calculado - reducao

    return {
        'tipo': 'Completa',
        'salario_bruto': salario_bruto,
        'inss': inss,
        'previdencia': contribuicao_previdencia,
        'deducoes_legais': deducoes,
        'base_calculo': base_calculo,
        'base_tributavel': base_tributavel,
        'ir_calculado': ir_calculado,
        'reducao': reducao,
        'ir_final': ir_final
    }


def calcular_ir_2026_simplificado(salario_bruto, contribuicao_previdencia):
    """
    Calcula IRRF 2026 com declaracao SIMPLIFICADA e reforma

    Args:
        salario_bruto (float): Salario bruto mensal
        contribuicao_previdencia (float): Contribuicao a previdencia privada

    Returns:
        dict: Dicionario com todos os valores do calculo
    """
    inss = calcular_inss(salario_bruto)
    base_calculo = salario_bruto - inss - contribuicao_previdencia

    # Desconto simplificado: 20%
    teto_desconto = 16754.34
    desconto = base_calculo * 0.20
    if desconto > teto_desconto:
        desconto = teto_desconto

    base_tributavel = base_calculo - desconto

    ir_calculado = calcular_ir_progressivo(base_tributavel)
    reducao = calcular_reducao_reforma_2026(base_tributavel, ir_calculado)
    ir_final = ir_calculado - reducao

    return {
        'tipo': 'Simplificada',
        'salario_bruto': salario_bruto,
        'inss': inss,
        'previdencia': contribuicao_previdencia,
        'desconto_simplificado': desconto,
        'base_calculo': base_calculo,
        'base_tributavel': base_tributavel,
        'ir_calculado': ir_calculado,
        'reducao': reducao,
        'ir_final': ir_final
    }


def exibir_comparacao_2025(salario_bruto, contribuicao_previdencia, 
                          despesa_saude=0):
    """
    Exibe comparacao Simplificada vs Completa para 2025
    """
    print("\n" + "="*70)
    print("COMPARACAO: DECLARACAO SIMPLIFICADA vs COMPLETA - 2025")
    print("="*70)

    completa = calcular_ir_2025_completo(salario_bruto, contribuicao_previdencia, 
                                         despesa_saude)
    simplificada = calcular_ir_2025_simplificado(salario_bruto, contribuicao_previdencia)

    # Dados de entrada
    print(f"\nDados de Entrada (mensal):")
    print(f"  Salario Bruto: R$ {salario_bruto:,.2f}")
    print(f"  INSS: R$ {completa['inss']:,.2f}")
    print(f"  Previdencia Privada (12%%): R$ {contribuicao_previdencia:,.2f}")
    print(f"  Saude Complementar: R$ {despesa_saude:,.2f}")
    print(f"  Base de Calculo IR: R$ {completa['base_calculo']:,.2f}")

    # Comparacao
    print(f"\n{'-'*70}")
    print("DECLARACAO COMPLETA:")
    print(f"{'-'*70}")
    print(f"  Deducoes Legais (Saude): R$ {completa['deducoes_legais']:,.2f}")
    print(f"  Base Tributavel: R$ {completa['base_tributavel']:,.2f}")
    print(f"  IR a Pagar: R$ {completa['ir_final']:,.2f}")

    print(f"\n{'-'*70}")
    print("DECLARACAO SIMPLIFICADA:")
    print(f"{'-'*70}")
    print(f"  Desconto Simplificado (20%%): R$ {simplificada['desconto_simplificado']:,.2f}")
    print(f"  Base Tributavel: R$ {simplificada['base_tributavel']:,.2f}")
    print(f"  IR a Pagar: R$ {simplificada['ir_final']:,.2f}")

    # Analise
    diferenca = completa['ir_final'] - simplificada['ir_final']
    print(f"\n{'-'*70}")
    print("ANALISE:")
    print(f"{'-'*70}")

    if abs(diferenca) < 0.01:
        print(f"  >> Praticamente igual! Escolha pela facilidade.")
    elif diferenca > 0:
        print(f"  OK MAIS VANTAJOSA: SIMPLIFICADA")
        print(f"  Economia: R$ {diferenca:,.2f} por mes")
        print(f"  Economia Anual: R$ {diferenca * 12:,.2f}")
    else:
        print(f"  OK MAIS VANTAJOSA: COMPLETA")
        print(f"  Economia: R$ {abs(diferenca):,.2f} por mes")
        print(f"  Economia Anual: R$ {abs(diferenca) * 12:,.2f}")


def exibir_comparacao_2026(salario_bruto, contribuicao_previdencia, 
                          despesa_saude=0):
    """
    Exibe comparacao Simplificada vs Completa para 2026 (com reforma)
    """
    print("\n" + "="*70)
    print("COMPARACAO: DECLARACAO SIMPLIFICADA vs COMPLETA - 2026 (COM REFORMA)")
    print("="*70)

    completa = calcular_ir_2026_completo(salario_bruto, contribuicao_previdencia, 
                                        despesa_saude)
    simplificada = calcular_ir_2026_simplificado(salario_bruto, contribuicao_previdencia)

    # Dados de entrada
    print(f"\nDados de Entrada (mensal):")
    print(f"  Salario Bruto: R$ {salario_bruto:,.2f}")
    print(f"  INSS: R$ {completa['inss']:,.2f}")
    print(f"  Previdencia Privada (12%%): R$ {contribuicao_previdencia:,.2f}")
    print(f"  Saude Complementar: R$ {despesa_saude:,.2f}")
    print(f"  Base de Calculo IR: R$ {completa['base_calculo']:,.2f}")

    # Comparacao
    print(f"\n{'-'*70}")
    print("DECLARACAO COMPLETA:")
    print(f"{'-'*70}")
    print(f"  Deducoes Legais (Saude): R$ {completa['deducoes_legais']:,.2f}")
    print(f"  Base Tributavel: R$ {completa['base_tributavel']:,.2f}")
    print(f"  IR Calculado: R$ {completa['ir_calculado']:,.2f}")
    print(f"  (-) Reducao da Reforma: R$ {completa['reducao']:,.2f}")
    print(f"  IR Final: R$ {completa['ir_final']:,.2f}")

    print(f"\n{'-'*70}")
    print("DECLARACAO SIMPLIFICADA:")
    print(f"{'-'*70}")
    print(f"  Desconto Simplificado (20%%): R$ {simplificada['desconto_simplificado']:,.2f}")
    print(f"  Base Tributavel: R$ {simplificada['base_tributavel']:,.2f}")
    print(f"  IR Calculado: R$ {simplificada['ir_calculado']:,.2f}")
    print(f"  (-) Reducao da Reforma: R$ {simplificada['reducao']:,.2f}")
    print(f"  IR Final: R$ {simplificada['ir_final']:,.2f}")

    # Analise
    diferenca = completa['ir_final'] - simplificada['ir_final']
    print(f"\n{'-'*70}")
    print("ANALISE:")
    print(f"{'-'*70}")

    if completa['base_tributavel'] <= 5000:
        print(f"  ISENCAO TOTAL (Completa): R$ 0,00")
    if simplificada['base_tributavel'] <= 5000:
        print(f"  ISENCAO TOTAL (Simplificada): R$ 0,00")

    if abs(diferenca) < 0.01:
        print(f"\n  >> Praticamente igual! Escolha pela facilidade.")
    elif diferenca > 0:
        print(f"\n  OK MAIS VANTAJOSA: SIMPLIFICADA")
        print(f"  Economia: R$ {diferenca:,.2f} por mes")
    else:
        print(f"\n  OK MAIS VANTAJOSA: COMPLETA")
        print(f"  Economia: R$ {abs(diferenca):,.2f} por mes")


def exibir_tendencia_2025_2026(salario_bruto, contribuicao_previdencia, 
                              despesa_saude=0):
    """
    Exibe tendencia de IR 2025 vs 2026 para ambos os modelos
    """
    print("\n" + "="*70)
    print("TENDENCIA 2025 vs 2026 (IMPACTO DA REFORMA)")
    print("="*70)

    # 2025
    compl_2025 = calcular_ir_2025_completo(salario_bruto, contribuicao_previdencia, 
                                           despesa_saude)
    simpl_2025 = calcular_ir_2025_simplificado(salario_bruto, contribuicao_previdencia)

    # 2026
    compl_2026 = calcular_ir_2026_completo(salario_bruto, contribuicao_previdencia, 
                                          despesa_saude)
    simpl_2026 = calcular_ir_2026_simplificado(salario_bruto, contribuicao_previdencia)

    # Tabela comparativa
    print(f"\n{'Modelo':<15} | {'2025':<12} | {'2026':<12} | {'Economia':<12}")
    print(f"{'-'*55}")
    print(f"{'Completa':<15} | R$ {compl_2025['ir_final']:>9,.2f} | R$ {compl_2026['ir_final']:>9,.2f} | R$ {compl_2025['ir_final'] - compl_2026['ir_final']:>9,.2f}")
    print(f"{'Simplificada':<15} | R$ {simpl_2025['ir_final']:>9,.2f} | R$ {simpl_2026['ir_final']:>9,.2f} | R$ {simpl_2025['ir_final'] - simpl_2026['ir_final']:>9,.2f}")

    economia_total_compl = (compl_2025['ir_final'] - compl_2026['ir_final']) * 12
    economia_total_simpl = (simpl_2025['ir_final'] - simpl_2026['ir_final']) * 12

    print(f"\nEconomia Anual (2025 >> 2026):")
    print(f"  Completa: R$ {economia_total_compl:,.2f}")
    print(f"  Simplificada: R$ {economia_total_simpl:,.2f}")


# Exemplo de uso
if __name__ == "__main__":
    print("\n" + "="*70)
    print("CALCULADORA COMPLETA DE IRRF 2025 vs 2026")
    print("Comparacao: Simplificada vs Completa")
    print("="*70)

    # Dados do contracheque (Daniel - seu caso)
    salario_bruto = 4161.00
    contribuicao_previdencia = 499.32  # FUNCEF 12%
    despesa_saude = 145.63  # Saude Caixa mensal

    print(f"\n### CENARIO: SEU CONTRACHEQUE (outubro/2025)")
    print(f"    Salario: R$ {salario_bruto:,.2f}")
    print(f"    FUNCEF (12%%): R$ {contribuicao_previdencia:,.2f}")
    print(f"    Saude: R$ {despesa_saude:,.2f}")

    # Comparacoes 2025
    exibir_comparacao_2025(salario_bruto, contribuicao_previdencia, despesa_saude)

    # Comparacoes 2026
    exibir_comparacao_2026(salario_bruto, contribuicao_previdencia, despesa_saude)

    # Tendencia
    exibir_tendencia_2025_2026(salario_bruto, contribuicao_previdencia, despesa_saude)

    # Exemplos adicionais
    print("\n\n### EXEMPLO 2: SALARIO R$ 9.000,00")
    salario_ex2 = 9000.00
    contrib_ex2 = salario_ex2 * 0.12
    saude_ex2 = 145.63

    exibir_comparacao_2025(salario_ex2, contrib_ex2, saude_ex2)
    exibir_comparacao_2026(salario_ex2, contrib_ex2, saude_ex2)
    exibir_tendencia_2025_2026(salario_ex2, contrib_ex2, saude_ex2)

    print("\n" + "="*70)
    print("Script atualizado com calculos de Simplificada vs Completa")
    print("Data: Novembro 2025 | PL 1087/2025 (Reforma do IR)")
    print("="*70)
