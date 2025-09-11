from app import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    custo_total = db.Column(db.Float, nullable=False, default=0.0)

    # Tipos de cálculo de lucro
    tipo_lucro = db.Column(db.String(20), nullable=False, default="margem")  # margem | alvo | preco
    margem = db.Column(db.Float, nullable=True, default=0.0)      # usado se tipo_lucro = margem
    lucro_alvo = db.Column(db.Float, nullable=True, default=0.0)  # usado se tipo_lucro = alvo
    preco_final_desejado = db.Column(db.Float, nullable=True, default=0.0)  # usado se tipo_lucro = preco

    # Impostos
    ipi = db.Column(db.Float, nullable=True, default=0.0)       # valor do IPI (pode ser % ou R$)
    ipi_tipo = db.Column(db.String(10), nullable=False, default="percent")  # percent | real
    difal = db.Column(db.Float, nullable=True, default=0.0)     # sempre em %

    # Valores calculados
    valor_ipi = db.Column(db.Float, nullable=True, default=0.0)
    valor_difal = db.Column(db.Float, nullable=True, default=0.0)
    preco_a_vista = db.Column(db.Float, nullable=True, default=0.0)
    lucro_liquido_real = db.Column(db.Float, nullable=True, default=0.0)

    def calcular_precos(self):
        """Calcula preço de venda e impostos com base no tipo de lucro e IPI selecionados."""

        preco_base = 0

        # Tipo de lucro escolhido
        if self.tipo_lucro == "margem":
            preco_base = self.custo_total * (1 + (self.margem or 0)/100)
        elif self.tipo_lucro == "alvo":
            preco_base = self.custo_total + (self.lucro_alvo or 0)
        elif self.tipo_lucro == "preco":
            preco_base = self.preco_final_desejado or self.custo_total

        # Cálculo do IPI
        if self.ipi_tipo == "percent":
            self.valor_ipi = preco_base * ((self.ipi or 0)/100)
        else:  # ipi_tipo == "real"
            self.valor_ipi = self.ipi or 0

        # Cálculo do DIFAL
        self.valor_difal = preco_base * ((self.difal or 0)/100)

        # Soma dos impostos
        total_impostos = (self.valor_ipi or 0) + (self.valor_difal or 0)

        # Preço final ao consumidor
        self.preco_a_vista = preco_base + total_impostos

        # Lucro líquido real (preço final - custo - impostos)
        self.lucro_liquido_real = self.preco_a_vista - self.custo_total - total_impostos
