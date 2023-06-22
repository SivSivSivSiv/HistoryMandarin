from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'Ya3eb123j'

xl = pd.ExcelFile('combined_file.xlsx')

# Load a sheet into a DataFrame
df = xl.parse(xl.sheet_names[0])

# Make sure that your columns are of type str
df.columns = df.columns.astype(str)


# This dictionary will hold our final data
data = {}

# Now we loop through the columns in steps of 3 (since every condition has 3 columns)
for i in range(0, len(df.columns), 3):
    # The condition is the name of the first column in the group
    condition = df.columns[i]
    # We create a DataFrame for the condition and transpose it so that terms are rows
    condition_df = df.iloc[:, i:i+3]
    # We make sure that the DataFrame's columns are the first row (English, Mandarin, Hanyu Pinyin)
    condition_df.columns = condition_df.iloc[0]
    # We remove the first row as it's now the column names
    
    condition_df = condition_df.drop(df.index[0])
    condition_df =  condition_df.dropna()

    # Finally, we add the DataFrame to our dictionary
    data[condition] = condition_df


# Read the response files
yes_data = pd.read_excel('Yes8.xlsx')
no_data = pd.read_excel('No3.xlsx')

print (yes_data)

yes_lresponses = [str(resp).strip() for resp in yes_data.iloc[:, 0].tolist() if str(resp) != 'nan']
print(yes_lresponses)

custom_data = pd.read_excel('OpenEnded2.xlsx')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['selected_condition'] = request.form.get('condition')
        session['show_pinyin'] = request.form.get('show_pinyin')
    selected_condition = session.get('selected_condition', None)
    show_pinyin = session.get('show_pinyin', 'show')
    df = data[selected_condition] if selected_condition else None
    yes_responses = [str(resp).strip() if pd.notnull(resp) else "" for resp in yes_data[selected_condition].tolist()] if selected_condition else None
    no_responses = [str(resp).strip() if pd.notnull(resp) else "" for resp in no_data[selected_condition].tolist()] if selected_condition else None
    custom_phrases = custom_data[selected_condition].tolist() if selected_condition else None
    return render_template('index9.html', conditions=data.keys(), selected_condition=selected_condition, df=df.to_dict('records') if df is not None else None, yes_responses=yes_responses, no_responses=no_responses, custom_phrases=custom_phrases, show_pinyin=show_pinyin)

@app.context_processor
def utility_processor():
    def custom_zip(*args):
        return zip(*args)
    return dict(zip=custom_zip)

if __name__ == '__main__':
    app.run(debug=True)
 