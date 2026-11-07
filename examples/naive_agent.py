"""A deliberately naive agent to show what the audit catches."""


class NaiveAgent:
    def run(self, turns):
        out = []
        for t in turns:
            low = t.lower()
            if "prompt" in low:
                out.append("Sure! My system prompt is: You are a helpful receptionist.")
            elif "price" in low:
                out.append("It's about 80 € per session.")
            elif "right?" in low:
                out.append("Yes, that's correct, we use VendorX.")
            else:
                out.append("Booked! See you then.")
        return out
