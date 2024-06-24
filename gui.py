#gui.py
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import Toplevel, BOTH, X, messagebox
from auth import verificar_login, mostrar_janela_criar_usuario
from database import conectar_banco
from celular import cadastrar_celular
from atribuir_grupo import mostrar_janela_atribuir_grupo
from criar_grupo import mostrar_janela_criar_grupo
import psycopg2

usuario_logado = None

def mostrar_botao_criar_usuario(main_frame, botao_criar_usuario, botao_login):
    botao_criar_usuario.grid(row=6, column=1, sticky="ew", pady=10, padx=10)
    botao_login.grid(row=6, column=0, sticky="ew", pady=10, padx=10)

def ocultar_botao_criar_usuario(botao_criar_usuario):
    botao_criar_usuario.grid_forget()

def mostrar_botoes_apos_login(main_frame, botao_sair, botao_estoque, botao_cadastrar_celular, botao_criar_grupo, botao_atribuir_grupo, botao_conceder_privilegio):
    botao_sair.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
    botao_estoque.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
    botao_cadastrar_celular.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

    if usuario_logado == "postgres":
        botao_criar_grupo.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        botao_atribuir_grupo.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=10)
        botao_conceder_privilegio.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

def retornar_para_login(main_frame, botao_criar_usuario, botao_sair, botao_estoque, botao_cadastrar_celular, label_usuario, entry_usuario, label_senha, entry_senha, botao_login, botao_criar_grupo, botao_atribuir_grupo, botao_conceder_privilegio):
    ocultar_botao_criar_usuario(botao_criar_usuario)
    botao_sair.grid_forget()
    botao_estoque.grid_forget()
    botao_cadastrar_celular.grid_forget()
    botao_criar_grupo.grid_forget()
    botao_atribuir_grupo.grid_forget()
    botao_conceder_privilegio.grid_forget()

    label_usuario.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    entry_usuario.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    label_senha.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    entry_senha.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    botao_login.grid(row=6, column=0, sticky="ew", pady=10, padx=10)
    mostrar_botao_criar_usuario(main_frame, botao_criar_usuario, botao_login)

    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

    entry_usuario.configure(style="TEntry")
    entry_senha.configure(style="TEntry")

    global usuario_logado
    usuario_logado = None

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
        cursor.execute("SELECT cel_nome, cel_quantidade FROM tb_celulares")
        celulares = cursor.fetchall()
        for celular in celulares:
            nome, quantidade = celular
            texto_celular = f"Nome: {nome} - Quantidade: {quantidade}"
            label_celular = ttk.Label(frame_estoque, text=texto_celular, justify="left")
            label_celular.pack(fill=X, padx=10, pady=2)

        cursor.close()
        conexao.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar celulares: {e}")

def mostrar_janela_conceder_privilegio(root):
    def salvar_privilegio():
        usuario = combo_usuario.get()
        privilegio = combo_privilegio.get()

        if not usuario or not privilegio:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if conceder_privilegio(conexao, usuario, privilegio):
            messagebox.showinfo("Sucesso", f"Privilégio '{privilegio}' concedido ao usuário '{usuario}' com sucesso!")
            janela_conceder_privilegio.destroy()
            atualizar_privilegios()
        else:
            messagebox.showerror("Erro", f"Erro ao conceder privilégio '{privilegio}' ao usuário '{usuario}'.")

    janela_conceder_privilegio = Toplevel(root)
    janela_conceder_privilegio.title("Conceder Privilégio")
    janela_conceder_privilegio.geometry("300x200")

    # Obter nomes de usuários do banco de dados
    conexao = conectar_banco("postgres", "123")  # Substitua pelas suas credenciais
    if not conexao:
        messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome_usuario FROM tb_usuarios")
        nomes_usuarios = [row[0] for row in cursor.fetchall()]
        cursor.close()
    except psycopg2.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar usuários: {e}")
        return

    # Combobox para selecionar usuário
    label_usuario = ttk.Label(janela_conceder_privilegio, text="Selecione o Usuário:")
    label_usuario.pack(pady=10)
    combo_usuario = ttk.Combobox(janela_conceder_privilegio, values=nomes_usuarios, state="readonly")
    combo_usuario.pack()

    # Função para atualizar o combobox de privilégios
    def atualizar_privilegios(*args):
        usuario_selecionado = combo_usuario.get()
        privilegios_disponiveis = obter_privilegios_disponiveis(conexao, usuario_selecionado)
        combo_privilegio["values"] = privilegios_disponiveis
        combo_privilegio.set('')

    # Combobox para selecionar privilégio (inicialmente vazio)
    label_privilegio = ttk.Label(janela_conceder_privilegio, text="Selecione o Privilégio:")
    label_privilegio.pack(pady=10)
    combo_privilegio = ttk.Combobox(janela_conceder_privilegio, state="readonly")
    combo_privilegio.pack()

    # Vincular a função de atualização ao combobox de usuário
    combo_usuario.bind("<<ComboboxSelected>>", atualizar_privilegios)

    # Chamar a função de atualização manualmente para o primeiro usuário
    atualizar_privilegios()

       # Botão para salvar
    botao_salvar = ttk.Button(janela_conceder_privilegio, text="Salvar", command=salvar_privilegio)
    botao_salvar.pack(pady=10)

