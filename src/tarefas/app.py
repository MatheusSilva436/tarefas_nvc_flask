from flask import Flask, redirect, render_template, request, url_for
 
from tarefas.models.database import init_db
from tarefas.models.tarefa import Tarefa
 
app = Flask(__name__)
 
with app.app_context():
    init_db()
   
@app.route('/test')
def test():
    return 'Servidor online!'
 
@app.route('/', methods=['GET', 'POST'])
def home():
 
    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa']
        data_conclusao_form = request.form['dataConclusao']
 
        data_corrigida = data_conclusao_form or None
    
        tarefa = Tarefa(titulo=titulo_form, data_conclusao=data_corrigida)
       
        tarefa.salvarTarefa()
 
        return redirect(url_for('home'))
 
    tarefas = Tarefa.listarTarefas()
 
    return render_template(
        'base.html',
        titulo_da_pagina='Minha lista de tarefas',
        titulo='Minha lista de tarefas',
        tarefas_da_pagina=tarefas,
        tarefa=None
    )
 
@app.route('/delete/<int:id>')
def apagar_id_especificado(id):
    Tarefa.apagarTarefa(id)
    return redirect(url_for('home'))
 

@app.route('/atualizar/<int:id_tarefa>', methods=['GET', 'POST'])
def atualizar_tarefa(id_tarefa):
 
    tarefa = Tarefa.buscarTarefa(id_tarefa)
 
    if tarefa is None:
        return redirect(url_for('home'))
 
    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa'] 
        data_conclusao_form = request.form['dataConclusao'] 
 
        data_corrigida = data_conclusao_form or None

        Tarefa.atualizarTarefa(
            id_tarefa,
            titulo_form,
            data_corrigida
        )
 
        return redirect(url_for('home'))
 
    return render_template(
        'base.html',
        titulo='Atualizar tarefa',
        titulo_da_pagina='Atualizar tarefa',
        tarefas_da_pagina=Tarefa.listarTarefas(),
        tarefa=tarefa
    )
 
 
if __name__ == '__main__':
    app.run()