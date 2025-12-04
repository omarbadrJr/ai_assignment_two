class TreeRecorder:
    def __init__(self):
        self.lines = []

    def clear(self):
        self.lines = []

    def node(self, level, label, col, value, alpha=None, beta=None):
        ab = f" (a={alpha}, b={beta})" if alpha is not None or beta is not None else ""
        self.lines.append((level, f"{label} | col={col} | val={value}{ab}"))

    def prune(self, level, alpha, beta):
        self.lines.append((level, f"PRUNED | a={alpha} | b={beta}"))