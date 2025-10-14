# python
"""
Wythoff's Game - implementacja gry dwuosobowej o sumie zerowej z interfejsem Pygame.

Zasady gry: https://en.wikipedia.org/wiki/Wythoff%27s_game

Autorzy: Michał Małolepszy (s29097), Aleksander Bastek (s27454)

Instrukcja:
1. Zainstaluj easyAI: pip install easyAI
2. Zainstaluj Pygame: pip install pygame
3. Uruchom: python wythoff.py
"""

import pygame
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax # algorytm minimax

class WythoffGame(TwoPlayerGame):
    """
    Klasa reprezentująca grę Wythoffa.

    Atrybuty:
        players (list): Lista graczy.
        heaps (list): Liczba obiektów w dwóch stosach.
        current_player (int): Indeks aktualnego gracza.
        selected (list): Lista zaznaczonych zapałek dla każdego stosu.
        last_move (str): Ostatni wykonany ruch (dla wyświetlania).

    Metody:
        possible_moves(): Zwraca listę możliwych ruchów.
        make_move(move): Wykonuje ruch.
        win(): Sprawdza, czy gra została wygrana.
        is_over(): Sprawdza, czy gra się zakończyła.
        scoring(): Zwraca wartość pozycji dla AI.
        show(): Wyświetla aktualny stan gry (w konsoli, dla debugowania).
        draw(screen): Rysuje stan gry na ekranie Pygame.
    """
    def __init__(self, players, heaps=None): # jeśli heaps=None, użyj domyślnych wartości
        self.players = players # lista graczy
        self.heaps = heaps if heaps is not None else [5, 7]  # początkowa liczba obiektów w stosach
        self.current_player = 1  # zgodne z easyAI (gracze indeksowani od 1)
        self.selected = [set(), set()]  # zaznaczone indeksy zapałek dla stosu 1 i 2
        self.last_move = None  # ostatni ruch

    def possible_moves(self):
        """Zwraca listę możliwych ruchów w formacie 'a,b'."""
        moves = [] # lista możliwych ruchów
        for i in range(1, self.heaps[0] + 1): # ruchy zabierające z pierwszego stosu
            moves.append(f"{i},0") # dodaj ruch do listy możliwych ruchów
        for i in range(1, self.heaps[1] + 1): # ruchy zabierające z drugiego stosu
            moves.append(f"0,{i}") # dodaj ruch do listy możliwych ruchów
        for i in range(1, min(self.heaps) + 1): # ruchy zabierające z obu stosów
            moves.append(f"{i},{i}") # dodaj ruch do listy możliwych ruchów
        return moves # zwróć listę możliwych ruchów

    def make_move(self, move):
        """Wykonuje ruch podany jako string 'a,b'."""
        a, b = map(int, move.split(",")) # rozdziel ruch na a i b
        self.heaps[0] -= a # zabierz a z pierwszego stosu
        self.heaps[1] -= b # zabierz b z drugiego stosu
        self.current_player = 3 - self.current_player  # przełączanie graczy (1 lub 2)
        self.selected = [set(), set()]  # reset zaznaczeń po ruchu
        self.last_move = move  # zapisz ostatni ruch

    def win(self):
        """Sprawdza, czy gra została wygrana (aktualny gracz wygrał)."""
        return self.heaps == [0, 0] # gra wygrana, jeśli oba stosy są puste

    def is_over(self):
        """Sprawdza, czy gra się zakończyła."""
        return self.win() # gra zakończona, jeśli ktoś wygrał

    def scoring(self):
        """Zwraca wartość pozycji dla AI (100 jeśli wygrana, 0 w przeciwnym razie)."""
        return 100 if self.win() else 0 # 100 punktów za wygraną, 0 w przeciwnym razie

    def show(self):
        """Wyświetla aktualny stan gry (w konsoli, dla debugowania)."""
        print(f"Stos 1: {self.heaps[0]}, Stos 2: {self.heaps[1]}") # wyświetl liczbę zapałek w stosach
        print(f"Ruch gracza {self.current_player}") # wyświetl aktualnego gracza

    def draw(self, screen):
        """Rysuje stan gry na ekranie Pygame."""
        screen.fill((255, 255, 255))  # białe tło
        font = pygame.font.Font(None, 36) # czcionka do tekstu
        # Wyświetl stosy jako tekst (zachowane dla czytelności)
        text1 = font.render(f"Stos 1: {self.heaps[0]}", True, (0, 0, 0))
        text2 = font.render(f"Stos 2: {self.heaps[1]}", True, (0, 0, 0))
        screen.blit(text1, (50, 50))
        screen.blit(text2, (50, 100))
        # Rysuj zapałki jako prostokąty
        matchstick_width = 20 # szerokość zapałki
        matchstick_height = 60 # wysokość zapałki
        spacing = 5 # odstęp między zapałkami
        x_start = 50 # początkowa pozycja x
        # Stos 1 (czerwony, zielony jeśli zaznaczony)
        y = 200 # pozycja y dla pierwszego stosu
        for i in range(self.heaps[0]): # rysuj zapałki pierwszego stosu
            color = (0, 255, 0) if i in self.selected[0] else (255, 0, 0) # zielony jeśli zaznaczony, czerwony w przeciwnym razie
            pygame.draw.rect(screen, color, (x_start + i * (matchstick_width + spacing), y, matchstick_width, matchstick_height))
        # Stos 2 (niebieski, zielony jeśli zaznaczony)
        y = 280 # pozycja y dla drugiego stosu
        for i in range(self.heaps[1]): # rysuj zapałki drugiego stosu
            color = (0, 255, 0) if i in self.selected[1] else (0, 0, 255) # zielony jeśli zaznaczony, niebieski w przeciwnym razie
            pygame.draw.rect(screen, color, (x_start + i * (matchstick_width + spacing), y, matchstick_width, matchstick_height)) # rysuj zapałkę
        # Wyświetl aktualnego gracza
        player_text = font.render("Twój ruch" if self.current_player == 1 else f"Ruch gracza {self.current_player}", True, (0, 0, 0))
        screen.blit(player_text, (50, 350)) # pozycja tekstu
        # Wyświetl ostatni ruch AI jeśli istnieje
        if self.last_move and self.current_player == 1:  # po ruchu AI
            ai_move_text = font.render(f"AI wykonał ruch: {self.last_move}", True, (0, 0, 0)) # tekst ostatniego ruchu AI
            screen.blit(ai_move_text, (50, 380)) # pozycja tekstu
        # Jeśli gra zakończona, wyświetl komunikat o zwycięzcy i przyciski
        if self.is_over():
            winner = 3 - self.current_player  # zwycięzca to poprzedni gracz
            if winner == 1: # jeśli wygrał gracz 1 (człowiek)
                end_text = font.render("Wygrałeś!", True, (255, 0, 0))
            else:
                end_text = font.render("Wygrał AI!", True, (255, 0, 0))
            screen.blit(end_text, (50, 400))
            # Przyciski
            restart_text = font.render("Zagraj ponownie", True, (0, 0, 255))
            screen.blit(restart_text, (50, 450))
            quit_text = font.render("Wyjdź z gry", True, (255, 0, 0))
            screen.blit(quit_text, (50, 490))
        else:
            # Przycisk "Zabierz"
            zabierz_text = font.render("Zabierz", True, (0, 0, 255))
            screen.blit(zabierz_text, (50, 450))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # większy ekran dla wizualizacji
    pygame.display.set_caption("Wythoff's Game") # tytuł okna
    clock = pygame.time.Clock() # zegar do kontroli klatek na sekundę

    ai = Negamax(6) # głębokość 6 dla AI
    game = WythoffGame([Human_Player(), AI_Player(ai)]) # człowiek vs AI
    running = True # zmienna kontrolująca pętlę gry

    while running:
        for event in pygame.event.get(): # obsługa zdarzeń
            if event.type == pygame.QUIT: # zamknięcie okna
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # obsługa kliknięć myszą
                mouse_x, mouse_y = event.pos # pozycja kliknięcia
                if game.is_over():
                    # Sprawdź przyciski na końcu gry
                    restart_rect = pygame.Rect(50, 450, 150, 30) # prostokąt przycisku "Zagraj ponownie"
                    quit_rect = pygame.Rect(50, 490, 120, 30) # prostokąt przycisku "Wyjdź z gry"
                    if restart_rect.collidepoint(mouse_x, mouse_y): # kliknięcie w "Zagraj ponownie"
                        game = WythoffGame([Human_Player(), AI_Player(ai)])  # nowa gra
                    elif quit_rect.collidepoint(mouse_x, mouse_y): # kliknięcie w "Wyjdź z gry"
                        running = False
                elif game.current_player == 1:  # ruch człowieka (gracz 1)
                    # Sprawdź kliknięcie na zapałkach
                    matchstick_width = 20
                    matchstick_height = 60
                    spacing = 5 # odstęp między zapałkami
                    x_start = 50 # początkowa pozycja x
                    # Stos 1
                    y = 200 # pozycja y dla pierwszego stosu
                    for i in range(game.heaps[0]): # sprawdź każdą zapałkę w pierwszym stosie
                        rect = pygame.Rect(x_start + i * (matchstick_width + spacing), y, matchstick_width, matchstick_height)
                        if rect.collidepoint(mouse_x, mouse_y): # jeśli kliknięto na zapałkę
                            if i in game.selected[0]: # jeśli zapałka już zaznaczona
                                game.selected[0].remove(i)
                            else:
                                game.selected[0].add(i)
                            break
                    # Stos 2
                    y = 280
                    for i in range(game.heaps[1]): # sprawdź każdą zapałkę w drugim stosie
                        rect = pygame.Rect(x_start + i * (matchstick_width + spacing), y, matchstick_width, matchstick_height)
                        if rect.collidepoint(mouse_x, mouse_y):
                            if i in game.selected[1]: # jeśli zapałka już zaznaczona
                                game.selected[1].remove(i)
                            else:
                                game.selected[1].add(i)
                            break
                    # Sprawdź kliknięcie na przycisku "Zabierz"
                    zabierz_rect = pygame.Rect(50, 450, 100, 30) # prostokąt przycisku "Zabierz"
                    if zabierz_rect.collidepoint(mouse_x, mouse_y): # jeśli kliknięto "Zabierz"
                        sel1 = len(game.selected[0]) # liczba zaznaczonych zapałek w pierwszym stosie
                        sel2 = len(game.selected[1]) # liczba zaznaczonych zapałek w drugim stosie
                        if sel1 > 0 and sel2 == 0 and sel1 <= game.heaps[0]: # valid move
                            move = f"{sel1},0" # ruch zabierający z pierwszego stosu
                        elif sel2 > 0 and sel1 == 0 and sel2 <= game.heaps[1]: # valid move
                            move = f"0,{sel2}" # ruch zabierający z drugiego stosu
                        elif sel1 == sel2 > 0 and sel1 <= min(game.heaps): # valid move
                            move = f"{sel1},{sel1}" # ruch zabierający z obu stosów
                        else:
                            move = None # nieprawidłowy ruch
                        if move and move in game.possible_moves(): # jeśli ruch jest prawidłowy
                            game.make_move(move) # wykonaj ruch
                            game.show()  # debug w konsoli

        if game.current_player == 2 and not game.is_over():  # ruch AI (gracz 2)
            move = ai(game)  # AI wybiera ruch
            game.make_move(move) # wykonaj ruch AI
            if not game.is_over():  # dodaj sprawdzenie
                game.show()  # debug w konsoli

        game.draw(screen) # rysuj stan gry
        pygame.display.flip() # aktualizacja ekranu
        clock.tick(60) # 60 FPS

    pygame.quit()