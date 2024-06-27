# from flask import Flask, request
# import os
# import google.generativeai as genai

# SECRET_KEY=os.environ.get('KEY')
# os.environ['GOOGLE_API_KEY'] = SECRET_KEY
# genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# model = genai.GenerativeModel('gemini-pro')

# app = Flask(__name__)

# @app.route('/api/answer/')

# def geminiresponse():
#     response = model.generate_content("Give song to learn about 7 continents of the world in form of song, easy for small kids in hindi",
#                                  generation_config = genai.types.GenerationConfig(
#                                   candidate_count = 1,
#                                   max_output_tokens = 800,
#                                   top_p = 0.6,
#                                   top_k = 5,
#                                   temperature = 0.8) )
#     return {'answer': response.text}

# @app.route('/api/next-word/', methods=['POST'])  
# def get_next_word_info():
    
#     data = request.json['word']
#     print(data)
#     response = model.generate_content("Give very simple information about " + data + "for small kids",
#                                  generation_config = genai.types.GenerationConfig(
#                                   candidate_count = 1,
#                                   max_output_tokens = 800,
#                                   top_p = 0.6,
#                                   top_k = 5,
#                                   temperature = 0.8) )
#     return {'answer': response.text}

#     return {'answer': data}

from flask import Flask, request
import os
import google.generativeai as genai

SECRET_KEY=os.environ.get('KEY')
os.environ['GOOGLE_API_KEY'] = SECRET_KEY
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# No model name change required for Gemini
model = genai.GenerativeModel()  # No need to specify 'gemini'

app = Flask(__name__)

@app.route('/api/answer/')

def geminiresponse():
  response = model.generate_content("Give song to learn about 7 continents of the world in form of song, easy for small kids in hindi",
                                    generation_config = genai.types.GenerationConfig(
                                        candidate_count = 1,
                                        max_output_tokens = 800,
                                        top_p = 0.6,
                                        top_k = 5,
                                        temperature = 0.8) )
  return {'answer': response.text}

@app.route('/api/next-word/', methods=['POST'])
def get_next_word_info():
  
  data = request.json['word']
  print(data)
  response = model.generate_content("Give very simple information about " + data + "for small kids",
                                    generation_config = genai.types.GenerationConfig(
                                        candidate_count = 1,
                                        max_output_tokens = 800,
                                        top_p = 0.6,
                                        top_k = 5,
                                        temperature = 0.8) )
  return {'answer': response.text}


