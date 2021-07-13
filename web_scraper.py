import requests
import re

# url = "https://pt.wikipedia.org/wiki/Divina_Com%C3%A9dia"
url = input("Type a URL:")

# Verifications
if not re.search('https://pt.wikipedia.org/.+', url):  # Verifica se é um link da wikipedia. REGEX#1
    print("Invalid URL")
    quit()
r = requests.get(url)
with open('file.txt', 'w', encoding="utf-8") as file:
    file.write(r.text)
file = open('file.txt', 'r', encoding="utf-8")
if re.search('<p><b>A Wikipédia não possui um artigo com este nome exato.</b>',
             file.read()):  # Verifica se o artigo existe REGEX#2
    print("This article does not exist.")
    quit()

# Menu
while True:
    while True:
        option = input(
            "\nChoose an option:\n1. Article topics\n2. Images list\n3. Bibliography\n4. Links of the cited "
            "articles\n5. Quit\n\n")
        if option in ('1', '2', '3', '4', '5'):
            break
        else:
            print("Invalid option!")

    if option == '1':
        list1 = []
        list2 = []
        file = open('file.txt', 'r', encoding="utf-8")
        while True:
            line = file.readline()
            regex1 = re.compile('"toctext">.+</span>')  # REGEX#3
            regex2 = re.compile('toclevel-\d')  # REGEX#4
            list1.append(regex1.findall(line))
            list2.append(regex2.findall(line))
            if "" == line:
                break

        list1 = [ele for ele in list1 if ele != []]  # limpa a lista 1 Remove os conjuntos vazios que findall() gera.
        list2 = [ele for ele in list2 if ele != []]  # limpa a lista 2

        for i in range(len(list1)):  # limpa a lista 1. Retira as sujeiras que vem nas laterais do dado.
            str = ''.join(list1[i])
            end = str.find("/")
            str = str[:(end - 1)][::-1]
            end = str.find(">")
            str = str[:(end)][::-1]
            list1[i] = str

        for i in range(len(list2)):  # limpa a lista 2
            str = ''.join(list2[i])
            end = str.find("-")
            str = str[(end + 1):]
            list2[i] = str

        index1 = index2 = index3 = index4 = index5 = 0
        print("\nArticle topics:")
        for i in range(len(list1)):  # Printa a table of contens
            if list2[i] == '1':
                index1 = index1 + 1
                print("%d %s" % (index1, list1[i]))
                index2 = 0
            elif list2[i] == '2':
                index2 = index2 + 1
                print("  %d.%d %s" % (index1, index2, list1[i]))
                index3 = 0
            elif list2[i] == '3':
                index3 = index3 + 1
                print("    %d.%d.%d %s" % (index1, index2, index3, list1[i]))
                index4 = 0
            elif list2[i] == '4':
                index4 = index4 + 1
                print("      %d.%d.%d.%d %s" % (index1, index2, index3, index4, list1[i]))
                index5 = 0
            elif list2[i] == '5':
                index5 = index5 + 1
                print("        %d.%d.%d.%d.%d %s" % (index1, index2, index3, index4, index5, list1[i]))
    elif option == '2':
        list1 = []
        file = open('file.txt', 'r', encoding="utf-8")
        while True:
            line = file.readline()
            regex1 = re.compile(
                'class="floatnone"><a href="/wiki/Ficheiro:\S+"|class="magnify"><a href="/wiki/Ficheiro:\S+')  # REGEX#5
            list1.append(regex1.findall(line))
            if "" == line:
                break
        list1 = [ele for ele in list1 if ele != []]
        for i in range(len(list1)):  # limpa a lista 1. Retira as sujeiras que vem nas laterais do dado.
            str = ''.join(list1[i])
            end = str.find(":")
            str = str[(end + 1):]
            str = str[:(len(str) - 1)]
            list1[i] = str
        print("\nImages list:")
        for i in range(len(list1)):
            print(list1[i])
        # Listar todos os nomes de arquivos de imagens presentes no artigo
    elif option == '3':
        list1 = []
        file = open('file.txt', 'r', encoding="utf-8")
        while True:
            line = file.readline()
            regex1 = re.compile('"reference-text">.+<|"citation book">.+<i>.+</i>.+</cite>')  # REGEX#6
            list1.append(regex1.findall(line))
            if "" == line:
                break
        list1 = [ele for ele in list1 if ele != []]
        for i in range(len(list1)):  # Remove as tags html e limpa a list1
            cleanr = re.compile('<.*?>')  # REGEX#7
            str = re.sub(cleanr, '', ''.join(list1[i]))
            str = str.replace("\"reference-text\">", "")
            str = str.replace("\"citation book\">", "")
            str = str[:(len(str) - 1)]
            list1[i] = str
        print("\nBibliography:")
        for i in range(len(list1)):
            print(list1[i])
    elif option == '4':
        list1 = []
        file = open('file.txt', 'r', encoding="utf-8")
        while True:
            line = file.readline()
            if re.search('Esta seção foi configurada para não ser editável diretamente.', line):  # REGEX#8
                break
            regex1 = re.compile('href="/wiki/(?!Wikipedia|Portal|Especial|Ajuda|Wikip%C3%A9dia)\S+\stitle=')  # REGEX#9
            list1.append(regex1.findall(line))

        list1 = [ele for ele in list1 if ele != []]
        list1 = [item for sublist in list1 for item in sublist]
        print("\nLinks to cited articles:")
        for i in range(len(list1)):  # limpa a lista 1
            str = ''.join(list1[i])
            str = str[::-1]
            end = str.find("\"")
            str = str[(end + 1):][::-1]
            str = str.replace("href=\"", "https://pt.wikipedia.org")
            list1[i] = str

        for i in range(len(list1)):
            print(list1[i])
    elif option == '5':
        print("Obrigado por utilizar nosso software.\n\t\tVolte Sempre!!!!")
        quit()
