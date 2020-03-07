import csv
import statistics

from pycorenlp import StanfordCoreNLP

DATA_FILES = ['data/2014.csv', 'data/2015.csv', 'data/2016.csv', 'data/2017.csv', 'data/2018.csv']
OUTPUT_FILE_NAME = 'result.csv'

SENTIMENT_TEXT_MAP = {
    0: 'VeryNegative',
    1: 'Negative',
    2: 'Neutral',
    3: 'Positive',
    4: 'VeryPositive'
}

nlp = StanfordCoreNLP('http://localhost:9000')


def main():
    output_data = []
    for row in movie_review_reader(DATA_FILES):
        output_row = {
            'title': row['title'],
            'award': row['award']
        }
        output_row.update(get_public_review(row))
        output_row.update(get_critic_review(row))

        output_data.append(output_row)

        with open(OUTPUT_FILE_NAME, 'w+') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'award', 'public_review_value', 'public_review_text',
                                                      'critic_review_value', 'critic_review_text'])
            writer.writeheader()
            writer.writerows(output_data)



def get_public_review(row):
    '''
    Return sentimental value for the public review or empty
    '''
    sentimental_value = ''
    sentimental_text = ''

    if row['public']:
        sentimental_value, sentimental_text = get_sentiment_value(row['public'])

    return {
        'public_review_value': sentimental_value,
        'public_review_text': sentimental_text
    }


def get_critic_review(row):
    '''
    Return sentimental value for the critic review or empty
    '''
    sentimental_value = ''
    sentimental_text = ''

    if row['critic']:
        sentimental_value, sentimental_text = get_sentiment_value(row['critic'])

    return {
        'critic_review_value': sentimental_value,
        'critic_review_text': sentimental_text
    }


def get_sentiment_value(text):
    '''
    Return sentimental value and text for given text
    '''
    sentimental_analysis = nlp.annotate(text, properties={
        'annotators': 'sentiment',
        'outputFormat': 'json',
        'timeout': 1000,
    })
    sentimental_value = round(
        statistics.mean([int(sentence['sentimentValue']) for sentence in sentimental_analysis['sentences']]))
    sentimental_text = SENTIMENT_TEXT_MAP[sentimental_value]
    return sentimental_value, sentimental_text


def movie_review_reader(file_list):
    '''
    Generator to return formated row from the dataset
    '''
    current_movie_name = None
    current_award = None
    for filename in file_list:
        count = 0
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:

                if row['title'] != '' and current_movie_name != row['title']:
                    current_movie_name = row['title']
                if row['award'] != '' and current_award != row['award']:
                    current_award = row['award']

                row['title'] = current_movie_name
                row['award'] = current_award
                count = count + 1
                print(row['title'], filename, count, len(row['public']), len(row['critic']))
                yield row


if __name__ == '__main__':
    main()
