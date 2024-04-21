from flask import Flask, request, jsonify, send_from_directory, render_template,Response
import pickle
import nltk
import os
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
# Load the trained model
with open('logistic_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('count_vectorizer.pickle', 'rb') as f:
    count_vect = pickle.load(f)

# Create the count vectorizer and TF-IDF transformer
with open('tfidf_transformer.pickle', 'rb') as f:
    tfidf_transformer = pickle.load(f)


def preprocess_complaint(complaint):
    # Convert the complaint to lowercase and tokenize it
    complaint = complaint.lower()
    tokens = word_tokenize(complaint)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(filtered_tokens)

topic_mapping = {
    0: 'bank',
    1: 'credit',
    2: 'other',
    3: 'theft',
    4: 'loan'
}

classified_complaints = []
last_sent_complaint_id = None
@app.route('/stream')
def stream():
    def event_stream():
        for complaint in classified_complaints:
            yield 'data: {}\n\n'.format(json.dumps(complaint))

    return Response(event_stream(), mimetype="text/event-stream")
    

@app.route('/submit-complaint', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the complaint text from the form
        # complaint = request.form.get('complaint')

        complaint = request.json['complaint']

        # Preprocess the complaint text
        preprocessed_complaint = preprocess_complaint(complaint)

        # Vectorize and TF-IDF transform
        test = count_vect.transform([preprocessed_complaint])
        test_tfidf = tfidf_transformer.transform(test)

        # Make a prediction
        
        prediction = model.predict(test_tfidf)
        print(prediction)
        department = topic_mapping[prediction[0]]
        #print(predicted_topic)
        # if(predicted_topic=="Theft/Dispute Reporting")
        # {
        #     predticted_topic=""
        # }
        # Render the prediction result templat
        new_complaint_id = len(classified_complaints)  # Use list length for simplicity
        classified_complaint = {'id': new_complaint_id, 'text': complaint, 'department': department}
        classified_complaints.append(classified_complaint)

        if(department=='loan'):
            refresh_loan_page=True
        elif(department=='credit'):
            refresh_credit_page=True
        elif(department=='bank'):
            refresh_bank_page=True
        elif(department=='other'):
            refresh_other_page=True
        elif(department=='theft'):
            refresh_theft_page=True
        
        if department == 'loan':
            return jsonify({'success': True, 'refresh_loan_page': refresh_loan_page})
        elif department == 'credit':
            return jsonify({'success': True,'refresh_credit_page': refresh_credit_page})
        elif department == 'theft':
            return jsonify({'success': True,'refresh_theft_page': refresh_theft_page})
        elif department == 'bank':
            return jsonify({'success': True,'refresh_bank_page': refresh_bank_page})
        elif department == 'other':
            return jsonify({'success': True,'refresh_other_page': refresh_other_page})
        else:
            return jsonify({'success': True})

        
        
    
    
@app.route('/')
def index():
    return render_template('predict.html')

@app.route('/department/loan')
def loan_department():
    loan_complaints = [complaint for complaint in classified_complaints if complaint['department'] == 'loan']
    return render_template('Loan.html', complaints=loan_complaints)

@app.route('/department/credit_card')
def credit_card_department():
    credit_card_complaints = [complaint for complaint in classified_complaints if complaint['department'] == 'credit']
    return render_template('credit_card.html', complaints=credit_card_complaints)

@app.route('/department/other')
def other_department():
    other_complaints = [complaint for complaint in classified_complaints if complaint['department'] == 'other']
    return render_template('other.html', complaints=other_complaints)

@app.route('/department/bank')
def bank_account_department():
    bank_account_complaints = [complaint for complaint in classified_complaints if complaint['department'] == 'bank']
    return render_template('Bank.html', complaints=bank_account_complaints)

@app.route('/department/theft')
def theft_department():
    theft_complaints = [complaint for complaint in classified_complaints if complaint['department'] == 'theft']
    return render_template('theft.html', complaints=theft_complaints)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)