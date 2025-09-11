from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from . import main
from .. import db
from ..models import Produto, User, TaxaPagamento

# --- ROTAS DE AUTENTICAÇÃO E DASHBOARD ---
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == "admin" and password == "admin":
            user = User.query.get(1)
            if not user:
                 admin_user = User(id=1, username='admin')
                 db.session.add(admin_user)
                 db.session.commit()
                 user = admin_user
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado.", "info")
    return redirect(url_for("main.login"))

@main.route("/")
@login_required
def dashboard():
    produtos = Produto.query.all()
    total_lucro = 0
    total_preco_venda = 0
    produto_mais_lucrativo = None
    if produtos:
        for produto in produtos:
            if produto.lucro_liquido_real is not None:
                total_lucro += produto.lucro_liquido_real
            if produto.preco_a_vista is not None:
                total_preco_venda += produto.preco_a_vista
            if produto_mais_lucrativo is None or (produto.lucro_liquido_real is not None and produto.lucro_liquido_real > (produto_mais_lucrativo.lucro_liquido_real or 0)):
                produto_mais_lucrativo = produto
    media_margem_lucro = (total_lucro / total_preco_venda * 100) if total_preco_venda > 0 else 0
    return render_template("dashboard.html", media_margem_lucro=media_margem_lucro, produto_mais_lucrativo=produto_mais_lucrativo)

# --- ROTAS DE PRODUTOS ---
@main.route("/produtos")
@login_required
def produtos():
    lista_produtos = Produto.query.order_by(Produto.id).all()
    return render_template('produtos.html', produtos=lista_produtos)

@main.route("/produto/novo", methods=["GET", "POST"])
@main.route("/produto/editar/<int:produto_id>", methods=["GET", "POST"])
@login_required
def gerenciar_produto(produto_id=None):
    produto = Produto.query.get_or_404(produto_id) if produto_id else None
            
    if request.method == 'POST':
        def to_float(value):
            if not value: return 0.0
            cleaned_value = str(value).replace('R$', '').replace('.', '').replace('%', '').strip()
            cleaned_value = cleaned_value.replace(',', '.')
            if not cleaned_value: return 0.0
            return float(cleaned_value)

        # Atualiza o objeto produto com os novos dados do formulário
        target_produto = produto if produto_id else Produto()
        target_produto.codigo = request.form.get('codigo')
        target_produto.nome = request.form.get('nome')
        target_produto.valor_fornecedor_real = to_float(request.form.get('valor_fornecedor_real'))
        target_produto.desconto_fornecedor_percentual = to_float(request.form.get('desconto_fornecedor_percentual'))
        target_produto.frete_real = to_float(request.form.get('frete_real'))
        target_produto.ipi_tipo = request.form.get('ipi_tipo')
        target_produto.ipi_valor = to_float(request.form.get('ipi_valor'))
        target_produto.difal_percentual = to_float(request.form.get('difal_percentual'))
        target_produto.imposto_venda_percentual = to_float(request.form.get('imposto_venda_percentual'))
        target_produto.metodo_precificacao = request.form.get('metodo_precificacao')
        target_produto.valor_metodo = to_float(request.form.get('valor_metodo'))
        
        # Recalcula tudo com os dados do formulário
        valor_compra_desconto = target_produto.valor_fornecedor_real * (1 - (target_produto.desconto_fornecedor_percentual / 100))
        valor_ipi = 0.0
        if target_produto.ipi_tipo == 'percentual' and target_produto.ipi_valor > 0:
            valor_ipi = valor_compra_desconto - (valor_compra_desconto / (1 + (target_produto.ipi_valor / 100)))
        else:
            valor_ipi = target_produto.ipi_valor
        base_calculo_difal = (valor_compra_desconto - valor_ipi) + target_produto.frete_real
        valor_difal = base_calculo_difal * (target_produto.difal_percentual / 100)
        target_produto.custo_total = valor_compra_desconto + target_produto.frete_real + valor_difal

        preco_a_vista = 0.0
        if target_produto.metodo_precificacao == 'margem' and target_produto.valor_metodo < 100:
            denominador = (1 - (target_produto.imposto_venda_percentual / 100) - (target_produto.valor_metodo / 100))
            if denominador > 0: preco_a_vista = target_produto.custo_total / denominador
        elif target_produto.metodo_precificacao == 'lucro_alvo':
            denominador = (1 - (target_produto.imposto_venda_percentual / 100))
            if denominador > 0: preco_a_vista = (target_produto.custo_total + target_produto.valor_metodo) / denominador
        elif target_produto.metodo_precificacao == 'preco_final':
            preco_a_vista = target_produto.valor_metodo

        valor_imposto_venda = preco_a_vista * (target_produto.imposto_venda_percentual / 100)
        target_produto.preco_a_vista = preco_a_vista
        target_produto.lucro_liquido_real = preco_a_vista - target_produto.custo_total - valor_imposto_venda
        
        if not produto_id:
            db.session.add(target_produto)
            flash('Produto salvo com sucesso!', 'success')
        else:
            flash('Produto atualizado com sucesso!', 'success')
        
        db.session.commit()
        return redirect(url_for('main.produtos'))

    taxas = TaxaPagamento.query.all()
    taxas_dict = {t.metodo: t for t in taxas}
    return render_template("produto_form.html", produto=produto, taxas_dict=taxas_dict)

@main.route('/produto/excluir/<int:produto_id>')
@login_required
def excluir_produto(produto_id):
    produto_para_excluir = Produto.query.get_or_404(produto_id)
    db.session.delete(produto_para_excluir)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'danger')
    return redirect(url_for('main.produtos'))

# --- ROTAS DE TAXAS ---
@main.route("/taxas")
@login_required
def taxas():
    lista_taxas = TaxaPagamento.query.order_by(TaxaPagamento.id).all()
    return render_template('taxas.html', taxas=lista_taxas)

@main.route('/taxa/nova', methods=['GET', 'POST'])
@main.route('/taxa/editar/<int:taxa_id>', methods=['GET', 'POST'])
@login_required
def gerenciar_taxa(taxa_id=None):
    taxa = TaxaPagamento.query.get_or_404(taxa_id) if taxa_id else None
    if request.method == 'POST':
        def to_float(value):
            if not value: return 0.0
            return float(str(value).replace(',', '.').strip())

        target_taxa = taxa if taxa_id else TaxaPagamento()
        target_taxa.metodo = request.form.get('metodo')
        target_taxa.taxa_percentual = to_float(request.form.get('taxa_percentual'))
        if target_taxa.taxa_percentual >= 0 and target_taxa.taxa_percentual < 100:
            target_taxa.coeficiente = 1 - (target_taxa.taxa_percentual / 100)
        
        if not taxa_id:
            db.session.add(target_taxa)
            flash('Taxa adicionada com sucesso!', 'success')
        else:
            flash('Taxa atualizada com sucesso!', 'success')
        
        db.session.commit()
        return redirect(url_for('main.taxas'))

    return render_template('taxa_form.html', taxa=taxa)

@main.route('/taxa/excluir/<int:taxa_id>')
@login_required
def excluir_taxa(taxa_id):
    taxa_para_excluir = TaxaPagamento.query.get_or_404(taxa_id)
    db.session.delete(taxa_para_excluir)
    db.session.commit()
    flash('Taxa excluída com sucesso!', 'danger')
    return redirect(url_for('main.taxas'))
