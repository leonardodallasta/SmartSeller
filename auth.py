from tkinter import messagebox, Toplevel
import ttkbootstrap as ttk
from database import conectar_banco, cadastrar_usuario


def verificar_login(entry_usuario, entry_senha, mostrar_botao_criar_usuario):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conexao = conectar_banco("postgres", "123")  # Substitua com suas credenciais
    if not conexao:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tb_usuarios WHERE nome_usuario = %s AND senha = %s", (usuario, senha))
        usuario_valido = cursor.fetchone()
        if usuario_valido:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            mostrar_botao_criar_usuario()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        
        conexao.commit()
        cursor.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar login: {e}")
    finally:
        conexao.close()

def mostrar_janela_criar_usuario(root):
    janela_criar_usuario = Toplevel(root)
    janela_criar_usuario.title("Criar Novo Usuário")
    janela_criar_usuario.geometry("300x250")

    label_nome_usuario = ttk.Label(janela_criar_usuario, text="Nome de Usuário")
    label_nome_usuario.pack(fill="x", padx=10, pady=(10, 5))
    entry_nome_usuario = ttk.Entry(janela_criar_usuario)
    entry_nome_usuario.pack(fill="x", padx=10, pady=5)

    label_senha = ttk.Label(janela_criar_usuario, text="Senha")
    label_senha.pack(fill="x", padx=10, pady=(5, 0))
    entry_senha_criar = ttk.Entry(janela_criar_usuario, show="*")
    entry_senha_criar.pack(fill="x", padx=10, pady=5)

    def registrar_usuario():
        novo_usuario = entry_nome_usuario.get()
        nova_senha = entry_senha_criar.get()

        try:
            conexao = conectar_banco("postgres", "123")  # Substitua com suas credenciais
            if conexao:
                if cadastrar_usuario_tb_usuarios(conexao, novo_usuario, nova_senha):
                    messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
                    janela_criar_usuario.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao registrar usuário.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")
            conexao.rollback()
        finally:
            if conexao:
                conexao.close()

    botao_registrar = ttk.Button(janela_criar_usuario, text="Registrar", command=registrar_usuario, bootstyle=(ttk.constants.SUCCESS, ttk.constants.OUTLINE))
    botao_registrar.pack(pady=20, padx=10)

# Função para cadastrar usuário na tabela tb_usuarios
def cadastrar_usuario_tb_usuarios(conexao, usuario, senha):
    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO tb_usuarios (nome_usuario, senha) VALUES (%s, %s)", (usuario, senha))
        conexao.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False
