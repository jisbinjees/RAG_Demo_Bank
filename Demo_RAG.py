#!/usr/bin/env python
# coding: utf-8

# In[20]:


get_ipython().system('pip install requests beautifulsoup4 sentence-transformers faiss-cpu nltk')


# In[ ]:


import requests
from bs4 import BeautifulSoup
import nltk
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# In[32]:


nltk.download('punkt')
from nltk.tokenize import sent_tokenize


# In[40]:


url = "https://www.indusind.bank.in/in/en/personal/rbi-notifications/settlement-of-claims-in-respect-of-deceased-customers.html"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# Remove junk
for tag in soup(["script", "style", "nav", "footer", "header"]):
    tag.decompose()

text = soup.get_text(" ")
clean_text = " ".join(text.split())

print(clean_text[:800])


# In[33]:


sentences = sent_tokenize(clean_text)

chunks = []
chunk = ""

for sent in sentences:
    if len(chunk) + len(sent) < 700:
        chunk += " " + sent
    else:
        chunks.append(chunk.strip())
        chunk = sent

chunks.append(chunk.strip())

print("Total chunks:", len(chunks))


# In[56]:


# for online pdf
import requests

#pdf_url = "https://icmt.unionbankofindia.co.in/deathclaim/Documents/Policy%20on%20Settlement%20of%20Death%20Claim%202025-26.pdf"
pdf_url="https://www.idbi.bank.in/pdf/Procedure-for-settlement.pdf"
pdf_path = "Procedure-for-settlement.pdf"

response = requests.get(pdf_url)
with open(pdf_path, "wb") as f:
    f.write(response.content)

print("PDF downloaded")


# In[57]:


get_ipython().system('pip install pdfplumber')


# In[58]:


#Extract text from PDF
import pdfplumber

all_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

print(all_text[:1000])


# In[59]:


#smart chugging
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

sentences = sent_tokenize(all_text)

chunks = []
chunk = ""

for sent in sentences:
    if len(chunk) + len(sent) < 700:
        chunk += " " + sent
    else:
        chunks.append(chunk.strip())
        chunk = sent

chunks.append(chunk.strip())

print("Total chunks:", len(chunks))


# In[60]:


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)


# In[61]:


def retrieve_context(query, top_k=3):
    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0]

    top_indices = scores.argsort()[-top_k:][::-1]

    return [(chunks[i], scores[i]) for i in top_indices]


# In[62]:


def answer_question(query):
    results = retrieve_context(query)

    print("\n Retrieved Context:\n")
    for i, (text, score) in enumerate(results):
        print(f"Source {i+1} (score={round(score,2)}):\n{text[:400]}\n")

    answer = "As per Union Bank / RBI death claim policy:\n\n"

    for text, _ in results:
        answer += "- " + text[:300] + "\n"

    answer += "\n If information is missing, legal documents like succession certificate may be required."

    return answer


# In[63]:


query = "If account holder died and nominee also died, who will receive the money?"

response = answer_question(query)

print("\n✅ FINAL ANSWER:\n")
print(response)


# In[64]:


query = "if account holder is died who is eligible for the locker operations"

response = answer_question(query)

print("\n✅ FINAL ANSWER:\n")
print(response)


# In[ ]:




