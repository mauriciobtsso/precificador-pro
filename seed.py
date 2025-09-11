from app.models import Produto, TaxaPagamento, User

def seed_data(db):
    """Popula o banco de dados com dados iniciais se estiver vazio."""
    print("Verificando se o banco de dados precisa ser populado...")
    if User.query.count() > 0:
        print("Banco de dados já populado.")
        return

    print("Populando banco de dados com dados iniciais...")
    
    db.session.add(User(id=1, username='admin'))

    taxas = [
        {'metodo': 'Pix', 'taxa_percentual': 0.00, 'coeficiente': 1.0000},
        {'metodo': 'Débito', 'taxa_percentual': 1.09, 'coeficiente': 0.9891},
        {'metodo': '1x', 'taxa_percentual': 3.48, 'coeficiente': 0.9652},
        {'metodo': '2x', 'taxa_percentual': 5.10, 'coeficiente': 0.9490},
        {'metodo': '3x', 'taxa_percentual': 5.92, 'coeficiente': 0.9408},
        {'metodo': '4x', 'taxa_percentual': 6.79, 'coeficiente': 0.9321},
        {'metodo': '5x', 'taxa_percentual': 7.61, 'coeficiente': 0.9239},
        {'metodo': '6x', 'taxa_percentual': 8.43, 'coeficiente': 0.9157},
        {'metodo': '7x', 'taxa_percentual': 9.25, 'coeficiente': 0.9075},
        {'metodo': '8x', 'taxa_percentual': 10.07, 'coeficiente': 0.8993},
        {'metodo': '9x', 'taxa_percentual': 10.89, 'coeficiente': 0.8911},
        {'metodo': '10x', 'taxa_percentual': 11.71, 'coeficiente': 0.8829},
        {'metodo': '11x', 'taxa_percentual': 12.53, 'coeficiente': 0.8747},
        {'metodo': '12x', 'taxa_percentual': 13.35, 'coeficiente': 0.8665}
    ]
    for t_data in taxas:
        db.session.add(TaxaPagamento(**t_data))

    produtos = [
        {'codigo': 'TAU0001', 'nome': 'Pistola Taurus G2C .38TPC', 'valor_fornecedor_real': 3424.00, 'desconto_fornecedor_percentual': 2.0},
        {'codigo': 'TAU00050', 'nome': 'PISTOLA TAURUS GX4 CARREY .38TPC PRETA', 'valor_fornecedor_real': 5100.00},
    ]
    for p_data in produtos:
        db.session.add(Produto(**p_data))

    db.session.commit()
    print("Dados iniciais inseridos com sucesso!")