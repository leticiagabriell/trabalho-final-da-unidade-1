salario_minimo = 1412 
lista_cadastrados = [] 

def menu():
    print("\n--- SISTEMA DE CESTA BÁSICA ---")
    print("1 - Cadastro de benefício")
    print("2 - Listar pessoas")
    print("3 - Sair")

def definir_cesta(renda, num_pessoas):
    renda_per_capita = renda / num_pessoas
    LIMITE_POBREZA = 300.00

    produtos_basicos = ["Arroz", "Feijão", "Óleo", "Açúcar", "Macarrão"]
    produtos_higiene = ["Sabonete", "Creme Dental", "Papel Higiênico", "Shampoo"]

    print(f"\n--- ITENS DA CESTA ---")
    print(f"Renda per capita: R$ {renda_per_capita:.2f}")

    if renda_per_capita <= LIMITE_POBREZA:
        cesta_final = produtos_basicos + produtos_higiene
        tipo = "Cesta Completa (Alimentação + Higiene)"
    else:
        cesta_final = produtos_basicos
        tipo = "Cesta Básica Padrão"

    print(f"Tipo de benefício: {tipo}")
    print("Produtos liberados:")
    for item in cesta_final:
        print(f"  [ ] {item}")
    return tipo

def cadastrar():
    print("\n--- CADASTRO ---")
    nome = input("Nome: ").strip()
    
    while True:
        cpf = input("Digite seu CPF (apenas números): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            break
        print("CPF inválido! Digite exatamente 11 números.")

    numero = input("Digite seu número de telefone: ")
    
    try:
        qtd_pessoas = int(input("Quantas pessoas tem na sua casa: "))
        renda_total = float(input("Renda mensal total da casa (R$): "))
    except ValueError:
        print("Erro: Digite apenas números para quantidade e renda.")
        return

   
    if renda_total <= salario_minimo:
        status = "Aprovado"
        print(f"\n✅ {nome}, seu benefício foi APROVADO!")
        
        tipo_cesta = definir_cesta(renda_total, qtd_pessoas)
    else:
        status = "Pode doar"
        tipo_cesta = "Nenhum (Doador)"
        print(f"\nℹ️ {nome}, sua renda está acima do limite para receber. Obrigado por se voluntariar!")

    novo_cadastro = {
        "nome": nome,
        "cpf": cpf,
        "renda": renda_total,
        "status": status,
        "tipo_cesta": tipo_cesta,
        "moradores": qtd_pessoas,
        "telefone": numero
    }

    lista_cadastrados.append(novo_cadastro)

def listar():
    print("\n--- LISTA DE PESSOAS ---")
    if not lista_cadastrados:
        print("Nenhuma pessoa cadastrada.")
        return

    for i, p in enumerate(lista_cadastrados, start=1):
        print(f"{i}. Nome: {p['nome']} | Status: {p['status']}")
        print(f"   Cesta: {p['tipo_cesta']} | Renda: R$ {p['renda']:.2f}")
        print("-" * 40)


while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar()
    elif opcao == "2":
        listar()
    elif opcao == "3":
        print("Encerrando sistema...")
        break
    else:
        print("Opção inválida.")
