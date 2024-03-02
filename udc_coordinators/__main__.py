from . import PARAMS_GEI
from .utils import get_coordinator
from .subject import Subject
from .subjects import SUBJECTS_GEI


def main():
    HEADER: str = 'SUBJECT_CODE,SUBJECT_NAME,COORDINATOR_NAME,COORDINATOR_EMAIL'
    print(HEADER)
    subjects: list[Subject] = []
    for subject_code, subject_name in SUBJECTS_GEI.items():
        url: str = Subject.get_subject_url(subject_code=subject_code,
                                           **PARAMS_GEI)
        subject: Subject = Subject(subject_code, subject_name, url)

        coordinator: str = get_coordinator(url)
        if coordinator is None:
            print(f'Coordinator for {subject_code}: {subject_name} not found!')
        else:
            subject.coordinator_name = ' '.join(
                coordinator['name'].split(', ')[::-1]
            )
            subject.coordinator_email = coordinator['email']
            print(subject.to_csv())
            subjects.append(subject)
            
    print('Dumping data to .csv...')
    with open('coordinators.csv', 'w') as f:
        f.write(HEADER + '\n')
        for s in subjects:
            f.write(s.to_csv() + '\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
