# fazer_compra.py
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import Toplevel, messagebox
from database import conectar_banco, vender_celular

def mostrar_janela_compra(root, entry_usuario, entry_senha):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conexao = conectar_banco(usuario, senha)
    if not conexao:
        return

    janela_compra = Toplevel(root)
    janela_compra.title("Comprar Celular")
    janela_compra.geometry("500x400")

    # Obter celulares do banco de dados
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT cel_codigo, cel_nome FROM tb_celulares")
        celulares = cursor.fetchall()
        cursor.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar celulares: {e}")
        return

    for celular in celulares:
        codigo, nome = celular
        botao_comprar = ttk.Button(janela_compra, text=f"Comprar {nome}", command=lambda codigo=codigo: realizar_compra(codigo))
        botao_comprar.pack(pady=10)

    def realizar_compra(codigo_celular):
        # Solicitar informações do cartão de crédito
        nome_cartao = input("Digite o nome no cartão: ")
        cpf = input("Digite o CPF: ")
        numero_cartao = input("Digite o número do cartão: ")
        data_vencimento = input("Digite a data de vencimento (MM/AA): ")
        codigo_seguranca = input("Digite o código de segurança: ")

        # Verificar se todas as informações foram preenchidas
        if not all([nome_cartao, cpf, numero_cartao, data_vencimento, codigo_seguranca]):
            messagebox.showerror("Erro", "Preencha todas as informações do cartão.")
            return

        # Tentar vender o celular
        if vender_celular(conexao, codigo_celular):
            messagebox.showinfo("Sucesso", "Compra realizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao realizar a compra.")

if __name__ == "__main__":
    root = tk.Tk()
    entry_usuario = ttk.Entry(root)
    entry_senha = ttk.Entry(root, show='*')
    mostrar_janela_compra(root, entry_usuario, entry_senha)
    root.mainloop()
