# estoque.py
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import Toplevel, BOTH, X, messagebox
from database import conectar_banco, vender_celular
import json

historico_transacoes = []

def mostrar_estoque(root, entry_usuario, entry_senha):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conexao = conectar_banco(usuario, senha)
    if not conexao:
        return

    janela_estoque = Toplevel(root)
    janela_estoque.title("Estoque de Celulares")
    janela_estoque.geometry("500x400")

    frame_estoque = ttk.Frame(janela_estoque)
    frame_estoque.pack(fill=BOTH, expand=True, padx=10, pady=10)

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT cel_codigo, cel_nome, cel_quantidade, cel_ano_fabricacao FROM tb_celulares")
        celulares = cursor.fetchall()
        
        for celular in celulares:
            codigo, nome, quantidade, ano_fabricacao = celular
            texto_celular = f"Nome: {nome} - Quantidade: {quantidade} - Ano de Fabricação: {ano_fabricacao}"
            label_celular = ttk.Label(frame_estoque, text=texto_celular, justify="left")
            label_celular.pack(fill=X, padx=10, pady=2)

            # Adiciona um botão de compra para cada celular
            botao_comprar = ttk.Button(frame_estoque, text="Vender", command=lambda codigo=codigo: realizar_compra(root, usuario, senha, codigo))
            botao_comprar.pack(pady=2)  # Adiciona o botão à interface gráfica

        cursor.close()
        conexao.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar celulares: {e}")
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def realizar_compra(root, usuario, senha, codigo_celular):
    janela_compra = Toplevel(root)
    janela_compra.title("Finalizar Compra")
    janela_compra.geometry("300x200")

    label_nome_cartao = ttk.Label(janela_compra, text="Nome no cartão:")
    entry_nome_cartao = ttk.Entry(janela_compra)
    label_cpf = ttk.Label(janela_compra, text="CPF:")
    entry_cpf = ttk.Entry(janela_compra)
    label_numero_cartao = ttk.Label(janela_compra, text="Número do cartão:")
    entry_numero_cartao = ttk.Entry(janela_compra)
    label_data_vencimento = ttk.Label(janela_compra, text="Data de vencimento (MM/AA):")
    entry_data_vencimento = ttk.Entry(janela_compra)
    label_codigo_seguranca = ttk.Label(janela_compra, text="Código de segurança:")
    entry_codigo_seguranca = ttk.Entry(janela_compra)

    label_nome_cartao.pack()
    entry_nome_cartao.pack()
    label_cpf.pack()
    entry_cpf.pack()
    label_numero_cartao.pack()
    entry_numero_cartao.pack()
    label_data_vencimento.pack()
    entry_data_vencimento.pack()
    label_codigo_seguranca.pack()
    entry_codigo_seguranca.pack()

    def finalizar_compra():
        nome_cartao = entry_nome_cartao.get()
        cpf = entry_cpf.get()
        numero_cartao = entry_numero_cartao.get()
        data_vencimento = entry_data_vencimento.get()
        codigo_seguranca = entry_codigo_seguranca.get()

        # Verificar se todas as informações foram preenchidas
        if not all([nome_cartao, cpf, numero_cartao, data_vencimento, codigo_seguranca]):
            messagebox.showerror("Erro", "Preencha todas as informações do cartão.")
            return

        # Tentar vender o celular
        conexao = conectar_banco(usuario, senha)
        if not conexao:
            return

        if vender_celular(conexao, codigo_celular):
            messagebox.showinfo("Sucesso", "Compra realizada com sucesso!")
            janela_compra.destroy()
            # Adicione a transação ao histórico
            historico_transacoes.append(('venda', codigo_celular))

            # Salve o histórico em um arquivo
            with open('historico_transacoes.json', 'w') as f:
                json.dump(historico_transacoes, f)
        else:
            messagebox.showerror("Erro", "Erro ao realizar a compra.")

    botao_finalizar_compra = ttk.Button(janela_compra, text="Finalizar Compra", command=finalizar_compra)
    botao_finalizar_compra.pack()


if __name__ == "__main__":
    root = tk.Tk()
    entry_usuario = ttk.Entry(root)
    entry_senha = ttk.Entry(root, show='*')
    mostrar_estoque(root, entry_usuario, entry_senha)
    root.mainloop()
