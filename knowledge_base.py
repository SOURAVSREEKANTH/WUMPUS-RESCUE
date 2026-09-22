class KnowledgeBase:

    UNKNOWN = "UNKNOWN"
    SAFE = "SAFE"
    UNSAFE = "UNSAFE"

    def __init__(self, size):

        self.size = size

        # Agent's internal map
        self.knowledge = [
            [self.UNKNOWN for _ in range(size)]
            for _ in range(size)
        ]

        # Store observations
        self.observations = {}

    # =====================================================
    # BASIC KNOWLEDGE OPERATIONS
    # =====================================================

    def mark_safe(self, row, col):

        if self.is_inside(row, col):

            # Don't overwrite a known unsafe cell
            if self.knowledge[row][col] != self.UNSAFE:
                self.knowledge[row][col] = self.SAFE

    def mark_unsafe(self, row, col):

        if self.is_inside(row, col):
            self.knowledge[row][col] = self.UNSAFE

    def get_status(self, row, col):

        if not self.is_inside(row, col):
            return None

        return self.knowledge[row][col]

    def is_inside(self, row, col):

        return (
            0 <= row < self.size
            and
            0 <= col < self.size
        )

    # =====================================================
    # STORE SENSOR OBSERVATIONS
    # =====================================================

    def add_observation(
        self,
        position,
        heat,
        smoke,
        instability,
        survivor
    ):

        self.observations[position] = {
            "heat": heat,
            "smoke": smoke,
            "instability": instability,
            "survivor": survivor
        }

    # =====================================================
    # LOGICAL INFERENCE
    # =====================================================

    def infer(self, position, neighbors):

        observation = self.observations.get(position)

        if observation is None:
            return

        smoke = observation["smoke"]
        instability = observation["instability"]
        survivor = observation["survivor"]

        # -------------------------------------------------
        # RULE 1
        # No smoke + no instability
        # → neighboring cells are safe
        # -------------------------------------------------

        if not smoke and not instability:

            for row, col in neighbors:

                self.mark_safe(row, col)

        # -------------------------------------------------
        # RULE 2
        # Smoke detected
        # → do NOT mark unknown neighbors as safe
        # -------------------------------------------------

        if smoke:

            for row, col in neighbors:

                if self.get_status(row, col) == self.UNKNOWN:

                    # Keep the cell unknown.
                    # It may contain a hazard.
                    pass

        # -------------------------------------------------
        # RULE 3
        # Instability detected
        # → do NOT blindly enter unknown cells
        # -------------------------------------------------

        if instability:

            for row, col in neighbors:

                if self.get_status(row, col) == self.UNKNOWN:

                    pass

        # -------------------------------------------------
        # RULE 4
        # Survivor signal
        # → survivor may be nearby
        # -------------------------------------------------

        if survivor:

            print(
                "LOGIC: Survivor detected nearby!"
            )

    # =====================================================
    # DISPLAY KNOWLEDGE
    # =====================================================

    def print_knowledge(self):

        print("\n============================")
        print("       KNOWLEDGE BASE")
        print("============================")

        for row in self.knowledge:

            symbols = []

            for cell in row:

                if cell == self.SAFE:
                    symbols.append("S")

                elif cell == self.UNSAFE:
                    symbols.append("X")

                else:
                    symbols.append("?")

            print(" ".join(symbols))

        print("============================")