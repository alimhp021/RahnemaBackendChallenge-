
class Tarikhche:

    def __init__(self, homepage: str):
        self.homepage = homepage
        self.current = [self.homepage, 0]
        self.hist = [self.homepage]

    def visit(self, url: str) -> None:
        del self.hist[self.current[1]+1:]

        self.current[0] = url
        self.current[1] = len(self.hist)
        self.hist.append(url)

    def redo(self, steps: int) -> str:
        if steps + self.current[1] > len(self.hist):
            steps = len(self.hist) - self.current[1] - 1

        self.current = [self.hist[self.current[1] + steps], self.current[1] + steps]
        print(self.current[0])
        return self.current[0]

    def undo(self, steps: int) -> str:
        if steps > self.current[1]:
            steps = self.current[1]

        self.current = [self.hist[self.current[1] - steps], self.current[1] - steps]
        print(self.current[0])
        return self.current[0]



# Your Tarikhche object will be instantiated and called as such:
#history = Tarikhche("rahnemacollege.com");
#history.visit("google.com");
#history.visit("facebook.com");
#history.visit("youtube.com");
#history.undo(1);
#history.undo(1);
#history.redo(1);
#history.visit("linkedin.com");
#history.redo(2);
#history.undo(2);
#history.undo(7);
