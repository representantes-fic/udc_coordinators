class Subject():

    GUIDES_URL: str = 'https://guiadocente.udc.es/guia_docent/index.php'

    def __init__(self, code: str, name: str, url: str) -> None:
        self.code: str = code
        self.name: str = name
        self.url: str = url
        self.coordinator_name: str | None = None
        self.coordinator_email: str | None = None

    @classmethod
    def get_subject_url(cls, faculty_code: str, degree_code: str,
                        subject_code: str, course_code: str) -> str:
        return cls.GUIDES_URL\
            + '?' + f'centre={faculty_code}'\
            + '&' + f'ensenyament={degree_code}'\
            + '&' + f'assignatura={subject_code}'\
            + '&' + f'any_academic={course_code}'

    def to_csv(self) -> str:
        return ','.join((
            self.code,
            self.name,
            self.coordinator_name,
            self.coordinator_email
        ))
