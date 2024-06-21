import psycopg2
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import messagebox, Toplevel, Entry, X, BOTH

# Função para conectar ao banco de dados
def conectar_banco(user, password):
    try:
        conexao = psycopg2.connect(
            database="pedido",
            host="localhost",
            user=user,
            password=password,
            port="5432",
            client_encoding='UTF8'
        )
        return conexao
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        else:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
    return None

# Função para verificar login
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    conexao = conectar_banco(usuario, senha)
    if conexao:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        mostrar_botao_criar_usuario()
        conexao.close()

# Função para mostrar a janela de criar novo usuário
def mostrar_janela_criar_usuario():
    janela_criar_usuario = Toplevel(root)
    janela_criar_usuario.title("Criar Novo Usuário")
    janela_criar_usuario.geometry("300x250")

    label_nome_usuario = ttk.Label(janela_criar_usuario, text="Nome de Usuário")
    label_nome_usuario.pack(fill=X, padx=10, pady=(10, 5))
    entry_nome_usuario = ttk.Entry(janela_criar_usuario)
    entry_nome_usuario.pack(fill=X, padx=10, pady=5)

    label_senha = ttk.Label(janela_criar_usuario, text="Senha")
    label_senha.pack(fill=X, padx=10, pady=(5, 0))
    entry_senha_criar = ttk.Entry(janela_criar_usuario, show="*")
    entry_senha_criar.pack(fill=X, padx=10, pady=5)

    def registrar_usuario():
        novo_usuario = entry_nome_usuario.get()
        nova_senha = entry_senha_criar.get()

        try:
            conexao = conectar_banco("postgres", "123")
            if conexao:
                cursor = conexao.cursor()
                query = f"CREATE USER {novo_usuario} WITH PASSWORD '{nova_senha}'"
                cursor.execute(query)
                conexao.commit()
                cursor.close()
                conexao.close()
                messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
                janela_criar_usuario.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")

    botao_registrar = ttk.Button(janela_criar_usuario, text="Registrar", command=registrar_usuario, bootstyle=(SUCCESS, OUTLINE))
    botao_registrar.pack(pady=20, padx=10)

# Função para mostrar o botão de criar novo usuário
def mostrar_botao_criar_usuario():
    label_usuario.pack_forget()
    entry_usuario.pack_forget()
    label_senha.pack_forget()
    entry_senha.pack_forget()
    botao_login.pack_forget()
    botao_criar_usuario.pack(pady=20, padx=10)
    botao_sair.pack(pady=20, padx=10)
    botao_estoque.pack(pady=20, padx=10)

# Função para voltar ao formulário de login
def retornar_para_login():
    botao_criar_usuario.pack_forget()
    botao_sair.pack_forget()
    botao_estoque.pack_forget()
    label_usuario.pack()
    entry_usuario.pack()
    label_senha.pack()
    entry_senha.pack()
    botao_login.pack(pady=(20, 10), padx=10)

# Função para mostrar o estoque de celulares
def mostrar_estoque():
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
        cursor.execute("SELECT cel_nome, cel_quantidade FROM tb_celulares")
        celulares = cursor.fetchall()

        for celular in celulares:
            nome, quantidade = celular
            texto_celular = f"Nome: {nome} - Quantidade: {quantidade}"
            label_celular = ttk.Label(frame_estoque, text=texto_celular, justify=LEFT)
            label_celular.pack(fill=X, padx=10, pady=2)

        cursor.close()
        conexao.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar celulares: {e}")

# Configurar a janela principal
root = ttk.Window(themename="cosmo")
root.title("Smart Seller")
root.geometry("420x450")
root.configure(bg="#E0FFFF")

main_frame = ttk.Frame(root)
main_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

imagem = Image.open("banner.png")
imagem = imagem.resize((250, 100), Image.Resampling.LANCZOS)
banner = ImageTk.PhotoImage(imagem)

label_banner = ttk.Label(main_frame, image=banner)
label_banner.pack(pady=20)

label_usuario = ttk.Label(main_frame, text="Usuário")
label_usuario.pack(fill=X, padx=10, pady=(0, 5))
entry_usuario = ttk.Entry(main_frame)
entry_usuario.pack(fill=X, padx=10, pady=5)

label_senha = ttk.Label(main_frame, text="Senha")
label_senha.pack(fill=X, padx=10, pady=(5, 0))
entry_senha = ttk.Entry(main_frame, show="*")
entry_senha.pack(fill=X, padx=10, pady=5)

botao_login = ttk.Button(main_frame, text="Entrar", command=verificar_login, bootstyle=(SUCCESS, OUTLINE))
botao_login.pack(pady=(20, 10), padx=10)

botao_criar_usuario = ttk.Button(main_frame, text="Criar Novo Usuário", command=mostrar_janela_criar_usuario, bootstyle=(SECONDARY, OUTLINE))

botao_sair = ttk.Button(main_frame, text="Sair", command=retornar_para_login, bootstyle=(DANGER, OUTLINE))

botao_estoque = ttk.Button(main_frame, text="Mostrar Estoque", command=mostrar_estoque, bootstyle=(INFO, OUTLINE))

root.mainloop()
