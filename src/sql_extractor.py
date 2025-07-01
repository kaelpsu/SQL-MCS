import sqlglot
from sqlglot import exp

def get_clauses_from_ast(where_clause_ast):
    """
    Versão simplificada do Algoritmo 1 que opera diretamente na AST (Árvore de Sintaxe Abstrata)
    gerada por um parser SQL para extrair os nós de cada tipo de cláusula.
    """
    if not where_clause_ast:
        return [], [], []

    in_clauses_nodes = []
    equals_clauses_nodes = []
    notnull_clauses_nodes = []

    # 1. Encontra todas as expressões 'IN'
    for expression in where_clause_ast.find_all(exp.In):
        print(f"Encontrada expressão IN: {expression}")
        if isinstance(expression.this, exp.Column):
            in_clauses_nodes.append(expression.this.name)

    # 2. Encontra todas as expressões de igualdade ('=')
    for expression in where_clause_ast.find_all(exp.EQ):
        print(f"Encontrada expressão de igualdade: {expression}")
        if isinstance(expression.left, exp.Column):
            equals_clauses_nodes.append(expression.left.name)

    # 3. Encontra todas as expressões 'IS NOT NULL'
    for expression in where_clause_ast.find_all(exp.Is):
        print(f"Encontrada expressão IS NOT NULL: {expression}")
        # Verifica se a expressão é do tipo '... IS NOT NULL'
        if isinstance(expression.this, exp.Column):
            notnull_clauses_nodes.append(expression.this.name)
    
    # O retorno usa set() para remover duplicatas, caso uma coluna apareça em múltiplas cláusulas do mesmo tipo.
    return list(set(in_clauses_nodes)), list(set(equals_clauses_nodes)), list(set(notnull_clauses_nodes))


# --- Demonstração de uso ---
if __name__ == "__main__":
    # Query de exemplo complexa
    sql = "SELECT a, b FROM table WHERE (c = 10 AND d IN ('x', 'y')) AND e IS NOT NULL AND c = 20;"

    # 1. Fazer o parsing da query completa
    ast = sqlglot.parse_one(sql)

    # 2. Isolar a cláusula WHERE da AST
    where_clause = ast.find(exp.Where)

    # 3. Chamar a função simplificada
    if where_clause:
        in_nodes, equals_nodes, notnull_nodes = get_clauses_from_ast(where_clause.this)

        print(f"Nós em cláusulas IN: {in_nodes}")
        print(f"Nós em cláusulas de IGUALDADE: {equals_nodes}")
        print(f"Nós em cláusulas IS NOT NULL: {notnull_nodes}")