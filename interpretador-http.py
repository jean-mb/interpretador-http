import sys
import re

if __name__ == "__main__":
    info = {} # Informações sobre a mensagem
    cabecalho = {} # Cabeçalho da mensagem
    quebra = False # Var de controle
    tipo_msg = None # Var de controle
    body = [] # Conteudo da Mensagem
    nome_do_arquivo = sys.argv[1]

    with open(nome_do_arquivo, 'r') as arquivo_original:
        string = arquivo_original.read()
        mensagem = string.split('\n')

    # Primeira linha = Tipo da mensagem
    protocolo = mensagem[0]

    if "GET" in protocolo or "POST" in protocolo: #
        info['Tipo'] = "PEDIDO"
        tipo_msg = 'p' #pedido

        protocolo = protocolo.split(" ")
        if "GET" in protocolo:
            info['Metodo||Status'] = "GET"
        elif "POST" in protocolo:
            info['Metodo||Status'] = "POST"
            info['Recurso'] = protocolo[1]
    else:
        info['Tipo'] = "RESPOSTA"
        tipo_msg = 'r' #resposta
        protocolo = protocolo.split(" ")

        for x in protocolo:
            s = re.match(r'[0-5][0-9][0-9]', x) # Procura pelo codigo de status
            if s:
                descricao = [] # lista auxiliar
                for x in range(2, len(protocolo)): # Repeticao em um intervalo de 2 até a qtd total de palavras da primeira linha
                    descricao.append(protocolo[x])
                info['Metodo||Status'] = f"{s.string} - {' '.join(str(e) for e in descricao)}"
    for x in protocolo:
        if "HTTP" in x:
            info['Versao'] = x

    for x in mensagem: # Percorre o conteudo inteiro
        if x == "": # Se encontrar a quebra de linha que separa o cabeçalho do body
            quebra = True
        elif ":" in x and quebra == False: # Se encontrar um ':' e o laço AINDA não encontrou a quebra de linha
            chave, conteudo = x.split(":", 1)
            cabecalho[chave] = conteudo
        elif quebra: # Se o laço JÁ encontrou a quebra de linha
            body.append(x)

    # --------------------------------------------------
    print('\n================== LEITURA DE PROTOCOLO ==================\n')
    print(f"Tipo de mensagem >>> {info['Tipo']}")
    print(f"Versão do Protocolo >>> {info['Versao']}")
    if tipo_msg == 'p': print(f"Método >>> {info['Metodo||Status']}")
    elif tipo_msg == 'r': print(f"Status >>> {info['Metodo||Status']}")

    print('\n================== CABEÇALHO  ==================\n')
    for chave in cabecalho:
        print(f"{chave} >>> {cabecalho[chave]}")

    print('\n================== CORPO DA MENSAGEM  ==================\n')
    body = ' '.join(body)
    print(body)