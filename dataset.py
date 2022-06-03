
""" przykład deklaracji klasy oraz metod (czyli funkcji wewnątrz klasy) i
ich wykorzystania """

class Dataset:

    # klasa może mieć swoje właściwości (nazywane też często polami)
    # jednak w Pythonie definiowanie ich w taki sposób powoduje utworzenie
    # pola klasy a nie instancji - różnica jest dość istotna
    # pole klasy współdzieli wartość między wieloma instancjami klasy
    # a pole instancji tylko w ramach danego obiektu/instancji
    # tutaj raczej nie chcemy tygo współdzielić pomiędzy obiektami typu dataset
    # input = []
    # labels = []

    def __init__(self):
        """ to jest konstruktor, czyli specjalna metoda, która jest automatycznie
            uruchamiana w momencie tworzenia (konstruowania) nowego obiektu
            najczęściej będziemy tutaj inicjalizować (czyli ustawiać po raz
            pierwszy) wartości niezbędnych zmiennych obiektu 
        """
        # słowo kluczowe self (w innych językach występuje często jako this)
        # oznacza odwołanie/referencję do instancji obiektu
        self.data = []
        self.labels = []

    # użyję tutaj dla przykładu type hinting (czyli sugerowanie typu wartości
    # wejściowej atrybutów oraz wartości zwracanej). Nie wymusza to jednak
    # w żaden sposób użycia takich typów - to tylko wskazówka.
    # należy również przemyśleć co zwracać, jeżeli metoda może zostać przerwana
    # za względu na wystąpienie błędu, przyjmijmy jednak, że pustą listę
    def read_file(self, filepath : str) -> list:
        """ metoda, która pobiera jeden atrybut w postaci ścieżki do pliku
            pewne sytuacje związane z obsługą plików da się przewidzieć i
            dlatego powinniśmy je obsłyżyć.
            poniżej przykład z obsługą błędu, który zostanie rzucony (zgłoszony)
            w momencie, kiedy plik z podanej ścieżki nie istnieje.
        """

        file_content = []
        # próbujemy coś wykonać w bloku try, ale to może się zakończyć błędem
        try:
            with open(filepath, encoding='utf-8') as file:
                for line in file:
                    file_content.append(line)
        except FileNotFoundError as ex:
            print('Plik nie został odnaleziony')
            # możemy też wyświetlić w tym przypadku oryginalny komunikat
            print(ex)

        return file_content

    def load_file_content(self, content: list, has_labels :  bool = False, separator: str =';') -> None:
        """ moglibyśmy to zrobić od razu w metodzie read_file, ale dla celów
            dydaktycznych pokazałem ja można podejść do tego inaczej
            tym razem zapiszemy te dane do pola klasy, co pozwoli na dostęp do
            nich z innych metod tej klasy
        """
        data_start_index = 0

        if has_labels:
            data_start_index = 1
            # powinnismy się też pozbyć "białych znaków" (zbędne spacje, znaki
            # nowej linii)
            self.labels = [val.strip() for val in content[0].split(separator)]
            
        # ładujemy dane
        for line_data in content[data_start_index:]:
            self.data.append([val.strip() for val in line_data.split(separator)])


# case 2
    # wydaje mi się lepszym pomysłem uczynienie metody read_file() metodą
    # magiczną (pseudo prywatną) i uruchamianie jej poprzez wywołanie funkcji load_file_content().
    # Tak w Pythonie nazywane są metody, których nazwy zaczynają i
    # kończą się podwójnym podkreśleniem i powinny być traktowane jako prywatne,
    # czyli uruchamiane z wnętrza samej klasy (np. w innych metodach).
    # implementacja tych metod wyglądałaby tak jak poniżej.

class Dataset2:

    def __init__(self):
        """ to jest konstruktor, czyli specjalna metoda, która jest automatycznie
            uruchamiana w momencie tworzenia (konstruowania) nowego obiektu
            najczęściej będziemy tutaj inicjalizować (czyli ustawiać po raz
            pierwszy) wartości niezbędnych zmiennych obiektu 
        """
        self.data = []
        self.labels = []

    def __read_file__(self, filepath : str) -> list:
        """ metoda, która pobiera jeden atrybut w postaci ścieżki do pliku
            pewne sytuacje związane z obsługą plików da się przewidzieć i
            dlatego powinniśmy je obsłyżyć.
            poniżej przykład z obsługą błędu, który zostanie rzucony (zgłoszony)
            w momencie, kiedy plik z podanej ścieżki nie istnieje.
        """

        file_content = []
        # próbujemy coś wykonać w bloku try, ale to może się zakończyć błędem
        try:
            with open(filepath, encoding='utf-8') as file:
                for line in file:
                    file_content.append(line)
        except FileNotFoundError as ex:
            print('Plik nie został odnaleziony')
            # możemy też wyświetlić w tym przypadku oryginalny komunikat
            print(ex)

        return file_content

    def load_file_content(self, file: str, has_labels :  bool = False, separator: str =';') -> None:
        
        data_start_index = 0
        content = self.__read_file__(file)

        # poniższy kod nie zadziała, jeżeli zawartość pliku jest pusta
        if len(content) != 0:
            if has_labels:
                data_start_index = 1
                self.labels = [val.strip() for val in content[0].split(separator)]
                
            # ładujemy dane
            for line_data in content[data_start_index:]:
                self.data.append([val.strip() for val in line_data.split(separator)])
        else:
            # możemy wypisać komunikat, ale uzywanie funkcji print nie 
            # zawsze jest dobrym pomysłem (np. jeżeli jest to kod, który
            # będzie uruchamiany jako aplikacja www np. Django)
            print('Brak zawartości')


# _____________________________________________________________________________
# przykładowe wywołanie tych metod może wyglądać tak:
# uruchamiane tylko wtedy gdy jest to skrypt "startowy" (główny - ang. main)

if __name__ == '__main__':
    # case 1
    dataset = Dataset()
    # poniższy plik u mnie istnieje
    file_content = dataset.read_file('dane.csv')
    # obsługujemy przypadek, gdy plik nie istnieje lub brak zawartości
    if len(file_content) > 0:
        dataset.load_file_content(file_content, has_labels=True)
    
    print(dataset.data)
    print(dataset.labels)

    # case 2
    dataset = Dataset2()
    # poniższy plik u mnie istnieje
    dataset.load_file_content('dane.csv', has_labels=True)
    
    print(dataset.data)
    print(dataset.labels)
    