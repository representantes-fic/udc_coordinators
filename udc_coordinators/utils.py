def get_subjects_from_txt(input_file: str) -> None:
    import json

    with open(input_file, 'r') as f:
        d = dict([l.split('\t')[0:2]
                 for l in [l for l in f.readlines() if l.startswith('614')]])
        d = {k: d[k] for k in sorted(d)}

    with open('./subjects.json', 'w') as j:
        json.dump(d, j, indent=4, ensure_ascii=False)


def get_coordinator(subject_url: str) -> dict | None:
    import requests
    from requests import Response
    from bs4 import BeautifulSoup as BS
    from bs4 import Tag, Comment

    # Request guide
    response: Response = requests.get(subject_url)

    # Parse html
    soup = BS(response.content, 'html.parser')

    # Search for coordinator info

    def text_filter(string):
        COMMENT_TEXT = 'Coordinador '
        return isinstance(string, Comment) and COMMENT_TEXT in string

    comment: Comment | None = soup.find(string=text_filter)

    if comment:

        # <!-- Coordinador -->
        # <tr>
        #     <td ...>Coordinación</td>
        #     <td ...>
        #       <table ...>
        #           <tr>
        #               <td>Apellido1 Apellido2, Nombre</td>
        #           </tr>
        #       </table>
        #     </td>
        #     <td ...>Correo electrónico</td>
        #     <td ...>
        #       <table ...>
        #           <tr>
        #               <td>emails@email.com</td>
        #           </tr>
        #       </table>
        #   </td>
        # </tr>

        next_element: Tag = comment.find_next_sibling()

        try:
            return {
                'name': next_element.find_all('td')[1].text.strip(),
                'email': next_element.find_all('td')[4].text.strip(),
            }
        except:
            return None
