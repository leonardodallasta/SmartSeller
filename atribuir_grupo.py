# atribuir_grupo.py
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from database import conectar_banco, atribuir_grupo
from auth import verificar_login

# Variáveis globais para armazenar a conexão e o usuário conectado
conexao = None
usuario_logado = None

def realizar_atribuicao(combo_usuario, combo_grupo):
    global conexao, usuario_logado
    
    if not conexao or not usuario_logado:
        messagebox.showerror("Erro", "Faça login para acessar esta funcionalidade.")
        return
    
    usuario = combo_usuario.get()
    grupo = combo_grupo.get()

    if not usuario or not grupo:
        messagebox.showerror("Erro", "Selecione um usuário e um grupo para atribuição.")
        return

    if atribuir_grupo(usuario, grupo):
        messagebox.showinfo("Sucesso", f"Grupo atribuído com sucesso ao usuário {usuario}.")
    else:
        messagebox.showerror("Erro", f"Erro ao atribuir grupo ao usuário {usuario}.")

def realizar_login(usuario, senha):
    global conexao, usuario_logado

    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conexao = conectar_banco(usuario, senha)
    if conexao:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        usuario_logado = usuario
        abrir_janela_atribuir_grupo()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        usuario_logado = None

def mostrar_janela_atribuir_grupo():
    janela_login = tk.Toplevel()
    janela_login.title("Login")
    janela_login.geometry("300x180")  # Ajuste de tamanho da janela

    frame_login = ttk.Frame(janela_login)
    frame_login.pack(pady=20, padx=10)

    label_usuario = ttk.Label(frame_login, text="Usuário:")
    label_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_usuario = ttk.Entry(frame_login)
    entry_usuario.grid(row=0, column=1, padx=5, pady=5)

    label_senha = ttk.Label(frame_login, text="Senha:")
    label_senha.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_senha = ttk.Entry(frame_login, show="*")
    entry_senha.grid(row=1, column=1, padx=5, pady=5)

    def realizar_login_event():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        realizar_login(usuario, senha)

    botao_login = ttk.Button(frame_login, text="Login", command=realizar_login_event)
    botao_login.grid(row=2, column=0, columnspan=2, pady=10)

    janela_login.mainloop()

def abrir_janela_atribuir_grupo():
    global conexao, usuario_logado

    janela_atribuir_grupo = tk.Toplevel()
    janela_atribuir_grupo.title("Atribuir Grupo")
    janela_atribuir_grupo.geometry("400x300")

    try:
        cursor = conexao.cursor()

        # Obter nomes de usuários
        cursor.execute("SELECT nome_usuario FROM tb_usuarios")
        nomes_usuarios = [row[0] for row in cursor.fetchall()]

        # Obter nomes de grupos
        cursor.execute("SELECT nome_grupo FROM tb_grupos")
        nomes_grupos = [row[0] for row in cursor.fetchall()]

        cursor.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar dados do banco de dados: {e}")
        return

    # Dropdown para selecionar usuário
    label_usuario = ttk.Label(janela_atribuir_grupo, text="Selecione o Usuário:")
    label_usuario.pack(pady=10)
    combo_usuario = ttk.Combobox(janela_atribuir_grupo, values=nomes_usuarios, state="readonly")
    combo_usuario.pack(pady=5)

    # Dropdown para selecionar grupo
    label_grupo = ttk.Label(janela_atribuir_grupo, text="Selecione o Grupo:")
    label_grupo.pack(pady=10)
    combo_grupo = ttk.Combobox(janela_atribuir_grupo, values=nomes_grupos, state="readonly")
    combo_grupo.pack(pady=5)

    # Botão para atribuir grupo
    botao_atribuir_grupo = ttk.Button(janela_atribuir_grupo, text="Atribuir Grupo", command=lambda: realizar_atribuicao(combo_usuario, combo_grupo))
    botao_atribuir_grupo.pack(pady=20, padx=10)

    janela_atribuir_grupo.mainloop()

# Exemplo de chamada para testar a função
# mostrar_janela_atribuir_grupo()
