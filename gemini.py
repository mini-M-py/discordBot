import google.generativeai as genai
import os
API_KEY = os.environ['AI_KEY'] 



def gemini(prompt):
  try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt,generation_config=genai.types.GenerationConfig(
                                       max_output_tokens=1000,
                                       temperature=1.0))
    return response.text
  except Exception as e:
    print(e)
    return "I am busy. Please! wait for a while"

