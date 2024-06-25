# celular.py
from tkinter import messagebox, Toplevel
import ttkbootstrap as ttk
from database import conectar_banco
from random import randint

def cadastrar_celular(root, entry_usuario, entry_senha):
    janela_cadastrar = Toplevel(root)
    janela_cadastrar.title("Cadastrar Celular")
    janela_cadastrar.geometry("400x500")

    labels_texts = ["Nome", "Ano de Fabricação (YYYY)", "Armazenamento (GB)", "Condição", "Valor (R$)", "Quantidade"]
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
            # Verificar se o ano de fabricação é válido
            ano_fabricacao = int(valores["Ano de Fabricação (YYYY)"])
            if ano_fabricacao < 1900 or ano_fabricacao > 2100:
                messagebox.showerror("Erro", "Ano de fabricação inválido.")
                return
            
            # Verificar se os outros valores numéricos são válidos
            armazenamento = int(valores["Armazenamento (GB)"])
            valor = float(valores["Valor (R$)"])
            quantidade = int(valores["Quantidade"])

            conexao = conectar_banco(entry_usuario.get(), entry_senha.get())
            if conexao:
                cursor = conexao.cursor()
                cel_codigo = randint(100000, 999999)
                query = """
                INSERT INTO tb_celulares (cel_codigo, cel_nome, cel_ano_fabricacao, cel_armazenamento, cel_condicao, cel_valor, cel_quantidade, tb_fornecedores_for_codigo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    cel_codigo,
                    valores["Nome"],
                    ano_fabricacao,
                    armazenamento,
                    valores["Condição"],
                    valor,
                    quantidade,
                    1  # Usando o código padrão do fornecedor (1)
                ))
                conexao.commit()
                cursor.close()
                messagebox.showinfo("Sucesso", "Celular cadastrado com sucesso!")
                janela_cadastrar.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Verifique se os valores de ano, armazenamento, valor e quantidade são válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar celular: {e}")
            if conexao:
                conexao.rollback()
        finally:
            if conexao:
                conexao.close()

    botao_salvar = ttk.Button(janela_cadastrar, text="Salvar", command=salvar_celular, style="success.TButton")
    botao_salvar.pack(pady=20, padx=10)

    janela_cadastrar.transient(root)
    janela_cadastrar.grab_set()
    janela_cadastrar.wait_window()
