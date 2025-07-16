def ask_titan(query):
    query = query.lower()

    if "hello" in query or "hi" in query:
        return "Hi, I am TITAN. How can I help you today?"

    elif "your name" in query:
        return "I am your A.I assistant, TITAN."

    elif "who created you" in query or "who made you" in query:
        return "I was created by Hritik Saini, a passionate developer."

    elif "how are you" in query:
        return "I'm always functioning at optimal performance. Thanks for asking!"

    elif "what can you do" in query:
        return "I can listen, speak, and help you with various tasks. Try saying something!"

    elif "time" in query:
        from datetime import datetime
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    elif "date" in query:
        from datetime import datetime
        today = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    elif "bye" in query or "exit" in query or "quit" in query:
        return "Goodbye! It was nice talking to you."

    else:
        return "I'm still learning. Please ask me something simple."
