from flask import Flask, render_template, request, redirect, url_for
from model import AppBD
from datetime import datetime

app = Flask(__name__)

banco = AppBD()
banco.criarTabelas()
# Dados para inserir na tabela codicoes

# inserir condições padrão
descricao_condicoes = ["Pix", "Dinheiro", "Boleto Bancário",
                       "Cartão de Crédito", "Cartão de Débito"]
banco.inserirCondicoesPadrao(descricao_condicoes)

# inserir condições padrão
descricao_Status = ["Receita", "Receita Pendente",
                    "Despesas Paga", "Despesas Pendente"]
banco.inserirStatusPadrao(descricao_Status)


def formatar_data(data):
    if isinstance(data, str):
        data = datetime.strptime(data, '%Y-%m-%d')
    return data.strftime('%d/%m/%Y')


def calcular_total(despesas):
    total = 0
    for despesa in despesas:
        total += despesa[3]  # Assume que o valor está na posição 3 da lista
    return total


app.jinja_env.filters['formatar_data'] = formatar_data


@app.route('/')
def index():
    condicoes = banco.selectCondicoes()
    status = banco.selectStatus()
    despesas = banco.selecionarDespesas()
    return render_template('index.html', condicoes=condicoes, status=status, despesas=despesas)


@app.route('/gerenciar_condicoes', methods=['GET', 'POST'])
def gerenciar_condicoes():
    if request.method == 'POST':
        if 'adicionar_condicao' in request.form:
            nova_condicao = request.form['nova_condicao']
            print(f'Adicionando condição: {nova_condicao}')
            banco.inserirCondicao(nova_condicao)
        elif 'deletar_condicao' in request.form:
            descricao_condicao = request.form['descricao_condicao']
            print(f'Deletando condição: {descricao_condicao}')
            banco.deletarCondicao(descricao_condicao)
        return redirect(url_for('index'))
    condicoes = banco.selectCondicoes()
    return render_template('index.html', condicoes=condicoes)


@app.route('/gerenciar_status', methods=['GET', 'POST'])
def gerenciar_status():
    if request.method == 'POST':
        if 'adicionar_status' in request.form:
            novo_status = request.form['novo_status']
            print(f'Adicionando status: {novo_status}')
            banco.inserirStatus(novo_status)
        elif 'deletar_status' in request.form:
            descricao_status = request.form['descricao_status']
            print(f'Deletando status: {descricao_status}')
            banco.deletarStatus(descricao_status)
        return redirect(url_for('index'))
    status = banco.selectStatus()
    return render_template('index.html', status=status)


@app.route('/adicionar_status', methods=['POST'])
def adicionar_status():
    if request.method == 'POST':
        novo_status = request.form['novo_status']
        banco.inserirStatus(novo_status)
        return redirect(url_for('index'))


@app.route('/gerenciar_despesas', methods=['GET', 'POST'])
def gerenciar_despesas():
    if request.method == 'POST':
        if 'adicionar_despesa' in request.form:
            descricao = request.form['descricao']
            data = request.form['data']
            valor = float(request.form['valor'])
            id_condicao = int(request.form['id_condicao'])
            id_status = int(request.form['id_status'])
            banco.inserirDespesa(descricao, data, valor,
                                 id_condicao, id_status)
        elif 'deletar_despesa' in request.form:
            despesa_id = int(request.form['despesa_id'])
            banco.deletarDespesa(despesa_id)
        elif 'atualizar_despesa' in request.form:
            despesa_id = int(request.form['despesa_id'])
            descricao = request.form['descricao']
            data = request.form['data']
            valor = float(request.form['valor'])
            id_condicao = int(request.form['id_condicao'])
            id_status = int(request.form['id_status'])
            banco.atualizarDespesa(despesa_id, descricao,
                                   data, valor, id_condicao, id_status)
        return redirect(url_for('index'))
    condicoes = banco.selectCondicoes()
    status = banco.selectStatus()
    despesas = banco.selecionarDespesas()
    return render_template('index.html', condicoes=condicoes, status=status, despesas=despesas)


@app.route('/atualizar_despesa', methods=['POST'])
def atualizar_despesa():
    if request.method == 'POST':
        despesa_id = request.form['despesa_id']
        descricao = request.form['descricao']
        data = request.form['data']
        valor = float(request.form['valor'])
        id_condicao = int(request.form['id_condicao'])
        id_status = int(request.form['id_status'])
        banco.atualizarDespesa(despesa_id, descricao,
                               data, valor, id_condicao, id_status)
        return redirect(url_for('index'))
    else:
        # Aqui você pode preencher as opções dos campos select com os dados do banco
        condicoes = banco.selectCondicoes()
        status = banco.selectStatus()
        return render_template('index.html', condicoes=condicoes, status=status)


@app.route('/editar_despesa/<int:despesa_id>', methods=['GET', 'POST'])
def editar_despesa(despesa_id):
    despesa = banco.selecionarDespesaPorID(despesa_id)
    condicoes = banco.selectCondicoes()
    status = banco.selectStatus()
    if request.method == 'POST':
        descricao = request.form['descricao']
        data = request.form['data']
        valor = float(request.form['valor'])
        id_condicao = int(request.form['id_condicao'])
        id_status = int(request.form['id_status'])
        banco.atualizarDespesa(despesa_id, descricao,
                               data, valor, id_condicao, id_status)
        return redirect(url_for('index'))
    return render_template('index.html', despesa=despesa, condicoes=condicoes, status=status)


if __name__ == '__main__':
    app.run(debug=True)
