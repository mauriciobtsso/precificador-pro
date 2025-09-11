from app import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    custo_total = db.Column(db.Float, nullable=False, default=0.0)
    margem = db.Column(db.Float, nullable=False, default=0.0)
    preco_a_vista = db.Column(db.Float, nullable=True)
    lucro_liquido_real = db.Column(db.Float, nullable=True)

    # Novos campos
    ipi = db.Column(db.Float, nullable=True, default=0.0)
    difal = db.Column(db.Float, nullable=True, default=0.0)
    valor_ipi = db.Column(db.Float, nullable=True, default=0.0)
    valor_difal = db.Column(db.Float, nullable=True, default=0.0)

    def calcular_precos(self):
        """Método auxiliar para calcular preços e impostos."""
        preco_base = self.custo_total * (1 + (self.margem or 0)/100)
        self.valor_ipi = preco_base * ((self.ipi or 0)/100)
        self.valor_difal = preco_base * ((self.difal or 0)/100)
        total_impostos = self.valor_ipi + self.valor_difal
        self.preco_a_vista = preco_base + total_impostos
        self.lucro_liquido_real = self.preco_a_vista - self.custo_total - total_impostos
