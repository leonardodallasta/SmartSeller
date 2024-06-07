import psycopg2
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import messagebox

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Verificar se os valores estão corretos
    print("Usuário:", usuario)
    print("Senha:", senha)

    # Validar se os campos estão preenchidos
    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        # Conectar ao banco de dados
        conexao = psycopg2.connect(
            database="pedido",
            host="localhost",
            user=usuario,
            password=senha,
            port="5432",
            client_encoding='UTF8'
        )

        # Verificar a conexão
        if conexao:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            mostrar_botao_criar_usuario()  # Mostrar o botão para criar um novo usuário
        else:
            messagebox.showerror("Login", "Login falhou!")

    # Lidar com erros específicos
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        else:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:  # Captura outros erros
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

def mostrar_janela_criar_usuario():
    # Função para criar e mostrar a janela para criar um novo usuário
    janela_criar_usuario = ttk.Window(themename="cosmo")
    janela_criar_usuario.title("Criar Novo Usuário")
    janela_criar_usuario.geometry("300x250")

    # Widgets para entrada de dados do novo usuário
    label_nome_usuario = ttk.Label(janela_criar_usuario, text="Nome de Usuário")
    label_nome_usuario.pack(fill=X, padx=10, pady=(10, 5))
    entry_nome_usuario = ttk.Entry(janela_criar_usuario)
    entry_nome_usuario.pack(fill=X, padx=10, pady=5)

    label_senha = ttk.Label(janela_criar_usuario, text="Senha")
    label_senha.pack(fill=X, padx=10, pady=(5, 0))
    entry_senha_criar = ttk.Entry(janela_criar_usuario, show="*")
    entry_senha_criar.pack(fill=X, padx=10, pady=5)

    # Função para registrar o novo usuário
    def registrar_usuario():
        novo_usuario = entry_nome_usuario.get()
        nova_senha = entry_senha_criar.get()

        try:
            # Conectar ao banco de dados
            conexao = psycopg2.connect(
                database="pedido",
                host="localhost",
                user="postgres",
                password="123",
                port="5432"
            )

            # Criar um cursor para executar consultas SQL
            cursor = conexao.cursor()

            # Query para criar o novo usuário no PostgreSQL
            query = f"CREATE USER {novo_usuario} WITH PASSWORD '{nova_senha}'"

            # Executar a query
            cursor.execute(query)

            # Confirmar a transação
            conexao.commit()

            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()

            # Mostrar mensagem de sucesso
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")

            # Limpar campos de entrada
            entry_nome_usuario.delete(0, 'end')
            entry_senha_criar.delete(0, 'end')

            # Fechar a janela de criação de usuário
            janela_criar_usuario.destroy()

        except Exception as e:
            # Mostrar mensagem de erro
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")

    # Botão para registrar o novo usuário
    botao_registrar = ttk.Button(janela_criar_usuario, text="Registrar", command=registrar_usuario, bootstyle=(SUCCESS, OUTLINE))
    botao_registrar.pack(pady=20, padx=10)

def mostrar_botao_criar_usuario():
    # Função para ocultar os widgets de login e mostrar apenas o botão para criar um novo usuário
    label_usuario.pack_forget()
    entry_usuario.pack_forget()
    label_senha.pack_forget()
    entry_senha.pack_forget()
    botao_login.pack_forget()

    # Mostrar o botão para criar um novo usuário
    botao_criar_usuario.pack(pady=20, padx=10)
    botao_sair.pack(pady=20, padx=10)

def mostrar_botao_entrar():
    # Mostrar o botão de entrar
    botao_login.pack(pady=(20, 10), padx=10)
def retornar_para_login():
    # Função para voltar ao formulário de login
    botao_criar_usuario.pack_forget()
    botao_sair.pack_forget()
    entry_usuario.pack()
    label_senha.pack()
    entry_senha.pack()
    mostrar_botao_entrar()


# Configurar a janela principal (ttkbootstrap)
root = ttk.Window(themename="cosmo")
root.title("Smart Seller")
root.geometry("420x450")

# Cor de fundo azul clarinho
root.configure(bg="#E0FFFF")  # Light Cyan

# Frame para o conteúdo principal
main_frame = ttk.Frame(root)
main_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

# Carregar a imagem do banner
imagem = Image.open("banner.png")
imagem = imagem.resize((250, 100), Image.Resampling.LANCZOS)
banner = ImageTk.PhotoImage(imagem)

# Label para exibir a imagem do banner (ttk.Label)
label_banner = ttk.Label(main_frame, image=banner)
label_banner.pack(pady=20)

# Label e Entry para o usuário (ttk.Label e ttk.Entry)
label_usuario = ttk.Label(main_frame, text="Usuário")
label_usuario.pack(fill=X, padx=10, pady=(0, 5))
entry_usuario = ttk.Entry(main_frame)
entry_usuario.pack(fill=X, padx=10, pady=5)

# Label e Entry para a senha (ttk.Label e ttk.Entry)
label_senha = ttk.Label(main_frame, text="Senha")
label_senha.pack(fill=X, padx=10, pady=(5, 0))
entry_senha = ttk.Entry(main_frame, show="*")
entry_senha.pack(fill=X, padx=10, pady=5)

# Botão de login (ttk.Button)
botao_login = ttk.Button(main_frame, text="Entrar", command=verificar_login, bootstyle=(SUCCESS, OUTLINE))
botao_login.pack(pady=(20, 10), padx=10)  # Adiciona espaço acima e abaixo do botão e nenhum à esquerda/direita


# Botão para criar um novo usuário (ttk.Button)
botao_criar_usuario = ttk.Button(main_frame, text="Criar Novo Usuário", command=mostrar_janela_criar_usuario, bootstyle=(SECONDARY, OUTLINE))

# Botão de sair (ttk.Button)
botao_sair = ttk.Button(main_frame, text="Sair", command=retornar_para_login, bootstyle=(DANGER, OUTLINE))

# Executar a aplicação
root.mainloop()
