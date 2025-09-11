from app.models import Produto, TaxaPagamento, User

def seed_data(db):
    """Popula o banco de dados com dados iniciais."""
    print("Verificando se o banco de dados precisa ser populado...")

    # Se já existir um usuário, não faz nada
    if User.query.count() > 0:
        print("Banco de dados já populado. Nenhuma ação necessária.")
        return

    print("Banco de dados vazio, populando com dados iniciais...")
    
    # Apaga dados antigos (garantia extra)
    db.session.query(Produto).delete()
    db.session.query(TaxaPagamento).delete()
    db.session.query(User).delete()

    # Adiciona usuário admin
    admin_user = User(id=1, username='admin')
    db.session.add(admin_user)

    # Adiciona taxas
    taxas = [
        {'metodo': 'Pix', 'taxa_percentual': 0.00, 'coeficiente': 1.0000},
        {'metodo': 'Débito', 'taxa_percentual': 1.09, 'coeficiente': 0.9891},
        {'metodo': '1x', 'taxa_percentual': 3.48, 'coeficiente': 0.9652},
        {'metodo': '2x', 'taxa_percentual': 5.10, 'coeficiente': 0.9490},
        # ... (pode adicionar as outras taxas se quiser)
    ]
    for t in taxas:
        nova_taxa = TaxaPagamento(**t)
        db.session.add(nova_taxa)

    # Adiciona produtos
    produtos = [
        {'codigo': 'TAU0001', 'nome': 'Pistola Taurus G2C .38TPC', 'valor_fornecedor_real': 3424.00, 'desconto_fornecedor_percentual': 2.0},
        {'codigo': 'TAU00050', 'nome': 'PISTOLA TAURUS GX4 CARREY .38TPC PRETA', 'valor_fornecedor_real': 5100.00},
    ]
    for p_data in produtos:
        novo_produto = Produto(**p_data)
        db.session.add(novo_produto)

    db.session.commit()
    print("Dados iniciais inseridos com sucesso!")