class ExponentialSmoothing:
    def __init__(self, alpha=0.75):
        """
        Initialize Exponential Moving Average smoothing.
        :param alpha: Smoothing factor. Higher = more responsive, lower = smoother.
        """
        self.alpha = alpha
        self.previous = None

    def update(self, current):
        """
        Update the smoothed value with a new reading.
        Supports single numbers and lists/tuples of numbers.
        """
        if self.previous is None:
            self.previous = current
            return current

        if isinstance(current, (list, tuple)):
            smoothed = []
            for i in range(len(current)):
                val = self.alpha * current[i] + (1.0 - self.alpha) * self.previous[i]
                smoothed.append(val)
            self.previous = type(current)(smoothed)
            return self.previous
        else:
            smoothed = self.alpha * current + (1.0 - self.alpha) * self.previous
            self.previous = smoothed
            return smoothed
