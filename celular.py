# celular py
from tkinter import messagebox, Toplevel
import ttkbootstrap as ttk
from database import conectar_banco
from random import randint

def cadastrar_celular(root, entry_usuario, entry_senha):
    janela_cadastrar = Toplevel(root)
    janela_cadastrar.title("Cadastrar Celular")
    janela_cadastrar.geometry("400x500")

    labels_texts = ["Nome", "Data de Fabricação (YYYY-MM-DD)", "Armazenamento (GB)", "Condição", "Valor (R$)", "Quantidade"]
    entries = {}

    for text in labels_texts:
        label = ttk.Label(janela_cadastrar, text=text)
        label.pack(fill="x", padx=10, pady=(10, 5))
        entry = ttk.Entry(janela_cadastrar)
        entry.pack(fill="x", padx=10, pady=5)
        entries[text] = entry

    def salvar_celular():
        valores = {k: v.get() for k, v in entries.items()}

        if not all(valores.values()):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            conexao = conectar_banco(entry_usuario.get(), entry_senha.get())
            if conexao:
                cursor = conexao.cursor()
                cel_codigo = randint(100000, 999999)
                query = """
                INSERT INTO tb_celulares (cel_codigo, cel_nome, cel_data_fabricacao, cel_armazenamento, cel_condicao, cel_valor, cel_quantidade, tb_fornecedores_for_codigo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    cel_codigo,
                    valores["Nome"],
                    valores["Data de Fabricação (YYYY-MM-DD)"],
                    int(valores["Armazenamento (GB)"]),
                    valores["Condição"],
                    float(valores["Valor (R$)"]),
                    int(valores["Quantidade"]),
                    1  # Usando o código padrão do fornecedor (1)
                ))
                conexao.commit()
                cursor.close()
                conexao.close()
                messagebox.showinfo("Sucesso", "Celular cadastrado com sucesso!")
                janela_cadastrar.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar celular: {e}")

    botao_salvar = ttk.Button(janela_cadastrar, text="Salvar", command=salvar_celular, bootstyle=(ttk.constants.SUCCESS, ttk.constants.OUTLINE))
    botao_salvar.pack(pady=20, padx=10)
