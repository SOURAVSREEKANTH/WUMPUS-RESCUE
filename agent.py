from collections import deque

from knowledge_base import KnowledgeBase


class RescueAgent:

    def __init__(self, environment):

        self.environment = environment

        # =============================================
        # POSITION
        # =============================================

        self.position = environment.agent_position

        # =============================================
        # KNOWLEDGE BASE
        # =============================================

        self.kb = KnowledgeBase(environment.size)

        row, col = self.position
        self.kb.mark_safe(row, col)

        # =============================================
        # SENSOR READINGS
        # =============================================

        self.heat = False
        self.smoke = False
        self.instability = False
        self.survivor_signal = False

        # =============================================
        # MEMORY
        # =============================================

        self.visited = set()
        self.visited.add(self.position)

        # =============================================
        # MISSION STATE
        # =============================================

        self.goal = "FIND_SURVIVOR"

        self.survivor_found = False
        self.rescue_complete = False
        self.mission_complete = False

        self.steps = 0

        # Path used for exploration/backtracking
        self.exploration_path = [self.position]


    # =================================================
    # GET NEIGHBORS
    # =================================================

    def get_neighbors(self):

        row, col = self.position

        directions = [
            (-1, 0),   # Up
            (1, 0),    # Down
            (0, -1),   # Left
            (0, 1)     # Right
        ]

        neighbors = []

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if self.environment.is_inside(
                new_row,
                new_col
            ):

                neighbors.append(
                    (new_row, new_col)
                )

        return neighbors


    # =================================================
    # SENSOR SYSTEM
    # =================================================

    def sense(self):

        self.heat = False
        self.smoke = False
        self.instability = False
        self.survivor_signal = False

        neighbors = self.get_neighbors()

        for row, col in neighbors:

            cell = self.environment.get_cell(
                row,
                col
            )

            # Fire
            if cell == self.environment.FIRE:

                self.heat = True
                self.smoke = True

                # Known hazardous cell
                self.kb.mark_unsafe(row, col)

            # Structural collapse
            elif cell == self.environment.COLLAPSE:

                self.instability = True

                # Known hazardous cell
                self.kb.mark_unsafe(row, col)

            # Survivor
            elif cell == self.environment.SURVIVOR:

                self.survivor_signal = True

                # Survivor cell can be entered
                self.kb.mark_safe(row, col)

        # Store percept
        self.kb.add_observation(
            self.position,
            self.heat,
            self.smoke,
            self.instability,
            self.survivor_signal
        )

        # Logical inference
        self.kb.infer(
            self.position,
            neighbors
        )


    # =================================================
    # PRINT SENSOR INFORMATION
    # =================================================

    def print_sensors(self):

        print("\n-----------------------------")
        print("       AGENT SENSORS")
        print("-----------------------------")

        print(f"Position:      {self.position}")
        print(f"Heat:          {self.heat}")
        print(f"Smoke:         {self.smoke}")
        print(f"Instability:   {self.instability}")
        print(f"Survivor:      {self.survivor_signal}")
        print(f"Goal:          {self.goal}")
        print(f"Steps:         {self.steps}")

        print("-----------------------------")


    # =================================================
    # CHECK SURVIVOR
    # =================================================

    def check_for_survivor(self):

        row, col = self.position

        cell = self.environment.get_cell(
            row,
            col
        )

        if cell == self.environment.SURVIVOR:

            self.survivor_found = True

            self.goal = "RESCUE"

            print()
            print("********************************")
            print("       SURVIVOR FOUND!")
            print("********************************")

            return True

        return False


    # =================================================
    # RESCUE SURVIVOR
    # =================================================

    def rescue_survivor(self):

        if not self.survivor_found:
            return False

        if self.rescue_complete:
            return True

        row, col = self.position

        cell = self.environment.get_cell(
            row,
            col
        )

        if cell == self.environment.SURVIVOR:

            # Survivor has been rescued
            self.environment.grid[row][col] = (
                self.environment.EMPTY
            )

            self.rescue_complete = True

            self.goal = "RETURN_TO_EXIT"

            print()
            print("********************************")
            print("       SURVIVOR RESCUED!")
            print("       RETURN TO EXIT")
            print("********************************")

            return True

        return False


    # =================================================
    # GET SAFE MOVES
    # =================================================

    def get_safe_moves(self):

        safe_moves = []

        for position in self.get_neighbors():

            row, col = position

            if self.kb.get_status(
                row,
                col
            ) == self.kb.SAFE:

                safe_moves.append(position)

        return safe_moves


    # =================================================
    # GET UNVISITED SAFE MOVES
    # =================================================

    def get_unvisited_safe_moves(self):

        moves = []

        for position in self.get_safe_moves():

            if position not in self.visited:

                moves.append(position)

        return moves


    # =================================================
    # FIND PATH TO EXIT
    # =================================================

    def find_path_to_exit(self):

        """
        Find a path through known-safe cells
        from the current position to the exit.
        """

        exit_position = None

        for row in range(self.environment.size):

            for col in range(self.environment.size):

                if (
                    self.environment.grid[row][col]
                    == self.environment.EXIT
                ):

                    exit_position = (row, col)

        if exit_position is None:
            return None

        start = self.position

        queue = deque([start])

        parent = {
            start: None
        }

        while queue:

            current = queue.popleft()

            if current == exit_position:
                break

            row, col = current

            neighbors = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1)
            ]

            for neighbor in neighbors:

                nr, nc = neighbor

                if not self.environment.is_inside(
                    nr,
                    nc
                ):
                    continue

                if neighbor in parent:
                    continue

                status = self.kb.get_status(
                    nr,
                    nc
                )

                # Exit itself is allowed
                is_exit = (
                    neighbor == exit_position
                )

                if (
                    status == self.kb.SAFE
                    or is_exit
                ):

                    parent[neighbor] = current
                    queue.append(neighbor)

        # No path found
        if exit_position not in parent:

            return None

        # Reconstruct path
        path = []

        current = exit_position

        while current != start:

            path.append(current)
            current = parent[current]

        path.reverse()

        return path


    # =================================================
    # CHOOSE EXPLORATION MOVE
    # =================================================

    def choose_exploration_move(self):

        """
        Choose an unvisited safe cell.

        If none exists, attempt to backtrack through
        already visited safe cells.
        """

        unvisited = self.get_unvisited_safe_moves()

        if unvisited:

            # Prefer first unvisited safe cell
            return unvisited[0]

        # No new safe cell around us.
        # Try backtracking.

        safe_moves = self.get_safe_moves()

        for move in safe_moves:

            if move != self.position:

                return move

        return None


    # =================================================
    # CHOOSE RETURN MOVE
    # =================================================

    def choose_return_move(self):

        path = self.find_path_to_exit()

        if path:

            return path[0]

        return None


    # =================================================
    # CHOOSE NEXT ACTION
    # =================================================

    def choose_move(self):

        # =============================================
        # FIND SURVIVOR
        # =============================================

        if self.goal == "FIND_SURVIVOR":

            move = self.choose_exploration_move()

            if move:

                print(
                    f"AGENT DECISION: "
                    f"Explore {move}"
                )

            return move


        # =============================================
        # RETURN TO EXIT
        # =============================================

        if self.goal == "RETURN_TO_EXIT":

            move = self.choose_return_move()

            if move:

                print(
                    f"AGENT DECISION: "
                    f"Return toward exit via {move}"
                )

            return move


        return None


    # =================================================
    # MOVE
    # =================================================

    def move(self, new_position):

        row, col = new_position

        status = self.kb.get_status(
            row,
            col
        )

        # Exit is allowed
        is_exit = (
            self.environment.get_cell(
                row,
                col
            )
            == self.environment.EXIT
        )

        # Safety check
        if (
            status != self.kb.SAFE
            and not is_exit
        ):

            print(
                f"AGENT REFUSED TO MOVE TO "
                f"{new_position} "
                f"- CELL IS {status}"
            )

            return False

        # Move
        self.position = new_position

        self.environment.agent_position = (
            new_position
        )

        self.visited.add(
            new_position
        )

        self.steps += 1

        print(
            f"AGENT MOVED TO "
            f"{self.position}"
        )

        return True


    # =================================================
    # CHECK EXIT
    # =================================================

    def check_exit(self):

        row, col = self.position

        cell = self.environment.get_cell(
            row,
            col
        )

        if cell == self.environment.EXIT:

            if self.rescue_complete:

                self.goal = "MISSION_COMPLETE"

                self.mission_complete = True

                print()
                print("********************************")
                print("       MISSION COMPLETE!")
                print("       SURVIVOR SAFE")
                print("       AGENT EXITED")
                print("********************************")

                return True

        return False


    # =================================================
    # ONE COMPLETE AGENT STEP
    # =================================================

    def step(self):

        if self.mission_complete:

            return

        print("\n============================")
        print("         AGENT STEP")
        print("============================")

        # =============================================
        # 1. SENSE
        # =============================================

        self.sense()

        self.print_sensors()

        # =============================================
        # 2. CHECK IF SURVIVOR FOUND
        # =============================================

        if self.check_for_survivor():

            self.rescue_survivor()

            return

        # =============================================
        # 3. CHECK EXIT
        # =============================================

        if self.check_exit():

            return

        # =============================================
        # 4. THINK
        # =============================================

        next_move = self.choose_move()

        # =============================================
        # 5. ACT
        # =============================================

        if next_move is not None:

            self.move(next_move)

        else:

            print(
                "AGENT: No suitable action available."
            )