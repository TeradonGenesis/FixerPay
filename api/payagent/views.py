from flask import request, jsonify
from . import payagent_blueprint
from .services import PayAgent
import os
from werkzeug.utils import secure_filename
import whisper
import base64
import openai

payagent = PayAgent()

@payagent_blueprint.route('/',methods=["POST"])
def run_process():
    try:
        
        query = request.json['query']
        
        user_story = payagent.retrieve_user_stories(index_name="payment-stories", query=query)

        if user_story == 'No user story found':
             raise Exception('Your request cannot be proccessed')

        api_call_tool = payagent.create_api_call_tool()
        # # # sql_query_tool = payagent.create_sql_query_tool()

        agent = payagent.create_agent([api_call_tool])
        # # result = payagent.run_api_chain(user_story)
        result = agent.run(user_story)
        return jsonify({
            'message': result
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400

@payagent_blueprint.route('/stories/upload',methods=["POST"])
def upload_stories():
    try:
        
        file = request.files['file']
        index_name = request.form['index_name']

        #rename the title if theres spacing
        filename = secure_filename(file.filename)
        
        #check if it a file and file type is pdf
        is_pdf = '.' in filename and filename.rsplit('.',1)[1].lower() in ['pdf']
        
        if is_pdf is False:
            raise Exception(f'Cannot upload. {filename} is not a pdf')
        
        # Set the destination folder
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')

        # Ensure that the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Set the filename and save the file
        filepath = os.path.join(destination_folder, filename)
        
        file.save(filepath)

        payagent.upload_stories(filename, index_name)

        return jsonify({
            'message': 'Stories uploaded',
            'index-name': index_name
        }), 201
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
    

@payagent_blueprint.route('/whisper',methods=["POST"])
def whisper_post():
    try:
        file = request.json['file']
        decode_bytes = base64.b64decode(file)
        filename = "audio.wav"
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
        doc_path = os.path.join(destination_folder, filename)

        with open(doc_path, "wb") as wav_file:
             wav_file.write(decode_bytes)
        audio_file= open(doc_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en")


        return jsonify({
            'text': transcript.text
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
    