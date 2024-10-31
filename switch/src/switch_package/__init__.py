class switch():
    def __init__(self, *caseOutPairs, end=None):
        self.dictionary = {}
        
        if len(caseOutPairs) % 2 != 0:
            raise ValueError("caseOutPairs must contain pairs of case-output elements.")

        for i in range(0, len(caseOutPairs), 2):
            case = caseOutPairs[i]
            output = caseOutPairs[i+1]
            self.dictionary[case] = output

        self.end = end
    
    def __call__(self, matchCase, *args, **kwargs):
        if matchCase in self.dictionary:
            result = self.dictionary[matchCase]
            if callable(result):
                return result(*args, **kwargs)  # Pass arguments if callable
            else:
                return result
        else:
            if callable(self.end):
                return self.end(*args, **kwargs)  # Pass arguments if callable
            else:
                return self.end
    
    def __getitem__(self, case):
        if case in self.dictionary:
            result = self.dictionary[case]
            if callable(result):
                return lambda *args, **kwargs: result(*args, **kwargs)
            else:
                return result
        else:
            if callable(self.end):
                return lambda *args, **kwargs: self.end(*args, **kwargs)
            else:
                return self.end

    def __setitem__(self, case, result):
        self.dictionary[case] = result