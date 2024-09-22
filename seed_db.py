import json 
import pg8000
import os 
import sys
import datetime

# DB credentials
host = "" 
port = 0   
database = "" 
user = "" 
pw = "" 


SQL_DIR = './sql/'

def load_json_data(file_name: str) -> list:
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    return data

def drop_table():
    try:
        conn = pg8000.connect(host=host, port=port, database=database, user=user, password=pw)
        cursor = conn.cursor()
        cursor.execute(
            """
            DROP TABLE startups;
            """
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return
    
def create_tables():
    '''
    Load all .SQL files and execute them to create tables
    '''

    # Connect to the database
    conn = pg8000.connect(host=host, port=port, database=database, user=user, password=pw)
    cursor = conn.cursor()

    # Load the SQL files, reading all lines and executing them
    sql_files = os.listdir(SQL_DIR)
    for file in sql_files:
        with open(SQL_DIR + file, 'r') as f:
            try:
                sql = f.read()
                if not sql:
                    continue
                print(f'Executing {file}')
                print(sql)
                cursor.execute(sql)
                conn.commit()
            except pg8000.dbapi.ProgrammingError as e:
                if 'already exists' in str(e):
                    continue
                else:
                    conn.rollback()
    
    cursor.close()
    conn.close()




def seed_events_db(data: dict):
    conn = pg8000.connect(host=host, port=port, database=database, user=user, password=pw)
    cursor = conn.cursor()

    for event in data:
        name = event['name']
        description = event['description']
        date = datetime.datetime.strptime(event['date'], '%Y-%m-%d')
        event_image_url = event['event_image_url']
        venue_name = event['venue_name']
        event_type = event['event_type']

        cursor.execute(
        """
        INSERT INTO events (name, description, date, event_image_url, venue_name, event_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, description, date, event_image_url, venue_name, event_type)
        )


    conn.commit()
    conn.close()


def seed_startups_db(data: list):
    conn = pg8000.connect(host=host, port=port, database=database, user=user, password=pw)
    cursor = conn.cursor()

    for startup in data:
        # extract social media links
        social_media = startup['socialMedia']
        twitter = social_media.get('twitter', None)
        linkedin = social_media.get('linkedin', None)
        website = social_media.get('website', None)
        instagram = social_media.get('instagram', None)
        event_id = int(startup['event_id'])
        cursor.execute(
            """
            INSERT INTO startups (name, pitcher_name, description_brief, description_long, logo_url, twitter, linkedin, website, instagram, event_name, pitch_order, event_id)   
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                startup['name'],
                startup['pitcherName'],
                startup['descriptionBrief'],
                startup['descriptionLong'],
                startup['logoUrl'],
                twitter,
                linkedin,
                website,
                instagram,
                'Hokkaido Entrepreneurship Expo 2024, vol. 2',
                startup['pitchOrder'],
                event_id
            )
        )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    drop_table()
    create_tables()
    data = load_json_data('startups.json')
    seed_startups_db(data)
    
    '''
    data = load_json_data('events.json')
    seed_events_db(data)
    '''