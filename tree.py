class TreeTXT:
    def __init__(self):
     pass


    def build_tree_lines(self, lines):
        result = []
        for level, text in lines:
            if level == 0:
                result.append(text)
            else:
                prefix = "│ " * (level - 1) + "├── "
                result.append(prefix + text)
        return result


    def save(self, lines, filename="tree.txt"):
        tree_lines = self.build_tree_lines(lines)
        with open(filename, "w", encoding="utf-8") as f:
            for line in tree_lines:
                f.write(line + "\n")