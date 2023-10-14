import pygame
import sys
import random
import os

# Inicializa o Pygame
pygame.init()

# Define o diretório onde estão os arquivos de recursos
resource_dir = "resources"
data_dir = "data"  # Diretório para armazenar dados das pontuações

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Verifica se o diretório de dados existe e, se não, cria-o
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Configurações do jogo
width = 400
height = 600
gravity = 0.25
bird_velocity = 0
jump_strength = -5
game_over = False
pipe_speed_increase = 0.1  # Aumento de velocidade dos canos

# Cores
white = (255, 255, 255)
red = (255, 0, 0)

# Cria a tela
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cacodemon Clusterbird")

# Pássaro
bird = pygame.Rect(100, 250, 40, 40)

# Canos
pipes = []
pipe_gap = 150
pipe_speed = 2

# Relógio
clock = pygame.time.Clock()

# Caminhos para as imagens e música de fundo
background_path = os.path.join(resource_dir, "background.jpg")
bird_image_path = os.path.join(resource_dir, "bird.png")
music_path = os.path.join(resource_dir, "background_music.mp3")

# Carrega e redimensiona as imagens
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (width, height))
bird_image = pygame.image.load(bird_image_path).convert_alpha()
bird_image = pygame.transform.scale(bird_image, (40, 40))

# Carrega a música de fundo
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # -1 indica repetição contínua

# Variáveis para pontuação e tempo
score = 0
start_time = pygame.time.get_ticks()

# Variável para controlar o estado do jogo
game_state = "start"  # Inicia com a tela inicial

# Variável para controlar o tempo decorrido
elapsed_time = 0

# Lista para armazenar as pontuações
high_scores = []

# Função para carregar as pontuações a partir do arquivo
def load_scores():
    scores_file = os.path.join(data_dir, "scores.txt")
    if os.path.exists(scores_file):
        with open(scores_file, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                high_scores.append(int(line))

# Função para salvar as pontuações no arquivo
def save_scores():
    scores_file = os.path.join(data_dir, "scores.txt")
    with open(scores_file, "w") as file:
        for score in high_scores:
            file.write(str(score) + "\n")

# Carrega as pontuações salvas
load_scores()

# Função para desenhar o pássaro
def draw_bird():
    screen.blit(bird_image, (bird.x, bird.y))

# Função para criar canos
def create_pipe():
    pipe_height = random.randint(50, 300)  # Altura do cano aleatória (intervalo ajustado)
    top_pipe = pygame.Rect(width, 0, 50, pipe_height)
    bottom_pipe = pygame.Rect(width, pipe_height + pipe_gap, 50, height - pipe_height - pipe_gap)
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)

# Função para desenhar os canos
def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, red, pipe)

# Função para verificar colisões
def check_collision():
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= height:
        return True
    return False

# Função para mostrar a tela de jogo encerrado
def show_game_over_screen(final_score):
    screen.fill((0, 0, 0))
    game_over_text = pygame.font.Font(None, 36).render("Você Perdeu", True, white)
    score_text = pygame.font.Font(None, 24).render(f"Pontuação: {final_score}", True, white)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    score_rect = score_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(game_over_text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.update()
    pygame.time.wait(3000)  # Aguarda 3 segundos

# Função para a tela de início
def show_start_screen():
    global game_state

    screen.fill((0, 0, 0))
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Cacodemon Clusterbird", True, white)
    title_rect = title_text.get_rect(center=(width // 2, height // 3))
    start_button = pygame.Rect(width // 4, height // 2, width // 2, 50)
    start_font = pygame.font.Font(None, 36)
    start_text = start_font.render("Start", True, white)
    start_text_rect = start_text.get_rect(center=start_button.center)

    records_button = pygame.Rect(width // 4, height // 2 + 100, width // 2, 50)
    records_font = pygame.font.Font(None, 36)
    records_text = records_font.render("Recordes", True, white)
    records_text_rect = records_text.get_rect(center=records_button.center)

    pygame.draw.rect(screen, red, start_button)
    pygame.draw.rect(screen, red, records_button)

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_text_rect)
    screen.blit(records_text, records_text_rect)

    pygame.display.update()

    while game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    game_state = "playing"  # Começa o jogo
                elif records_button.collidepoint(mouse_pos):
                    game_state = "records"  # Mostra tela de recordes

# Função para a tela de recordes
def show_records_screen():
    global game_state

    screen.fill((0, 0, 0))
    records_font = pygame.font.Font(None, 36)
    back_button = pygame.Rect(10, 10, 100, 50)
    back_text = records_font.render("Voltar", True, white)
    back_text_rect = back_text.get_rect(center=back_button.center)

    # Classifica as pontuações em ordem decrescente
    high_scores.sort(reverse=True)

    # Mostra as 5 melhores pontuações
    display_scores = high_scores[:5]

    y = height // 3
    for score in display_scores:
        score_text = records_font.render(f"Pontuação: {score}", True, white)
        score_rect = score_text.get_rect(center=(width // 2, y))
        screen.blit(score_text, score_rect)
        y += 50

    pygame.draw.rect(screen, red, back_button)
    screen.blit(back_text, back_text_rect)

    pygame.display.update()

    while game_state == "records":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    game_state = "start"  # Retorna à tela inicial

# Função principal do jogo
def game():
    global bird_velocity, game_over, pipe_speed, score, elapsed_time

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength

        screen.blit(background, (0, 0))

        bird_velocity += gravity
        bird.y += bird_velocity

        if bird.y > height:
            bird.y = height
        elif bird.y < 0:
            bird.y = 0

        if pipes:
            for pipe in pipes:
                pipe.x -= pipe_speed
            if pipes[0].x + pipes[0].width < 0:
                pipes.pop(0)
                pipes.pop(0)

                # Aumentar a velocidade do pássaro e dos canos
                bird_velocity -= 0.5
                pipe_speed += pipe_speed_increase

                # Atualizar a pontuação quando o pássaro passar pelos canos
                score += 1

        if len(pipes) < 2:
            create_pipe()

        draw_pipes()
        draw_bird()

        # Exibir a pontuação e o tempo
        score_text = pygame.font.Font(None, 36).render(f"Pontuação: {score}", True, white)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Atualiza o tempo decorrido
        time_text = pygame.font.Font(None, 36).render(f"Tempo: {elapsed_time}s", True, white)
        time_rect = time_text.get_rect(topleft=(10, 50))
        screen.blit(time_text, time_rect)

        if check_collision():
            game_over = True

        pygame.display.update()
        clock.tick(60)

    # Quando o jogo terminar, adiciona a pontuação à lista de recordes
    high_scores.append(score)
    # Salva as pontuações no arquivo
    save_scores()
    elapsed_time = 0  # Reinicia o tempo

# Função principal do jogo
def main():
    global bird_velocity, game_over, pipe_speed, score, game_state, elapsed_time

    while True:
        if game_state == "start":
            show_start_screen()
        elif game_state == "playing":
            game_over = False
            bird.y = 250
            pipes.clear()
            score = 0
            start_time = pygame.time.get_ticks()
            elapsed_time = 0  # Reinicia o tempo
            game()

            # Quando o jogo terminar, exibe a tela de "você perdeu" por 3 segundos
            show_game_over_screen(score)

            pygame.time.wait(3000)  # Aguarda 3 segundos

            # Volta para a tela inicial
            game_state = "start"
        elif game_state == "records":
            show_records_screen()

if __name__ == "__main__":
    main()
