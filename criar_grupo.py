# criar_grupo.py
from tkinter import messagebox, Toplevel
import ttkbootstrap as ttk
from database import salvar_grupo

def mostrar_janela_criar_grupo():
    def salvar_novo_grupo():
        nome_grupo = entry_nome_grupo.get()
        privilegios = {
            'ver_estoque': var_ver_estoque.get(),
            'cadastrar_celular': var_cadastrar_celular.get(),
            'criar_usuario': var_criar_usuario.get(),
            'sair': var_sair.get()
        }
        if nome_grupo.strip() == "":
            messagebox.showerror("Erro", "O nome do grupo não pode estar vazio.")
            return

        try:
            if salvar_grupo(nome_grupo, privilegios):
                messagebox.showinfo("Sucesso", f"Grupo '{nome_grupo}' cadastrado com sucesso!")
                janela_criar_grupo.destroy()
            else:
                messagebox.showerror("Erro", f"Erro ao salvar o grupo '{nome_grupo}'.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o grupo: {e}")

    janela_criar_grupo = Toplevel()
    janela_criar_grupo.title("Criar Novo Grupo")
    janela_criar_grupo.geometry("300x250")

    label_nome_grupo = ttk.Label(janela_criar_grupo, text="Nome do Grupo")
    label_nome_grupo.pack(fill="x", padx=10, pady=(10, 5))
    entry_nome_grupo = ttk.Entry(janela_criar_grupo)
    entry_nome_grupo.pack(fill="x", padx=10, pady=5)

    var_ver_estoque = ttk.BooleanVar(value=False)
    var_cadastrar_celular = ttk.BooleanVar(value=False)
    var_criar_usuario = ttk.BooleanVar(value=False)
    var_sair = ttk.BooleanVar(value=False)

    check_ver_estoque = ttk.Checkbutton(janela_criar_grupo, text="Ver Estoque", variable=var_ver_estoque)
    check_ver_estoque.pack(fill="x", padx=10, pady=5)
    check_cadastrar_celular = ttk.Checkbutton(janela_criar_grupo, text="Cadastrar Celular", variable=var_cadastrar_celular)
    check_cadastrar_celular.pack(fill="x", padx=10, pady=5)
    check_criar_usuario = ttk.Checkbutton(janela_criar_grupo, text="Criar Usuário", variable=var_criar_usuario)
    check_criar_usuario.pack(fill="x", padx=10, pady=5)
    check_sair = ttk.Checkbutton(janela_criar_grupo, text="Sair", variable=var_sair)
    check_sair.pack(fill="x", padx=10, pady=5)

    botao_salvar = ttk.Button(janela_criar_grupo, text="Salvar", command=salvar_novo_grupo, style="success.TButton")
    botao_salvar.pack(pady=20, padx=10)

    janela_criar_grupo.transient()
    janela_criar_grupo.grab_set()
    janela_criar_grupo.wait_window()

if __name__ == "__main__":
    mostrar_janela_criar_grupo()
