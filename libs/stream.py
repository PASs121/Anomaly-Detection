import pandas as pd

class DataStream:

    def __init__(self, path: str) -> None:
        self.data = pd.read_csv(path)
        self.data["ctime"] = pd.to_datetime(self.data["ctime"])

        self._readings = self.reading_generator()
        self._exhausted = False

    @property
    def next_reading(self):
        if self._exhausted:
            raise StopIteration("Data stream has been exhausted.")

        try:
            row = next(self._readings)
            reading = {
            "timestamp": row["ctime"],
            "active_power": float(row["activePower"]),
            }
            if "label" in row.index:
                reading["label"] = row["label"]
            return reading

        except StopIteration:
            self._exhausted = True
            raise

    def reading_generator(self):
        for i in range(len(self.data)):
            yield self.data.iloc[i]

