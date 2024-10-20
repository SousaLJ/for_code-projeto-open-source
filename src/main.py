import os
import re
import json

CONTRIBUTORS_DIR = "./contributors"
README_PATH = "./README.md"
ALL_CONTRIBUTORS_PATH = "./.all-contributorsrc"

def is_contributor_in_readme(username):
    with open(README_PATH, 'r', encoding='utf-8') as file:
        return username in file.read()

def is_contributor_in_all_contributors(username):
    with open(ALL_CONTRIBUTORS_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for contributor in data["contributors"]:
            if contributor["login"] == username:
                return True
    return False

def add_contributor_to_readme(username, avatar_url, contribution_type="📖"):
    with open(README_PATH, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # Encontrar a tabela de contribuidores
    table_match = re.search(r"<tbody>(.*?)</tbody>", readme_content, re.DOTALL)

    if not table_match:
        print("Erro: Seção de contribuidores não encontrada no README.md")
        return

    table_content = table_match.group(1)
    
    # Buscar o último <tr> para verificar a quantidade de <td>
    last_tr_match = re.search(r"(<tr>.*?</tr>)\s*$", table_content, re.DOTALL)

    new_entry = f"""
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/{username}"><img src="{avatar_url}" width="100px;" alt="{username}"/><br /><sub><b>{username}</b></sub></a><br /><a href="https://github.com/SousaLJ/meu-projeto-open-source/commits?author={username}" title="Contribution">{contribution_type}</a></td>"""

    if last_tr_match:
        last_tr = last_tr_match.group(1)
        current_tds = last_tr.count("<td>")

        # Se houver menos de 7 <td>, adicionar na mesma linha
        if current_tds < 7:
            updated_tr = last_tr.replace("</tr>", f"{new_entry}\n</tr>")
            updated_table_content = table_content.replace(last_tr, updated_tr)
        else:
            # Caso contrário, criar uma nova linha <tr> com o novo <td>
            updated_table_content = table_content + f"<tr>\n{new_entry}\n</tr>"
    else:
        # Se não houver nenhum <tr>, adicionar a primeira linha
        updated_table_content = f"<tr>\n{new_entry}\n</tr>"

    # Substituir o conteúdo da tabela
    updated_readme = readme_content.replace(table_content, updated_table_content)

    with open(README_PATH, 'w', encoding='utf-8') as file:
        file.write(updated_readme)

    print(f"Contribuidor {username} adicionado ao README.md.")


def update_all_contributors(username, avatar_url):
    with open(ALL_CONTRIBUTORS_PATH, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        new_contributor = {
            "login": username,
            "avatar_url": avatar_url,
            "contributions": ["doc"]
        }
        data["contributors"].append(new_contributor)
        
        # Regravar o arquivo com a nova entrada
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    print(f"Contribuidor {username} adicionado ao .all-contributorsrc.")

def process_contributors():
    for file_name in os.listdir(CONTRIBUTORS_DIR):
        if file_name.endswith(".md"):
            username = file_name.replace(".md", "")
            avatar_url = f"https://github.com/{username}.png?size=100"
            
            # Verificar se já está no README.md ou .all-contributorsrc
            if not is_contributor_in_readme(username):
                add_contributor_to_readme(username, avatar_url)
            if not is_contributor_in_all_contributors(username):
                update_all_contributors(username, avatar_url)

if __name__ == "__main__":
    process_contributors()
