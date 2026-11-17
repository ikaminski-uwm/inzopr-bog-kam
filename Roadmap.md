# Roadmap V1

| Widok | Dane | Funkcjonalność |
| :---- | :---- | :---- |
| W01 Interfejs magazynu | Magazyn | F01 Użytkownik ma wgląd do ilości żetonów w magazynieF02 Użytkownik może wprowadzać zmiany ilości żetonów w magazynie po fizycznym ich wyjęciu. F04 System informuje użytkownika o małej oraz krytycznej ilości żetonów w magazynie.F05 Walidacja nie pozwala wprowadzenie niepoprawnych danych. |
| W02 Historia transakcji | Historia | F03 Użytkownik ma wgląd do chronologicznej historii transakcji. F06 System automatycznie aktualizuje historię transakcji po dokonanych zmianach. |

| Struktura Danych |  |
| ----- | ----- |
| Baza SQLite |  |
| Tabela | Pola |
| Historia | id\_transakcji, id maszyny, is\_wplata, data\_czas, 10, 20, 50, 100, 200 |
| Maszyny\* | Id\_maszyny, nazwa, 10, 20, 50, 100, 200 |

\*pomimo iż v1 nie zawiera wsparcia wielu maszyny, jest to następny logiczny krok w rozwoju, więc warto o nim myśleć

| Etap v1  | Od czego zależy?  | Oczekiwany rezultat |
| :---- | :---- | :---- |
| Cel i zakres | Pomysł z laboratorium 01 | Jasny cel v1 i wybrane funkcje MVP. |
| 1\. Interfejs użytkownika | Cel i zakres v1 | Działający program graficzny z zakładkami maszyny i historia |
| 2\. Logika backendowa | Kod interfejsu użytkownika | Logika backendowa, która zwraca dane, którymi łatwo manipulować kontekście codebaseu frontendu. |
| 3\. Baza Danych | Logika backendowa | Program czyta dane z lokalnej bazy, lub tworzy nową według schematu, jeżeli jej nie znajdzie |
| 4\. Integracja frontendu z publicznymi funkcjami backendu | Baza Danych | Program populowany danymi z bazy danych |
| Sprawdzenie spójności | Zintegrowany frontend i backend | Wszystkie przewidziane funkcje programu działają w przewidywalny i poprawny sposób. |

d3GGXzCD0nJ8dY5xF6QkKCjNAjIiKM7YxH6CUlJQ7bwH8h0AF8mFmgNzc307Bhw2j27Nny2B7PoaenpxvrWVlZNHPmTDp16hQFBwfLGwHj5/GF1YqKCuNY8G8IdAAfZhboGzdupKFDh1JTU5PDwvgul549e1J1dbVcJOVbG4uLi2Ufj+gXL14sj1esWCG3LkLgQKAD+DCzQF+wYIHsc174bhfG96FzkPOFUvv70PkOF55jj4yMxH3oAQiBDuDDzAIdoCUIdAAfhkAHFQh0AB+GQAcVCHQAH4ZABxUIdAAfhkAHFQh0AB+GQAcVCHQAH4ZABxUIdAAfhkAHFQh0AB+GQAcVCHQAH8YnKBYsKov0jVMfAQCAn/o/rN7lNNH8WdkAAAAASUVORK5CYII=>