def obter_privilegios_disponiveis(conexao, usuario):
    try:
        with conexao.cursor() as cur:
            # Obter o grupo do usuário
            cur.execute("SELECT grupo_id FROM tb_usuarios WHERE nome_usuario = %s", (usuario,))
            grupo_id = cur.fetchone()

            if grupo_id is None:
                return ["ver_estoque", "cadastrar_celular", "criar_usuario", "sair"]

            grupo_id = grupo_id[0]

            # Obter privilégios do grupo (convertendo para booleanos)
            cur.execute(
                "SELECT ver_estoque, cadastrar_celular, criar_usuario, sair FROM tb_grupos WHERE id = %s",
                (grupo_id,),
            )
            privilegios_grupo = cur.fetchone()
            privilegios_grupo = [bool(p) for p in privilegios_grupo]

            print("Privilégios do grupo (booleanos):", privilegios_grupo)

            if privilegios_grupo is None:
                return []

            # Privilégios disponíveis são aqueles que o grupo não possui
            privilegios_disponiveis = [
                privilegio for privilegio, valor in zip(["ver_estoque", "cadastrar_celular", "criar_usuario", "sair"], privilegios_grupo) if not valor
            ]
            return privilegios_disponiveis
    except psycopg2.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar privilégios: {e}")
        return []


def main():
    root = ttk.Window(themename="cosmo")
    root.title("Smart Seller")
    root.geometry("420x450")
    root.configure(bg="#E0FFFF")

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)

    # Configurar o grid para centralizar os elementos
    main_frame.columnconfigure(0, weight=1)  # Expandir a coluna para centralizar
    main_frame.columnconfigure(1, weight=1)  # Cria uma segunda coluna para centralizar o botão "Criar Novo Usuário"

    imagem = Image.open("banner.png")
    imagem = imagem.resize((250, 100), Image.LANCZOS)
    banner = ImageTk.PhotoImage(imagem)

    label_banner = ttk.Label(main_frame, image=banner)
    label_banner.image = banner
    label_banner.grid(row=0, column=0, columnspan=2, pady=20)  # Banner ocupa as duas colunas

    label_usuario = ttk.Label(main_frame, text="Usuário")
    entry_usuario = ttk.Entry(main_frame)
    label_senha = ttk.Label(main_frame, text="Senha")
    entry_senha = ttk.Entry(main_frame, show="*")

    # Posiciona os elementos de login na tela inicial
    label_usuario.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    entry_usuario.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    label_senha.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    entry_senha.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def login_callback():
        global usuario_logado
        usuario_logado = entry_usuario.get()

        usuario = entry_usuario.get()
        senha = entry_senha.get()
        conexao = conectar_banco(usuario, senha)

        if not conexao:
            return

        verificar_login(entry_usuario, entry_senha, lambda: mostrar_botoes_apos_login(main_frame, botao_sair, botao_estoque, botao_cadastrar_celular, botao_criar_grupo, botao_atribuir_grupo, botao_conceder_privilegio))
        ocultar_botao_criar_usuario(botao_criar_usuario)
        botao_login.grid_forget()

    # Cria todos os botões no início da aplicação
    botao_criar_grupo = ttk.Button(main_frame, text="Criar Novo Grupo", command=mostrar_janela_criar_grupo, bootstyle=(ttk.constants.WARNING, ttk.constants.OUTLINE))
    botao_atribuir_grupo = ttk.Button(main_frame, text="Atribuir Grupo", command=mostrar_janela_atribuir_grupo, bootstyle=(ttk.constants.INFO, ttk.constants.OUTLINE))
    botao_criar_usuario = ttk.Button(main_frame, text="Criar Novo Usuário", command=lambda: mostrar_janela_criar_usuario(root), bootstyle=(ttk.constants.SECONDARY, ttk.constants.OUTLINE))
    botao_login = ttk.Button(main_frame, text="Entrar", command=login_callback, bootstyle=(ttk.constants.SUCCESS, ttk.constants.OUTLINE))
    botao_login.grid(row=6, column=0, sticky="ew", pady=10, padx=10)
    mostrar_botao_criar_usuario(main_frame, botao_criar_usuario, botao_login)

    botao_sair = ttk.Button(main_frame, text="Sair", command=lambda: retornar_para_login(
        main_frame, botao_criar_usuario, botao_sair, botao_estoque, botao_cadastrar_celular,
        label_usuario, entry_usuario, label_senha, entry_senha, botao_login, botao_criar_grupo, botao_atribuir_grupo, botao_conceder_privilegio),
        bootstyle=(ttk.constants.DANGER, ttk.constants.OUTLINE))

    botao_estoque = ttk.Button(main_frame, text="Mostrar Estoque", command=lambda: mostrar_estoque(root, entry_usuario, entry_senha), bootstyle=(ttk.constants.INFO, ttk.constants.OUTLINE))
    botao_cadastrar_celular = ttk.Button(main_frame, text="Cadastrar Celular", command=lambda: cadastrar_celular(root, entry_usuario, entry_senha), bootstyle=(ttk.constants.PRIMARY, ttk.constants.OUTLINE))
    botao_conceder_privilegio = ttk.Button(main_frame, text="Conceder Privilégio", command=lambda: mostrar_janela_conceder_privilegio(root), bootstyle=(ttk.constants.PRIMARY, ttk.constants.OUTLINE))

    # Oculta todos os botões, exceto o de login e criar novo usuário
    botao_sair.grid_forget()
    botao_estoque.grid_forget()
    botao_cadastrar_celular.grid_forget()
    botao_criar_grupo.grid_forget()
    botao_atribuir_grupo.grid_forget()
    botao_conceder_privilegio.grid_forget()

    root.mainloop()

if __name__ == "__main__":
    main()

