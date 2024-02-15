import requests
from requests import Response
from bs4 import BeautifulSoup as BS
from bs4 import Tag, Comment


SUBJECTS: dict[str, str] = {
    '614G01009': 'Administración e Xestión de Organizacións'
}

URL: str = 'https://guiadocente.udc.es/guia_docent/index.php'
FACULTY_CODE_FIC: str = 614  # 614: Facultade de Informática
DEGREE_CODE_GEI: str = '614G01'
DEGREE_CODE_GCED: str = '614G02'
DEGREE_CODE_GIA: str = '614G03'

COURSE_CODE: str = '2023_24'

PARAMS_GEI: dict = {
    'faculty_code': FACULTY_CODE_FIC,
    'degree_code': DEGREE_CODE_GEI,
    'course_code': COURSE_CODE
}

PARAMS_GCED: dict = {
    'faculty_code': FACULTY_CODE_FIC,
    'degree_code': DEGREE_CODE_GCED,
    'course_code': COURSE_CODE
}

PARAMS_GCED: dict = {
    'faculty_code': FACULTY_CODE_FIC,
    'degree_code': DEGREE_CODE_GIA,
    'course_code': COURSE_CODE
}


def get_subject_url(faculty_code: str, degree_code: str, subject_code: str,
                    course_code: str) -> str:
    return URL\
        + '?' + f'centre={faculty_code}'\
        + '&' + f'ensenyament={degree_code}'\
        + '&' + f'assignatura={subject_code}'\
        + '&' + f'any_academic={course_code}'


def get_coordinator(subject_url: str) -> dict | None:

    # Request guide
    response: Response = requests.get(url)

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

        return {
            'name': next_element.find_all('td')[1].text.strip(),
            'email': next_element.find_all('td')[4].text.strip(),
        }


if __name__ == '__main__':
    url: str = get_subject_url(subject_code='614G01009', **PARAMS_GEI)
    print(get_coordinator(url))
