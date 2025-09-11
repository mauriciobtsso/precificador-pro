from app import create_app, db
from app.models import Produto, TaxaPagamento, User

# Cria uma instância da aplicação para termos acesso ao contexto do banco de dados
app = create_app()

def seed_data():
    with app.app_context():
        print("Limpando dados antigos...")
        # Apaga todos os dados para evitar duplicatas
        db.session.query(Produto).delete()
        db.session.query(TaxaPagamento).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("Inserindo usuário admin...")
        admin_user = User(id=1, username='admin')
        db.session.add(admin_user)
        db.session.commit()

        print("Inserindo taxas de pagamento...")
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
        for t in taxas:
            nova_taxa = TaxaPagamento(**t)
            db.session.add(nova_taxa)
        db.session.commit()

        print("Inserindo produtos iniciais...")
        produtos = [
            {'codigo': 'TAU0001', 'nome': 'Pistola Taurus G2C .38TPC', 'valor_fornecedor_real': 3424.00, 'desconto_fornecedor_percentual': 2.0},
            {'codigo': 'TAU00050', 'nome': 'PISTOLA TAURUS GX4 CARREY .38TPC PRETA', 'valor_fornecedor_real': 5100.00},
            {'codigo': 'TAU00229', 'nome': 'PISTOLA TAURUS GX2 .38TPC PRETA', 'valor_fornecedor_real': 4800.00},
            {'codigo': 'TAU00239', 'nome': 'PISTOLA TAURUS G3 TORO .38TPC PRETA', 'valor_fornecedor_real': 5250.00}
        ]
        for p_data in produtos:
            novo_produto = Produto(**p_data)
            db.session.add(novo_produto)
        db.session.commit()

        print("Dados iniciais inseridos com sucesso!")

# Permite que o script seja executado diretamente pelo terminal
if __name__ == '__main__':
    seed_data()