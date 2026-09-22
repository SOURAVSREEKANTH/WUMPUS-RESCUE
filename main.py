import pygame

from environment import Environment
from agent import RescueAgent

from config import (
    GRID_SIZE,
    CELL_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS
)


# =========================================================
# INITIALIZE PYGAME
# =========================================================

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption(
    "Wumpus-Style Disaster Search & Rescue"
)

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)

RED = (220, 50, 50)
ORANGE = (240, 150, 40)
GREEN = (70, 180, 90)
BLUE = (60, 120, 220)
YELLOW = (240, 220, 70)


# =========================================================
# CREATE ENVIRONMENT
# =========================================================

environment = Environment(GRID_SIZE)


# =========================================================
# CREATE AGENT
# =========================================================

agent = RescueAgent(environment)


# =========================================================
# AGENT CONTROL
# =========================================================

agent_running = True

agent_timer = 0

# One decision every 700 milliseconds
agent_delay = 700


# =========================================================
# DRAW GRID
# =========================================================

def draw_grid():

    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            cell = environment.get_cell(
                row,
                col
            )

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # Default
            color = WHITE

            # Fire
            if cell == environment.FIRE:

                color = RED

            # Structural collapse
            elif cell == environment.COLLAPSE:

                color = ORANGE

            # Survivor
            elif cell == environment.SURVIVOR:

                color = GREEN

            # Exit
            elif cell == environment.EXIT:

                color = BLUE

            # Visited empty cell
            elif (
                (row, col) in agent.visited
                and cell == environment.EMPTY
            ):

                color = (210, 235, 215)

            # Draw cell
            pygame.draw.rect(
                screen,
                color,
                (
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )

            # Grid border
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                1
            )


# =========================================================
# DRAW AGENT
# =========================================================

def draw_agent():

    row, col = agent.position

    center_x = (
        col * CELL_SIZE
        + CELL_SIZE // 2
    )

    center_y = (
        row * CELL_SIZE
        + CELL_SIZE // 2
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (
            center_x,
            center_y
        ),
        CELL_SIZE // 3
    )


# =========================================================
# DRAW INFORMATION PANEL
# =========================================================

def draw_information():

    font = pygame.font.SysFont(
        None,
        24
    )

    information = [

        "DISASTER RESCUE AGENT",

        f"Position: {agent.position}",

        f"Goal: {agent.goal}",

        f"Heat: {agent.heat}",

        f"Smoke: {agent.smoke}",

        f"Instability: {agent.instability}",

        f"Survivor Signal: "
        f"{agent.survivor_signal}",

        f"Visited Cells: "
        f"{len(agent.visited)}",

        f"Steps: {agent.steps}",

        "SPACE = Pause / Resume"

    ]

    start_y = (
        GRID_SIZE * CELL_SIZE
        + 5
    )

    for i, text in enumerate(information):

        rendered_text = font.render(
            text,
            True,
            BLACK
        )

        screen.blit(
            rendered_text,
            (
                10,
                start_y + i * 12
            )
        )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:

            running = False

        # Keyboard
        if event.type == pygame.KEYDOWN:

            # SPACE
            if event.key == pygame.K_SPACE:

                agent_running = not agent_running

                if agent_running:

                    print(
                        "AGENT RESUMED"
                    )

                else:

                    print(
                        "AGENT PAUSED"
                    )


    # =====================================================
    # AUTONOMOUS AGENT
    # =====================================================

    if agent_running:

        current_time = pygame.time.get_ticks()

        if (
            current_time - agent_timer
            >= agent_delay
        ):

            agent.step()

            agent_timer = current_time


    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(GRAY)

    draw_grid()

    draw_agent()

    draw_information()

    pygame.display.flip()

    clock.tick(FPS)


# =========================================================
# EXIT
# =========================================================

pygame.quit()