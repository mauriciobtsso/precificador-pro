from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Produto
from . import main

@main.route('/produtos')
def produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@main.route('/produto/novo', methods=['GET', 'POST'])
@main.route('/produto/editar/<int:produto_id>', methods=['GET', 'POST'])
def gerenciar_produto(produto_id=None):
    produto = Produto.query.get(produto_id) if produto_id else None

    if request.method == 'POST':
        if not produto:
            produto = Produto()
            db.session.add(produto)

        produto.codigo = request.form['nome'][:6].upper()
        produto.nome = request.form['nome']
        produto.custo_total = float(request.form.get('custo', 0))
        produto.margem = float(request.form.get('margem', 0))
        produto.ipi = float(request.form.get('ipi', 0))
        produto.difal = float(request.form.get('difal', 0))

        produto.calcular_precos()

        db.session.commit()
        flash('Produto salvo com sucesso!', 'success')
        return redirect(url_for('main.produtos'))

    return render_template('produto_form.html', produto=produto)

@main.route('/produto/excluir/<int:produto_id>')
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('main.produtos'))
