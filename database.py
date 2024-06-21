import psycopg2
from tkinter import messagebox

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

def cadastrar_fornecedor(conexao, nome_fornecedor):
    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO tb_fornecedores (for_nome) VALUES (%s) RETURNING for_codigo", (nome_fornecedor,))
        for_codigo = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        return for_codigo
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar fornecedor: {e}")
        return None

def salvar_grupo(nome_grupo, privilegios):
    try:
        conexao = conectar_banco("postgres", "123")  # Substitua com suas credenciais
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO tb_grupos (nome_grupo, ver_estoque, cadastrar_celular, criar_usuario, sair) VALUES (%s, %s, %s, %s, %s)",
                           (nome_grupo, privilegios['ver_estoque'], privilegios['cadastrar_celular'], privilegios['criar_usuario'], privilegios['sair']))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
    except Exception as e:
        print(f"Erro ao salvar grupo: {e}")
        return False

def cadastrar_usuario(nome_usuario, senha):
    try:
        conexao = conectar_banco("postgres", "123")  # Substitua com suas credenciais
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO tb_usuarios (nome_usuario, senha) VALUES (%s, %s)", (nome_usuario, senha))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False

def atribuir_grupo(usuario, grupo):
    try:
        conexao = conectar_banco("postgres", "123")  # Substitua com suas credenciais
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM tb_grupos WHERE nome_grupo = %s", (grupo,))
            grupo_id = cursor.fetchone()
            if grupo_id:
                grupo_id = grupo_id[0]
            else:
                cursor.execute("INSERT INTO tb_grupos (nome_grupo) VALUES (%s) RETURNING id", (grupo,))
                grupo_id = cursor.fetchone()[0]

            cursor.execute("UPDATE tb_usuarios SET grupo_id = %s WHERE nome_usuario = %s",
                           (grupo_id, usuario))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
    except Exception as e:
        print(f"Erro ao atribuir grupo: {e}")
        return False
