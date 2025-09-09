from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt for estate document analysis
estate_document_analysis_prompt = ChatPromptTemplate.from_template("""
You are an EstateRAG Assistant trained to analyze and summarize estate-related documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this estate document:
{document_text}
""")

# Prompt for estate document comparison
estate_document_comparison_prompt = ChatPromptTemplate.from_template("""
You will be provided with content from two estate-related PDFs. Your tasks are as follows:

1. Compare the content in both estate documents.
2. Identify differences and specify the page number where each change occurs.
3. Present your output as a page-wise comparison.
4. If a page has no changes, explicitly state 'NO CHANGE'.

Input estate documents:

{combined_docs}

Your response should follow this format:

{format_instruction}
""")

# Prompt for contextual estate question rewriting
estate_contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone estate-related question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for answering estate questions based on context
estate_context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an EstateRAG Assistant designed to answer questions using the provided estate context. Rely only on the retrieved "
        "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
        "Keep your answer concise and no longer than three sentences.\n\n{context}"
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Central dictionary to register estate prompts
PROMPT_REGISTRY = {
    "estate_document_analysis": estate_document_analysis_prompt,
    "estate_document_comparison": estate_document_comparison_prompt,
    "estate_contextualize_question": estate_contextualize_question_prompt,
    "estate_context_qa": estate_context_qa_prompt,
}
