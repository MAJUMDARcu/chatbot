Resume / Portfolio Bot

A lightweight, retrieval based chatbot built with Python. The bot
answers questions about a resume or portfolio by matching a user's input
against predefined intent patterns using TF IDF vectors and cosine
similarity.

Features

Natural language style question matching

TF IDF based text representation

Cosine similarity for matching user queries to known patterns

Intent based responses

Configurable similarity threshold

JSON based knowledge base

Fallback response when no sufficiently similar pattern is found

Optional debug mode showing the matched intent, similarity score,
and pattern

Simple command line interface

How It Works

The chatbot follows a retrieval based approach rather than generating
responses with a large language model.

1. Tokenization

Input text is converted to lowercase, punctuation is removed, and common
stopwords are filtered.

2. TF IDF Indexing

The predefined patterns from knowledge_base.json are converted into TF
IDF vectors.

Term frequency measures how often a word appears in a pattern, while
inverse document frequency gives more importance to words that are less
common across the pattern collection.

3. Cosine Similarity

When a user asks a question, the chatbot converts the question into a TF
IDF vector and calculates cosine similarity against every stored
pattern.

The pattern with the highest similarity score is selected.

4. Threshold Based Response

The default similarity threshold is 0.15. If the best match is below
this threshold, the chatbot returns a fallback response instead of
guessing.

Project Structure

resume-chatbot/
├── chatbot.py
├── cli.py
├── knowledge_base.json
└── README.md

chatbot.py

Contains the main RetrievalChatbot class, including tokenization, TF
IDF vector construction, cosine similarity, intent matching, response
retrieval, and exit handling.

cli.py

Provides the command line interface. It loads the knowledge base, starts
the chatbot, accepts user questions, displays responses, and supports
optional debug output.

knowledge_base.json

Stores the chatbot topic, intents, example question patterns, and
corresponding responses.

Requirements

The project uses Python's standard library, including:

json

math

string

collections.Counter

os

sys

No external Python packages are required for the current implementation.

Installation

Clone the repository:

git clone https://github.com/MAJUMDARcu/chatbot.git
cd chatbot

Usage

Run the chatbot with:

python cli.py

The chatbot will display the configured topic and greeting, then wait
for user input.

Example:

=== Resume / Portfolio Bot ===
Type 'quit' to exit.

Hey! I'm ResumeBot 👋 Ask me about my skills, work experience, education, projects, or how to contact me.

You: what are your skills

Bot: Core skills: ...

To exit:

quit

You can also use:

bye
exit
goodbye

Debug Mode

The CLI supports a debug mode:

python cli.py --debug

Debug mode displays:

Matched intent tag

Similarity score

Matched pattern

This is useful for understanding how the retrieval system is making its
selection.

Knowledge Base

The chatbot currently uses intents covering areas such as:

Greeting

Goodbye

Thanks

Name

Skills

Experience

Education

Projects

Contact

Availability

Strengths

These intents and their response patterns are stored in
knowledge_base.json.

Technical Approach

The project demonstrates a simple information retrieval pipeline:

User Query
    ↓
Tokenization
    ↓
TF IDF Vectorization
    ↓
Cosine Similarity
    ↓
Best Matching Pattern
    ↓
Intent
    ↓
Response

Limitations

This chatbot is retrieval based. It does not generate new answers or
understand conversation context like a large language model.

Its responses depend on the patterns and responses defined in
knowledge_base.json. Questions that are significantly different from
the stored patterns may result in the fallback response.

Future Improvements

Possible improvements include:

Expanding the knowledge base

Adding more robust text preprocessing

Supporting conversation history

Adding a web interface

Adding automated evaluation of retrieval accuracy

Adding more advanced semantic embeddings

License

No license has been specified for this repository yet.
