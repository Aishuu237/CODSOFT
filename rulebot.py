"""
RuleBot — A rule-based chatbot using if-else + regex pattern matching.
Demonstrates basic NLP concepts: tokenization, intent detection, and response generation.

Run: python rulebot.py
"""

import re
import random
from datetime import datetime


class Rule:
    """A single conversation rule: patterns → responses."""

    def __init__(self, patterns: list[str], responses: list, tag: str = ""):
        # Compile regex patterns for efficiency
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.responses = responses
        self.tag = tag

    def matches(self, text: str) -> bool:
        """Return True if any pattern matches the input text."""
        return any(p.search(text) for p in self.patterns)

    def respond(self) -> str:
        """Pick a random response; call it if it's a callable."""
        choice = random.choice(self.responses)
        return choice() if callable(choice) else choice


def current_time() -> str:
    return f"It's currently {datetime.now().strftime('%I:%M %p')} on your system. ⏰"

def current_date() -> str:
    return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}. 📅"

def coin_flip() -> str:
    result = random.choice(["HEADS", "TAILS"])
    return f"🪙  It's... {result}!"

def dice_roll() -> str:
    result = random.randint(1, 6)
    return f"🎲  You rolled a {result}!"


RULES: list[Rule] = [

    Rule(
        patterns=[r"\b(hi|hello|hey|howdy|greetings|sup|yo)\b"],
        responses=[
            "Hey there! 👋 What's on your mind?",
            "Hello! Great to see you. How can I help?",
            "Hi! I'm all ears — what do you need?",
        ],
        tag="greeting",
    ),

    Rule(
        patterns=[r"\b(bye|goodbye|see you|cya|later|farewell|quit|exit)\b"],
        responses=[
            "Take care! Come back anytime. 👋",
            "Goodbye! It was nice chatting with you.",
            "See you later! Stay curious 🚀",
        ],
        tag="farewell",
    ),

    Rule(
        patterns=[r"how are you", r"how('s| is) it going", r"what'?s up", r"are you okay"],
        responses=[
            "I'm doing great, thanks for asking! How about you?",
            "Running at full capacity! 😄 How's your day going?",
            "All good in my world! What can I do for you?",
        ],
        tag="status",
    ),

    Rule(
        patterns=[r"what.*(your name|you called|who are you)", r"who made you"],
        responses=[
            "I'm RuleBot — a pattern-matching chatbot built to demonstrate NLP basics!",
            "The name's RuleBot. I use if-else logic and regex to understand you.",
        ],
        tag="identity",
    ),

    Rule(
        patterns=[r"what can you do", r"your (abilities|features|skills|capabilities)", r"\bhelp\b"],
        responses=[
            "I can chat about greetings, the time, jokes, weather vibes, and more. Try me!",
            "I understand greetings, farewells, small-talk, jokes, time, and games. What would you like?",
        ],
        tag="capabilities",
    ),

    Rule(
        patterns=[r"what time", r"current time", r"what'?s the time", r"tell me the time"],
        responses=[current_time],
        tag="time",
    ),

    Rule(
        patterns=[r"what day", r"today'?s date", r"what date", r"current date"],
        responses=[current_date],
        tag="date",
    ),

    Rule(
        patterns=[r"\b(joke|funny|make me laugh|humor)\b"],
        responses=[
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "I asked the chatbot if it dreams. It said: 'Only in Boolean.' 🤖",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
        ],
        tag="joke",
    ),

    Rule(
        patterns=[r"\b(weather|raining|sunny|temperature|forecast|hot|cold|cloudy|snow)\b"],
        responses=[
            "I can't check live weather, but I hope it's a beautiful day wherever you are! ☀️",
            "No weather API here — but may your skies be clear and your code bug-free! 🌤️",
        ],
        tag="weather",
    ),

    Rule(
        patterns=[r"\b(thank(s| you)|cheers|appreciate|grateful|thx|ty)\b"],
        responses=[
            "You're welcome! 😊 Anything else I can help with?",
            "Happy to help! Don't hesitate to ask more.",
            "Anytime! That's what I'm here for.",
        ],
        tag="thanks",
    ),

    Rule(
        patterns=[r"\b(sad|unhappy|depressed|upset|bad day|feeling down|not okay)\b"],
        responses=[
            "I'm sorry to hear that 😔. Remember, tough moments pass. I'm here to chat if it helps.",
            "Hang in there! Things have a way of getting better. Want to talk about it?",
        ],
        tag="emotion-negative",
    ),

    Rule(
        patterns=[r"\b(happy|excited|great|wonderful|amazing|awesome|fantastic|thrilled)\b"],
        responses=[
            "That's wonderful to hear! 🎉 Keep riding that positive wave!",
            "Love the energy! 😄 What's got you feeling so good?",
        ],
        tag="emotion-positive",
    ),

    Rule(
        patterns=[r"\b(flip a coin|heads or tails|coin toss)\b"],
        responses=[coin_flip],
        tag="game",
    ),

    Rule(
        patterns=[r"\b(roll a dice|dice|random number|pick a number)\b"],
        responses=[dice_roll],
        tag="game",
    ),

    Rule(
        patterns=[r"\b(what is|explain|define|tell me about|how does|why is)\b"],
        responses=[
            "That's a deep question! I'm rule-based, so my knowledge is limited. Try a search engine for detailed answers. 🔍",
            "Great curiosity! I don't have a fact database, but a quick web search would nail that for you.",
        ],
        tag="knowledge",
    ),
]

FALLBACKS = [
    "Hmm, I'm not sure about that one. Try rephrasing? 🤔",
    "I didn't quite catch that. Could you say it differently?",
    "That's outside my pattern library! Try asking something else.",
    "Interesting! But I'm stumped. Maybe ask me a joke or the time? 😄",
]



def preprocess(text: str) -> str:
    """Basic normalisation: strip whitespace, collapse spaces."""
    return re.sub(r"\s+", " ", text.strip())


def get_response(user_input: str) -> tuple[str, str]:
    """
    Match input against rules in order.
    Returns (response_text, matched_tag).
    """
    cleaned = preprocess(user_input)
    for rule in RULES:
        if rule.matches(cleaned):
            return rule.respond(), rule.tag
    return random.choice(FALLBACKS), "fallback"


def is_farewell(text: str) -> bool:
    """Detect exit intent so the main loop can stop."""
    farewell_rule = next(r for r in RULES if r.tag == "farewell")
    return farewell_rule.matches(preprocess(text))



def chat():
    print(f"RuleBot: Hey! I'm RuleBot 🤖 — ask me anything!\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nRuleBot: Goodbye! 👋")
            break

        if not user_input:
            print("RuleBot: (silence) ... Say something! 😄\n")
            continue

        response, tag = get_response(user_input)
        print(f"RuleBot [{tag}]: {response}\n")

        if is_farewell(user_input):
            break



if __name__ == "__main__":
    chat()