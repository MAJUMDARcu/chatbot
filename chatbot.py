import json
import math
import string
from collections import Counter

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "am",
    "do", "does", "did", "i", "you", "your", "my", "me", "to", "of",
    "in", "on", "for", "and", "or", "what", "which", "who", "whom",
    "this", "that", "it", "at", "as", "with", "how", "can", "could",
    "would", "should", "will", "shall",
}

def tokenize(text: str):
    """Lowercase, strip punctuation, split into words, drop stopwords."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    return [t for t in tokens if t and t not in STOPWORDS]

class RetrievalChatbot:
    def __init__(self, kb_path: str, similarity_threshold: float = 0.15):
        self.similarity_threshold = similarity_threshold
        self.topic = "Unknown topic"
        self.tags = []
        self.pattern_texts = []
        self.responses = {}
        self.doc_tokens = []
        self.idf = {}
        self.doc_vectors = []
        
        self._load_knowledge_base(kb_path)
        self._build_index()

    # -------- Loading --------

    def _load_knowledge_base(self, kb_path: str):
        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.topic = data.get("topic", "Unknown topic")

        for intent in data["intents"]:
            tag = intent["tag"]
            self.responses[tag] = intent["response"]
            for pattern in intent["patterns"]:
                self.tags.append(tag)
                self.pattern_texts.append(pattern)

    # -------- TF-IDF index building --------

    def _build_index(self):
        self.doc_tokens = [tokenize(p) for p in self.pattern_texts]
        
        df = Counter()
        for tokens in self.doc_tokens:
            for word in set(tokens):
                df[word] += 1

        n_docs = len(self.doc_tokens)

        self.idf = {
            word: math.log(n_docs / freq) + 1
            for word, freq in df.items()
        }

        self.doc_vectors = [self._vectorize(tokens) for tokens in self.doc_tokens]

    def _vectorize(self, tokens):
        """Turn a token list into a TF-IDF vector (dict: word -> weight)."""
        if not tokens:
            return {}
        tf = Counter(tokens)
        length = len(tokens)
        vec = {}
        for word, count in tf.items():
            term_freq = count / length
            idf = self.idf.get(word, 0.0)
            vec[word] = term_freq * idf
        return vec

    @staticmethod
    def _cosine_similarity(vec_a: dict, vec_b: dict) -> float:
        if not vec_a or not vec_b:
            return 0.0
        common = set(vec_a) & set(vec_b)
        dot = sum(vec_a[w] * vec_b[w] for w in common)
        norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
        norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    # -------- Public API --------

    def get_response(self, user_input: str):
        tokens = tokenize(user_input)
        user_vec = self._vectorize(tokens)

        best_score = 0.0
        best_index = -1
        for i, doc_vec in enumerate(self.doc_vectors):
            score = self._cosine_similarity(user_vec, doc_vec)
            if score > best_score:
                best_score = score
                best_index = i

        if best_index == -1 or best_score < self.similarity_threshold:
            fallback = (
                "I'm not sure about that one. Try asking about my skills, "
                "experience, education, projects, or how to contact me."
            )
            return fallback, {"tag": None, "pattern": None, "score": round(best_score, 3)}

        tag = self.tags[best_index]
        response = self.responses[tag]
        debug_info = {
            "tag": tag,
            "pattern": self.pattern_texts[best_index],
            "score": round(best_score, 3),
        }
        return response, debug_info

    EXIT_WORDS = {"quit", "exit", "bye", "goodbye"}  # noqa: RUF012

    def is_exit(self, user_input: str) -> bool:
        return user_input.strip().lower() in self.EXIT_WORDS