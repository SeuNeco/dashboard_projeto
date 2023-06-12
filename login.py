import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='projeto',
)
cursor = conexao.cursor()

print("Bem Vindo ao Código de criação de contas!")
print("Suas opções são: ")
print("1- Criar sua conta")
print("2- Ver sua conta")
print("3- Atualizar sua Conta")
print("4- Deletar sua Conta")
print("5- Encerrar o programa")
opcao = int(input("\nSelecione o que deseja fazer: "))


if opcao == 1:
    # criar
    email = "admin"
    senha = "admin"
    comando = f'INSERT INTO contas (email, senha) VALUES ("{email}", "{senha}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

elif opcao == 2:
    # ler
    comando = f'SELECT * FROM contas'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    print(resultado)
    cursor.close()
    conexao.close()

elif opcao == 3:
    # atualizar
    email = "admin"
    senha = "adm"
    comando = f'UPDATE contas SET senha = "{senha}" WHERE email = "{email}"'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

elif opcao == 4:
    # deletar
    email = "admin"
    comando = f'DELETE FROM contas WHERE email = "{email}"'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

elif opcao == 5:
    exit()

